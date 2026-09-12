# Testing Guide: System Control AI

This document provides complete instructions for the testing environment built to validate components, verify cross-platform configurations, and test browser automation and OpenRouter integration.

---

## 🧪 Testing Architecture

```
+------------------------------------------------------------------------+
|                          TEST SUITE RUNNER                             |
|                        (run_tests.py / pytest)                         |
+-------------------+--------------------+-------------------+-----------+
                    |                    |                   |
                    v                    v                   v
        +-----------------------+ +--------------+ +--------------------+
        |  test_environment.py  | |  test_cross_ | |  test_browser_     |
        |  - Python >= 3.11     | |  platform.py | |  mcp.py            |
        |  - Dependency imports | |  - OS detect | |  - MCP Tool reg    |
        |  - Playwright Chromium| |  - uv find   | |  - Navigation      |
        |  - .env template keys | |  - Goose dirs| |  - Screenshots     |
        +-----------------------+ +--------------+ |  - Teardown        |
                                                   +--------------------+
                                                             |
                                                             v
                                                   +--------------------+
                                                   | test_openrouter_   |
                                                   | config.py          |
                                                   | - Goose YAML/JSON  |
                                                   | - Provider format  |
                                                   | - Client init      |
                                                   +--------------------+
```

---

## 🚀 Running Tests

### 1. Full Test Suite (17 Tests)
Runs all unit tests, environment checks, and real browser actuation tests:
```bash
# From project root:
uv run python run_tests.py

# Or directly with pytest:
cd desktop-agent-workspace
uv run pytest -v
```

### 2. Fast Unit Tests (Skip Browser UI)
Runs tests in ~4 seconds without launching Chromium:
```bash
uv run python run_tests.py --fast
```

### 3. Browser Automation Only
Runs only the Playwright Chromium actuation tests:
```bash
uv run python run_tests.py --browser
```

### 4. Test Live OpenRouter Connection
Verifies your `OPENROUTER_API_KEY` from `.env` against the OpenRouter API:
```bash
uv run python run_tests.py --live
```

---

## 📁 Test Directory Structure

```
desktop-agent-workspace/tests/
├── __init__.py                     # Test package initializer
├── test_environment.py             # Python version, dependencies, and Playwright binary
├── test_cross_platform.py          # OS detection and path discovery logic
├── test_browser_mcp.py             # MCP server tools, navigation, and screenshots
└── test_openrouter_config.py       # Goose config structure & OpenRouter settings
```

---

## 🔍 What Each Test Validates

| Test Function | What It Validates |
| :--- | :--- |
| `test_python_version` | Ensures runtime is Python >= 3.11 |
| `test_core_dependencies_importable` | Verifies `browser_use`, `playwright`, `mcp`, `pydantic`, `dotenv` |
| `test_playwright_chromium_installed` | Confirms Chromium binary is downloaded and ready |
| `test_env_example_template_keys` | Ensures `.env.example` has all required keys |
| `test_uv_executable_discovery` | Verifies `uv` binary discovery works |
| `test_current_os_detection` | Validates OS identification (Linux, macOS, Windows) |
| `test_get_goose_config_dirs` | Checks Goose configuration directory discovery |
| `test_mcp_server_initialization` | Checks MCP server name (`browser-use`) and version |
| `test_mcp_tools_registration` | Checks that all browser tools are callable with docstrings |
| `test_browser_navigation_and_content` | Launches Chromium, navigates, and extracts page text |
| `test_browser_screenshot_generation` | Takes screenshot and verifies PNG file on disk |
| `test_browser_scroll_and_teardown` | Tests scrolling and graceful resource release |
| `test_goose_config_yaml_structure` | Validates `config.yaml` syntax and OpenRouter provider |
| `test_goose_config_json_validity` | Validates `config.json` formatting and MCP blocks |
| `test_openrouter_client_instantiation` | Verifies OpenAI client initialization with OpenRouter base URL |

---

## 🔄 Adding New Tests

To add tests for new features:
1. Create a new test file in `desktop-agent-workspace/tests/test_<feature>.py`.
2. Use `@pytest.mark.asyncio` for asynchronous tool and browser tests.
3. Run `uv run python run_tests.py` to verify.
