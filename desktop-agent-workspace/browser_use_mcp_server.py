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
import json
import os
import platform
import sys
import urllib.request
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

# Chrome Profile & CDP Configuration
CHROME_MODE = os.getenv("CHROME_MODE", "auto").strip().lower()
CHROME_CDP_URL = os.getenv("CHROME_CDP_URL", "http://localhost:9222").strip()
CHROME_PROFILE_DIR = os.getenv("CHROME_PROFILE_DIRECTORY", "Profile 9").strip()
CHROME_USER_DATA_DIR = os.getenv("CHROME_USER_DATA_DIR", "").strip()

# Initialize MCP Server
mcp_server = MCPServer(
    name="browser-use",
    version="1.2.0",
    instructions="Universal cross-platform browser control server powered by Browser-Use, Playwright, Chrome Profiles, and OpenRouter."
)

# Global browser session state
_playwright = None
_browser: Optional[Browser] = None
_context: Optional[BrowserContext] = None
_page: Optional[Page] = None
_is_cdp_session: bool = False
_lock = asyncio.Lock()


def is_cdp_available(url: str = "http://localhost:9222") -> bool:
    """Quickly verify if a Chrome instance with remote debugging is active."""
    try:
        endpoint = f"{url.rstrip('/')}/json/version"
        req = urllib.request.Request(endpoint, headers={"User-Agent": "SystemControlAI"})
        with urllib.request.urlopen(req, timeout=1.2) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8", errors="ignore"))
                return "webSocketDebuggerUrl" in data or "Browser" in data
    except Exception:
        return False
    return False


async def _get_or_create_page() -> Page:
    """Ensure a Chrome/Chromium browser instance is active and return the current page."""
    global _playwright, _browser, _context, _page, _is_cdp_session
    async with _lock:
        if _playwright is None:
            _playwright = await async_playwright().start()

        # Check if current page is still open and responsive
        if _page is not None and not _page.is_closed():
            return _page

        # If context is alive and has open pages
        if _context is not None:
            try:
                pages = _context.pages
                if pages and not pages[-1].is_closed():
                    _page = pages[-1]
                    return _page
                _page = await _context.new_page()
                return _page
            except Exception:
                pass

        # 1. Connect over CDP (Remote Debugging) to existing Chrome if available
        if CHROME_MODE in ("cdp", "auto") and is_cdp_available(CHROME_CDP_URL):
            try:
                print(f"[browser-use] Attaching to active Chrome via CDP at {CHROME_CDP_URL}...", file=sys.stderr)
                _browser = await _playwright.chromium.connect_over_cdp(CHROME_CDP_URL)
                _is_cdp_session = True
                if _browser.contexts:
                    _context = _browser.contexts[0]
                else:
                    _context = await _browser.new_context()

                if _context.pages:
                    _page = _context.pages[-1]
                else:
                    _page = await _context.new_page()

                title = await _page.title()
                print(f"[browser-use] Successfully attached to existing Chrome! Current Tab: '{title}'", file=sys.stderr)
                return _page
            except Exception as e:
                print(f"[browser-use] CDP attach failed: {e}. Falling back to persistent profile...", file=sys.stderr)
                _is_cdp_session = False

        # 2. Launch real Google Chrome with persistent profile if mode is profile/auto
        if CHROME_MODE in ("profile", "auto"):
            user_data_path = CHROME_USER_DATA_DIR
            if not user_data_path and CURRENT_OS == "Windows":
                user_data_path = str(Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data")

            launch_args = ["--no-sandbox"]
            if CURRENT_OS == "Windows":
                launch_args.append("--start-maximized")
            if CHROME_PROFILE_DIR:
                launch_args.append(f"--profile-directory={CHROME_PROFILE_DIR}")

            try:
                print(f"[browser-use] Launching real Chrome with profile '{CHROME_PROFILE_DIR}'...", file=sys.stderr)
                _context = await _playwright.chromium.launch_persistent_context(
                    user_data_dir=user_data_path,
                    channel="chrome",
                    headless=HEADLESS,
                    no_viewport=True if CURRENT_OS == "Windows" else False,
                    viewport=None if CURRENT_OS == "Windows" else {"width": 1280, "height": 800},
                    args=launch_args
                )
                _is_cdp_session = False
                _page = _context.pages[0] if _context.pages else await _context.new_page()
                return _page
            except Exception as e:
                print(f"[browser-use] Notice: Standard Chrome profile locked ({e}). Using dedicated agent profile...", file=sys.stderr)
                agent_profile = str(Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "User Data - SystemControlAI")
                _context = await _playwright.chromium.launch_persistent_context(
                    user_data_dir=agent_profile,
                    channel="chrome",
                    headless=HEADLESS,
                    no_viewport=True if CURRENT_OS == "Windows" else False,
                    viewport=None if CURRENT_OS == "Windows" else {"width": 1280, "height": 800},
                    args=["--no-sandbox", "--start-maximized"]
                )
                _is_cdp_session = False
                _page = _context.pages[0] if _context.pages else await _context.new_page()
                return _page

        # 3. Default fallback: Clean temporary Chromium sandbox
        launch_args = ["--no-sandbox"]
        if CURRENT_OS == "Windows":
            launch_args.append("--start-maximized")

        _browser = await _playwright.chromium.launch(
            headless=HEADLESS,
            args=launch_args
        )
        _is_cdp_session = False
        _context = await _browser.new_context(
            no_viewport=True if CURRENT_OS == "Windows" else False,
            viewport=None if CURRENT_OS == "Windows" else {"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        )
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
    """Close the active browser session or disconnect from CDP."""
    global _playwright, _browser, _context, _page, _is_cdp_session
    async with _lock:
        if _is_cdp_session:
            # For CDP, disconnect without closing the user's active Chrome!
            if _browser and _browser.is_connected():
                await _browser.close()
            _page = None
            _context = None
            _browser = None
            _is_cdp_session = False
            if _playwright:
                await _playwright.stop()
                _playwright = None
            return "Disconnected from active Chrome session successfully (Chrome and your tabs remain open)."
        else:
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
