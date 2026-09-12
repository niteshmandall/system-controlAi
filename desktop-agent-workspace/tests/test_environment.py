"""
Tests for System Environment, Python Runtime, and Dependencies
"""

import os
import platform
import shutil
import sys
from pathlib import Path
import pytest


def test_python_version():
    """Verify running under supported Python version (>= 3.11)."""
    assert sys.version_info >= (3, 11), f"Python >= 3.11 required, got {sys.version}"


def test_core_dependencies_importable():
    """Verify all core dependencies are installed and importable."""
    modules = [
        "browser_use",
        "playwright",
        "mcp",
        "dotenv",
        "pydantic",
    ]
    for mod in modules:
        __import__(mod)


def test_playwright_chromium_installed():
    """Verify Playwright Chromium executable is available."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        # Check executable path without launching
        exec_path = p.chromium.executable_path
        assert exec_path is not None
        assert Path(exec_path).exists(), f"Chromium binary not found at: {exec_path}"


def test_env_example_template_keys():
    """Verify .env.example contains all required configuration keys."""
    workspace_dir = Path(__file__).resolve().parent.parent
    env_example = workspace_dir / ".env.example"
    assert env_example.is_file(), ".env.example file must exist"

    content = env_example.read_text(encoding="utf-8")
    required_keys = [
        "OPENROUTER_API_KEY",
        "OPENROUTER_MODEL",
        "OPENROUTER_BASE_URL",
        "GOOSE_PROVIDER",
        "BROWSER_HEADLESS",
    ]
    for key in required_keys:
        assert key in content, f"Missing key '{key}' in .env.example"


def test_uv_executable_discovery():
    """Verify uv package manager is discoverable."""
    which_uv = shutil.which("uv")
    if not which_uv:
        # Check common fallback locations
        home = Path.home()
        candidates = [
            home / ".local" / "bin" / ("uv.exe" if platform.system() == "Windows" else "uv"),
            home / ".cargo" / "bin" / ("uv.exe" if platform.system() == "Windows" else "uv"),
            Path("/usr/local/bin/uv"),
        ]
        which_uv = next((str(c) for c in candidates if c.is_file()), None)

    assert which_uv is not None, "uv executable could not be located"
