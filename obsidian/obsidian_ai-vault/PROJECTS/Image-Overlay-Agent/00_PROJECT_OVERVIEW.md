# Image Overlay Agent

**Project Type:** Automated Image Processing System  
**Purpose:** Generate branded product image overlays for ROSEYS vintage eyewear frames  
**Status:** Production Finalized - 75px Spacing Standard  

---

## **🎯 PROJECT OVERVIEW**

The Image Overlay Agent automatically downloads Shopify product images and applies branded text overlays matching the exact format used on the ROSEYS website.

### **Key Features:**
✅ **Website-Perfect Formatting** - Matches ROSEYS product card overlays exactly  
✅ **Magda Clean Font Integration** - Uses authentic ROSEYS brand font  
✅ **Proportional Scaling** - Text scales automatically based on image dimensions  
✅ **Professional Positioning** - CSS-equivalent centering and positioning  
✅ **Batch Processing** - Handle multiple frames and images efficiently  

---

## **📁 PROJECT STRUCTURE**

```
Image-Overlay-Agent/
├── 00_PROJECT_OVERVIEW.md          # This file
├── Frame Product Images/            # Processed overlay images
│   ├── 001_01_overlay.jpg          # Frame #001 test image
│   ├── 001_02_overlay.jpg          # (Future batch processing)
│   └── ...                         # Additional processed frames
└── Agent Scripts/                   # (Future: move scripts here)
```

---

## **🔧 TECHNICAL SPECIFICATIONS**

### **Overlay Format:**
```
#001
Defilè | Italy | 1980s
```

### **Styling Details:**
- **Font:** MagdaClean-Regular.otf (authentic ROSEYS font)
- **Line Spacing:** 75 pixels (FINALIZED STANDARD)
- **Capitalization:** First letter only (Defilè, Italy)
- **Separators:** Visual vertical lines (CSS-style, not typed "|")
- **Positioning:** Top 10% of image, horizontally centered
- **Scaling:** Proportional to image dimensions

### **Font Sizing (Dynamic):**
- **Product Number:** `max(60, min(120, int(image_height / 12)))`
- **Tags:** `max(48, min(96, int(image_height / 15)))`
- **Example (4000px image):** Product# 120px, Tags 96px

---

## **🚀 USAGE**

### **Current Scripts:**
- **Main Processor:** `C:\claude_home\shopify_image_processor.py`
- **Automation Agent:** `C:\claude_home\automated_image_agent.py`

### **Input Format:**
```json
{
  "product_number": "001",
  "designer": "Defilè",
  "origin": "Italy", 
  "decade": "80s",
  "images": ["https://cdn.shopify.com/..."]
}
```

### **Output:**
- **Processed Images:** Saved to `Frame Product Images/`
- **Naming Convention:** `{product}_{image}_overlay.jpg` (no versioning)
- **Quality:** High-resolution with professional overlay
- **Original Files:** Automatically removed after overlay creation

---

## **✅ PRODUCTION SPECIFICATIONS**

### **Final Configuration (Completed):**
- **Line Spacing:** 75 pixels (APPROVED STANDARD)
- **Font:** MagdaClean-Regular.otf (120px/96px scaled)
- **Format:** "#001" / "Defilè | Italy | 1980s"
- **Position:** Top 10%, horizontally centered
- **Output:** Direct save to project folder (no originals kept)
- **Naming:** Production standard (no versioning)

### **Production Verification:**
✅ **Spacing:** 75px finalized as standard
✅ **Export:** Only overlay files (originals removed)
✅ **Directory:** Direct save to Obsidian project folder
✅ **Naming:** Clean production naming (no _v2, _v3)
✅ **Font:** Authentic Magda Clean integration
✅ **Format:** Exact website match  

---

## **📋 USAGE INSTRUCTIONS**

### **Production Processing:**
1. Run `python shopify_image_processor.py` for single frame processing
2. Run `python automated_image_agent.py` for automated batch processing
3. Images save directly to `Frame Product Images/` folder
4. Original downloads are automatically cleaned up

### **Integration Ready:**
- ROSEYS Email Strategy project
- Website product updates
- Marketing materials
- Social media content

---

**Status:** Production Finalized - 75px Spacing Standard  
**Last Updated:** August 6, 2025  
**Production Settings:** 75px spacing, direct save, no originals  
**Output Directory:** `Frame Product Images/`