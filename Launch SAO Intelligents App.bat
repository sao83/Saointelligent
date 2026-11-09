@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title SAO Intelligents Desktop App
set "URL=http://127.0.0.1:8790/space_nova.html"

REM Reuse the app server if this package is already running.
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-RestMethod -Uri 'http://127.0.0.1:8790/api/health' -TimeoutSec 1 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 1 (
  where py >nul 2>nul
  if not errorlevel 1 (
    start "SAO Intelligents App Server" /min /D "%~dp0" py -3 space_nova_server.py
  ) else (
    where python >nul 2>nul
    if errorlevel 1 (
      echo Python 3 is required for this SAO Intelligents desktop package.
      echo Install Python 3 from https://www.python.org/downloads/ and run this file again.
      pause
      exit /b 1
    )
    start "SAO Intelligents App Server" /min /D "%~dp0" python space_nova_server.py
  )
)

set "READY="
for /l %%I in (1,1,20) do (
  powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-RestMethod -Uri 'http://127.0.0.1:8790/api/health' -TimeoutSec 1 | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
  if not errorlevel 1 set "READY=1"
  if defined READY goto :openapp
  timeout /t 1 /nobreak >nul
)

echo SAO Intelligents's local service did not start. Check whether port 8790 is available and Python 3 is installed.
pause
exit /b 1

:openapp
set "BROWSER="
if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" set "BROWSER=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
if not defined BROWSER if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" set "BROWSER=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
if not defined BROWSER if exist "%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe" set "BROWSER=%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"
if not defined BROWSER if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set "BROWSER=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
if not defined BROWSER if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set "BROWSER=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
if not defined BROWSER if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" set "BROWSER=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
if defined BROWSER (
  start "" "%BROWSER%" --app="%URL%"
) else (
  start "" "%URL%"
)
endlocal
