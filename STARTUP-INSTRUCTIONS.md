# Claude Code Startup Instructions

## Complete Startup Sequence

**Copy and paste these commands every time you start Claude Code:**

```powershell
# Navigate to workspace
cd C:\claude_home

# Set ElevenLabs API Key
$env:ELEVENLABS_API_KEY="sk_9cbac5d08d3ce6818edaa04c499255a46f6f41f1051d49b7"

# Set Custom Voice ID  
$env:ELEVENLABS_VOICE_ID="3amfxwMsHb1NVY2zKFZQ"

# Start Claude Code with full context
.\claude.bat -c
```

## What This Gives You
- ✅ Full access to all ROSEYS business documents and strategy
- ✅ ElevenLabs voice integration with your custom voice
- ✅ Session continuity and memory preservation
- ✅ All AI agents and automation systems
- ✅ Complete todo tracking and project management

## Quick Test
Once Claude starts, test voice by asking:
"Can you give me a quick status update and speak the response?"

## Alternative: One-Time PowerShell Profile Setup
To avoid typing environment variables every time:

1. `notepad $PROFILE`
2. Add these lines to the file:
```powershell
# ElevenLabs Voice Integration
$env:ELEVENLABS_API_KEY="sk_9cbac5d08d3ce6818edaa04c499255a46f6f41f1051d49b7"
$env:ELEVENLABS_VOICE_ID="3amfxwMsHb1NVY2zKFZQ"
```
3. Save and close
4. Restart PowerShell

Then you only need:
```powershell
cd C:\claude_home
.\claude.bat -c
```

---
**Keep this document handy for quick reference!**