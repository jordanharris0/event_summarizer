@echo off
REM Launch the Event Log Summarizer in PowerShell
echo Launching Event Log Summarizer in PowerShell...
echo.

REM Start PowerShell and run everything inside it
start powershell -NoExit -Command ^
"cd '%~dp0'; ^
if (Test-Path .venv\\Scripts\\Activate.ps1) { . .venv\\Scripts\\Activate.ps1 }; ^
python event_summarizer.py; ^
Write-Host ''; ^
Write-Host 'Press any key to exit...' -ForegroundColor Yellow; ^
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')"