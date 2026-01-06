#!/usr/bin/env python3
"""
Auto-Build Knowledge Base Helper

This script checks if a knowledge base exists and offers to build it automatically
if missing. Used by both hooks and commands to provide a seamless first-time experience.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Tuple


def find_knowledge_base(start_dir: Optional[Path] = None) -> Optional[Path]:
    """
    Find the knowledge base directory.

    Searches upward from start_dir for .fellow-data/semantic/
    """
    if start_dir is None:
        start_dir = Path.cwd()

    current = start_dir
    for _ in range(10):  # Search up to 10 levels
        kb_dir = current / '.fellow-data' / 'semantic'
        if kb_dir.exists() and kb_dir.is_dir():
            # Check if KB has files
            required_files = [
                'factual_knowledge.json',
                'procedural_knowledge.json',
                'conceptual_knowledge.json'
            ]
            if any((kb_dir / f).exists() for f in required_files):
                return kb_dir
        if current.parent == current:  # Reached root
            break
        current = current.parent

    return None


def get_project_root(start_dir: Optional[Path] = None) -> Path:
    """
    Get the project root directory (where KB should be built).

    Returns current directory or the first parent with .git/
    """
    if start_dir is None:
        start_dir = Path.cwd()

    current = start_dir
    for _ in range(10):
        if (current / '.git').exists():
            return current
        if current.parent == current:  # Reached root
            break
        current = current.parent

    # No .git found, use current directory
    return start_dir


def kb_exists() -> Tuple[bool, Optional[Path]]:
    """
    Check if knowledge base exists.

    Returns:
        (exists, kb_path)
    """
    kb_dir = find_knowledge_base()
    return (kb_dir is not None, kb_dir)


def should_prompt_build(source: str = "hook") -> bool:
    """
    Determine if we should prompt to build KB.

    Args:
        source: "hook" or "command"

    Returns:
        True if we should prompt, False otherwise
    """
    # For hooks, only prompt once per session (avoid spam)
    # For commands, always prompt (user explicitly invoked)

    if source == "command":
        return True

    # For hooks, check if we've already prompted this session
    # Use a marker file to track this
    marker_file = Path.home() / '.claude' / '.fellow-kb-prompt-shown'

    if marker_file.exists():
        # Already prompted this session
        return False

    # Mark as prompted
    marker_file.parent.mkdir(parents=True, exist_ok=True)
    marker_file.touch()

    return True


def display_kb_missing_message(source: str = "hook", user_request: str = ""):
    """
    Display a helpful message when KB is missing.

    Args:
        source: "hook" or "command"
        user_request: The original user request
    """
    project_root = get_project_root()

    print("", file=sys.stderr)
    print("⚠️  **Fellow Knowledge Base Not Found**", file=sys.stderr)
    print("", file=sys.stderr)

    if source == "hook":
        print("Fellow detected a coding request but couldn't find a knowledge base for this project.", file=sys.stderr)
        print("", file=sys.stderr)
        print("**To enable context enrichment:**", file=sys.stderr)
        print("1. Build the knowledge base: `/build-kb`", file=sys.stderr)
        print("   (Takes 2-5 minutes for first extraction)", file=sys.stderr)
        print("", file=sys.stderr)
        print("**Or continue without enrichment:**", file=sys.stderr)
        print("Your request will proceed without Fellow's architectural context.", file=sys.stderr)
        print("", file=sys.stderr)
    else:  # command
        print("This appears to be the first time using Fellow on this project.", file=sys.stderr)
        print("To enable context enrichment, Fellow needs to extract semantic knowledge", file=sys.stderr)
        print("from your codebase.", file=sys.stderr)
        print("", file=sys.stderr)
        print(f"**Project directory:** {project_root}", file=sys.stderr)
        print("**Time required:** 2-5 minutes (one-time process)", file=sys.stderr)
        print("", file=sys.stderr)
        print("**Would you like to build the knowledge base now?**", file=sys.stderr)
        print("", file=sys.stderr)
        print("Options:", file=sys.stderr)
        print("1. Build now (recommended) - Fellow will extract knowledge automatically", file=sys.stderr)
        print("2. Cancel and build later - Run `/build-kb` manually when ready", file=sys.stderr)
        print("", file=sys.stderr)


def prompt_user_for_build() -> bool:
    """
    Prompt user to build KB.

    Returns:
        True if user wants to build, False otherwise
    """
    try:
        response = input("Build knowledge base now? (y/n): ").strip().lower()
        return response in ['y', 'yes', '1']
    except (EOFError, KeyboardInterrupt):
        print("\n", file=sys.stderr)
        return False


def trigger_kb_build(project_root: Optional[Path] = None) -> bool:
    """
    Trigger knowledge base build.

    This outputs a special command that Claude Code can execute.

    Returns:
        True if build was triggered successfully
    """
    if project_root is None:
        project_root = get_project_root()

    print("", file=sys.stderr)
    print("🔨 **Building Knowledge Base**", file=sys.stderr)
    print("", file=sys.stderr)
    print(f"Project: {project_root}", file=sys.stderr)
    print("This will take 2-5 minutes...", file=sys.stderr)
    print("", file=sys.stderr)

    # Output a command for Claude Code to execute
    # This is a special format that tells Claude to run /build-kb
    print(f"FELLOW_AUTO_BUILD:{project_root}", file=sys.stderr)

    return True


def main():
    """Main entry point for testing."""
    source = sys.argv[1] if len(sys.argv) > 1 else "command"
    user_request = sys.argv[2] if len(sys.argv) > 2 else ""

    # Check if KB exists
    exists, kb_path = kb_exists()

    if exists:
        print(f"✓ Knowledge base found at: {kb_path}", file=sys.stderr)
        sys.exit(0)
    else:
        print("✗ Knowledge base not found", file=sys.stderr)

        # Display message
        display_kb_missing_message(source, user_request)

        if source == "command":
            # Prompt for build
            if prompt_user_for_build():
                trigger_kb_build()
                sys.exit(0)  # Build triggered
            else:
                print("", file=sys.stderr)
                print("ℹ️  Knowledge base build cancelled.", file=sys.stderr)
                print("", file=sys.stderr)
                print("To use Fellow later:", file=sys.stderr)
                print("1. Run `/build-kb` to extract knowledge (2-5 minutes)", file=sys.stderr)
                print("2. Then use `/fellow` or enable automatic enrichment", file=sys.stderr)
                print("", file=sys.stderr)
                sys.exit(1)  # Build cancelled
        else:
            # Hook - just display message
            sys.exit(1)  # KB not found


if __name__ == '__main__':
    main()
