#!/usr/bin/env python3
"""
Toggle Fellow hooks on/off for automatic context enrichment.

This tool manages the enabled state of Fellow's context enrichment hooks
by modifying the .claude-plugin/hooks.json configuration file.
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional


def find_plugin_dir() -> Optional[Path]:
    """
    Find the Fellow plugin directory by searching multiple locations.

    Returns:
        Path to the plugin directory, or None if not found
    """
    # Method 1: Check if we're in the plugin development directory
    current = Path.cwd()
    plugin_json = current / ".claude-plugin" / "plugin.json"

    if plugin_json.exists():
        try:
            with open(plugin_json) as f:
                data = json.load(f)
                if data.get("name") == "fellow":
                    return current
        except (json.JSONDecodeError, OSError):
            pass

    # Method 2: Search Claude Code's plugin installation directories
    home = Path.home()
    installed_plugins = home / ".claude" / "plugins" / "installed_plugins.json"

    if installed_plugins.exists():
        try:
            with open(installed_plugins) as f:
                data = json.load(f)
                # Look for fellow plugin entries
                for key, value in data.items():
                    if key.startswith("fellow@") and isinstance(value, dict):
                        install_path = value.get("installPath")
                        if install_path:
                            path = Path(install_path)
                            if path.exists():
                                return path
        except (json.JSONDecodeError, OSError):
            pass

    # Method 3: Search common plugin cache locations
    cache_dir = home / ".claude" / "plugins" / "cache"
    if cache_dir.exists():
        for vendor_dir in cache_dir.iterdir():
            fellow_dir = vendor_dir / "fellow"
            if fellow_dir.exists():
                # Find the latest version
                versions = sorted(fellow_dir.iterdir(), key=lambda p: p.name)
                if versions:
                    return versions[-1]

    return None


def get_hooks_file(plugin_dir: Path) -> Path:
    """Get the path to hooks.json file."""
    return plugin_dir / ".claude-plugin" / "hooks.json"


def read_hooks_config(hooks_file: Path) -> dict:
    """Read and parse hooks.json configuration."""
    try:
        with open(hooks_file) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"❌ Error reading hooks configuration: {e}", file=sys.stderr)
        sys.exit(1)


def write_hooks_config(hooks_file: Path, config: dict) -> None:
    """Write hooks configuration to hooks.json."""
    try:
        # Create backup
        backup = hooks_file.with_suffix(hooks_file.suffix + ".bak")
        if hooks_file.exists():
            import shutil
            shutil.copy2(hooks_file, backup)

        # Write new configuration
        with open(hooks_file, "w") as f:
            json.dump(config, f, indent=2)
    except OSError as e:
        print(f"❌ Error writing hooks configuration: {e}", file=sys.stderr)
        sys.exit(1)


def get_hook_status(config: dict) -> bool:
    """Get the current enabled status of the fellow-context-enrichment hook."""
    for hook in config.get("hooks", []):
        if hook.get("name") == "fellow-context-enrichment":
            return hook.get("enabled", False)
    return False


def set_hook_status(config: dict, enabled: bool) -> dict:
    """Set the enabled status of the fellow-context-enrichment hook."""
    for hook in config.get("hooks", []):
        if hook.get("name") == "fellow-context-enrichment":
            hook["enabled"] = enabled
            break
    return config


def show_status(enabled: bool) -> None:
    """Display the current hook status."""
    if enabled:
        print("✅ Fellow hooks are ENABLED")
        print("   Coding requests will be automatically enriched with context")
        print()
        print("To disable: /fellow:toggle-hooks off")
    else:
        print("❌ Fellow hooks are DISABLED")
        print("   Use /fellow command for explicit enrichment")
        print()
        print("To enable: /fellow:toggle-hooks on")


def enable_hooks(hooks_file: Path) -> None:
    """Enable the fellow-context-enrichment hook."""
    config = read_hooks_config(hooks_file)
    config = set_hook_status(config, True)
    write_hooks_config(hooks_file, config)

    print("✅ Fellow hooks ENABLED")
    print("   Coding requests will now be automatically enriched with context")


def disable_hooks(hooks_file: Path) -> None:
    """Disable the fellow-context-enrichment hook."""
    config = read_hooks_config(hooks_file)
    config = set_hook_status(config, False)
    write_hooks_config(hooks_file, config)

    print("❌ Fellow hooks DISABLED")
    print("   Automatic enrichment is now off")
    print("   Use /fellow command for explicit enrichment when needed")


def main():
    """Main entry point for the toggle-hooks tool."""
    # Get command from arguments
    command = sys.argv[1] if len(sys.argv) > 1 else "status"

    # Find plugin directory
    plugin_dir = find_plugin_dir()
    if not plugin_dir:
        print("⚠️  Could not locate Fellow plugin directory", file=sys.stderr)
        print("   Searched in:", file=sys.stderr)
        print("   - Current directory (development mode)", file=sys.stderr)
        print("   - ~/.claude/plugins/installed_plugins.json", file=sys.stderr)
        print("   - ~/.claude/plugins/cache/*", file=sys.stderr)
        sys.exit(1)

    # Get hooks file
    hooks_file = get_hooks_file(plugin_dir)
    if not hooks_file.exists():
        print(f"⚠️  Hook configuration not found at: {hooks_file}", file=sys.stderr)
        sys.exit(1)

    # Execute command
    if command in ["status", "s"]:
        config = read_hooks_config(hooks_file)
        enabled = get_hook_status(config)
        show_status(enabled)

    elif command in ["on", "enable", "true"]:
        enable_hooks(hooks_file)

    elif command in ["off", "disable", "false"]:
        disable_hooks(hooks_file)

    else:
        print("Usage: toggle_hooks.py [status|on|off]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Commands:", file=sys.stderr)
        print("  status  - Show current hook status (default)", file=sys.stderr)
        print("  on      - Enable automatic context enrichment", file=sys.stderr)
        print("  off     - Disable automatic context enrichment", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
