#!/usr/bin/env python3
"""
Cross-Platform Environment & Goose MCP Configuration Generator
--------------------------------------------------------------
Works seamlessly on Windows, macOS, and Linux.
Configures:
  1. Dynamic path and binary discovery (uv, python, workspace)
  2. OpenRouter provider configuration for Goose
  3. Browser-Use MCP server registration in Goose (config.yaml & config.json)
  4. .env synchronization
"""

import json
import os
import platform
import shutil
import sys
from pathlib import Path

# Ensure UTF-8 output handling on all platforms
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Detect Operating System
CURRENT_OS = platform.system()  # 'Windows', 'Darwin' (macOS), 'Linux'

def find_uv_executable() -> str:
    """Dynamically locate the uv executable on any operating system."""
    # 1. Check current system PATH
    which_uv = shutil.which("uv")
    if which_uv:
        return str(Path(which_uv).resolve())

    # 2. Check standard installation directories
    home = Path.home()
    candidate_paths = [
        home / ".local" / "bin" / ("uv.exe" if CURRENT_OS == "Windows" else "uv"),
        home / ".cargo" / "bin" / ("uv.exe" if CURRENT_OS == "Windows" else "uv"),
        Path("/usr/local/bin/uv"),
        Path("/opt/homebrew/bin/uv"),
    ]

    for candidate in candidate_paths:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate.resolve())

    # Fallback to "uv" command name
    return "uv.exe" if CURRENT_OS == "Windows" else "uv"


def get_goose_config_dirs() -> list[Path]:
    """Return all standard Goose configuration directories for the current OS."""
    home = Path.home()
    dirs = []

    if CURRENT_OS == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            dirs.append(Path(appdata) / "Block" / "goose" / "config")
            dirs.append(Path(appdata) / "goose")
        dirs.append(home / ".config" / "goose")
    elif CURRENT_OS == "Darwin":  # macOS
        dirs.append(home / "Library" / "Application Support" / "goose")
        dirs.append(home / "Library" / "Application Support" / "Block" / "goose" / "config")
        dirs.append(home / ".config" / "goose")
    else:  # Linux
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            dirs.append(Path(xdg_config) / "goose")
            dirs.append(Path(xdg_config) / "Block" / "goose" / "config")
        dirs.append(home / ".config" / "goose")

    return dirs


def load_env_file(env_path: Path) -> dict[str, str]:
    """Parse key-value pairs from a .env file."""
    values = {}
    if not env_path.is_file():
        return values

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            values[key.strip()] = val.strip().strip("'\"")
    return values


