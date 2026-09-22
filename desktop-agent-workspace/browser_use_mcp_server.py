"""
Universal Browser-Use MCP Server for Goose & Antigravity
--------------------------------------------------------
Exposes browser automation tools via Model Context Protocol (MCP stdio).
Uses Playwright and Browser-Use to automate web interactions.
Supports:
  - Cross-platform execution (Linux, macOS, Windows)
  - OpenRouter as primary LLM provider
  - Real-time visible browser actuation (BROWSER_HEADLESS=false)
"""

import asyncio
import os
import platform
import sys
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load local environment variables (.env)
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

from mcp.server.mcpserver import MCPServer
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

CURRENT_OS = platform.system()
HEADLESS = os.getenv("BROWSER_HEADLESS", "false").strip().lower() in ("true", "1", "yes")

# Initialize MCP Server
mcp_server = MCPServer(
    name="browser-use",
    version="1.1.0",
    instructions="Universal cross-platform browser control server powered by Browser-Use, Playwright, and OpenRouter."
)

# Global browser session state
_playwright = None
_browser: Optional[Browser] = None
_context: Optional[BrowserContext] = None
_page: Optional[Page] = None
_lock = asyncio.Lock()


async def _get_or_create_page() -> Page:
    """Ensure a Chromium browser instance is active and return the current page."""
    global _playwright, _browser, _context, _page
    async with _lock:
        if _playwright is None:
            _playwright = await async_playwright().start()

        if _browser is None or not _browser.is_connected():
            launch_args = ["--no-sandbox"]
            if CURRENT_OS == "Windows":
                launch_args.append("--start-maximized")

            _browser = await _playwright.chromium.launch(
                headless=HEADLESS,
                args=launch_args
            )
            _context = await _browser.new_context(
                no_viewport=True if CURRENT_OS == "Windows" else False,
                viewport=None if CURRENT_OS == "Windows" else {"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
            )
            _page = await _context.new_page()

        if _page is None or _page.is_closed():
            if _context:
                _page = await _context.new_page()

        return _page


@mcp_server.tool()
async def browser_navigate(url: str) -> str:
    """Navigate Chromium to the specified URL.

    Args:
        url: Full web address (e.g. 'https://www.google.com')
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    page = await _get_or_create_page()
    response = await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    title = await page.title()
    status = response.status if response else "Unknown"
    return f"Successfully navigated to {url} [Status: {status}]. Page title: '{title}'"


@mcp_server.tool()
async def browser_click(selector: str) -> str:
    """Click an element matching the given CSS selector or text.

    Args:
        selector: CSS selector, text selector (e.g. 'text=Login'), or element ID.
    """
    page = await _get_or_create_page()
    await page.click(selector, timeout=10000)
    await page.wait_for_load_state("domcontentloaded")
    return f"Successfully clicked element matching: '{selector}'"


@mcp_server.tool()
async def browser_type(selector: str, text: str, press_enter: bool = False) -> str:
    """Type text into an input field or editable element.

    Args:
        selector: CSS selector or input selector
        text: Text string to type
        press_enter: Whether to press Enter after typing
    """
    page = await _get_or_create_page()
    await page.fill(selector, text, timeout=10000)
    if press_enter:
        await page.press(selector, "Enter")
        await page.wait_for_load_state("domcontentloaded")
    return f"Typed '{text}' into '{selector}' (press_enter={press_enter})"


@mcp_server.tool()
async def browser_press_key(key: str) -> str:
    """Press a keyboard key on the active page (e.g. 'Enter', 'Escape', 'Tab', 'ArrowDown').

    Args:
        key: The key identifier to press.
    """
    page = await _get_or_create_page()
    await page.keyboard.press(key)
    return f"Pressed key '{key}'"


@mcp_server.tool()
async def browser_get_content(max_length: int = 4000) -> str:
    """Get the current page URL, title, and visible text content.

    Args:
        max_length: Maximum characters of text content to return.
    """
    page = await _get_or_create_page()
    title = await page.title()
    url = page.url
    text_content = await page.evaluate("() => document.body.innerText || ''")
    truncated = text_content[:max_length]
    if len(text_content) > max_length:
        truncated += f"\n... [Truncated: {len(text_content) - max_length} more characters]"

    return f"URL: {url}\nTitle: {title}\n\nContent:\n{truncated}"


@mcp_server.tool()
async def browser_take_screenshot(filename: str = "") -> str:
    """Take a screenshot of the active browser viewport and save it.

    Args:
        filename: Optional filename (saves in workspace screenshots directory if empty).
    """
    page = await _get_or_create_page()
    out_dir = Path(__file__).resolve().parent / "screenshots"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not filename:
        import time
        filename = f"screenshot_{int(time.time())}.png"
    elif not filename.endswith(".png"):
        filename += ".png"

    dest_path = out_dir / filename
    await page.screenshot(path=str(dest_path.resolve()), full_page=False)
    return f"Screenshot saved to: {dest_path.resolve()}"


@mcp_server.tool()
async def browser_scroll(direction: str = "down", amount: int = 500) -> str:
    """Scroll the active web page.

    Args:
        direction: 'down' or 'up'
        amount: Number of pixels to scroll (default 500)
    """
    page = await _get_or_create_page()
    delta = amount if direction.lower() == "down" else -amount
    await page.evaluate(f"() => window.scrollBy(0, {delta})")
    return f"Scrolled {direction} by {amount}px"


@mcp_server.tool()
async def browser_run_agent(task_instruction: str) -> str:
    """Run an autonomous Browser-Use agent to achieve a complex multi-step web task.
    Uses OPENROUTER_API_KEY by default, with fallbacks to GEMINI_API_KEY or ANTHROPIC_API_KEY.

    Args:
        task_instruction: Clear instruction of what to accomplish on the web.
    """
    use_local = os.getenv("USE_LOCAL_LLM", "false").strip().lower() in ("true", "1", "yes")
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if not use_local and not any([openrouter_key, gemini_key, anthropic_key, openai_key]):
        return (
            "Error: No LLM configured. Please set USE_LOCAL_LLM=true in .env to use local models, "
            "or set OPENROUTER_API_KEY."
        )

    try:
        from browser_use import Agent

        # 1. Local Open Source Model (Ollama / LM Studio / vLLM)
        if use_local:
            from langchain_openai import ChatOpenAI
            local_base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/v1")
            local_model = os.getenv("LOCAL_LLM_MODEL", "qwen2.5-coder:7b")
            llm = ChatOpenAI(
                model=local_model,
                api_key="local-token",
                base_url=local_base_url,
            )
        # 2. Primary Cloud: OpenRouter (Universal Provider)
        elif openrouter_key:
            from langchain_openai import ChatOpenAI
            model_name = os.getenv("OPENROUTER_MODEL", "google/gemini-3.8-flash")
            base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
            llm = ChatOpenAI(
                model=model_name,
                api_key=openrouter_key,
                base_url=base_url,
                default_headers={
                    "HTTP-Referer": "https://github.com/system-controlAi",
                    "X-Title": "System Control AI Agent"
                }
            )
        # 2. Fallbacks
        elif gemini_key:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-pro",
                google_api_key=gemini_key
            )
        elif anthropic_key:
            from langchain_anthropic import ChatAnthropic
            llm = ChatAnthropic(
                model_name="claude-3-5-sonnet-20241022",
                anthropic_api_key=anthropic_key
            )
        else:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-4o")

        agent = Agent(
            task=task_instruction,
            llm=llm
        )
        history = await agent.run()
        return f"Autonomous agent finished task. Result summary:\n{history}"
    except Exception as e:
        return f"Autonomous agent encountered an error: {e}"


@mcp_server.tool()
async def browser_close() -> str:
    """Close the active Chromium browser session."""
    global _playwright, _browser, _context, _page
    async with _lock:
        if _page and not _page.is_closed():
            await _page.close()
            _page = None
        if _context:
            await _context.close()
            _context = None
        if _browser and _browser.is_connected():
            await _browser.close()
            _browser = None
        if _playwright:
            await _playwright.stop()
            _playwright = None
    return "Browser session closed successfully."


def main():
    """Main entry point. Runs stdio MCP server for Goose or CLI test mode."""
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        async def run_test():
            print(f"Testing browser-use MCP server on {CURRENT_OS} (Headless: {HEADLESS})...")
            res = await browser_navigate("https://news.ycombinator.com")
            print(res)
            shot = await browser_take_screenshot("test_nav.png")
            print(shot)
            content = await browser_get_content(max_length=300)
            print("Content preview:\n", content)
            await browser_close()
            print("Test completed successfully!")
        asyncio.run(run_test())
    else:
        # Run stdio MCP server for Goose / Claude / Antigravity
        mcp_server.run(transport="stdio")


if __name__ == "__main__":
    main()
