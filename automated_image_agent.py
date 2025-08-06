#!/usr/bin/env python3
"""
Automated Shopify Image Processing Agent - Production Mode
==========================================================

A complete automation wrapper that handles dependency installation,
environment setup, and image processing with finalized 75px spacing.

Author: Claude Code
Created: 2025-08-05
Finalized: 2025-08-06
"""

import os
import sys
import subprocess
import time
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import platform

class AutomatedImageAgent:
    """
    Automated agent for running Shopify image processing system
    """
    
    def __init__(self, log_level: str = "INFO"):
        """Initialize the automated agent"""
        self.start_time = time.time()
        self.setup_logging(log_level)
        self.status = {
            'dependency_check': False,
            'dependency_install': False,
            'processor_import': False,
            'processing_complete': False,
            'errors': [],
            'warnings': [],
            'processed_files': []
        }
        
        # Frame #001 data as specified in requirements (updated to match website format)
        self.frame_001_data = {
            "product_number": "001",
            "designer": "Defilè",
            "origin": "Italy", 
            "decade": "1980s",  # Updated to match website format (19XX format)
            "lens_mm": "46",
            "bridge_mm": "20", 
            "arm_mm": "135",
            "images": [
                "https://cdn.shopify.com/s/files/1/0705/8469/7123/files/ROSEY_sFinishedGlasses-377.jpg?v=1729751841",
                "https://cdn.shopify.com/s/files/1/0705/8469/7123/files/ROSEY_sFinishedGlasses-376.jpg?v=1729751841",
                "https://cdn.shopify.com/s/files/1/0705/8469/7123/files/ROSEY_sFinishedGlasses-378.jpg?v=1729751841"
            ]
        }
        
    def setup_logging(self, log_level: str):
        """Setup comprehensive logging system"""
        log_format = '%(asctime)s - [%(levelname)s] - %(message)s'
        
        # Create logs directory
        logs_dir = Path("automation_logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Setup file handler with timestamp
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        log_file = logs_dir / f"automation_agent_{timestamp}.log"
        
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.log_file = log_file
        
        # Log system information
        self.logger.info("="*60)
        self.logger.info("AUTOMATED SHOPIFY IMAGE PROCESSING AGENT STARTED")
        self.logger.info("="*60)
        self.logger.info(f"Python Version: {sys.version}")
        self.logger.info(f"Platform: {platform.platform()}")
        self.logger.info(f"Working Directory: {os.getcwd()}")
        self.logger.info(f"Log File: {log_file}")
        
    def print_banner(self):
        """Print startup banner"""
        banner = """
================================================================
                  ROSEYS AUTOMATION AGENT                    
              Shopify Image Processing System                 
                                                              
  * Auto-installs dependencies                               
  * Processes Frame #001 automatically                       
  * Handles errors gracefully                                
  * Provides detailed status reporting                       
================================================================
"""
        print(banner)
        self.logger.info("Automation Agent initialized successfully")
        
    def check_python_version(self) -> bool:
        """Check if Python version is compatible"""
        self.logger.info("Checking Python version compatibility...")
        
        version_info = sys.version_info
        required_major, required_minor = 3, 7
        
        if version_info.major < required_major or (version_info.major == required_major and version_info.minor < required_minor):
            error_msg = f"Python {required_major}.{required_minor}+ required. Current: {version_info.major}.{version_info.minor}"
            self.logger.error(error_msg)
            self.status['errors'].append(error_msg)
            return False
            
        self.logger.info(f"✓ Python {version_info.major}.{version_info.minor}.{version_info.micro} is compatible")
        return True
        
    def check_dependencies(self) -> Tuple[bool, List[str]]:
        """Check if required dependencies are installed"""
        self.logger.info("Checking required dependencies...")
        
        required_packages = {
            'requests': 'requests',
            'PIL': 'Pillow',
            'urllib3': 'urllib3',
            'certifi': 'certifi'
        }
        
        missing_packages = []
        installed_packages = []
        
        for import_name, package_name in required_packages.items():
            try:
                __import__(import_name)
                installed_packages.append(package_name)
                self.logger.info(f"✓ {package_name} is installed")
            except ImportError:
                missing_packages.append(package_name)
                self.logger.warning(f"✗ {package_name} is missing")
                
        if not missing_packages:
            self.logger.info("✓ All required dependencies are installed")
            self.status['dependency_check'] = True
            return True, []
        else:
            self.logger.warning(f"Missing packages: {', '.join(missing_packages)}")
            return False, missing_packages
            
    def install_dependencies(self, missing_packages: Optional[List[str]] = None) -> bool:
        """Install missing dependencies automatically"""
        self.logger.info("Installing dependencies...")
        
        try:
            # Check if requirements.txt exists
            requirements_file = Path("requirements.txt")
            if requirements_file.exists():
                self.logger.info("Found requirements.txt, installing from file...")
                cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"]
            else:
                # Install individual packages if requirements.txt not found
                if missing_packages:
                    self.logger.info(f"Installing missing packages: {missing_packages}")
                    packages = missing_packages
                else:
                    # Install all required packages
                    packages = ["requests>=2.31.0", "Pillow>=10.0.0", "urllib3>=1.26.0", "certifi>=2023.0.0"]
                    
                cmd = [sys.executable, "-m", "pip", "install"] + packages + ["--upgrade"]
            
            self.logger.info(f"Running: {' '.join(cmd)}")
            
            # Run pip install with real-time output
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Stream output in real-time
            output_lines = []
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    output_lines.append(line)
                    if any(keyword in line.lower() for keyword in ['installing', 'successfully', 'requirement', 'error']):
                        self.logger.info(f"PIP: {line}")
                        
            return_code = process.poll()
            
            if return_code == 0:
                self.logger.info("✓ Dependencies installed successfully")
                self.status['dependency_install'] = True
                return True
            else:
                error_msg = f"Dependency installation failed with return code {return_code}"
                self.logger.error(error_msg)
                self.status['errors'].append(error_msg)
                return False
                
        except Exception as e:
            error_msg = f"Error during dependency installation: {e}"
            self.logger.error(error_msg)
            self.status['errors'].append(error_msg)
            return False
            
    def verify_processor_files(self) -> bool:
        """Verify that required processor files exist"""
        self.logger.info("Verifying processor files...")
        
        required_files = [
            "shopify_image_processor.py",
            "requirements.txt"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
                self.logger.error(f"✗ Missing required file: {file_path}")
            else:
                self.logger.info(f"✓ Found: {file_path}")
                
        if missing_files:
            error_msg = f"Missing required files: {', '.join(missing_files)}"
            self.status['errors'].append(error_msg)
            return False
            
        return True
        
    def import_processor(self) -> bool:
        """Import the shopify image processor"""
        self.logger.info("Importing Shopify Image Processor...")
        
        try:
            # Add current directory to path if needed
            if '.' not in sys.path:
                sys.path.insert(0, '.')
                
            # Import the processor
            global ShopifyImageProcessor
            from shopify_image_processor import ShopifyImageProcessor
            
            self.logger.info("✓ Successfully imported ShopifyImageProcessor")
            self.status['processor_import'] = True
            return True
            
        except ImportError as e:
            error_msg = f"Failed to import ShopifyImageProcessor: {e}"
            self.logger.error(error_msg)
            self.status['errors'].append(error_msg)
            return False
        except Exception as e:
            error_msg = f"Unexpected error importing processor: {e}"
            self.logger.error(error_msg)
            self.status['errors'].append(error_msg)
            return False
            
    def process_frame_001(self) -> bool:
        """Process Frame #001 automatically"""
        self.logger.info("Starting Frame #001 processing...")
        self.logger.info(f"Product: {self.frame_001_data['product_number']} - {self.frame_001_data['designer']}")
        self.logger.info(f"Origin: {self.frame_001_data['origin']}")
        self.logger.info(f"Decade: {self.frame_001_data['decade']}")
        self.logger.info(f"Images to process: {len(self.frame_001_data['images'])}")
        
        try:
            # Initialize processor with finalized production settings
            processor = ShopifyImageProcessor(
                output_dir=r"C:\claude_home\obsidian_ai-vault\PROJECTS\Image-Overlay-Agent\Frame Product Images",
                base_font_size_product=75,  # Final production font size
                base_font_size_tags=60,     # Final production font size
                quality=95
            )
            
            self.logger.info("✓ Processor initialized successfully")
            
            # Process Frame #001 with finalized 75px spacing
            results = processor.process_from_json(self.frame_001_data)
            
            # Analyze results
            if results and 'results' in results and results['results']:
                product_result = results['results'][0]
                
                if product_result.get('success', False):
                    processed_files = product_result.get('processed_images', [])
                    self.status['processed_files'] = processed_files
                    
                    self.logger.info("✓ Frame #001 processing completed successfully!")
                    self.logger.info(f"✓ Generated {len(processed_files)} processed images")
                    
                    for file_path in processed_files:
                        if os.path.exists(file_path):
                            file_size = os.path.getsize(file_path) / 1024  # KB
                            self.logger.info(f"  - {os.path.basename(file_path)} ({file_size:.1f} KB)")
                        else:
                            self.logger.warning(f"  - {os.path.basename(file_path)} (FILE NOT FOUND)")
                            
                    # Generate and save processing report
                    report = processor.generate_report()
                    report_file = "automated_processing_report.txt"
                    
                    with open(report_file, 'w') as f:
                        f.write(report)
                        
                    self.logger.info(f"✓ Processing report saved: {report_file}")
                    
                    # Log statistics
                    stats = results.get('stats', {})
                    self.logger.info("Processing Statistics:")
                    self.logger.info(f"  - Total Products: {stats.get('total_products', 0)}")
                    self.logger.info(f"  - Total Images: {stats.get('total_images', 0)}")
                    self.logger.info(f"  - Successful Downloads: {stats.get('successful_downloads', 0)}")
                    self.logger.info(f"  - Successful Overlays: {stats.get('successful_overlays', 0)}")
                    self.logger.info(f"  - Errors: {stats.get('errors', 0)}")
                    
                    if stats.get('errors', 0) == 0:
                        self.status['processing_complete'] = True
                        return True
                    else:
                        warning_msg = f"Processing completed with {stats.get('errors', 0)} errors"
                        self.logger.warning(warning_msg)
                        self.status['warnings'].append(warning_msg)
                        return True  # Still consider successful if some images processed
                else:
                    error_msg = "Frame #001 processing failed"
                    self.logger.error(error_msg)
                    self.status['errors'].append(error_msg)
                    return False
            else:
                error_msg = "No processing results returned"
                self.logger.error(error_msg)
                self.status['errors'].append(error_msg)
                return False
                
        except Exception as e:
            error_msg = f"Error during Frame #001 processing: {e}"
            self.logger.error(error_msg)
            self.status['errors'].append(error_msg)
            return False
            
    def generate_final_report(self) -> str:
        """Generate comprehensive final report"""
        elapsed_time = time.time() - self.start_time
        
        report = f"""
================================================================
                    AUTOMATION AGENT REPORT                  
================================================================

EXECUTION SUMMARY:
==================
Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.start_time))}
End Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
Total Duration: {elapsed_time:.2f} seconds

STATUS CHECKS:
==============
* Python Version Check: {"PASSED" if sys.version_info >= (3, 7) else "FAILED"}
* Dependency Check: {"PASSED" if self.status['dependency_check'] else "COMPLETED WITH INSTALL"}
* Dependency Install: {"PASSED" if self.status['dependency_install'] else "NOT REQUIRED"}
* Processor Import: {"PASSED" if self.status['processor_import'] else "FAILED"}
* Frame #001 Processing: {"PASSED" if self.status['processing_complete'] else "FAILED"}

PROCESSED FILES:
================
"""
        
        if self.status['processed_files']:
            for i, file_path in enumerate(self.status['processed_files'], 1):
                file_name = os.path.basename(file_path)
                exists = "OK" if os.path.exists(file_path) else "MISSING"
                size = f"({os.path.getsize(file_path) / 1024:.1f} KB)" if os.path.exists(file_path) else "(NOT FOUND)"
                report += f"{i}. [{exists}] {file_name} {size}\n"
        else:
            report += "No files were processed successfully.\n"
            
        if self.status['warnings']:
            report += f"\nWARNINGS ({len(self.status['warnings'])}):\n"
            report += "=" * 20 + "\n"
            for i, warning in enumerate(self.status['warnings'], 1):
                report += f"{i}. {warning}\n"
                
        if self.status['errors']:
            report += f"\nERRORS ({len(self.status['errors'])}):\n"
            report += "=" * 20 + "\n"
            for i, error in enumerate(self.status['errors'], 1):
                report += f"{i}. {error}\n"
                
        report += f"\nLOG FILE: {self.log_file}\n"
        report += f"OUTPUT DIRECTORY: {os.path.abspath(r'C:\claude_home\obsidian_ai-vault\PROJECTS\Image-Overlay-Agent\Frame Product Images')}\n"
        
        # Overall status
        overall_success = (
            self.status['processor_import'] and 
            (self.status['processing_complete'] or len(self.status['processed_files']) > 0)
        )
        
        report += f"\nOVERALL STATUS: {'SUCCESS' if overall_success else 'FAILED'}\n"
        
        if overall_success:
            report += "\n*** AUTOMATION COMPLETED SUCCESSFULLY! ***\n"
            report += "Your Frame #001 images have been processed with overlays.\n"
        else:
            report += "\n*** AUTOMATION FAILED! ***\n"
            report += "Check the errors above and log file for details.\n"
            
        report += "\n" + "="*60 + "\n"
        
        return report
        
    def run(self) -> bool:
        """Run the complete automation process"""
        try:
            # Print startup banner
            self.print_banner()
            
            # Step 1: Check Python version
            if not self.check_python_version():
                return False
                
            # Step 2: Verify required files exist
            if not self.verify_processor_files():
                return False
                
            # Step 3: Check dependencies
            deps_ok, missing_packages = self.check_dependencies()
            
            # Step 4: Install dependencies if needed
            if not deps_ok:
                if not self.install_dependencies(missing_packages):
                    return False
                    
                # Re-check dependencies after installation
                deps_ok, remaining_missing = self.check_dependencies()
                if not deps_ok:
                    error_msg = f"Dependencies still missing after installation: {remaining_missing}"
                    self.logger.error(error_msg)
                    self.status['errors'].append(error_msg)
                    return False
                    
            # Step 5: Import processor
            if not self.import_processor():
                return False
                
            # Step 6: Process Frame #001
            if not self.process_frame_001():
                return False
                
            return True
            
        except KeyboardInterrupt:
            self.logger.warning("Automation interrupted by user")
            return False
        except Exception as e:
            error_msg = f"Unexpected error in automation: {e}"
            self.logger.error(error_msg)
            self.status['errors'].append(error_msg)
            return False


def main():
    """Main entry point for automation agent - Production Mode with 75px spacing"""
    
    # Create and run automation agent
    agent = AutomatedImageAgent(log_level="INFO")
    
    try:
        success = agent.run()
        
        # Generate and display final report
        final_report = agent.generate_final_report()
        print(final_report)
        
        # Save final report
        with open("automation_final_report.txt", "w") as f:
            f.write(final_report)
            
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"Fatal error in automation agent: {e}")
        agent.logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()