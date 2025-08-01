@echo off
echo Starting ROSEYS AI System...
cd /d C:\claude_home
echo.
echo Current location: %CD%
echo.
echo Recent activity:
git log --oneline -3
echo.
echo System status: Ready
echo.
echo To start Claude with full context:
echo   claude --context ClaudeSystem/claude.md
echo.
pause