#!/usr/bin/env python3
"""
Collect git repository information for knowledge base metadata.

This tool gathers git repository metadata including commit hash, branch name,
and uncommitted changes status for tracking extraction state.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional


def is_git_repo(project_path: Path) -> bool:
    """Check if the project is a git repository."""
    git_dir = project_path / ".git"
    return git_dir.exists() and git_dir.is_dir()


def get_current_commit(project_path: Path) -> Optional[str]:
    """Get the current git commit hash."""
    try:
        os.chdir(project_path)
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except Exception as e:
        print(f"⚠️  Warning: Could not get commit hash: {e}", file=sys.stderr)
        return None


def get_current_branch(project_path: Path) -> Optional[str]:
    """Get the current git branch name."""
    try:
        os.chdir(project_path)
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except Exception as e:
        print(f"⚠️  Warning: Could not get branch name: {e}", file=sys.stderr)
        return None


def has_uncommitted_changes(project_path: Path) -> bool:
    """Check if there are uncommitted changes in the repository."""
    try:
        os.chdir(project_path)

        # Check for uncommitted changes in tracked files
        result = subprocess.run(
            ["git", "diff", "--quiet"],
            capture_output=True,
            check=False  # Don't raise exception on non-zero exit
        )

        if result.returncode != 0:
            return True

        # Check for staged changes
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            capture_output=True,
            check=False
        )

        if result.returncode != 0:
            return True

        # Check for untracked files
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
            check=True
        )

        if result.stdout.strip():
            return True

        return False

    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        print(f"⚠️  Warning: Could not check for uncommitted changes: {e}", file=sys.stderr)
        return False


def get_remote_url(project_path: Path) -> Optional[str]:
    """Get the remote URL for the origin remote."""
    try:
        os.chdir(project_path)
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except Exception as e:
        print(f"⚠️  Warning: Could not get remote URL: {e}", file=sys.stderr)
        return None


def get_commit_message(project_path: Path) -> Optional[str]:
    """Get the current commit message."""
    try:
        os.chdir(project_path)
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=%B"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except Exception as e:
        print(f"⚠️  Warning: Could not get commit message: {e}", file=sys.stderr)
        return None


def get_commit_author(project_path: Path) -> Optional[str]:
    """Get the current commit author."""
    try:
        os.chdir(project_path)
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=%an <%ae>"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except Exception as e:
        print(f"⚠️  Warning: Could not get commit author: {e}", file=sys.stderr)
        return None


def get_commit_date(project_path: Path) -> Optional[str]:
    """Get the current commit date in ISO format."""
    try:
        os.chdir(project_path)
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=%aI"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
    except Exception as e:
        print(f"⚠️  Warning: Could not get commit date: {e}", file=sys.stderr)
        return None


def collect_git_info(project_path: Path, detailed: bool = False) -> Dict:
    """
    Collect git repository information.

    Args:
        project_path: Path to the project
        detailed: If True, collect additional detailed information

    Returns:
        Dictionary with git information
    """
    if not is_git_repo(project_path):
        return {
            "is_git_repo": False,
            "error": "Not a git repository"
        }

    info = {
        "is_git_repo": True,
        "commit_hash": get_current_commit(project_path),
        "branch": get_current_branch(project_path),
        "has_uncommitted_changes": has_uncommitted_changes(project_path)
    }

    if detailed:
        info.update({
            "remote_url": get_remote_url(project_path),
            "commit_message": get_commit_message(project_path),
            "commit_author": get_commit_author(project_path),
            "commit_date": get_commit_date(project_path)
        })

    return info


def print_git_info(info: Dict) -> None:
    """Print git information in a user-friendly format."""
    if not info.get("is_git_repo", False):
        print("\n📋 Git Repository Information:")
        print("   ⚠️  Not a git repository")
        print()
        return

    print("\n📋 Git Repository Information:")
    print()

    if info.get("commit_hash"):
        print(f"  📌 Commit: {info['commit_hash'][:12]}")

    if info.get("branch"):
        print(f"  🌿 Branch: {info['branch']}")

    has_changes = info.get("has_uncommitted_changes", False)
    status = "⚠️  Yes (uncommitted changes present)" if has_changes else "✅ No"
    print(f"  📝 Uncommitted Changes: {status}")

    if info.get("remote_url"):
        print(f"  🔗 Remote: {info['remote_url']}")

    if info.get("commit_message"):
        message = info['commit_message'].split('\n')[0]  # First line only
        if len(message) > 60:
            message = message[:57] + "..."
        print(f"  💬 Latest Commit: {message}")

    if info.get("commit_author"):
        print(f"  👤 Author: {info['commit_author']}")

    if info.get("commit_date"):
        print(f"  📅 Date: {info['commit_date']}")

    print()


def main():
    """Main entry point for the git-info tool."""
    if len(sys.argv) < 2:
        print("Usage: git_info.py <target-project-path> [--detailed]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Collects git repository information for knowledge base metadata.", file=sys.stderr)
        print("", file=sys.stderr)
        print("Options:", file=sys.stderr)
        print("  --detailed    Include additional information (remote URL, commit message, etc.)", file=sys.stderr)
        sys.exit(1)

    # Get target project path
    project_path = Path(sys.argv[1]).resolve()
    detailed = "--detailed" in sys.argv

    if not project_path.exists():
        print(f"❌ Error: Target project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    if not project_path.is_dir():
        print(f"❌ Error: Target project path is not a directory: {project_path}", file=sys.stderr)
        sys.exit(1)

    try:
        info = collect_git_info(project_path, detailed=detailed)

        # Print user-friendly output
        print_git_info(info)

        # Also output JSON to stdout for programmatic use
        print("📄 JSON Output:", file=sys.stderr)
        print(json.dumps(info, indent=2))

    except Exception as e:
        print(f"❌ Error collecting git information: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
