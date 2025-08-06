#!/usr/bin/env python3
"""
Shopify Product Image Processor with Text Overlays
==================================================

A complete automation agent for downloading Shopify product images and adding
branded text overlays for ROSEYS vintage eyewear frames.

Author: Claude Code
Created: 2025-08-05
"""

import os
import json
import csv
import logging
import requests
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union
from PIL import Image, ImageDraw, ImageFont
from urllib.parse import urlparse
import time
from dataclasses import dataclass


@dataclass
class ProductData:
    """Data structure for product information"""
    product_number: str
    designer: str
    origin: str
    decade: str
    images: List[str]
    lens_mm: Optional[str] = None
    bridge_mm: Optional[str] = None
    arm_mm: Optional[str] = None


class ShopifyImageProcessor:
    """
    Main class for processing Shopify product images with text overlays
    """
    
    def __init__(self, output_dir: str = r"C:\claude_home\obsidian_ai-vault\PROJECTS\Image-Overlay-Agent\Frame Product Images", 
                 base_font_size_product: int = 75, base_font_size_tags: int = 60, quality: int = 95):
        """
        Initialize the image processor
        
        Args:
            output_dir: Directory to save processed images
            base_font_size_product: Base size for product number text (scales with image)
            base_font_size_tags: Base size for tags text (scales with image)
            quality: JPEG quality for output images (1-100)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.base_font_size_product = base_font_size_product
        self.base_font_size_tags = base_font_size_tags
        self.quality = quality
        
        # Setup logging
        self._setup_logging()
        
        # Fonts will be loaded per image with proper scaling
        self.font_product = None
        self.font_tags = None
        
        # Session for efficient HTTP requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ROSEYS-Image-Processor/1.0'
        })
        
        # Processing statistics
        self.stats = {
            'total_products': 0,
            'total_images': 0,
            'successful_downloads': 0,
            'successful_overlays': 0,
            'errors': 0
        }
        
    def _get_versioned_filename(self, base_path: str, filename: str) -> str:
        """
        Generate versioned filename if file already exists to prevent overwrites
        
        Args:
            base_path: Directory path where file will be saved
            filename: Original filename
            
        Returns:
            Versioned filename (original if doesn't exist, or with _v2, _v3, etc.)
        """
        full_path = os.path.join(base_path, filename)
        
        if not os.path.exists(full_path):
            return filename
        
        # Extract name and extension
        name, ext = os.path.splitext(filename)
        version = 2
        
        while True:
            versioned_name = f"{name}_v{version}{ext}"
            versioned_path = os.path.join(base_path, versioned_name)
            
            if not os.path.exists(versioned_path):
                return versioned_name
            
            version += 1
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('shopify_processor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _load_fonts(self, product_font_size: int, tags_font_size: int) -> Tuple[ImageFont.FreeTypeFont, ImageFont.FreeTypeFont]:
        """
        Load fonts with fallback system - prioritizing actual Magda Clean OTF file
        to match ROSEYS website exact specifications
        
        Args:
            product_font_size: Font size for product number
            tags_font_size: Font size for tags
        
        Returns:
            Tuple of (product font, tags font) PIL ImageFont objects
        """
        # Priority order: Actual Magda Clean OTF file first, then fallbacks
        font_options = [
            # Actual Magda Clean font file (copied to script directory)
            "MagdaClean-Regular.otf",
            # Magda Clean font variations 
            "Magda Clean.ttf",
            "MagdaClean.ttf",
            "magda-clean.ttf", 
            "MagdaClean-Bold.ttf",
            "MagdaClean-Regular.ttf",
            "MagdaClean_Regular.ttf",
            "magdaclean.ttf",
            "magda clean.ttf",
            "Magda-Clean.ttf",
            # Website fallback fonts (Arial, sans-serif)
            "arial.ttf",
            "Arial.ttf",
            "Arial Bold.ttf",
            "arialbd.ttf",
            # Additional system fallbacks
            "helvetica.ttf",
            "Helvetica.ttf",
            "DejaVuSans-Bold.ttf",
            "DejaVuSans.ttf",
            "calibri.ttf",
            "Calibri.ttf"
        ]
        
        # Try to load fonts from system
        font_product = None
        font_tags = None
        
        for font_name in font_options:
            try:
                # Try loading from current directory first
                if os.path.exists(font_name):
                    if font_product is None:
                        font_product = ImageFont.truetype(font_name, product_font_size)
                    if font_tags is None:
                        font_tags = ImageFont.truetype(font_name, tags_font_size)
                    self.logger.info(f"Loaded font: {font_name} (Product: {product_font_size}px, Tags: {tags_font_size}px)")
                    return font_product, font_tags
                    
                # Try loading from system fonts
                if font_product is None:
                    font_product = ImageFont.truetype(font_name, product_font_size)
                if font_tags is None:
                    font_tags = ImageFont.truetype(font_name, tags_font_size)
                self.logger.info(f"Loaded system font: {font_name} (Product: {product_font_size}px, Tags: {tags_font_size}px)")
                return font_product, font_tags
                
            except (OSError, IOError):
                continue
                
        # Fallback to default font
        self.logger.warning("Could not load preferred fonts, using default")
        font_product = ImageFont.load_default()
        font_tags = ImageFont.load_default()
        return font_product, font_tags
        
    def download_image(self, url: str, product_number: str, 
                      image_index: int) -> Optional[str]:
        """
        Download image from Shopify CDN
        
        Args:
            url: Image URL
            product_number: Product identifier
            image_index: Image index for naming
            
        Returns:
            Path to downloaded image or None if failed
        """
        try:
            self.logger.info(f"Downloading image {image_index} for product {product_number}")
            
            # Create temporary filename for download
            parsed_url = urlparse(url)
            extension = os.path.splitext(parsed_url.path)[1] or '.jpg'
            temp_filename = f"temp_{product_number}_{image_index:02d}{extension}"
            filepath = self.output_dir / temp_filename
            
            # Download with timeout and retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.session.get(url, timeout=30, stream=True)
                    response.raise_for_status()
                    
                    # Save image
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    self.stats['successful_downloads'] += 1
                    self.logger.info(f"Successfully downloaded: {temp_filename}")
                    return str(filepath)
                    
                except requests.RequestException as e:
                    if attempt < max_retries - 1:
                        self.logger.warning(f"Download attempt {attempt + 1} failed, retrying: {e}")
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        raise
                        
        except Exception as e:
            self.logger.error(f"Failed to download image from {url}: {e}")
            self.stats['errors'] += 1
            return None
            
    def _format_decade(self, decade: str) -> str:
        """
        Format decade to match ROSEYS website specification (19XX format)
        
        Args:
            decade: Input decade (e.g., "80s" or "1980s")
            
        Returns:
            Formatted decade (e.g., "1980s")
        """
        decade = decade.strip().lower()
        
        # Handle various input formats
        if decade.endswith('s'):
            decade_num = decade[:-1]
            if len(decade_num) == 2 and decade_num.isdigit():
                # Convert "80" to "1980"
                return f"19{decade_num}s"
            elif len(decade_num) == 4 and decade_num.startswith('19'):
                # Already in correct format "1980s"
                return f"{decade_num}s"
        elif len(decade) == 2 and decade.isdigit():
            # Convert "80" to "1980s"
            return f"19{decade}s"
        elif len(decade) == 4 and decade.startswith('19') and decade.isdigit():
            # Convert "1980" to "1980s"
            return f"{decade}s"
            
        # Return as-is if format not recognized
        return decade.upper()
        
    def create_text_overlay(self, image_path: str, product_data: ProductData,
                           image_index: int, spacing_px: int = 75) -> Optional[str]:
        """
        Add text overlay to image with SIMPLE format using "|" character separators:
        Line 1: #[PRODUCT_NUMBER]
        Line 2: DESIGNER | ORIGIN | DECADE
        
        Args:
            image_path: Path to source image
            product_data: Product information for overlay
            image_index: Image index for naming
            spacing_px: Spacing in pixels between the two text lines
            
        Returns:
            Path to processed image or None if failed
        """
        try:
            self.logger.info(f"Adding overlay to {os.path.basename(image_path)}")
            
            # Open image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Get image dimensions
                img_width, img_height = img.size
                
                # Calculate proportional font sizes based on image dimensions
                product_font_size = max(60, min(120, int(img_height / 12)))  # ~75-100px for typical images
                tag_font_size = max(48, min(96, int(img_height / 15)))       # ~60-80px for typical images
                
                # Load fonts with calculated sizes
                self.font_product, self.font_tags = self._load_fonts(product_font_size, tag_font_size)
                
                self.logger.info(f"Image dimensions: {img_width}x{img_height}")
                self.logger.info(f"Calculated font sizes - Product: {product_font_size}px, Tags: {tag_font_size}px")
                
                # Format decade to match website specification (19XX format)
                formatted_decade = self._format_decade(product_data.decade)
                
                # Prepare overlay text with EXACT website capitalization format
                # First letter capitalized only (not all caps) as per requirements
                designer_formatted = product_data.designer.capitalize()
                origin_formatted = product_data.origin.capitalize()
                
                # Simple text strings with "|" character separators
                line1 = f"#{product_data.product_number}"
                line2 = f"{designer_formatted} | {origin_formatted} | {formatted_decade}"
                
                # Create drawing context
                draw = ImageDraw.Draw(img)
                
                # Calculate text dimensions for proper centering
                line1_bbox = draw.textbbox((0, 0), line1, font=self.font_product)
                line1_width = line1_bbox[2] - line1_bbox[0]
                line1_height = line1_bbox[3] - line1_bbox[1]
                
                line2_bbox = draw.textbbox((0, 0), line2, font=self.font_tags)
                line2_width = line2_bbox[2] - line2_bbox[0]
                line2_height = line2_bbox[3] - line2_bbox[1]
                
                # Simple positioning
                y1 = int(img_height * 0.10)  # 10% from top as before
                y2 = y1 + product_font_size + spacing_px  # Line spacing - configurable pixels
                
                # Simple centering
                x1 = (img_width - line1_width) // 2
                x2 = (img_width - line2_width) // 2
                
                self.logger.info(f"Text positioning - Line1: ({x1}, {y1}), Line2: ({x2}, {y2}), Spacing: {spacing_px}px")
                
                # Draw text with simple dark color (dark gray #141414)
                text_color = (20, 20, 20)  # #141414 RGB
                
                # Draw line 1 (product number)
                draw.text(
                    (x1, y1),
                    line1,
                    font=self.font_product,
                    fill=text_color
                )
                
                # Draw line 2 (designer | origin | decade)
                draw.text(
                    (x2, y2),
                    line2,
                    font=self.font_tags,
                    fill=text_color
                )
                
                # Save processed image - production naming (no versioning)
                base_output_filename = f"{product_data.product_number}_{image_index:02d}_overlay.jpg"
                output_path = self.output_dir / base_output_filename
                
                img.save(output_path, 'JPEG', quality=self.quality, optimize=True)
                
                self.stats['successful_overlays'] += 1
                self.logger.info(f"Successfully created overlay: {versioned_output_filename}")
                return str(output_path)
                
        except Exception as e:
            self.logger.error(f"Failed to create overlay for {image_path}: {e}")
            self.stats['errors'] += 1
            return None
            
    def process_product(self, product_data: ProductData, spacing_px: int = 75) -> List[str]:
        """
        Process all images for a single product
        
        Args:
            product_data: Product information
            spacing_px: Spacing in pixels between text lines
            
        Returns:
            List of paths to processed images
        """
        self.logger.info(f"Processing product {product_data.product_number} - {product_data.designer}")
        self.stats['total_products'] += 1
        self.stats['total_images'] += len(product_data.images)
        
        processed_images = []
        
        for i, image_url in enumerate(product_data.images, 1):
            try:
                # Download original image
                downloaded_path = self.download_image(
                    image_url, product_data.product_number, i
                )
                
                if downloaded_path:
                    # Create overlay
                    overlay_path = self.create_text_overlay(
                        downloaded_path, product_data, i, spacing_px
                    )
                    
                    if overlay_path:
                        processed_images.append(overlay_path)
                        
                    # Remove original downloaded file to save space (production mode)
                    try:
                        os.remove(downloaded_path)
                        self.logger.info(f"Removed original file: {os.path.basename(downloaded_path)}")
                    except Exception as e:
                        self.logger.warning(f"Could not remove original file {downloaded_path}: {e}")
                    
            except Exception as e:
                self.logger.error(f"Error processing image {i} for product {product_data.product_number}: {e}")
                self.stats['errors'] += 1
                
        return processed_images
        
    def process_from_json(self, json_data: Union[str, Dict, List]) -> Dict:
        """
        Process products from JSON data
        
        Args:
            json_data: JSON string, dict, or list of product data
            
        Returns:
            Processing results summary
        """
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
            
        # Handle single product or list of products
        if isinstance(data, dict):
            products = [data]
        else:
            products = data
            
        results = []
        
        for product_info in products:
            try:
                product_data = ProductData(
                    product_number=product_info.get('product_number', ''),
                    designer=product_info.get('designer', ''),
                    origin=product_info.get('origin', ''),
                    decade=product_info.get('decade', ''),
                    images=product_info.get('images', []),
                    lens_mm=product_info.get('lens_mm'),
                    bridge_mm=product_info.get('bridge_mm'),
                    arm_mm=product_info.get('arm_mm')
                )
                
                processed_paths = self.process_product(product_data)
                results.append({
                    'product_number': product_data.product_number,
                    'processed_images': processed_paths,
                    'success': len(processed_paths) > 0
                })
                
            except Exception as e:
                self.logger.error(f"Error processing product data: {e}")
                self.stats['errors'] += 1
                
        return {
            'results': results,
            'stats': self.stats
        }
        
    def process_from_csv(self, csv_file: str) -> Dict:
        """
        Process products from CSV file
        
        Expected CSV columns: product_number, designer, origin, decade, image_urls, lens_mm, bridge_mm, arm_mm
        Image URLs should be semicolon-separated
        
        Args:
            csv_file: Path to CSV file
            
        Returns:
            Processing results summary
        """
        results = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    try:
                        # Parse image URLs
                        image_urls = [url.strip() for url in row.get('image_urls', '').split(';') if url.strip()]
                        
                        product_data = ProductData(
                            product_number=row.get('product_number', ''),
                            designer=row.get('designer', ''),
                            origin=row.get('origin', ''),
                            decade=row.get('decade', ''),
                            images=image_urls,
                            lens_mm=row.get('lens_mm'),
                            bridge_mm=row.get('bridge_mm'),
                            arm_mm=row.get('arm_mm')
                        )
                        
                        processed_paths = self.process_product(product_data)
                        results.append({
                            'product_number': product_data.product_number,
                            'processed_images': processed_paths,
                            'success': len(processed_paths) > 0
                        })
                        
                    except Exception as e:
                        self.logger.error(f"Error processing CSV row: {e}")
                        self.stats['errors'] += 1
                        
        except Exception as e:
            self.logger.error(f"Error reading CSV file {csv_file}: {e}")
            
        return {
            'results': results,
            'stats': self.stats
        }
        
    def generate_report(self) -> str:
        """
        Generate processing summary report
        
        Returns:
            Formatted report string
        """
        report = f"""
SHOPIFY IMAGE PROCESSING REPORT
===============================
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

STATISTICS:
- Total Products Processed: {self.stats['total_products']}
- Total Images Found: {self.stats['total_images']}
- Successful Downloads: {self.stats['successful_downloads']}
- Successful Overlays: {self.stats['successful_overlays']}
- Errors Encountered: {self.stats['errors']}

SUCCESS RATE:
- Download Success: {(self.stats['successful_downloads'] / max(self.stats['total_images'], 1)) * 100:.1f}%
- Overlay Success: {(self.stats['successful_overlays'] / max(self.stats['successful_downloads'], 1)) * 100:.1f}%

OUTPUT DIRECTORY: {self.output_dir.absolute()}
"""
        return report


def main():
    """Production overlay processing with finalized 75px spacing"""
    
    # Example Frame #001 data (single image for testing)
    frame_001_data = {
        "product_number": "001",
        "designer": "Defilè",
        "origin": "Italy",
        "decade": "1980s",  # Updated to match website format (19XX format)
        "lens_mm": "46",
        "bridge_mm": "20",
        "arm_mm": "135",
        "images": [
            "https://cdn.shopify.com/s/files/1/0705/8469/7123/files/ROSEY_sFinishedGlasses-377.jpg?v=1729751841"
            # Only processing first image for testing
        ]
    }
    
    # Initialize processor with finalized 75px spacing
    processor = ShopifyImageProcessor(
        base_font_size_product=75,  # Base size for product number (scales with image)
        base_font_size_tags=60,     # Base size for tags (scales with image)
        quality=95
    )
    
    print("Starting ROSEYS Image Processing Agent - PRODUCTION MODE...")
    print("=" * 70)
    print("Processing Frame #001 with finalized 75px spacing")
    print("Format: Line 1: '#001'")
    print("        Line 2: 'Defilè | Italy | 1980s'")
    print("Spacing: 75 pixels between lines (FINAL APPROVED)")
    print()
    
    # Create ProductData object
    from dataclasses import asdict
    product_data = ProductData(
        product_number=frame_001_data["product_number"],
        designer=frame_001_data["designer"],
        origin=frame_001_data["origin"],
        decade=frame_001_data["decade"],
        images=frame_001_data["images"],
        lens_mm=frame_001_data.get("lens_mm"),
        bridge_mm=frame_001_data.get("bridge_mm"),
        arm_mm=frame_001_data.get("arm_mm")
    )
    
    # Process with finalized 75px spacing
    print("Processing with 75px spacing (FINAL PRODUCTION SETTING):")
    print("-" * 50)
    
    processed_images = processor.process_product(product_data, spacing_px=75)
    
    if processed_images:
        for img_path in processed_images:
            filename = os.path.basename(img_path)
            print(f"  ✅ Created: {filename}")
    else:
        print(f"  ❌ Failed to process images")
    
    print()
    print("PROCESSING SUMMARY:")
    print("=" * 50)
    
    if processed_images:
        print(f"✅ Successfully processed {len(processed_images)} images")
        print(f"📁 Output directory: {processor.output_dir}")
        print(f"📏 Line spacing: 75 pixels (FINAL APPROVED)")
        for img_path in processed_images:
            print(f"   - {os.path.basename(img_path)}")
    else:
        print("❌ No images were processed successfully")
    
    # Generate and display report
    report = processor.generate_report()
    print(report)
    
    # Create production documentation
    production_report = f"""
ROSEYS IMAGE OVERLAY PRODUCTION REPORT
======================================
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

FRAME: #001 - Defilè | Italy | 1980s

PRODUCTION SETTINGS:
- Line Spacing: 75 pixels (FINALIZED)
- Font: MagdaClean-Regular.otf
- Format: "#001" / "Defilè | Italy | 1980s"
- Position: Top 10%, horizontally centered
- Output: Direct save to Obsidian project folder

PROCESSED FILES:
"""
    
    if processed_images:
        for img_path in processed_images:
            production_report += f"- {os.path.basename(img_path)}\n"
    else:
        production_report += "- None (processing failed)\n"
    
    production_report += f"""

OUTPUT DIRECTORY: {processor.output_dir.absolute()}

STATUS: Production-ready with 75px spacing standard
USAGE: Images are ready for use in ROSEYS website and marketing
"""
    
    # Save production documentation
    with open('production_overlay_report.txt', 'w') as f:
        f.write(production_report)
    
    # Save general processing report
    with open('processing_report.txt', 'w') as f:
        f.write(report)
    
    print(f"\n🎉 Processing complete! Check '{processor.output_dir}' for results.")
    if processed_images:
        print(f"✅ Created {len(processed_images)} production overlay files")
        print("📝 Documentation saved:")
        print("  - production_overlay_report.txt (production settings)")
        print("  - processing_report.txt (processing statistics)")
        print("  - shopify_processor.log (detailed execution log)")
    else:
        print("❌ No files were created - check logs for errors")


if __name__ == "__main__":
    main()