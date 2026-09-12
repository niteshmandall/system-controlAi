# Desktop Agent Workspace (Universal & OpenRouter)

This directory contains the Python agent runtime, Model Context Protocol (MCP) server, and browser automation toolchain.

---

## 📁 Workspace Contents

| File / Folder | Purpose |
| :--- | :--- |
| `browser_use_mcp_server.py` | Universal MCP Server (FastMCP / MCPServer) exposing browser navigation, clicks, keystrokes, and screenshot tools over stdio with OpenRouter support |
| `antigravity_agent.py` | Universal OpenRouter / Native Antigravity Agent script |
| `.env` | Active environment keys (`OPENROUTER_API_KEY`, `OPENROUTER_MODEL`, `BROWSER_HEADLESS`, etc.) |
| `.env.example` | Template environment configuration |
| `pyproject.toml` | UV project configuration pinning Python >=3.11 with cross-platform dependencies |
| `tests/` | Test suite covering environment, cross-platform config, browser MCP, and OpenRouter |
| `screenshots/` | Output directory where browser screenshots are saved |

---

## 🚀 Commands

### Run Test Suite:
```bash
uv run pytest -v
```

### Direct Browser Test (Visible Chromium):
```bash
uv run python browser_use_mcp_server.py --test
```

### Run Universal Agent:
```bash
uv run python antigravity_agent.py
```
