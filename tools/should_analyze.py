#!/usr/bin/env python3
"""
Helper script to check if a file should be analyzed for knowledge extraction.

Usage:
    python3 should_analyze.py <file-path> [<file-path> ...]

Returns:
    - Exit code 0 if ALL files should be analyzed
    - Exit code 1 if ANY file should be excluded
    - Prints "ANALYZE" or "SKIP" for each file to stdout
"""

import sys
from pathlib import Path

# Add the tools directory to Python path to ensure imports work
SCRIPT_DIR = Path(__file__).parent.resolve()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from file_filters import should_exclude_path, should_analyze_file


def main():
    if len(sys.argv) < 2:
        print("Usage: should_analyze.py <file-path> [<file-path> ...]", file=sys.stderr)
        sys.exit(1)

    should_skip_any = False

    for file_path in sys.argv[1:]:
        if should_analyze_file(file_path):
            print(f"ANALYZE: {file_path}")
        else:
            print(f"SKIP: {file_path}")
            should_skip_any = True

    # Exit with code 1 if any file should be skipped
    sys.exit(1 if should_skip_any else 0)


if __name__ == "__main__":
    main()
