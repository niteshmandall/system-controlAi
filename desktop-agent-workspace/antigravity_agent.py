"""
Universal Antigravity Agent (Cross-Platform with OpenRouter)
------------------------------------------------------------
A concise, production-ready script that creates a local agent capable of
reasoning, executing code, and actuating browser tools.

Supports:
  - OpenRouter as universal LLM provider (Claude 3.5, Gemini 2.5, DeepSeek, GPT-4o)
  - Cross-platform runtime (Linux, macOS, Windows)
  - Native Google Antigravity SDK or standard OpenAI-compatible client

Usage:
  uv run python antigravity_agent.py
"""

import asyncio
import os
import platform
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load local environment variables (.env)
load_dotenv(Path(__file__).resolve().parent / ".env")

CURRENT_OS = platform.system()

async def run_antigravity_agent():
    print("=" * 60)
    print(f"[*] Initializing Universal Agent on {CURRENT_OS}")
    print("=" * 60)

    try:
        # 1. Native Google Antigravity SDK (if installed)
        from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig
        
        config = LocalAgentConfig(
            system_instructions=(
                "You are an autonomous Computer-Use Agent. "
                "You have access to terminal execution, filesystem, and browser tools. "
                "Execute tasks thoroughly and verify every step."
            ),
            capabilities=CapabilitiesConfig(enable_system_access=True, enable_terminal=True),
        )

        async with Agent(config) as agent:
            prompt = "List files in the current workspace and report browser MCP status."
            print(f"[>] Sending prompt to Antigravity Agent: '{prompt}'\n")
            response = await agent.chat(prompt)

            async for token in response:
                sys.stdout.write(token)
                sys.stdout.flush()
            print("\n")

    except ImportError:
        # 2. Universal OpenRouter Agent Runner
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")

        if openrouter_key:
            print("[*] Running via Universal OpenRouter Provider...")
            from openai import OpenAI

            model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
            base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

            client = OpenAI(
                base_url=base_url,
                api_key=openrouter_key,
                default_headers={
                    "HTTP-Referer": "https://github.com/system-controlAi",
                    "X-Title": "Antigravity Computer-Use Agent"
                }
            )

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an autonomous Computer-Use Agent with system and browser control access."
                    },
                    {
                        "role": "user",
                        "content": "Confirm agent readiness for cross-platform computer control and browser actuation."
                    }
                ]
            )
            print(f"\n[OpenRouter ({model}) Response]:\n{response.choices[0].message.content}\n")

        elif gemini_key:
            print("[*] Running via Google GenAI fallback...")
            from google import genai
            client = genai.Client(api_key=gemini_key)
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents="Confirm agent readiness for autonomous computer control and browser actuation.",
            )
            print(f"\n[Gemini Agent Response]:\n{response.text}\n")

        else:
            print("[X] No API Key found.")
            print("    Please set OPENROUTER_API_KEY in desktop-agent-workspace/.env to run.")


if __name__ == "__main__":
    asyncio.run(run_antigravity_agent())
