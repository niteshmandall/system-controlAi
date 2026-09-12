#!/usr/bin/env python3
"""
Interactive & Automated Test Runner for System Control AI
---------------------------------------------------------
Runs the test suite across all subsystems:
  - Environment & Python dependencies
  - Cross-platform configuration & binary discovery
  - Browser-Use MCP server & Playwright Chromium actuation
  - Goose configuration & OpenRouter settings
  - (Optional) Live OpenRouter ping

Usage:
  uv run python run_tests.py            # Run full test suite
  uv run python run_tests.py --fast     # Run quick unit tests (skip browser)
  uv run python run_tests.py --browser  # Run browser actuation tests only
  uv run python run_tests.py --live     # Test live OpenRouter API connection
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

# Ensure UTF-8 output handling
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CURRENT_OS = platform.system()
ROOT_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = ROOT_DIR / "desktop-agent-workspace"


def test_openrouter_live_ping():
    """Verify live authentication and response from OpenRouter API if key exists."""
    env_file = WORKSPACE_DIR / ".env"
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key and env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("OPENROUTER_API_KEY="):
                api_key = line.split("=", 1)[1].strip().strip("'\"")
                break

    if not api_key:
        print("[!] No OPENROUTER_API_KEY found in .env or environment.")
        print("    Set OPENROUTER_API_KEY in desktop-agent-workspace/.env to run live test.")
        return False

    print(f"[*] Testing live OpenRouter connection with key: {api_key[:8]}...{api_key[-4:]}")
    try:
        from openai import OpenAI
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/system-controlAi",
                "X-Title": "System Control AI Test Runner"
            }
        )
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Respond with 'pong'"}],
            max_tokens=5
        )
        reply = response.choices[0].message.content.strip()
        print(f"[v] OpenRouter Live Response: {reply}")
        return True
    except Exception as e:
        print(f"[X] OpenRouter Live Test Failed: {e}")
        return False


def main():
    args = sys.argv[1:]

    print("=" * 65)
    print(">> System Control AI: Test Environment Runner")
    print(f"   OS: {CURRENT_OS} | Workspace: {WORKSPACE_DIR}")
    print("=" * 65)

    if "--live" in args:
        success = test_openrouter_live_ping()
        sys.exit(0 if success else 1)

    # Build pytest argument list
    pytest_args = ["-v"]

    if "--fast" in args:
        print("[*] Running Fast Unit Tests (skipping browser actuation)...")
        pytest_args.extend(["-k", "not browser_navigation and not browser_screenshot"])
    elif "--browser" in args:
        print("[*] Running Browser Automation Tests Only...")
        pytest_args.append("tests/test_browser_mcp.py")
    else:
        print("[*] Running Full Test Suite...")

    # Execute pytest through uv in the workspace directory
    cmd = ["uv", "--directory", str(WORKSPACE_DIR), "run", "pytest"] + pytest_args

    try:
        result = subprocess.run(cmd, cwd=str(WORKSPACE_DIR))
        print("=" * 65)
        if result.returncode == 0:
            print("[v] All tests PASSED successfully!")
        else:
            print(f"[X] Tests failed with exit code: {result.returncode}")
        print("=" * 65)
        sys.exit(result.returncode)
    except FileNotFoundError:
        # Fallback to direct pytest if uv isn't in shell path
        cmd = [sys.executable, "-m", "pytest"] + pytest_args
        result = subprocess.run(cmd, cwd=str(WORKSPACE_DIR))
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
