#!/usr/bin/env python3
"""
Detect changed files since last knowledge base extraction.

This tool identifies which files have been modified, added, or deleted since
the last extraction, enabling incremental updates to the knowledge base.
"""

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Add the tools directory to Python path to ensure imports work
SCRIPT_DIR = Path(__file__).parent.resolve()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Import shared filtering utilities
from file_filters import (
    EXCLUDE_DIRS,
    should_exclude_path,
    is_source_file,
    SOURCE_EXTENSIONS
)


def load_metadata(kb_dir: Path) -> Optional[Dict]:
    """Load extraction metadata from the knowledge base directory."""
    metadata_path = kb_dir / "extraction_metadata.json"

    if not metadata_path.exists():
        return None

    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"⚠️  Warning: Could not load metadata: {e}", file=sys.stderr)
        return None


def is_git_repo(project_path: Path) -> bool:
    """Check if the project is a git repository."""
    git_dir = project_path / ".git"
    return git_dir.exists() and git_dir.is_dir()


def get_git_changed_files(project_path: Path, last_commit: Optional[str]) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Get changed files using git.

    Args:
        project_path: Path to the project
        last_commit: Last commit hash from metadata

    Returns:
        Tuple of (modified_files, new_files, deleted_files)
    """
    modified = set()
    new = set()
    deleted = set()

    try:
        os.chdir(project_path)

        # Get committed changes since last extraction
        if last_commit:
            # Get files changed between last commit and HEAD
            result = subprocess.run(
                ["git", "diff", "--name-status", last_commit, "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )

            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                parts = line.split('\t', 1)
                if len(parts) != 2:
                    continue
                status, filepath = parts

                if status == 'M':
                    modified.add(filepath)
                elif status == 'A':
                    new.add(filepath)
                elif status == 'D':
                    deleted.add(filepath)
                elif status.startswith('R'):  # Renamed
                    # Format: R100  old_path  new_path
                    # Treat as delete old + add new
                    if '\t' in filepath:
                        old_path, new_path = filepath.split('\t')
                        deleted.add(old_path)
                        new.add(new_path)

        # Get uncommitted changes
        result = subprocess.run(
            ["git", "diff", "--name-status"],
            capture_output=True,
            text=True,
            check=True
        )

        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('\t', 1)
            if len(parts) != 2:
                continue
            status, filepath = parts

            if status == 'M':
                modified.add(filepath)
            elif status == 'D':
                deleted.add(filepath)

        # Get untracked files
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
            check=True
        )

        for line in result.stdout.strip().split('\n'):
            if line:
                new.add(line)

        # Get staged changes
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-status"],
            capture_output=True,
            text=True,
            check=True
        )

        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('\t', 1)
            if len(parts) != 2:
                continue
            status, filepath = parts

            if status == 'M':
                modified.add(filepath)
            elif status == 'A':
                new.add(filepath)
            elif status == 'D':
                deleted.add(filepath)

    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Git command failed: {e}", file=sys.stderr)
    except Exception as e:
        print(f"⚠️  Warning: Error detecting git changes: {e}", file=sys.stderr)

    return modified, new, deleted


def calculate_file_hash(file_path: Path) -> str:
    """Calculate SHA-256 hash of a file."""
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return f"sha256:{sha256_hash.hexdigest()}"
    except OSError:
        return ""


def get_fallback_changed_files(
    project_path: Path,
    metadata: Optional[Dict]
) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Get changed files using file modification times and hashes (fallback method).

    Args:
        project_path: Path to the project
        metadata: Extraction metadata

    Returns:
        Tuple of (modified_files, new_files, deleted_files)
    """
    modified = set()
    new = set()
    deleted = set()

    if not metadata:
        # No metadata, treat as full extraction (all files are new)
        return modified, new, deleted

    file_registry = metadata.get("file_registry", {})

    # Check existing files in registry
    for file_path, file_info in file_registry.items():
        full_path = project_path / file_path

        if not full_path.exists():
            # File was deleted
            deleted.add(file_path)
        else:
            # Check if file changed (compare hash)
            current_hash = calculate_file_hash(full_path)
            stored_hash = file_info.get("hash", "")

            if current_hash and stored_hash and current_hash != stored_hash:
                modified.add(file_path)

    # Find new files (files not in registry)
    for root, dirs, files in os.walk(project_path):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            file_path = Path(root) / file

            # Only consider source code files
            if file_path.suffix not in SOURCE_EXTENSIONS:
                continue

            # Get relative path
            try:
                rel_path = str(file_path.relative_to(project_path))
            except ValueError:
                continue

            # Check if file is new (not in registry and not already in modified/new sets)
            if rel_path not in file_registry and rel_path not in modified and rel_path not in new:
                new.add(rel_path)

    return modified, new, deleted


