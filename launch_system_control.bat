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
echo  [1] Start Goose Session (HYBRID: Cloud Orchestrator + Local Ollama Worker) [RECOMMENDED]
echo  [2] Start Goose Session (100%% Local: Ollama Qwen2.5-Coder:7B)
echo  [3] Start Goose Session (100%% Cloud: OpenRouter Gemini 3.8 Flash)
echo  [4] Open Google Chrome (Profile 9: Anjali Kashyap) with Remote Debugging (port 9222)
echo  [5] Auto-Apply Startup Jobs from CSV (Anjali Profile + Chrome Profile 9)
echo  [6] Test Browser Control (Visible Chromium Actuator Test)
echo  [7] Run Antigravity Agent Script
echo  [8] Test Local LLM Benchmark (Qwen2.5-Coder:7B via Ollama)
echo  [9] Run Diagnostics & Tests
echo  [0] Exit
echo.
echo =====================================================================

choice /c 1234567890 /n /t 5 /d 1 /m "Select option (1-9, 0 to exit, default 1 in 5s): "
set "SEL=%ERRORLEVEL%"

if "%SEL%"=="1" goto start_goose_hybrid
if "%SEL%"=="2" goto start_goose_local
if "%SEL%"=="3" goto start_goose_cloud
if "%SEL%"=="4" goto start_chrome_cdp
if "%SEL%"=="5" goto run_apply_jobs
if "%SEL%"=="6" goto test_browser
if "%SEL%"=="7" goto run_antigravity
if "%SEL%"=="8" goto test_local_llm
if "%SEL%"=="9" goto run_tests
if "%SEL%"=="10" exit /b 0

:start_goose_hybrid
cls
echo =====================================================================
echo Starting Goose Session in HYBRID MODE...
echo Orchestrator: OpenRouter (Gemini 3.8 Flash) [High-Level Intelligence]
echo Worker Agent: Local Ollama (Qwen2.5-Coder:7B on GTX 1650) [$0 Tokens]
echo Savings:      ~90%% reduction in cloud API token usage
echo =====================================================================
echo.
python configure_environment.py --mode hybrid
goose session --provider openrouter --model google/gemini-3.8-flash
goto end

:start_goose_local
cls
echo =====================================================================
echo Starting Goose Session with 100%% LOCAL OLLAMA (Qwen2.5-Coder:7B)...
echo Hardware: NVIDIA GTX 1650 (CUDA) + AMD Ryzen 5
echo Model:    qwen2.5-coder:7b (100%% Local - Zero Cloud Tokens)
echo Toolshim: Enabled via Ollama (mistral-nemo alias)
echo =====================================================================
echo.
python configure_environment.py --mode local
goose session --provider ollama --model qwen2.5-coder:7b
goto end

:start_goose_cloud
cls
echo =====================================================================
echo Starting Goose Session with 100%% CLOUD OPENROUTER...
echo Provider: OpenRouter
echo Model:    google/gemini-3.8-flash
echo =====================================================================
echo.
python configure_environment.py --mode cloud
goose session --provider openrouter --model google/gemini-3.8-flash
goto end

:start_chrome_cdp
call launch_chrome_for_agent.bat
goto :eof

:run_apply_jobs
cls
echo =====================================================================
echo Launching Automated Startup Job Application Runner...
echo Candidate: Anjali Kashyap (anjalikashyap9608@gmail.com)
echo CSV:       C:\Users\nites\Downloads\STARTUP_2026-09-22 - Sheet1.csv
echo Resume:    C:\Users\nites\Music\ai_data\anjali_data\AnjaliResume.pdf
echo =====================================================================
echo.
uv --directory desktop-agent-workspace run python ..\apply_startup_jobs.py
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