def main():
    root_dir = Path(__file__).resolve().parent
    workspace_dir = root_dir / "desktop-agent-workspace"
    env_file = workspace_dir / ".env"
    server_script = workspace_dir / "browser_use_mcp_server.py"

    print("=" * 65)
    print(">> Universal Agent Configuration Generator")
    print(f"   OS: {CURRENT_OS} ({platform.platform()})")
    print(f"   Python: {sys.version.split()[0]}")
    print("=" * 65)

    # 1. Discover uv binary
    uv_bin = find_uv_executable()
    print(f"[+] uv Binary Detected: {uv_bin}")
    print(f"[+] Workspace Directory: {workspace_dir}")
    print(f"[+] Server Script:       {server_script}")

    # 2. Read environment variables from .env
    env_vars = load_env_file(env_file)
    use_local = env_vars.get("USE_LOCAL_LLM", "false").strip().lower() in ("true", "1", "yes")
    openrouter_key = env_vars.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_API_KEY", "")
    openrouter_model = env_vars.get("OPENROUTER_MODEL", "google/gemini-3.8-flash")
    headless = env_vars.get("BROWSER_HEADLESS", "false")

    local_provider = env_vars.get("LOCAL_LLM_PROVIDER", "ollama")
    local_model = env_vars.get("LOCAL_LLM_MODEL", "qwen2.5-coder:7b")
    local_base_url = env_vars.get("LOCAL_LLM_BASE_URL", "http://localhost:11434/v1")
    ollama_host = env_vars.get("OLLAMA_HOST", "http://localhost:11434")

    if use_local:
        active_provider = local_provider
        active_model = local_model
        print(f"[+] Mode:                LOCAL OPEN SOURCE ({local_provider})")
        print(f"[+] Provider:            {local_provider}")
        print(f"[+] Model:               {local_model}")
        print(f"[+] Endpoint:            {local_base_url}")
    else:
        active_provider = "openrouter"
        active_model = openrouter_model
        print(f"[+] Mode:                CLOUD (OpenRouter)")
        print(f"[+] Provider:            openrouter")
        print(f"[+] Model:               {openrouter_model}")

    print(f"[+] Browser Headless:    {headless}")

    # 3. Generate cross-platform MCP Server configuration
    uv_posix = Path(uv_bin).resolve().as_posix()
    workspace_posix = workspace_dir.resolve().as_posix()

    mcp_env = {
        "BROWSER_HEADLESS": headless,
        "BROWSER_USE_LOGGING_LEVEL": "info",
        "USE_LOCAL_LLM": "true" if use_local else "false",
        "LOCAL_LLM_BASE_URL": local_base_url,
        "LOCAL_LLM_MODEL": local_model,
        "OPENROUTER_API_KEY": openrouter_key,
        "OPENROUTER_MODEL": openrouter_model
    }

    mcp_config = {
        "GOOSE_PROVIDER": active_provider,
        "GOOSE_MODEL": active_model,
        "mcpServers": {
            "browser-use": {
                "command": uv_posix,
                "args": [
                    "--directory",
                    workspace_posix,
                    "run",
                    "python",
                    "browser_use_mcp_server.py"
                ],
                "env": mcp_env
            }
        },
        "extensions": {
            "developer": {
                "enabled": True,
                "name": "developer",
                "type": "platform"
            },
            "browser_use": {
                "enabled": True,
                "name": "browser_use",
                "type": "stdio",
                "cmd": uv_posix,
                "args": [
                    "--directory",
                    workspace_posix,
                    "run",
                    "python",
                    "browser_use_mcp_server.py"
                ],
                "envs": mcp_env,
                "timeout": 300,
                "description": "Browser-Use MCP Server: Autonomous browser actuation powered by Playwright and Chromium"
            }
        }
    }

    # Prepare YAML version
    yaml_lines = [
        "# Goose Global Configuration (Generated by configure_environment.py)",
        f"# Provider Mode: {'LOCAL (' + active_provider + ')' if use_local else 'CLOUD (OpenRouter)'}",
        "",
        f"GOOSE_PROVIDER: {active_provider}",
        f"GOOSE_MODEL: {active_model}",
    ]
    if use_local and active_provider == "ollama":
        yaml_lines.append(f"OLLAMA_HOST: {ollama_host}")

    yaml_lines.extend([
        "",
        "extensions:",
        "  developer:",
        "    enabled: true",
        "    name: developer",
        "    type: platform",
        "  browser_use:",
        "    enabled: true",
        "    name: browser_use",
        "    type: stdio",
        f"    cmd: \"{uv_posix}\"",
        "    args:",
        "      - --directory",
        f"      - \"{workspace_posix}\"",
        "      - run",
        "      - python",
        "      - browser_use_mcp_server.py",
        "    envs:",
        f"      BROWSER_HEADLESS: \"{headless}\"",
        "      BROWSER_USE_LOGGING_LEVEL: \"info\"",
        f"      USE_LOCAL_LLM: \"{'true' if use_local else 'false'}\"",
        f"      LOCAL_LLM_BASE_URL: \"{local_base_url}\"",
        f"      LOCAL_LLM_MODEL: \"{local_model}\"",
        f"      OPENROUTER_API_KEY: \"{openrouter_key}\"",
        f"      OPENROUTER_MODEL: \"{openrouter_model}\"",
        "    timeout: 300",
        "    description: \"Browser-Use MCP Server: Autonomous browser actuation powered by Playwright and Chromium\"",
        ""
    ])
    yaml_content = "\n".join(yaml_lines)
    json_content = json.dumps(mcp_config, indent=2)

    # 4. Write configs to all valid Goose config directories on the host
    config_dirs = get_goose_config_dirs()
    written_files = []

    for cdir in config_dirs:
        try:
            cdir.mkdir(parents=True, exist_ok=True)
            yaml_path = cdir / "config.yaml"
            json_path = cdir / "config.json"
            secrets_path = cdir / "secrets.yaml"
            secrets_content = f"OPENROUTER_API_KEY: {openrouter_key}\n"

            with open(yaml_path, "w", encoding="utf-8") as f:
                f.write(yaml_content)
            with open(json_path, "w", encoding="utf-8") as f:
                f.write(json_content)
            with open(secrets_path, "w", encoding="utf-8") as f:
                f.write(secrets_content)

            written_files.append(yaml_path)
            written_files.append(json_path)
            written_files.append(secrets_path)
            print(f"[v] Successfully configured Goose in: {cdir}")
        except Exception as e:
            print(f"[!] Warning: Could not write to {cdir}: {e}")

    print("=" * 65)
    print("Agent Configuration Complete!")
    print(f"Configured files: {len(written_files)} files across {len(config_dirs)} directories.")
    if not openrouter_key:
        print("[!] Remember to paste your OPENROUTER_API_KEY in:")
        print(f"    {env_file}")
        print("    Then re-run: python configure_environment.py")
    else:
        print("[v] OpenRouter API Key registered.")
    print("=" * 65)


if __name__ == "__main__":
    main()
