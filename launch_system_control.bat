@echo off
setlocal enabledelayedexpansion
title System Control AI - Autonomous Agent

:: Ensure user local bin is in PATH for goose and uv
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
set "WORKSPACE=C:\Users\nites\Documents\ExpertByAi\system-controlAi"
cd /d "%WORKSPACE%"

cls
echo =====================================================================
echo              SYSTEM CONTROL AI - AUTONOMOUS AGENT
echo =====================================================================
echo  Stack: AAIF Goose + Browser-Use MCP + Playwright + OpenRouter
echo  Workspace: %WORKSPACE%
echo =====================================================================
echo.
echo  [1] Start Goose Session (Autonomous OS + Browser Control) [DEFAULT]
echo  [2] Test Browser Control (Visible Chromium Actuator Test)
echo  [3] Run Antigravity Agent Script
echo  [4] Run Diagnostics & Tests
echo  [5] Test Local LLM (Qwen2.5-Coder:7B via Ollama)
echo  [6] Exit
echo.
echo =====================================================================

:: Default choice 1 after 5 seconds if no key pressed
choice /c 123456 /n /t 5 /d 1 /m "Select option (1-6, default 1 in 5s): "
set "SEL=%ERRORLEVEL%"

if "%SEL%"=="1" goto start_goose
if "%SEL%"=="2" goto test_browser
if "%SEL%"=="3" goto run_antigravity
if "%SEL%"=="4" goto run_tests
if "%SEL%"=="5" goto test_local_llm
if "%SEL%"=="6" exit /b 0

:start_goose
cls
echo =====================================================================
echo Starting Goose Autonomous Agent Session...
echo Type your prompt, or ask it to navigate and control the browser.
echo =====================================================================
echo.
goose session
goto end

:test_browser
cls
echo =====================================================================
echo Launching Visible Chromium Browser Test...
echo =====================================================================
echo.
uv --directory desktop-agent-workspace run python browser_use_mcp_server.py --test
goto end

:run_antigravity
cls
echo =====================================================================
echo Running Antigravity Agent Script...
echo =====================================================================
echo.
uv --directory desktop-agent-workspace run python antigravity_agent.py
goto end

:run_tests
cls
echo =====================================================================
echo Running Fast Test Suite...
echo =====================================================================
echo.
uv run python run_tests.py --fast
goto end

:test_local_llm
cls
echo =====================================================================
echo Testing Local LLM Inference (Qwen2.5-Coder:7B via Ollama)...
echo =====================================================================
echo.
uv --directory desktop-agent-workspace run python test_local_inference.py
goto end

:end
echo.
echo Press any key to return to menu, or close window...
pause >nul
goto :eof
