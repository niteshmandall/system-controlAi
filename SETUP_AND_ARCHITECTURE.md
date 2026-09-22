# Architecture & Setup Reference: Hybrid, Local & Cloud Agent

This document records the exact architecture, OpenRouter & Ollama wiring, and cross-platform configuration specifications for the autonomous Computer-Use agent setup.

---

## 🏛️ System Architecture

System Control AI connects high-level AI reasoning with low-level OS and browser control via three distinct execution tiers:

```
+-------------------------------------------------------------------------+
|                              USER PROMPT                                |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                  TIER 1: HIGH-LEVEL ORCHESTRATOR                        |
|                                                                         |
|   OpenRouter (Gemini 3.8 Flash / Claude 3.5 Sonnet)                     |
|   • Decides high-level multi-step plans                                 |
|   • Dispatches sub-tasks to local actuators                             |
|   • Low token consumption (sent only for orchestrating decisions)       |
+------------------------------------+------------------------------------+
                                     |
                    Model Context Protocol (MCP over stdio)
                                     |
                                     v
+-------------------------------------------------------------------------+
|                  TIER 2: BROWSER-USE MCP SERVER                         |
|             (desktop-agent-workspace/browser_use_mcp_server.py)         |
|                                                                         |
|  Tools Registered:                                                      |
|   - browser_navigate(url)                                               |
|   - browser_click(selector)                                             |
|   - browser_type(selector, text, press_enter)                           |
|   - browser_press_key(key)                                              |
|   - browser_get_content(max_length)                                     |
|   - browser_take_screenshot(filename)                                   |
|   - browser_scroll(direction, amount)                                   |
|   - browser_run_agent(task_instruction)                                 |
|   - browser_close()                                                     |
+------------------------------------+------------------------------------+
                                     |
           Autonomous Task Loop powered by Local Sub-Agent
                                     |
                                     v
+-------------------------------------------------------------------------+
|                  TIER 3: LOCAL SUB-AGENT WORKER                         |
|                                                                         |
|   Ollama: Qwen 2.5 Coder 7B / 3B on NVIDIA GeForce GTX 1650 (CUDA)      |
|   • Repetitive DOM analysis, clicking, and typing                       |
|   • 100% Free on GPU ($0.00 Tokens)                                     |
|   • Zero network latency for sub-agent iterations                       |
+------------------------------------+------------------------------------+
                                     |
                                 Playwright
                                     |
                                     v
+-------------------------------------------------------------------------+
|                         PLAYWRIGHT CHROMIUM                             |
|          Visible Window on Desktop (BROWSER_HEADLESS=false)             |
|          Actions executed: click, scroll, fill, navigation              |
|          Supported OS: Windows, Linux, macOS                            |
+-------------------------------------------------------------------------+
```

---

## ⚙️ Cross-Platform Goose Configuration (`config.yaml`)

Generated automatically by `configure_environment.py`:
```yaml
# Goose Global Configuration
active_provider: openrouter
GOOSE_PROVIDER: openrouter
GOOSE_MODEL: google/gemini-3.8-flash
GOOSE_TELEMETRY_ENABLED: false
GOOSE_TOOLSHIM: false

providers:
  ollama:
    enabled: true
    model: qwen2.5-coder:7b
    host: http://localhost:11434
    configured: true
  openrouter:
    enabled: true
    model: google/gemini-3.8-flash
    configured: true

extensions:
  developer:
    enabled: true
    name: developer
    type: platform
  browser_use:
    enabled: true
    name: browser_use
    type: stdio
    cmd: "<detected uv binary>"
    args:
      - --directory
      - "<workspace path>"
      - run
      - python
      - browser_use_mcp_server.py
    envs:
      BROWSER_HEADLESS: "false"
      BROWSER_USE_LOGGING_LEVEL: "info"
      USE_LOCAL_LLM: "true"
      LOCAL_LLM_BASE_URL: "http://localhost:11434/v1"
      LOCAL_LLM_MODEL: "qwen2.5-coder:7b"
      OPENROUTER_API_KEY: "<registered_openrouter_key>"
    timeout: 300
    description: "Browser-Use MCP Server: Autonomous browser actuation powered by Playwright and Chromium"
```

### Key Optimizations:
1. **`GOOSE_TOOLSHIM: false`**: OpenRouter models natively support function calling. Disabling toolshim eliminates unnecessary 404 queries looking for `mistral-nemo`.
2. **Platform Extension Pruning**: Unused default extensions (`todo`, `analyze`, `tom`, `scheduler`, `apps`, `chatrecall`) are disabled (`enabled: false`), preventing slow background loading.
3. **Hardware Acceleration**: `USE_LOCAL_LLM: "true"` routes inner-loop browser actions to local Ollama on the laptop's GTX 1650.

---

## 🔑 Mode Comparison Table

| Feature | Hybrid Mode | Pure Local Mode | Pure Cloud Mode |
| :--- | :--- | :--- | :--- |
| **Top Orchestrator** | OpenRouter (Gemini / Claude) | Ollama (Qwen2.5-Coder:7B) | OpenRouter |
| **Inner Sub-Agent** | Ollama (Qwen2.5-Coder:7B) | Ollama (Qwen2.5-Coder:7B) | OpenRouter |
| **Cloud Token Cost** | **Minimal (~90% savings)** | **$0.00 (Zero)** | Standard per-token cost |
| **Internet Requirement**| Required for planner | Completely Air-gapped | Required |
| **Launch Command** | `launch_system_control.bat` [1] | `launch_system_control.bat` [2] | `launch_system_control.bat` [3] |

---

## 🛠️ Verification Commands

```powershell
# Run all unit and integration tests
uv run pytest

# Test visible Chromium actuation
uv run python browser_use_mcp_server.py --test

# Test local LLM inference on GTX 1650
python test_local_inference.py
```
