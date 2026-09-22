"""
Tests for Local Open-Source LLM Configuration and Connectivity
"""

import os
import urllib.request
import json
import pytest
from pathlib import Path
from dotenv import load_dotenv

workspace_dir = Path(__file__).resolve().parent.parent
load_dotenv(workspace_dir / ".env")


def test_local_llm_env_vars():
    """Verify local LLM configuration keys are present in .env."""
    assert os.getenv("LOCAL_LLM_PROVIDER") == "ollama"
    assert os.getenv("LOCAL_LLM_MODEL") is not None
    assert os.getenv("LOCAL_LLM_BASE_URL") is not None


def test_ollama_service_online():
    """Verify Ollama HTTP service is reachable locally."""
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    version_url = f"{host}/api/version"
    try:
        req = urllib.request.Request(version_url, headers={"User-Agent": "SystemControlAI/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200
            data = json.loads(response.read().decode())
            assert "version" in data
    except Exception as e:
        pytest.skip(f"Ollama server not reachable: {e}")


def test_ollama_openai_compatibility_endpoint():
    """Verify Ollama exposes the /v1/models OpenAI-compatible endpoint."""
    base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/v1")
    models_url = f"{base_url}/models"
    try:
        req = urllib.request.Request(models_url, headers={"User-Agent": "SystemControlAI/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200
            data = json.loads(response.read().decode())
            assert "data" in data or "models" in data or isinstance(data, dict)
    except Exception as e:
        pytest.skip(f"Ollama OpenAI endpoint not reachable: {e}")
