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
echo  [1] Start Goose Session (Local Ollama: Qwen2.5-Coder:7B) [DEFAULT]
echo  [2] Start Goose Session (Cloud OpenRouter: Gemini 3.8 Flash)
echo  [3] Test Browser Control (Visible Chromium Actuator Test)
echo  [4] Run Antigravity Agent Script
echo  [5] Test Local LLM Benchmark (Qwen2.5-Coder:7B via Ollama)
echo  [6] Run Diagnostics & Tests
echo  [7] Exit
echo.
echo =====================================================================

:: Default choice 1 after 5 seconds if no key pressed
choice /c 1234567 /n /t 5 /d 1 /m "Select option (1-7, default 1 in 5s): "
set "SEL=%ERRORLEVEL%"

if "%SEL%"=="1" goto start_goose_local
if "%SEL%"=="2" goto start_goose_cloud
if "%SEL%"=="3" goto test_browser
if "%SEL%"=="4" goto run_antigravity
if "%SEL%"=="5" goto test_local_llm
if "%SEL%"=="6" goto run_tests
if "%SEL%"=="7" exit /b 0

:start_goose_local
cls
echo =====================================================================
echo Starting Goose Session with LOCAL OLLAMA (Qwen2.5-Coder:7B)...
echo Hardware: NVIDIA GTX 1650 (CUDA) + AMD Ryzen 5
echo Model:    qwen2.5-coder:7b (100%% Local - Zero Cloud Tokens)
echo =====================================================================
echo.
goose session --provider ollama --model qwen2.5-coder:7b
goto end

:start_goose_cloud
cls
echo =====================================================================
echo Starting Goose Session with CLOUD OPENROUTER...
echo Provider: OpenRouter
echo Model:    google/gemini-3.8-flash
echo =====================================================================
echo.
goose session --provider openrouter --model google/gemini-3.8-flash
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
