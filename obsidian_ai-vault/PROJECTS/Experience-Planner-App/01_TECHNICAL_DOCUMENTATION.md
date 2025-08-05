# Technical Documentation - Experience Planner App

## 🏗️ Architecture Overview

### **Frontend Framework**
- **Vue.js 3** - Reactive framework for dynamic UI
- **Tailwind CSS** - Utility-first styling
- **Vis.js Network** - Interactive branching visualization
- **Native HTML5** - Video preview and file handling

### **Core Components**

#### **1. Data Management**
```javascript
// Core data structure
steps: [
  {
    id: unique_id,
    title: string,
    videoUrl: string,
    duration: string,
    copy: string,
    cta: string,
    userInput: enum,
    branches: [
      {
        condition: enum,
        value: string,
        nextStep: id
      }
    ]
  }
]
```

#### **2. Video Management System**
```javascript
availableVideos: [
  {
    filename: string,
    name: string,
    url: string (blob or file path),
    size: string,
    file: File object (for uploads)
  }
]
```

#### **3. View System**
- **Table View:** Excel-style editing interface
- **Timeline View:** Visual storyboard with video previews  
- **Branching View:** Interactive flow diagram using Vis.js

## 🔧 Key Functions

### **Video Integration**
```javascript
// Drag & Drop Implementation
handleDragStart(event, video) // Start drag from library
handleDrop(event, stepId)     // Drop video on step
handleFileUpload(event)       // Upload new video files
processFiles(files)           // Process dropped/selected files
```

### **Branching Logic**
```javascript
// Branching System
editBranching(stepId)         // Open branching editor
addBranchingRule()           // Add new conditional rule
saveBranchingLogic()         // Save branching configuration
calculateAllPaths()         // Analyze possible user paths
```

### **Analytics & Statistics**
```javascript
// Computed Properties
totalDuration()              // Calculate total experience time
videoCount()                 // Count assigned videos
interactionCount()           // Count user interaction points
branchingPoints()            // Count branching decision points
completionRate()             // Calculate completion percentage
```

## 💾 Data Persistence

### **Local Storage**
```javascript
// Auto-save implementation
saveToLocalStorage() {
  localStorage.setItem('mindjourney-planner', JSON.stringify({
    steps: this.steps,
    availableVideos: this.availableVideos
  }));
}
```

### **Export Format**
```json
{
  "experience": "MindJourney",
  "version": "2.0",
  "steps": [...],
  "statistics": {
    "totalSteps": number,
    "totalDuration": string,
    "videoCount": number,
    "interactionCount": number,
    "branchingPoints": number,
    "completionRate": number
  },
  "exportedAt": "ISO_timestamp"
}
```

## 🎥 Video System Integration

### **Supported Formats**
- **Upload:** MP4, WebM, MOV (up to 100MB)
- **Preview:** Native HTML5 video element
- **Storage:** Browser File API with blob URLs

### **File Handling**
```javascript
// File processing pipeline
1. User drops/selects video files
2. Create blob URLs for preview
3. Add to availableVideos array
4. Enable drag-drop assignment to steps
5. Store file metadata for export
```

## 🌳 Branching Logic System

### **Condition Types**
```javascript
conditions = {
  'contains': 'Response contains keyword',
  'equals': 'Response equals exact text',
  'sentiment_positive': 'Positive sentiment detected',
  'sentiment_negative': 'Negative sentiment detected', 
  'length_short': 'Short response (< 50 chars)',
  'length_long': 'Long response (> 200 chars)'
}
```

### **Visualization Engine**
```javascript
// Vis.js Network Configuration
nodes = steps.map(step => ({
  id: step.id,
  label: step.title,
  color: hasBranching ? '#ff6b6b' : '#4ecdc4'
}));

edges = branches.map(branch => ({
  from: step.id,
  to: branch.nextStep,
  label: branch.condition + ': ' + branch.value,
  arrows: 'to'
}));
```

## 📊 Performance Considerations

### **Optimization Features**
- **Lazy Loading:** Videos load only when previewed
- **Local Storage:** Persistent state without server dependency
- **Debounced Updates:** Reduced re-renders during editing
- **Blob URL Management:** Proper cleanup of temporary URLs

### **Browser Compatibility**
- **Chrome/Edge:** Full support (recommended)
- **Firefox:** Full support
- **Safari:** Full support with minor styling differences
- **Mobile:** Responsive design, touch-friendly interface

## 🔌 Integration Points

### **MindJourney App Integration**
```javascript
// Export format compatible with MindJourney schema
{
  experimentLevels: [
    {
      levelNumber: index + 1,
      videoUrl: step.videoUrl,
      questions: parseQuestions(step.copy),
      branchingRules: step.branches
    }
  ]
}
```

### **Database Schema Mapping**
```sql
-- Compatible with existing MindJourney schema
experiment_levels (
  id, experiment_id, level_number,
  video_url, background_video_url,
  questions (jsonb), branching_rules (jsonb)
)
```

## 🚀 Deployment Options

### **Current: Static HTML File**
- **Location:** `C:\claude_home\mindjourney-planner-advanced.html`
- **Dependencies:** None (CDN resources)
- **Usage:** Double-click to open in browser

### **Future: Web Server Deployment**
```bash
# Simple HTTP server
python -m http.server 8000
# Access at: http://localhost:8000/mindjourney-planner-advanced.html
```

### **Future: Desktop App**
```bash
# Electron wrapper for desktop deployment
npm install electron
# Package as standalone desktop application
```

## 🔐 Security Considerations

### **File Upload Safety**
- Client-side file type validation
- Size limits (100MB max)
- Blob URL sandboxing
- No server-side storage by default

### **Data Privacy**
- All data stored locally in browser
- No external API calls (except CDN resources)
- Export files contain no sensitive information
- Manual data export/import only

## 🧪 Testing Approach

### **Manual Testing Checklist**
- [ ] Video upload and preview functionality
- [ ] Drag-drop between library and steps
- [ ] Branching logic editor saves correctly
- [ ] Export/import maintains data integrity  
- [ ] All three views render correctly
- [ ] Local storage persistence works
- [ ] Statistics calculate accurately

### **Browser Testing**
- [ ] Chrome (primary target)
- [ ] Firefox compatibility
- [ ] Safari compatibility  
- [ ] Edge compatibility
- [ ] Mobile responsive design

---

**File Locations:**
- **Main App:** `C:\claude_home\mindjourney-planner-advanced.html`
- **Basic Version:** `C:\claude_home\mindjourney-planner.html`
- **Video Assets:** `C:\claude_home\00_imports\MindJourney-v1\client\public\videos\`