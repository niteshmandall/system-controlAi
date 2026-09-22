# System Control AI: Universal Autonomous Computer-Use Agent

A **general-purpose, cross-platform** autonomous computer and browser actuation agent powered by **AAIF Goose**, **Ollama**, **Playwright**, and **OpenRouter**.

Supports **Windows**, **macOS**, and **Linux** with hardware-accelerated local execution and intelligent cloud orchestration.

---

## ⚡ System Architecture

System Control AI supports **three flexible execution modes**, giving you the optimal balance between high intelligence and zero token costs:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MODE 1: HYBRID [RECOMMENDED]                    │
│                                                                        │
│   [ Cloud Orchestrator ]            [ Local Worker Sub-Agent ]        │
│   OpenRouter (Gemini / Claude) ───► Ollama Qwen2.5-Coder:7B (GPU)     │
│   • High-level task planning        • Repetitive DOM clicks & typing   │
│   • Vision reasoning                • Chromium navigation & scrolling  │
│   • 1–2 cloud calls only            • $0.00 Tokens (100% Free on GPU)  │
│                       Savings: ~90% Cost Reduction                     │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                        MODE 2: 100% LOCAL (AIR-GAPPED)                 │
│   • Orchestrator & Worker: Ollama (Qwen2.5-Coder:7B or 3B)            │
│   • Hardware: NVIDIA GeForce GTX 1650 (CUDA) + Ryzen 5 CPU            │
│   • Cost: $0.00 / Zero Cloud API Keys Required                        │
└────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                        MODE 3: 100% CLOUD                              │
│   • Orchestrator & Worker: OpenRouter (Gemini 3.8 Flash / Claude 3.5) │
│   • Maximum capability for complex multi-modal workflows               │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Hardware Acceleration (Auto-Detected)

Tested and verified on laptop hardware:
- **GPU**: NVIDIA GeForce GTX 1650 (4 GB GDDR6 VRAM, CUDA 13.3) — 12 model layers offloaded into VRAM (~1.9 GB VRAM usage).
- **CPU**: AMD Ryzen 5 4600H (6 Cores / 12 Threads, 4.0 GHz) — handles remaining offloaded layers.
- **RAM**: 16 GB DDR4.
- **Local Model**: `qwen2.5-coder:7b` (4.7 GB) or ultra-fast `qwen2.5-coder:3b` (1.9 GB, 100% VRAM fit).

---

## 🚀 Quickstart

### 1. Configure Your Environment
Create or edit `desktop-agent-workspace/.env`:
```dotenv
# Execution Mode: hybrid | local | cloud
EXECUTION_MODE=hybrid

# OpenRouter (Cloud Orchestrator)
OPENROUTER_API_KEY=sk-or-v1-your_key_here
OPENROUTER_MODEL=google/gemini-3.8-flash
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# Local LLM (Ollama Worker on GTX 1650)
USE_LOCAL_LLM=true
LOCAL_LLM_PROVIDER=ollama
LOCAL_LLM_BASE_URL=http://localhost:11434/v1
LOCAL_LLM_MODEL=qwen2.5-coder:7b
OLLAMA_HOST=http://localhost:11434

# Browser Automation & Real Google Chrome Profile
BROWSER_HEADLESS=false
BROWSER_USE_LOGGING_LEVEL=info

# Real Chrome Profile & Remote Debugging (CDP)
CHROME_MODE=auto
CHROME_CDP_URL=http://localhost:9222
CHROME_PROFILE_DIRECTORY=Profile 9
CHROME_USER_DATA_DIR=C:\Users\nites\AppData\Local\Google\Chrome\User Data
```

### 2. Generate Configuration
Run the automatic cross-platform configurator:
```bash
python configure_environment.py
```
This registers the `browser_use` MCP server in Goose's global configuration with Chrome Profile and CDP auto-attach support.

