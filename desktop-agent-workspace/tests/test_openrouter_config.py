"""
Tests for OpenRouter Integration and Goose MCP Configuration Files
"""

import json
import os
import platform
from pathlib import Path
import pytest


def get_active_goose_config_file() -> Path:
    """Locate the active Goose config.yaml on the current platform."""
    home = Path.home()
    candidates = []

    if platform.system() == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            candidates.append(Path(appdata) / "Block" / "goose" / "config" / "config.yaml")
            candidates.append(Path(appdata) / "goose" / "config.yaml")
        candidates.append(home / ".config" / "goose" / "config.yaml")
    else:
        candidates.append(home / ".config" / "goose" / "config.yaml")
        candidates.append(home / "Library" / "Application Support" / "goose" / "config.yaml")

    for c in candidates:
        if c.is_file():
            return c
    pytest.fail(f"No active Goose config.yaml found in candidates: {candidates}")


def test_goose_config_yaml_structure():
    """Verify Goose config.yaml contains valid OpenRouter & MCP settings."""
    cfg_file = get_active_goose_config_file()
    content = cfg_file.read_text(encoding="utf-8")

    assert "GOOSE_PROVIDER: openrouter" in content
    assert "GOOSE_MODEL:" in content
    assert "browser_use:" in content
    assert "browser_use_mcp_server.py" in content
    assert "BROWSER_HEADLESS:" in content


def test_goose_config_json_validity():
    """Verify Goose config.json is valid JSON with expected keys."""
    cfg_file = get_active_goose_config_file()
    json_file = cfg_file.parent / "config.json"

    assert json_file.is_file(), f"Expected config.json at: {json_file}"
    data = json.loads(json_file.read_text(encoding="utf-8"))

    assert data.get("GOOSE_PROVIDER") == "openrouter"
    assert "mcpServers" in data
    assert "browser-use" in data["mcpServers"]
    assert "extensions" in data
    assert "browser_use" in data["extensions"]


def test_openrouter_client_instantiation():
    """Verify standard OpenAI client can be configured for OpenRouter."""
    from openai import OpenAI

    # Test initialization with dummy key (verifies base_url and headers format)
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="sk-or-v1-dummy-test-key-0000000000000000",
        default_headers={
            "HTTP-Referer": "https://github.com/system-controlAi",
            "X-Title": "System Control AI Test Suite"
        }
    )
    assert str(client.base_url) == "https://openrouter.ai/api/v1/"
    assert client.api_key == "sk-or-v1-dummy-test-key-0000000000000000"
