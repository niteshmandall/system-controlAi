@echo off
setlocal enabledelayedexpansion
title System Control AI - Job Application Agent (Profile 9)

set "PATH=%USERPROFILE%\.local\bin;%PATH%"
set "WORKSPACE=C:\Users\nites\Documents\ExpertByAi\system-controlAi"
cd /d "%WORKSPACE%"

cls
echo =====================================================================
echo       SYSTEM CONTROL AI - 1-CLICK JOB APPLICATION AGENT
echo =====================================================================
echo  Target Profile: Profile 9 (Anjali Kashyap)
echo  Execution Mode: HYBRID (Cloud Orchestrator + Local GPU Worker)
echo =====================================================================
echo.

:: 1. Locate Chrome Binary
set "CHROME_BIN="
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set "CHROME_BIN=C:\Program Files\Google\Chrome\Application\chrome.exe"
if not defined CHROME_BIN if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" set "CHROME_BIN=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
if not defined CHROME_BIN if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" set "CHROME_BIN=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"

:: 2. Check if Chrome with Remote Debugging (port 9222) is already running
netstat -ano | findstr ":9222" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [v] Chrome with Remote Debugging is ALREADY active on port 9222.
) else (
    echo [*] Starting Google Chrome (Profile 9) with Remote Debugging on port 9222...
    tasklist /FI "IMAGENAME eq chrome.exe" 2>NUL | find /I /N "chrome.exe">NUL
    if !ERRORLEVEL! equ 0 (
        echo [!] Chrome is currently running without remote debugging.
        echo     Restarting Chrome to enable remote debugging for your active profile...
        taskkill /F /IM chrome.exe >nul 2>&1
        timeout /t 2 /nobreak >nul
    )
    start "" "%CHROME_BIN%" --remote-debugging-port=9222 --profile-directory="Profile 9"
    timeout /t 3 /nobreak >nul
    echo [v] Chrome (Profile 9) launched on port 9222!
)

echo.
echo =====================================================================
echo  Starting System Control AI Agent (Hybrid Mode)...
echo  Connecting to your active Chrome (all your logins are ready)...
echo =====================================================================
echo.

goose session --provider openrouter --model google/gemini-3.8-flash

echo.
echo =====================================================================
echo Session ended. Chrome remains open.
echo =====================================================================
pause
