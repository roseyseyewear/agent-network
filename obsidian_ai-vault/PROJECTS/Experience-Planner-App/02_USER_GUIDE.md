# User Guide - Experience Planner App
*Simple, step-by-step instructions for planning your interactive experiences*

## 🚀 Getting Started (30 seconds)

### **Open the App**
1. **Navigate to:** `C:\claude_home\mindjourney-planner-advanced.html`
2. **Double-click** the file (opens in your web browser)
3. **You're ready!** The app loads with your MindJourney experience already loaded

---

## 📊 Understanding the Interface

### **Top Navigation**
- **📊 Table** - Excel-style editing (start here)
- **📅 Timeline** - Visual storyboard view
- **🌳 Branching** - User path flow diagram
- **+ Add Step** - Create new experience step
- **📹 Videos** - Manage your video library
- **💾 Export** - Save your work

### **Stats Bar** (shows live updates)
- **Total Steps** - Number of experience steps
- **Est. Duration** - Total experience length
- **Videos** - How many videos you've added
- **Interactions** - User input points
- **Branches** - Decision points in experience
- **Complete %** - How finished your plan is

---

## 🎯 Basic Workflow

### **Step 1: Plan Your Content (Table View)**
*Use this like Excel - click any cell to edit*

| Column | What to Put | Example |
|--------|-------------|---------|
| **Title** | Name of this step | "Welcome Screen" |
| **Duration** | How long it takes | "30s" or "2m" |
| **Copy** | All text users see | "Welcome! Click to begin..." |
| **CTA** | Button text | "Press Play to Begin" |
| **User Input** | How users respond | "Button Click" or "Text Input" |

### **Step 2: Add Videos**
1. **Click** the **+ box** in the Visual column
2. **Video Library opens** - you'll see all your videos
3. **Click any video** to assign it to that step
4. **OR drag videos** directly onto the + boxes

### **Step 3: Preview Your Experience (Timeline View)**
1. **Click "📅 Timeline"** at the top
2. **See your visual storyboard** with video thumbnails
3. **Click any video thumbnail** to preview it full-screen
4. **Review the flow** from step to step

### **Step 4: Set Up Smart Paths (Branching View)**
1. **Click "🌳 Branching"** at the top
2. **See the flow diagram** of your experience
3. **In Table view, click branching buttons** to add conditional logic
4. **Set rules** like "If user says 'positive', go to Step 4"

---

## 🎥 Working with Videos

### **Upload New Videos**
1. **Click "📹 Videos"** button
2. **Drag video files** into the upload zone
3. **OR click the upload zone** to browse files
4. **Supported formats:** MP4, WebM, MOV (up to 100MB)

### **Assign Videos to Steps**
**Method 1 - Library Selection:**
- Click + box in any step → Select from library

**Method 2 - Drag & Drop:**
- Open Video Library → Drag thumbnails to + boxes

**Method 3 - Direct Drop:**
- Drag video files from computer → Drop on + boxes

### **Preview Videos**
- **Click any video thumbnail** anywhere in the app
- **Full-screen preview** opens with controls
- **Click X** or press Escape to close

---

## 🌳 Setting Up Branching Logic

### **What is Branching?**
Smart paths that send users to different next steps based on their responses.

### **How to Add Branching**
1. **In Table view**, find the "Branching" column
2. **Click "Add rules"** for any step
3. **Branching editor opens** with these options:

| Condition | When to Use | Example |
|-----------|-------------|---------|
| **Contains** | Response includes keyword | "positive", "happy", "excited" |
| **Equals** | Exact response match | "yes", "no", specific phrase |
| **Positive Sentiment** | Happy/optimistic responses | Auto-detects positive feelings |
| **Negative Sentiment** | Sad/pessimistic responses | Auto-detects negative feelings |
| **Short Response** | Brief answers | Less than 50 characters |
| **Long Response** | Detailed answers | More than 200 characters |

### **Example Branching Setup**
```
Step 3: "How do you feel about rose-colored glasses?"

Rule 1: If response CONTAINS "love" → Go to Step 4 (Positive Path)
Rule 2: If response CONTAINS "hate" → Go to Step 5 (Negative Path)
Rule 3: If POSITIVE SENTIMENT → Go to Step 4 (Positive Path)
Default: Go to Step 6 (Neutral Path)
```

---

## 💾 Saving Your Work

### **Auto-Save (Happens Automatically)**
- **Every change saves instantly** to your browser
- **Close and reopen** - your work is still there
- **No internet required** - everything stored locally

### **Manual Export (Backup)**
1. **Click "💾 Export"** button
2. **JSON file downloads** with complete configuration
3. **Keep this file** as backup of your work
4. **Share with team members** or save to cloud storage

---

## 🎭 Three Different Views Explained

### **📊 Table View - For Detailed Editing**
*Like Excel - best for content creation*
- Edit text, assign videos, set durations
- Add branching logic, configure user inputs
- Most detailed view for building content

### **📅 Timeline View - For Story Review**
*Like a storyboard - best for reviewing flow*
- See video thumbnails in sequence
- Review content flow and pacing
- Click videos to preview them
- Perfect for client presentations

### **🌳 Branching View - For Path Analysis**  
*Like a flowchart - best for understanding user journeys*
- Visual diagram of all possible paths
- See branching logic connections
- Analyze shortest/longest user journeys
- Identify complex decision points

---

## 🔧 Pro Tips

### **Organizing Your Experience**
- **Use descriptive titles** for each step
- **Set realistic durations** (helps with planning)
- **Write complete copy** (all text users will see)
- **Test your branching logic** before launching

### **Video Management**
- **Name videos clearly** when uploading
- **Keep file sizes reasonable** (under 10MB if possible)
- **Preview videos before assigning** to steps
- **Remove unused videos** to keep library clean

### **Planning Workflow**
1. **Start in Table view** - plan all content
2. **Switch to Timeline** - review the story flow  
3. **Use Branching view** - set up smart paths
4. **Export regularly** - backup your work

---

## ❓ Troubleshooting

### **Video Won't Upload**
- Check file format (MP4, WebM, MOV only)
- Check file size (under 100MB)
- Try refreshing the page

### **Can't See My Videos**
- Make sure you're in the correct folder
- Check if videos were uploaded to the library
- Refresh the page if needed

### **Branching Not Working**
- Make sure you clicked "Save Logic" after editing
- Check that target steps exist
- Test your conditional logic with sample responses

### **Lost My Work**
- Check browser's local storage (should auto-restore)
- Look for exported JSON backup files
- Contact support if data is critical

---

## 📞 Quick Reference

### **File Locations**
- **Main App:** `C:\claude_home\mindjourney-planner-advanced.html`
- **Your Videos:** Uploaded to browser memory (export to save permanently)

### **Keyboard Shortcuts**
- **Escape** - Close any modal/preview
- **Tab** - Move between form fields
- **Enter** - Save text input

### **Supported Formats**
- **Video:** MP4, WebM, MOV (up to 100MB)
- **Export:** JSON format
- **Browsers:** Chrome, Firefox, Safari, Edge

---

**🎯 Remember:** This tool is designed to feel like Excel but with video superpowers. Start simple, add complexity as you get comfortable!