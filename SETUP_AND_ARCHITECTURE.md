# Architecture & Setup Reference (Universal & OpenRouter)

This document records the exact architecture, OpenRouter wiring, and cross-platform configuration specifications for the autonomous Computer-Use agent setup.

---

## 🏛️ System Architecture

```
+-------------------------------------------------------------------------+
|                              USER PROMPT                                |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                       LLM PROVIDER: OPENROUTER                          |
|             Base URL: https://openrouter.ai/api/v1                      |
|             Supported: Claude 3.5 Sonnet, Gemini 2.5 Pro, DeepSeek,     |
|                        GPT-4o, Llama 3.3, Qwen Coder                    |
+------------------------------------+------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                        ORCHESTRATOR / CORE AGENT                        |
|                                                                         |
|   AAIF Goose CLI              <OR>    Universal Python Agent Script     |
|   Provider: openrouter                Client: OpenAI-compatible API     |
+------------------------------------+------------------------------------+
                                     |
               Model Context Protocol (MCP over stdio)
                                     |
                                     v
+-------------------------------------------------------------------------+
|                       BROWSER-USE MCP SERVER                            |
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
|   - browser_run_agent(task_instruction)  [Powered by OpenRouter]        |
|   - browser_close()                                                     |
+------------------------------------+------------------------------------+
                                     |
                               Playwright
                                     |
                                     v
+-------------------------------------------------------------------------+
|                         PLAYWRIGHT CHROMIUM                             |
|          Visible Window on Desktop (BROWSER_HEADLESS=false)             |
|          Actions executed: click, scroll, fill, navigation              |
|          Supported OS: Linux, macOS, Windows                            |
+-------------------------------------------------------------------------+
```

---

## ⚙️ Cross-Platform Goose Configuration

Goose natively supports OpenRouter as a provider:
```yaml
GOOSE_PROVIDER: openrouter
GOOSE_MODEL: anthropic/claude-3.5-sonnet

extensions:
  developer:
    enabled: true
    name: developer
    type: platform
  browser_use:
    enabled: true
    name: browser_use
    type: stdio
    cmd: "<dynamically detected uv binary>"
    args:
      - --directory
      - "<dynamically detected workspace path>"
      - run
      - python
      - browser_use_mcp_server.py
    envs:
      BROWSER_HEADLESS: "false"
      BROWSER_USE_LOGGING_LEVEL: "info"
      OPENROUTER_API_KEY: "<your_openrouter_api_key>"
      OPENROUTER_MODEL: "anthropic/claude-3.5-sonnet"
    timeout: 300
    description: "Browser-Use MCP Server: Autonomous browser actuation powered by Playwright and Chromium"
```

### Automatic Path Resolution (`configure_environment.py`)
Rather than maintaining separate OS configurations manually, `configure_environment.py`:
1. Discovers the active `uv` binary via `shutil.which("uv")` or standard user paths (`~/.local/bin/uv`, `/usr/local/bin/uv`, `/opt/homebrew/bin/uv`).
2. Calculates the absolute path of `desktop-agent-workspace`.
3. Injects the configuration into every standard Goose directory:
   - **Linux**: `~/.config/goose` and `$XDG_CONFIG_HOME/goose`
   - **macOS**: `~/Library/Application Support/goose` and `~/.config/goose`
   - **Windows**: `%APPDATA%\Block\goose\config`, `%APPDATA%\goose`, and `~/.config/goose`

---

## 🔑 OpenRouter Integration Details

1. **Authentication**: `OPENROUTER_API_KEY` (passed to Goose, Browser-Use, and the Python agent).
2. **Model Routing**: Models follow the format `<provider>/<model-slug>`, for example:
   - `anthropic/claude-3.5-sonnet`
   - `google/gemini-2.5-pro`
   - `deepseek/deepseek-chat`
3. **Endpoint**: `https://openrouter.ai/api/v1` (OpenAI-compatible chat completions endpoint).
