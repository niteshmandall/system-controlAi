"""
Tests for Cross-Platform Configuration Generator
"""

import os
import sys
from pathlib import Path
import pytest

# Add parent project root to sys.path to import configure_environment
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from configure_environment import (
    find_uv_executable,
    get_goose_config_dirs,
    load_env_file,
    CURRENT_OS,
)


def test_current_os_detection():
    """Verify CURRENT_OS is recognized."""
    assert CURRENT_OS in ("Windows", "Darwin", "Linux")


def test_find_uv_executable():
    """Verify find_uv_executable locates a valid binary string."""
    uv_path = find_uv_executable()
    assert isinstance(uv_path, str)
    assert len(uv_path) > 0
    assert "uv" in uv_path.lower()


def test_get_goose_config_dirs():
    """Verify get_goose_config_dirs returns valid path objects for current OS."""
    dirs = get_goose_config_dirs()
    assert isinstance(dirs, list)
    assert len(dirs) >= 1
    for d in dirs:
        assert isinstance(d, Path)


def test_load_env_file_parser(tmp_path):
    """Verify load_env_file correctly parses key=value pairs, ignores comments and whitespace."""
    test_env = tmp_path / "test.env"
    test_env.write_text(
        "# Comment line\n"
        "KEY1=value1\n"
        "KEY2='quoted_value'\n"
        "KEY3=\"double_quoted\"\n"
        "\n"
        "INVALID_LINE_NO_EQUALS\n"
        "KEY4=value_with=equals\n",
        encoding="utf-8"
    )

    result = load_env_file(test_env)
    assert result["KEY1"] == "value1"
    assert result["KEY2"] == "quoted_value"
    assert result["KEY3"] == "double_quoted"
    assert result["KEY4"] == "value_with=equals"
    assert "INVALID_LINE_NO_EQUALS" not in result
