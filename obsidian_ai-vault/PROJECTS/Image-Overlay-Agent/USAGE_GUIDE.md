# Image Overlay Agent - Usage Guide

**Production Ready System with 75px Spacing Standard**

---

## **🚀 QUICK START**

### **Single Frame Processing:**
```bash
cd C:\claude_home
python shopify_image_processor.py
```

### **Automated Processing:**
```bash
cd C:\claude_home
python automated_image_agent.py
```

---

## **📋 PRODUCTION SETTINGS**

### **Finalized Configuration:**
- **Line Spacing:** 75 pixels (APPROVED STANDARD)
- **Font:** MagdaClean-Regular.otf
- **Font Sizes:** Product# 120px, Tags 96px (auto-scaled)
- **Format:** "#001" / "Defilè | Italy | 1980s"
- **Position:** Top 10%, horizontally centered

### **Output Specifications:**
- **Directory:** `C:\claude_home\obsidian_ai-vault\PROJECTS\Image-Overlay-Agent\Frame Product Images`
- **Naming:** `001_01_overlay.jpg`, `001_02_overlay.jpg`, etc.
- **Quality:** High-resolution JPEG (95% quality)
- **Cleanup:** Original downloads automatically removed

---

## **📝 INPUT FORMAT**

### **JSON Structure:**
```json
{
  "product_number": "001",
  "designer": "Defilè",
  "origin": "Italy",
  "decade": "1980s",
  "images": [
    "https://cdn.shopify.com/s/files/1/0705/8469/7123/files/ROSEY_sFinishedGlasses-377.jpg"
  ]
}
```

### **CSV Format (Alternative):**
```csv
product_number,designer,origin,decade,image_urls
001,Defilè,Italy,1980s,"https://cdn.shopify.com/...;https://cdn.shopify.com/..."
```

---

## **⚙️ SYSTEM REQUIREMENTS**

### **Dependencies:**
- Python 3.7+
- PIL/Pillow
- Requests
- MagdaClean-Regular.otf font file

### **Auto-Installation:**
The automated agent handles dependency installation automatically.

---

## **📂 FILE STRUCTURE**

```
Image-Overlay-Agent/
├── 00_PROJECT_OVERVIEW.md          # Project documentation
├── USAGE_GUIDE.md                  # This file
├── Frame Product Images/            # Output directory
│   ├── 001_01_overlay.jpg          # Processed overlay images
│   ├── 001_02_overlay.jpg
│   └── ...
└── Agent Scripts/                   # (Future organization)
```

---

## **✅ SUCCESS CRITERIA VERIFIED**

✅ **75px spacing set as default**  
✅ **Only overlay files exported (no originals)**  
✅ **Direct save to Obsidian project folder**  
✅ **Clean production naming (no versioning)**  
✅ **Documentation updated in Obsidian**  

---

## **🔧 TROUBLESHOOTING**

### **Common Issues:**

1. **Font Missing:**
   - Ensure `MagdaClean-Regular.otf` is in script directory
   - System will fallback to Arial if font not found

2. **Directory Permissions:**
   - Ensure write access to output directory
   - Directory is auto-created if missing

3. **Network Issues:**
   - Check internet connection for image downloads
   - CDN URLs may require valid user agent

### **Log Files:**
- `shopify_processor.log` - Processing details
- `automation_logs/` - Automated agent logs

---

## **🎯 PRODUCTION READY**

The system is now configured for production use with:
- Finalized 75px spacing
- Streamlined export process  
- Complete documentation
- Error handling and logging

**Ready for ROSEYS marketing and website integration!**