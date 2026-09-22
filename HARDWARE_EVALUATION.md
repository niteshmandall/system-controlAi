# Laptop Hardware Evaluation & Local LLM Sizing

This document records the exact hardware audit of this laptop and provides the optimal local open-source LLM recommendations tailored to its specifications.

---

## 💻 Hardware Audit Results

| Component | Specification | Usable Capacity |
| :--- | :--- | :--- |
| **CPU** | **AMD Ryzen 5 4600H** (6 Cores / 12 Threads, up to 4.0 GHz) | Fast multi-threaded CPU inference |
| **RAM** | **16.0 GB Physical RAM** | ~9 – 10 GB available for model weights |
| **Dedicated GPU** | **NVIDIA GeForce GTX 1650** | **4.0 GB VRAM** (CUDA 13.3 / 610.88) |
| **Free VRAM** | Windows desktop uses ~1.2 GB | **~2.8 GB VRAM dedicated to model layers** |
| **Storage** | **C: Drive** (NVMe SSD) | **60.4 GB Free Disk Space** |

---

## ⚖️ Performance Tiers on This Machine

Because the GPU has **4GB VRAM** and the system has **16GB RAM**, local LLMs will execute in one of two modes:
1. **100% GPU Offload (Full CUDA acceleration)**: Model weights < 2.8 GB. Runs at **40 – 60+ tokens/sec** (instantaneous).
2. **Hybrid GPU + CPU Offload**: Model weights between 3.5 GB and 8.0 GB. The GPU accelerates ~2.5 GB of transformer layers, while the 12-thread AMD Ryzen CPU processes the rest via system RAM. Runs at **15 – 25 tokens/sec** (very usable and responsive).

---

## 🏆 The Verdict: Best Models for This Laptop

### 🥇 1. Best Overall Recommendation: `qwen2.5-coder:7b`
- **Download Size**: ~4.7 GB (Q4_K_M quantization)
- **Execution Mode**: Hybrid (2.5 GB in GTX 1650 VRAM + 2.2 GB in System RAM)
- **Speed**: ~**18 – 25 tokens/sec**
- **Why it's the best**:
  - State-of-the-art function/tool calling in the 7B class.
  - Native 32k context window.
  - Generates flawless JSON for `browser_navigate`, `browser_click`, `browser_type`.
- **Command to install**:
  ```bash
  ollama run qwen2.5-coder:7b
  ```

---

### ⚡ 2. Best for Ultra-Fast / 100% GPU Execution: `qwen2.5-coder:3b` or `llama3.2:3b`
- **Download Size**: ~2.0 GB
- **Execution Mode**: **100% inside NVIDIA GTX 1650 VRAM**
- **Speed**: **45 – 60+ tokens/sec** (blazing fast, zero CPU latency)
- **Why choose this**: If you want instant tool actuation without taxing your CPU or battery.
- **Command to install**:
  ```bash
  ollama run qwen2.5-coder:3b
  ```

---

### 👁️ 3. Best for Visual Screenshot Analysis: `llama3.2-vision:11b`
- **Download Size**: ~7.9 GB
- **Execution Mode**: Hybrid (2.5 GB GPU + 5.4 GB System RAM)
- **Speed**: ~**8 – 12 tokens/sec**
- **Why choose this**: If your browser automation tasks require inspecting complex image screenshots.
- **Command to install**:
  ```bash
  ollama run llama3.2-vision:11b
  ```

---

## 🚫 Models NOT Recommended on this Laptop

- **14B Models (e.g. `qwen2.5-coder:14b`)**: Requires ~9GB RAM. Will run at ~5–8 tok/s, leaving little RAM for your browser and IDE.
- **32B / 70B Models**: Exceeds available RAM, causes aggressive Windows paging (thrashing), speed drops to < 1.5 tok/s.

---

## 🚀 How to Set Up the #1 Pick (`qwen2.5-coder:7b`) on this Laptop

1. **Install Ollama** (if not installed yet):
   Download and install from [ollama.com](https://ollama.com).
2. **Pull the model**:
   ```bash
   ollama run qwen2.5-coder:7b
   ```
3. **Configure the Project**:
   In `desktop-agent-workspace/.env`, set:
   ```ini
   USE_LOCAL_LLM=true
   LOCAL_LLM_PROVIDER=ollama
   LOCAL_LLM_BASE_URL=http://localhost:11434/v1
   LOCAL_LLM_MODEL=qwen2.5-coder:7b
   OLLAMA_HOST=http://localhost:11434
   ```
4. **Sync with Goose & Agent**:
   ```bash
   uv run python configure_environment.py
   ```
5. **Run Locally**:
   ```bash
   goose session
   ```
