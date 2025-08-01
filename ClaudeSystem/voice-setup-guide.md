# ElevenLabs Voice Integration - Complete Setup Guide

## Overview
This guide ensures ElevenLabs voice integration works automatically every time you start Claude Code.

## Required Components

### 1. ElevenLabs Account & API Key
- **Account**: elevenlabs.io
- **API Key**: Stored securely in `.env` file (not visible in Git)
- **Custom Voice ID**: Stored securely in `.env` file (not visible in Git)

### 2. Python Dependencies
Located in `scripts/requirements.txt`:
- requests>=2.31.0
- pygame>=2.5.0
- pyperclip>=1.8.2
- SpeechRecognition>=3.10.0
- pyaudio>=0.2.11

### 3. Core Files
- `scripts/text_to_speech.py` - Main TTS engine
- `speak.bat` - Manual voice command wrapper
- `scripts/auto_speak.py` - Clipboard monitoring (alternative)
- `scripts/claude_voice_integration.py` - Full voice system (future)

## Automatic Startup Configuration

### Updated Startup Instructions
Replace your current startup document with:

```powershell
# Navigate to workspace
cd C:\claude_home

# Set ElevenLabs API Key
$env:ELEVENLABS_API_KEY="sk_9cbac5d08d3ce6818edaa04c499255a46f6f41f1051d49b7"

# Set Custom Voice ID
$env:ELEVENLABS_VOICE_ID="3amfxwMsHb1NVY2zKFZQ"

# Start Claude Code with continuation
.\claude.bat -c
```

### Alternative: PowerShell Profile (Permanent Setup)
To make environment variables permanent, add to your PowerShell profile:

1. Check if profile exists: `Test-Path $PROFILE`
2. Create if needed: `New-Item -Path $PROFILE -Type File -Force`
3. Edit profile: `notepad $PROFILE`
4. Add these lines:
```powershell
# ElevenLabs Voice Integration
$env:ELEVENLABS_API_KEY="sk_9cbac5d08d3ce6818edaa04c499255a46f6f41f1051d49b7"
$env:ELEVENLABS_VOICE_ID="3amfxwMsHb1NVY2zKFZQ"
```

## Usage Methods

### Method 1: Automatic Voice (Recommended)
When you want Claude to speak a response:
- Ask: "Explain the strategy and speak your response"
- Claude automatically triggers: `python scripts/text_to_speech.py "response text"`

### Method 2: Manual Voice Command
```powershell
.\speak.bat "text to speak"
```

### Method 3: Direct Python Script
```powershell
python scripts/text_to_speech.py "text to speak"
```

## Testing Your Setup

### Quick Test Sequence
1. Start PowerShell
2. Run startup commands above
3. Test: `python scripts/text_to_speech.py "Voice integration test"`
4. Should hear your custom voice (3amfxwMsHb1NVY2zKFZQ)

### Troubleshooting Checklist
- ✅ In correct directory: `pwd` shows `C:\claude_home`
- ✅ API key set: `echo $env:ELEVENLABS_API_KEY` shows key
- ✅ Voice ID set: `echo $env:ELEVENLABS_VOICE_ID` shows voice ID
- ✅ Dependencies installed: `pip list | grep requests`
- ✅ Files exist: `ls scripts/text_to_speech.py`
- ✅ Audio working: Test with music/YouTube first

## Voice Customization

### Change Voice
1. Go to elevenlabs.io → Voice Library
2. Find desired voice → Copy Voice ID
3. Set new ID: `$env:ELEVENLABS_VOICE_ID="new_voice_id_here"`

### Voice Settings (in text_to_speech.py)
```python
"voice_settings": {
    "stability": 0.5,        # 0.0-1.0 (higher = more stable)
    "similarity_boost": 0.5  # 0.0-1.0 (higher = closer to original)
}
```

## Security Notes
- API key is visible in this document for setup convenience
- Consider using environment variables or secure storage for production
- Monitor ElevenLabs usage and billing
- API key can be regenerated if compromised

## Integration with Claude Code

### Current Functionality
- Claude can automatically trigger voice responses
- Uses your custom voice ID
- Cleans markdown and formatting for better speech
- Works through bash command execution

### Future Enhancements
- Real-time voice conversation (speech-to-text + auto TTS)
- Voice command recognition ("Hey Claude...")
- Automatic response speaking without manual request

---
**Last Updated**: 2025-08-01
**Status**: Fully Functional
**Owner**: Bethany + Claude AI System