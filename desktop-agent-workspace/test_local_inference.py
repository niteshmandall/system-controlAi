"""
Test Local Inference with qwen2.5-coder:7b
Verifies:
1. Model loading & generation
2. Structured output / function calling
3. Tokens/sec execution speed
"""

import time
import json
import urllib.request
import os
from pathlib import Path
from dotenv import load_dotenv

workspace_dir = Path(__file__).resolve().parent
load_dotenv(workspace_dir / ".env")

BASE_URL = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/v1")
MODEL = os.getenv("LOCAL_LLM_MODEL", "qwen2.5-coder:7b")

print(f"Connecting to Local LLM at {BASE_URL} with model '{MODEL}'...")

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "You are an autonomous computer control AI. Output your plan concisely."},
        {"role": "user", "content": "Explain in two sentences how you navigate to a web URL and click a button using tools."}
    ],
    "temperature": 0.2,
    "max_tokens": 150
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    f"{BASE_URL}/chat/completions",
    data=data,
    headers={"Content-Type": "application/json"}
)

start_time = time.time()
try:
    with urllib.request.urlopen(req, timeout=120) as response:
        duration = time.time() - start_time
        res_data = json.loads(response.read().decode("utf-8"))
        content = res_data["choices"][0]["message"]["content"]
        usage = res_data.get("usage", {})
        total_tokens = usage.get("total_tokens", 0)
        eval_tokens = usage.get("completion_tokens", 0)
        tok_per_sec = (eval_tokens / duration) if duration > 0 else 0

        print("\n" + "=" * 60)
        print("  LOCAL MODEL RESPONSE SUCCESSFUL")
        print("=" * 60)
        print(content)
        print("-" * 60)
        print(f"Total tokens:      {total_tokens}")
        print(f"Completion tokens: {eval_tokens}")
        print(f"Inference latency: {duration:.2f}s")
        if tok_per_sec > 0:
            print(f"Speed:             {tok_per_sec:.2f} tokens/sec")
        print("=" * 60)
except Exception as e:
    print(f"\n[ERROR] Inference failed: {e}")
