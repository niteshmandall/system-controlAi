@echo off
setlocal enabledelayedexpansion
title Launch Google Chrome for System Control AI (Profile 9)

set "WORKSPACE=C:\Users\nites\Documents\ExpertByAi\system-controlAi"
cd /d "%WORKSPACE%"

:: 1. Locate Chrome Binary
set "CHROME_BIN="
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" set "CHROME_BIN=C:\Program Files\Google\Chrome\Application\chrome.exe"
if not defined CHROME_BIN if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" set "CHROME_BIN=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
if not defined CHROME_BIN if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" set "CHROME_BIN=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"

if not defined CHROME_BIN (
    echo [ERROR] Google Chrome could not be found on this system.
    pause
    exit /b 1
)

cls
echo =====================================================================
echo    GOOGLE CHROME LAUNCHER - SYSTEM CONTROL AI (PROFILE 9)
echo =====================================================================
echo  Chrome Binary: %CHROME_BIN%
echo  Target Profile: Profile 9 (Anjali Kashyap - anjalikashyap9608@gmail.com)
echo  Remote Debugging: Port 9222 (CDP)
echo =====================================================================
echo.

:: 2. Check if port 9222 is already open
netstat -ano | findstr ":9222" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [v] SUCCESS: Google Chrome is ALREADY running with Remote Debugging on port 9222!
    echo [v] System Control AI agent can immediately attach to your active Chrome window.
    echo.
    echo Press any key to return...
    pause >nul
    exit /b 0
)

:: 3. Check if Chrome is running without port 9222
tasklist /FI "IMAGENAME eq chrome.exe" 2>NUL | find /I /N "chrome.exe">NUL
if %ERRORLEVEL% equ 0 (
    echo [!] Chrome is currently running, but Remote Debugging (port 9222) is NOT enabled.
    echo     Chrome requires remote debugging to allow the AI agent to use your logged-in session.
    echo.
    echo  [1] Restart Chrome with Remote Debugging (Profile 9) [RECOMMENDED]
    echo      (Closes existing Chrome and re-opens Profile 9 with port 9222 active)
    echo.
    echo  [2] Launch Separate Agent Window on Port 9222
    echo      (Keeps your current Chrome open, launches dedicated agent window)
    echo.
    echo  [3] Cancel
    echo.
    choice /c 123 /n /m "Select option (1-3): "
    set "CHOICE=!ERRORLEVEL!"

    if "!CHOICE!"=="1" (
        echo.
        echo Closing current Chrome windows...
        taskkill /F /IM chrome.exe >nul 2>&1
        timeout /t 2 /nobreak >nul
        echo Launching Google Chrome (Profile 9) on port 9222...
        start "" "%CHROME_BIN%" --remote-debugging-port=9222 --profile-directory="Profile 9"
        timeout /t 2 /nobreak >nul
        echo [v] Chrome launched successfully! System Control AI can now control your active session.
        timeout /t 3 >nul
        exit /b 0
    )
    if "!CHOICE!"=="2" (
        echo.
        echo Launching separate Agent Chrome on port 9222...
        start "" "%CHROME_BIN%" --remote-debugging-port=9222 --user-data-dir="%LOCALAPPDATA%\Google\Chrome\User Data - SystemControlAI"
        timeout /t 2 /nobreak >nul
        echo [v] Separate Chrome window launched!
        timeout /t 3 >nul
        exit /b 0
    )
    exit /b 0
)

:: 4. If Chrome was not running at all, launch directly
echo Launching Google Chrome with Profile 9 and Remote Debugging on port 9222...
start "" "%CHROME_BIN%" --remote-debugging-port=9222 --profile-directory="Profile 9"
timeout /t 2 /nobreak >nul
echo [v] Chrome launched successfully!
echo [v] You can now start System Control AI to automate your active browser session.
timeout /t 3 >nul
exit /b 0