### 3. Launch System Control AI
On Windows, run the interactive launcher:
```powershell
.\launch_system_control.bat
```

You will see the 9-option interactive menu:
```text
=====================================================================
             SYSTEM CONTROL AI - AUTONOMOUS AGENT
=====================================================================
 [1] Start Goose Session (HYBRID: Cloud Orchestrator + Local Worker) [RECOMMENDED]
 [2] Start Goose Session (100% Local: Ollama Qwen2.5-Coder:7B)
 [3] Start Goose Session (100% Cloud: OpenRouter Gemini 3.8 Flash)
 [4] Open Google Chrome (Profile 9: Anjali Kashyap) with Remote Debugging (port 9222)
 [5] Test Browser Control (Visible Chromium Actuator Test)
 [6] Run Antigravity Agent Script
 [7] Test Local LLM Benchmark (Qwen2.5-Coder:7B via Ollama)
 [8] Run Diagnostics & Tests
 [9] Exit
=====================================================================
```

> **Applying for Jobs with Active Logins**:
> 1. Select **`[4]`** to open your real Google Chrome with **Profile 9** and Remote Debugging on port 9222.
> 2. Open any job platform (LinkedIn, Ashby, Wellfound, Peerlist, Greenhouse) where you are already signed in.
> 3. Start your Goose session with **`[1]`**. Goose will automatically attach directly to your open Chrome window, using your existing cookies, saved logins, and active sessions!

---

## 🧪 Testing & Verification

Run the comprehensive 21-test automated test suite:
```bash
cd desktop-agent-workspace
uv run pytest
```
```text
tests\test_browser_mcp.py ......      [ 28%]
tests\test_cross_platform.py ....     [ 47%]
tests\test_environment.py .....       [ 71%]
tests\test_local_llm.py ...           [ 85%]
tests\test_openrouter_config.py ...   [100%]

============================= 21 passed in 35.60s =============================
```

To test visible Chromium actuation directly:
```bash
cd desktop-agent-workspace
uv run python browser_use_mcp_server.py --test
```

---

## 📁 Repository Documentation

| Guide | Description |
| :--- | :--- |
| [HYBRID_ARCHITECTURE.md](file:///c:/Users/nites/Documents/ExpertByAi/system-controlAi/HYBRID_ARCHITECTURE.md) | In-depth cost comparison, sequence diagrams, and token savings breakdown. |
| [LOCAL_LLM_GUIDE.md](file:///c:/Users/nites/Documents/ExpertByAi/system-controlAi/LOCAL_LLM_GUIDE.md) | Complete guide for setting up Ollama, downloading models, and optimizing GPU offload. |
| [HARDWARE_EVALUATION.md](file:///c:/Users/nites/Documents/ExpertByAi/system-controlAi/HARDWARE_EVALUATION.md) | Hardware profile, VRAM benchmarks, and model fit evaluation. |
| [SETUP_AND_ARCHITECTURE.md](file:///c:/Users/nites/Documents/ExpertByAi/system-controlAi/SETUP_AND_ARCHITECTURE.md) | Technical architecture, Goose MCP wiring, and protocol specifications. |
| [TESTING_GUIDE.md](file:///c:/Users/nites/Documents/ExpertByAi/system-controlAi/TESTING_GUIDE.md) | Test runner reference and unit testing instructions. |
| [MEMORY_AND_OPERATIONS_GUIDE.md](file:///c:/Users/nites/Documents/ExpertByAi/system-controlAi/MEMORY_AND_OPERATIONS_GUIDE.md) | Operational playbooks, debugging, and memory retention. |

---

## 🛡️ Privacy & Safety
- **No Secrets in Git**: Sensitive credentials in `.env` are automatically ignored by `.gitignore`.
- **Local Control**: With `USE_LOCAL_LLM=true`, inner-loop browser actions stay completely on your machine.
- **Cross-Platform**: Works identically on Windows, Linux, and macOS.
