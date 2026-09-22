# System Control AI: Universal Computer-Use Agent

A **general-purpose, cross-platform** local "Computer Use" agent powered by **AAIF Goose**, **uv**, **Browser-Use MCP**, and **OpenRouter**.

Supports **Windows**, **macOS**, and **Linux** without OS lock-in.

---

## ⚡ System Overview

| Component | Role | Details |
| :--- | :--- | :--- |
| **LLM Provider** | **OpenRouter** (Universal) | Single key for Claude 3.5 Sonnet, Gemini 2.5 Pro, DeepSeek R1, GPT-4o |
| **Core System Agent** | **Goose (AAIF)** | Autonomous system agent (terminal, code execution, MCP) |
| **Browser Actuator** | **Browser-Use MCP Server** | Live Playwright Chromium control (click, type, navigate, screenshot) |
| **Package Manager** | **Astral uv** | Cross-platform fast Python & virtualenv manager |
| **Configuration Generator** | **`configure_environment.py`** | Automatic OS & path detection for Windows, macOS, and Linux |

---

## 🚀 Quickstart

### 1. Set Your OpenRouter API Key
Open `desktop-agent-workspace/.env` and paste your OpenRouter key:
```ini
OPENROUTER_API_KEY=sk-or-v1-your_key_here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
BROWSER_HEADLESS=false
```

### 2. Run the Universal Configurator
Run this command on any operating system (Windows, macOS, Linux):
```bash
# Windows (PowerShell / CMD):
uv run python configure_environment.py

# macOS / Linux (bash / zsh):
uv run python3 configure_environment.py
```
> This dynamically locates your `uv` binary, detects your OS, and registers the `browser_use` MCP server in Goose's global configuration with OpenRouter enabled.

### 3. Test the Environment & Capabilities
Run the automated test suite across all subsystems:
```bash
# Run full suite (17 tests: environment, cross-platform, MCP, OpenRouter)
uv run python run_tests.py

# Run quick unit tests (skip browser UI)
uv run python run_tests.py --fast

# Test live OpenRouter API connection
uv run python run_tests.py --live
```
See the full [TESTING_GUIDE.md](file:///c:/Users/nites/Documents/ExpertByAi/system-controlAi/TESTING_GUIDE.md) for detailed test architecture.

### 4. Test Browser-Use MCP Directly (Visible Window)
Verify that Chromium launches and actuates visibly on your screen:
```bash
cd desktop-agent-workspace
uv run python browser_use_mcp_server.py --test
```
Chromium will open, navigate to Hacker News, save a screenshot to `screenshots/test_nav.png`, and report status.

### 5. Launch Goose with Autonomous Browser Control
```bash
goose session
```
In the Goose session, ask it to operate the browser:
```text
> Use the browser-use extension to open https://news.ycombinator.com and summarize the top 3 stories.
```
Because `BROWSER_HEADLESS=false`, you will watch the browser navigate, click, and interact with the web live on your screen!

### 5. Run Native Antigravity / OpenRouter Script
```bash
cd desktop-agent-workspace
uv run python antigravity_agent.py
```

---

## 🌐 Supported OpenRouter Models

You can change `OPENROUTER_MODEL` in `.env` to any model on [openrouter.ai/models](https://openrouter.ai/models):

- `anthropic/claude-3.5-sonnet` (Recommended for complex reasoning & computer use)
- `google/gemini-2.5-pro` (Fast, high-context reasoning)
- `deepseek/deepseek-chat` (High performance, low cost)
- `openai/gpt-4o` (Multimodal, general coding)
- `meta-llama/llama-3.3-70b-instruct` (Open source weights)

---

## 🖥️ Cross-Platform Commands

### Linux / macOS
```bash
# Install uv (if needed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Configure environment
uv run python3 configure_environment.py

# Launch agent
goose session
```

### Windows
```powershell
# Install uv (if needed)
powershell -ExecutionPolicy ByPass -Command "irm https://astral.sh/uv/install.ps1 | iex"

# Configure environment
uv run python configure_environment.py

# Launch agent
goose session
```

---

## 📁 Repository Layout

```
system-controlAi/
├── configure_environment.py            # Universal cross-platform configuration generator
├── README.md                           # Main documentation & quickstart
├── LOCAL_LLM_GUIDE.md                  # Comprehensive guide for running open-source local LLMs (Ollama / LM Studio)
├── TESTING_GUIDE.md                    # Test suite runner and automated test cases
├── SETUP_AND_ARCHITECTURE.md           # Architecture, OpenRouter wiring & MCP schema
├── MEMORY_AND_OPERATIONS_GUIDE.md      # Maintenance guide, commands, and debugging
└── desktop-agent-workspace/            # Python agent workspace
    ├── .env                            # Active environment variables (API keys)
    ├── .env.example                    # Template environment file
    ├── pyproject.toml                  # Python 3.12 dependencies
    ├── browser_use_mcp_server.py       # Cross-platform MCP server (stdio & test mode)
    ├── antigravity_agent.py            # Universal OpenRouter / Local LLM agent
    ├── screenshots/                    # Captured browser screenshots
    └── src/                            # Package source modules
```