def filter_source_files(
    modified: Set[str],
    new: Set[str],
    deleted: Set[str]
) -> Tuple[Set[str], Set[str], Set[str]]:
    """Filter to only include source code files and exclude generated/test files."""
    return (
        {f for f in modified if is_source_file(f) and not should_exclude_path(f)},
        {f for f in new if is_source_file(f) and not should_exclude_path(f)},
        {f for f in deleted if is_source_file(f) and not should_exclude_path(f)}
    )


def detect_changes(project_path: Path) -> Dict:
    """
    Detect all changes since last extraction.

    Args:
        project_path: Path to the target project

    Returns:
        Dictionary with change information
    """
    kb_dir = project_path / ".fellow-data" / "semantic"

    # Load metadata
    metadata = load_metadata(kb_dir)

    if not metadata:
        print("ℹ️  No extraction metadata found", file=sys.stderr)
        print("   This appears to be a first-time extraction", file=sys.stderr)
        return {
            "status": "no_metadata",
            "mode": "full",
            "modified": [],
            "new": [],
            "deleted": [],
            "total": 0
        }

    # Get last commit from metadata
    last_commit = metadata.get("git_info", {}).get("commit_hash")

    # Try git-based detection first
    if is_git_repo(project_path):
        print("🔍 Detecting changes using git...", file=sys.stderr)
        modified, new, deleted = get_git_changed_files(project_path, last_commit)
    else:
        print("🔍 Detecting changes using file comparison...", file=sys.stderr)
        modified, new, deleted = get_fallback_changed_files(project_path, metadata)

    # Filter to only source files
    modified, new, deleted = filter_source_files(modified, new, deleted)

    total_changes = len(modified) + len(new) + len(deleted)

    return {
        "status": "success",
        "mode": "incremental" if total_changes > 0 else "up_to_date",
        "modified": sorted(list(modified)),
        "new": sorted(list(new)),
        "deleted": sorted(list(deleted)),
        "total": total_changes,
        "detection_method": "git" if is_git_repo(project_path) else "file_comparison"
    }


def print_changes(changes: Dict) -> None:
    """Print change detection results in a user-friendly format."""
    if changes["status"] == "no_metadata":
        print("\n📋 Change Detection Result:")
        print("   Mode: Full Extraction (no previous extraction found)")
        print("   All source files will be analyzed")
        print()
        print("ℹ️  Note: Excluding build dirs (dist, node_modules, etc.) and test files")
        print()
        return

    if changes["mode"] == "up_to_date":
        print("\n✅ Knowledge base is up-to-date")
        print()
        print("   No files changed since last extraction")
        print(f"   Detection method: {changes['detection_method']}")
        print()
        print("💡 Tip: Make code changes and run /fellow:build-kb again to update")
        print()
        return

    print("\n📋 Files Changed Since Last Extraction:")
    print()

    if changes["modified"]:
        print(f"  📝 Modified ({len(changes['modified'])} files):")
        for file in changes["modified"][:10]:  # Show first 10
            print(f"     • {file}")
        if len(changes["modified"]) > 10:
            print(f"     ... and {len(changes['modified']) - 10} more")
        print()

    if changes["new"]:
        print(f"  ✨ New ({len(changes['new'])} files):")
        for file in changes["new"][:10]:  # Show first 10
            print(f"     • {file}")
        if len(changes["new"]) > 10:
            print(f"     ... and {len(changes['new']) - 10} more")
        print()

    if changes["deleted"]:
        print(f"  🗑️  Deleted ({len(changes['deleted'])} files):")
        for file in changes["deleted"][:10]:  # Show first 10
            print(f"     • {file}")
        if len(changes["deleted"]) > 10:
            print(f"     ... and {len(changes['deleted']) - 10} more")
        print()

    print(f"📊 Total: {changes['total']} files to re-analyze")
    print(f"🔍 Detection method: {changes['detection_method']}")
    print()
    print("ℹ️  Note: Excluding build dirs (dist, node_modules, etc.) and test files")
    print()


def main():
    """Main entry point for the detect-changes tool."""
    if len(sys.argv) < 2:
        print("Usage: detect_changes.py <target-project-path>", file=sys.stderr)
        print("", file=sys.stderr)
        print("Detects changed files since last knowledge base extraction.", file=sys.stderr)
        sys.exit(1)

    # Get target project path
    project_path = Path(sys.argv[1]).resolve()

    if not project_path.exists():
        print(f"❌ Error: Target project path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)

    if not project_path.is_dir():
        print(f"❌ Error: Target project path is not a directory: {project_path}", file=sys.stderr)
        sys.exit(1)

    try:
        changes = detect_changes(project_path)

        # Print user-friendly output
        print_changes(changes)

        # Also output JSON to stdout for programmatic use
        print("📄 JSON Output:", file=sys.stderr)
        print(json.dumps(changes, indent=2))

    except Exception as e:
        print(f"❌ Error detecting changes: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
