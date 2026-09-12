# Memory & Operations Guide (Universal & OpenRouter)

Use this guide for ongoing maintenance, troubleshooting, and testing of your general-purpose Computer-Use agent.

---

## 📌 Checklist

- [x] **Cross-Platform Compatibility**: No hardcoded OS paths or user directories.
- [x] **Universal Configurator**: `configure_environment.py` runs on Windows, macOS, and Linux.
- [x] **OpenRouter Integration**:
  - Goose configured with `GOOSE_PROVIDER: openrouter`
  - `browser_use_mcp_server.py` uses OpenRouter with LangChain ChatOpenAI
  - `antigravity_agent.py` uses OpenRouter with OpenAI client
- [x] **Visible Browser Actuation**: Chromium launches in real visible window (`BROWSER_HEADLESS=false`).
- [x] **Playwright Chromium**: Tested and verified.

---

## 🔧 Operational Commands by Operating System

### 1. Run Automated Test Suite
```bash
# Run full suite (17 tests)
uv run python run_tests.py

# Fast unit tests (skip browser launch)
uv run python run_tests.py --fast

# Browser-specific tests
uv run python run_tests.py --browser

# Test live OpenRouter API connectivity
uv run python run_tests.py --live
```
See [TESTING_GUIDE.md](file:///c:/Users/nites/Documents/ExpertByAi/system-controlAi/TESTING_GUIDE.md) for complete details.

### 2. Re-configure / Synchronize Environment
Whenever you change your API key or model in `desktop-agent-workspace/.env`:
```bash
# Any OS:
uv run python configure_environment.py
```

### 2. Standalone Browser Automation Test
Test that Chromium opens visibly, navigates, and captures a screenshot:
```bash
cd desktop-agent-workspace
uv run python browser_use_mcp_server.py --test
```

### 3. Launch Goose
```bash
goose session
```

### 4. Run OpenRouter Agent Directly
```bash
cd desktop-agent-workspace
uv run python antigravity_agent.py
```

---

## 🐛 Troubleshooting

### Issue: "OpenRouter API Key Invalid / Rate Limited"
- Verify that your key starts with `sk-or-v1-` in `desktop-agent-workspace/.env`.
- Check your balance and credits at [openrouter.ai/credits](https://openrouter.ai/credits).
- If one model is temporarily rate limited or congested, simply switch `OPENROUTER_MODEL` in `.env` to another top model:
  - From `anthropic/claude-3.5-sonnet` -> `google/gemini-2.5-pro` -> `deepseek/deepseek-chat`.
  - Re-run `uv run python configure_environment.py`.

### Issue: "Browser window does not appear on Linux"
- If running on a headless Linux server or Docker container without a display server (X11 / Wayland), set `BROWSER_HEADLESS=true` in `.env`.
- On Linux desktop (Ubuntu/Fedora/Arch), ensure `DISPLAY` environment variable is set (usually `:0`).
