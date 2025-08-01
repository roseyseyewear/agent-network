@echo off
echo Setting up ElevenLabs Voice Integration...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from python.org
    pause
    exit /b 1
)

echo Python found. Installing requirements...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo To use:
echo 1. Get your ElevenLabs API key from elevenlabs.io
echo 2. Set environment variable:
echo    set ELEVENLABS_API_KEY=your_api_key_here
echo 3. Test with:
echo    python text_to_speech.py "Hello, this is a test"
echo.
pause