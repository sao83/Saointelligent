@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Create Desktop Shortcut.ps1"
if errorlevel 1 (
  echo Could not create the desktop shortcut. You can still use Launch SAO Intelligents App.bat.
  pause
  exit /b 1
)
echo.
echo SAO Intelligents was added to your Desktop and Start Menu.
echo Double-click the SAO Intelligents shortcut to open the desktop app.
pause
endlocal
