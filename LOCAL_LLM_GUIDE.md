# Running System Control AI with Open Source Local LLMs

You can run this entire system **100% locally and offline** using open-source models (via **Ollama**, **LM Studio**, **vLLM**, or **LocalAI**). No external API keys or cloud costs required.

---

## 🎯 Can Local Open-Source LLMs Handle Computer Use & Browser Tasks?

**Yes.** However, computer control and browser automation require specific capabilities that not all local LLMs possess:

1. **Structured Tool/Function Calling**: The model must output strictly formatted tool arguments (`browser_navigate`, `browser_click`, `browser_type`, `browser_scroll`) without hallucinating syntax.
2. **Context Window**: Browser DOM trees and system command outputs can be large. A minimum context window of **16k - 32k tokens** is recommended.
3. **Vision / Multimodal (Optional but Recommended)**: For complex web pages with dynamic canvas elements, a vision model (VL) can analyze screenshots directly.

---

## 🏆 Top Recommended Open-Source Local Models

| Model | Recommended Size | Strengths | Minimum Hardware |
| :--- | :--- | :--- | :--- |
| **Qwen 2.5 Coder** | `14B` or `32B` | 🥇 **Best overall for tool calling & code execution**. Outperforms many proprietary models in function calling. | 16GB - 32GB RAM / 8GB - 16GB VRAM |
| **Qwen 2.5 VL** | `7B` or `72B` | 🥇 **Best local vision model**. Can see screenshots, identify coordinates, and navigate visual web layouts. | 12GB - 16GB RAM (for 7B) |
| **Llama 3.3** | `70B` (Q4_K_M) | Exceptional reasoning, robust system prompt adherence, state-of-the-art open weights. | 40GB+ RAM / 24GB VRAM |
| **Llama 3.2 Vision** | `11B` | Good multimodal balance with moderate hardware requirements. | 16GB RAM / 8GB VRAM |
| **Qwen 2.5 Coder (7B)** | `7B` | ⚡ **Best lightweight option for consumer laptops**. Runs fast on standard CPUs or 6GB GPUs. | 8GB - 16GB RAM |
| **DeepSeek R1 / V3** | `14B` (Distill) or `32B` | Excellent step-by-step reasoning for multi-stage system automation tasks. | 16GB - 32GB RAM |

---

## 💻 Hardware Requirements Reference

- **Lightweight (7B - 8B models)**:
  - RAM: 8 GB – 16 GB
  - GPU: 6 GB VRAM (RTX 3060 / 4060, or Apple Silicon M1/M2/M3 16GB)
  - Speed: Fast (~30–50 tokens/sec)
- **Mid-Tier (14B - 32B models)** *(Recommended sweet spot)*:
  - RAM: 16 GB – 32 GB
  - GPU: 12 GB – 16 GB VRAM (RTX 3080/4070/4080, or Apple Silicon 24GB+)
  - Speed: Moderate (~15–30 tokens/sec)
- **Heavyweight (70B models)**:
  - RAM: 48 GB – 64 GB
  - GPU: 24 GB+ VRAM (RTX 3090/4090, or Apple Silicon 64GB+)
  - Speed: ~10–18 tokens/sec

---

## 🚀 Setup Option 1: Ollama (Recommended & Easiest)

Ollama is the easiest way to run local models with built-in OpenAI-compatible API and native Goose support.

### 1. Install Ollama
- **Windows / macOS**: Download installer from [ollama.com](https://ollama.com)
- **Linux**:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

### 2. Pull Your Chosen Model
```bash
# Recommended for tool use & coding (14B):
ollama run qwen2.5-coder:14b

# Lightweight for 8GB-16GB machines (7B):
ollama run qwen2.5-coder:7b

# For Vision / Screenshot analysis (11B):
ollama run llama3.2-vision:11b
```
Ollama will automatically start serving on `http://localhost:11434`.

---

## 🚀 Setup Option 2: LM Studio

If you prefer a visual GUI to manage, quantize, and run GGUF models:

1. Download **LM Studio** from [lmstudio.ai](https://lmstudio.ai).
2. Search and download `qwen2.5-coder-14b-instruct-gguf` or `llama-3.2-11b-vision-instruct`.
3. Go to the **Developer / Local Server** tab (`<->` icon).
4. Click **Start Server** on port `1234`.
5. Your local OpenAI-compatible endpoint is: `http://localhost:1234/v1`.

---

## ⚙️ How to Switch System Control AI to Local Mode

Open `desktop-agent-workspace/.env` and configure:

```ini
# --- Toggle Local LLM Mode ---
USE_LOCAL_LLM=true

# Choose provider: 'ollama' or 'lmstudio'
LOCAL_LLM_PROVIDER=ollama
LOCAL_LLM_BASE_URL=http://localhost:11434/v1
LOCAL_LLM_MODEL=qwen2.5-coder:14b

# --- Goose Provider Override ---
GOOSE_PROVIDER=ollama
GOOSE_MODEL=qwen2.5-coder:14b
OLLAMA_HOST=http://localhost:11434
```

### Synchronize Configuration
Run the universal environment configurator:
```bash
uv run python configure_environment.py
```
`configure_environment.py` will automatically update Goose's `config.yaml` to route to your local Ollama / LM Studio instance instead of OpenRouter.

---

## 🎮 Running with Local Models

### 1. Launch Interactive Goose Session
```bash
goose session
```
Ask Goose to automate:
```text
> Use the browser-use extension to navigate to https://news.ycombinator.com and list the top 3 stories.
```

### 2. Run Autonomous Python Script
```bash
uv run python desktop-agent-workspace/antigravity_agent.py
```
The script will route requests to `http://localhost:11434/v1` and use your local open-source LLM.

---

## 🔄 Switching Back to Cloud (OpenRouter)

Whenever you want to switch back to cloud models (e.g., Claude 3.5 Sonnet or Gemini 2.5 Pro):

1. In `.env`, set:
   ```ini
   USE_LOCAL_LLM=false
   ```
2. Re-run:
   ```bash
   uv run python configure_environment.py
   ```
No reinstallation required!
