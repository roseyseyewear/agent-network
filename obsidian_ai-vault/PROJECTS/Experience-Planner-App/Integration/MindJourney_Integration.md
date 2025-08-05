# MindJourney Integration Guide

## 🔗 How Experience Planner Connects with MindJourney

### **Data Flow Overview**
```
Experience Planner → JSON Export → Database Population → MindJourney App
```

## 📊 Database Schema Mapping

### **Experience Planner Structure**
```javascript
step: {
  id: "step_1",
  title: "Welcome Screen", 
  videoUrl: "/videos/level1.mp4",
  duration: "60s",
  copy: "Welcome to the experiment...",
  cta: "Press Play to Begin",
  userInput: "button",
  branches: [
    {
      condition: "contains",
      value: "positive", 
      nextStep: "step_4"
    }
  ]
}
```

### **MindJourney Database Schema**
```sql
-- Maps to experimentLevels table
experiment_levels (
  id varchar primary key,
  experiment_id varchar,
  level_number integer,
  video_url text,
  background_video_url text,
  questions jsonb,
  branching_rules jsonb
)
```

## 🔄 Conversion Process

### **Step 1: Export from Planner**
1. Open Experience Planner
2. Click "💾 Export" button
3. Save JSON file with complete configuration

### **Step 2: Database Population Script**
```javascript
// Convert Experience Planner export to MindJourney format
function convertPlannerToMindJourney(plannerData) {
  return plannerData.steps.map((step, index) => ({
    level_number: index + 1,
    video_url: step.videoUrl,
    background_video_url: getBackgroundVideo(step),
    questions: parseQuestionsFromCopy(step.copy),
    branching_rules: step.branches.map(branch => ({
      condition: branch.condition,
      target_path: branch.nextStep,
      next_level_id: findLevelByStepId(branch.nextStep)
    }))
  }));
}
```

### **Step 3: Video Asset Management**
```javascript
// Ensure video paths are correctly mapped
const videoPathMapping = {
  // Experience Planner paths
  './00_imports/MindJourney-v1/client/public/videos/level1.mp4': 
  // MindJourney production paths  
  '/videos/level1.mp4'
};
```

## 🎥 Video Integration Points

### **Current Video Assets**
| Planner Asset | MindJourney Path | Usage |
|---------------|------------------|-------|
| level1.mp4 | /videos/level1.mp4 | Main level video |
| chat-loop.mp4 | /videos/chat-loop.mp4 | Background during questions |
| hypothesis-post-submission.mp4 | /videos/hypothesis-post-submission.mp4 | After completion |

### **Video Assignment Logic**
```javascript
// Automatic video type detection
function categorizeVideo(step) {
  if (step.userInput === 'multimodal') {
    return {
      video_url: step.videoUrl,
      background_video_url: '/videos/chat-loop.mp4'
    };
  } else if (step.cta === 'Auto-transition') {
    return {
      video_url: step.videoUrl,
      background_video_url: null
    };
  }
  // Additional logic for different step types
}
```

## 🌳 Branching Logic Integration

### **Planner Branching Format**
```javascript
branches: [
  {
    condition: "contains",
    value: "positive",
    nextStep: "step_4"
  }
]
```

### **MindJourney Branching Format**
```json
{
  "branching_rules": [
    {
      "condition": "contains:positive",
      "target_path": "positive_path",
      "next_level_id": "level_4"
    }
  ]
}
```

### **Conversion Logic**
```javascript
function convertBranching(plannerBranches, steps) {
  return plannerBranches.map(branch => ({
    condition: `${branch.condition}:${branch.value}`,
    target_path: generatePathName(branch.condition, branch.value),
    next_level_id: findMindJourneyLevelId(branch.nextStep, steps)
  }));
}
```

## 📝 Question Parsing System

### **Extract Questions from Copy Field**
```javascript
function parseQuestionsFromCopy(copyText) {
  // Parse chat interface questions from copy text
  const lines = copyText.split('\n').filter(line => line.trim());
  
  const questions = [];
  let currentQuestion = null;
  
  lines.forEach(line => {
    if (line.includes('?')) {
      // This is a question
      questions.push({
        id: generateQuestionId(),
        type: 'text',
        text: line.trim(),
        required: true
      });
    }
  });
  
  return questions;
}
```

## 🔧 Implementation Script

### **Complete Integration Script**
```javascript
// integration-script.js
async function integratePlannerExport(jsonFile) {
  // 1. Load planner export
  const plannerData = JSON.parse(jsonFile);
  
  // 2. Convert to MindJourney format
  const mindJourneyLevels = convertPlannerToMindJourney(plannerData);
  
  // 3. Populate database
  for (const level of mindJourneyLevels) {
    await db.experimentLevels.create({
      experiment_id: 'current_experiment_id',
      ...level
    });
  }
  
  // 4. Update video paths
  await updateVideoAssets(plannerData.steps);
  
  console.log('Integration complete!');
}
```

## 🧪 Testing Integration

### **Validation Checklist**
- [ ] All videos load correctly in MindJourney app
- [ ] Questions appear in chat interface as expected
- [ ] Branching logic routes users to correct next levels
- [ ] Duration estimates match actual experience timing
- [ ] User input types work with chat interface
- [ ] Export/import maintains data integrity

### **Test Scenarios**
1. **Linear Flow Test** - No branching, sequential steps
2. **Branching Test** - Multiple paths based on user responses
3. **Video Integration Test** - All video assets load and play
4. **Chat Integration Test** - Questions extracted correctly
5. **Duration Test** - Timing estimates vs actual experience

## 🚀 Deployment Process

### **Development to Production**
1. **Plan in Experience Planner** - Create complete experience
2. **Export Configuration** - Generate JSON with all settings
3. **Run Integration Script** - Populate MindJourney database
4. **Test in Development** - Validate complete user flow
5. **Deploy to Production** - Release updated experience

### **Rollback Strategy**
```javascript
// Keep backup of previous configuration
const backupExperiment = async () => {
  const currentLevels = await db.experimentLevels.findAll();
  fs.writeFileSync('backup.json', JSON.stringify(currentLevels));
};
```

## 📊 Analytics Integration

### **Tracking Experience Performance**
```javascript
// Add analytics to track planner-designed experiences
const trackExperienceStep = (stepId, plannerStepTitle) => {
  analytics.track('experience_step_completed', {
    step_id: stepId,
    planner_title: plannerStepTitle,
    designed_with: 'experience_planner'
  });
};
```

---

**Integration Status:** Ready for implementation  
**Testing Required:** Database population and video path validation  
**Dependencies:** MindJourney database access, video asset paths