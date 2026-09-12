"""
Unit and Integration Tests for Browser-Use MCP Server
"""

import asyncio
from pathlib import Path
import pytest

from browser_use_mcp_server import (
    mcp_server,
    browser_navigate,
    browser_get_content,
    browser_take_screenshot,
    browser_scroll,
    browser_close,
)


def test_mcp_server_initialization():
    """Verify MCP server metadata and naming."""
    assert mcp_server.name == "browser-use"
    assert mcp_server.version == "1.1.0"


def test_mcp_tools_registration():
    """Verify all required tools are defined and callable."""
    tools = [
        browser_navigate,
        browser_get_content,
        browser_take_screenshot,
        browser_scroll,
        browser_close,
    ]
    for tool in tools:
        assert callable(tool), f"Tool {tool} must be callable"
        assert tool.__doc__ is not None, f"Tool {tool} must have a docstring"


@pytest.mark.asyncio
async def test_browser_navigation_and_content():
    """Test browser navigation to a live standard test domain and content retrieval."""
    try:
        # Navigate to standard example.com
        result = await browser_navigate("https://example.com")
        assert "200" in result or "Example Domain" in result
        assert "Example Domain" in result

        # Extract content
        content = await browser_get_content(max_length=500)
        assert "Example Domain" in content
        assert "URL: https://example.com" in content
    finally:
        await browser_close()


@pytest.mark.asyncio
async def test_browser_screenshot_generation():
    """Test screenshot capture produces a readable PNG file on disk."""
    try:
        await browser_navigate("https://example.com")
        res = await browser_take_screenshot("pytest_screenshot.png")
        assert "Screenshot saved to:" in res

        screenshot_path = Path(__file__).resolve().parent.parent / "screenshots" / "pytest_screenshot.png"
        assert screenshot_path.is_file(), f"Screenshot file not found at: {screenshot_path}"
        assert screenshot_path.stat().st_size > 1000, "Screenshot file should not be empty"
    finally:
        await browser_close()


@pytest.mark.asyncio
async def test_browser_scroll_and_teardown():
    """Test page scroll and graceful browser session teardown."""
    try:
        await browser_navigate("https://example.com")
        res_down = await browser_scroll(direction="down", amount=200)
        assert "Scrolled down by 200px" in res_down

        res_up = await browser_scroll(direction="up", amount=100)
        assert "Scrolled up by 100px" in res_up
    finally:
        res_close = await browser_close()
        assert "closed successfully" in res_close
