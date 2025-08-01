# Claude Code Startup Instructions (Secure Version)

## Complete Startup Sequence

**Simple startup commands (API keys loaded automatically):**

```powershell
# Navigate to workspace
cd C:\claude_home

# Start Claude Code with full context
.\claude.bat -c
```

## Security Features
- ✅ API keys stored in `.env` file (not in Git)
- ✅ Automatic loading from secure file
- ✅ No sensitive data in startup commands
- ✅ Protected by `.gitignore`

## API Key Management

### Your API Keys (Secure Storage)
**Location**: `C:\claude_home\.env` (automatically ignored by Git)
- ElevenLabs API Key: `sk_9cbac...` (hidden in secure file)
- Custom Voice ID: `3amfx...` (hidden in secure file)

### If You Need to Update Keys
1. Edit: `notepad .env`
2. Update the values
3. Restart Claude Code

### If You Forget Your Keys
- **ElevenLabs API**: Go to elevenlabs.io → Profile → API Keys
- **Voice ID**: Go to elevenlabs.io → Voice Library → Your Voice

## What This Gives You
- ✅ Full access to all ROSEYS business documents and strategy
- ✅ ElevenLabs voice integration with your custom voice
- ✅ Session continuity and memory preservation
- ✅ All AI agents and automation systems
- ✅ Complete todo tracking and project management
- ✅ **Secure API key management**

## Quick Test
Once Claude starts, test voice by asking:
"Can you give me a quick status update and speak the response?"

---
**Security Note**: Your API keys are now protected and won't be accidentally shared or committed to Git!