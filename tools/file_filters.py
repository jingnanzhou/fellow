#!/usr/bin/env python3
"""
Shared file filtering utilities for Fellow knowledge base extraction.

This module provides consistent filtering logic to exclude:
- Build/generated directories (dist, build, node_modules, etc.)
- Test files and directories
- IDE and cache directories
"""

from pathlib import Path
from typing import Set


# Directories to exclude from analysis
EXCLUDE_DIRS: Set[str] = {
    # Version control
    '.git', '.svn', '.hg',

    # Build outputs and generated code
    'dist', 'build', 'out', 'target', 'bin', 'obj',
    '.next', '.nuxt', '.output', '.vitepress',
    'coverage', '.nyc_output',

    # Dependencies
    'node_modules', 'bower_components',
    'vendor', 'packages',
    'venv', '.venv', 'env', '.env',
    '__pycache__', '.pytest_cache',

    # IDE and editor files
    '.idea', '.vscode', '.vs',

    # Fellow data
    '.fellow-data',

    # Other common generated/cache directories
    '.cache', 'tmp', 'temp',
    '.parcel-cache', '.webpack',
    'public/build', 'static/build',
}

# Test-related path patterns to exclude
TEST_PATTERNS: list[str] = [
    'test', 'tests', '__tests__',
    'spec', 'specs',
    'e2e', 'integration',
    'fixtures', 'mocks',
]

# Source code file extensions to analyze
SOURCE_EXTENSIONS: Set[str] = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.go',
    '.rs', '.c', '.cpp', '.h', '.hpp', '.cs', '.rb',
    '.php', '.swift', '.kt', '.scala', '.sh', '.bash'
}


def is_test_file(file_path: str) -> bool:
    """
    Check if a file is a test file based on path patterns.

    Args:
        file_path: Relative or absolute path to the file

    Returns:
        True if the file appears to be a test file, False otherwise
    """
    path_parts = Path(file_path).parts

    # Check if any part of the path contains test-related terms
    for pattern in TEST_PATTERNS:
        if any(pattern in part.lower() for part in path_parts):
            return True

    # Check filename patterns
    filename = Path(file_path).name.lower()
    if any(pattern in filename for pattern in ['test', 'spec', 'mock', 'fixture']):
        return True

    # Check for common test file suffixes
    if any(filename.endswith(suffix) for suffix in [
        '.test.js', '.test.ts', '.test.jsx', '.test.tsx',
        '.spec.js', '.spec.ts', '.spec.jsx', '.spec.tsx',
        '_test.py', '_test.go', 'test.py', 'test.go',
        '.test.java', 'test.java'
    ]):
        return True

    return False


def should_exclude_path(file_path: str) -> bool:
    """
    Check if a file path should be excluded from analysis.

    This function checks if:
    - Any directory in the path is in EXCLUDE_DIRS
    - The file is a test file (based on is_test_file)

    Args:
        file_path: Relative or absolute path to the file

    Returns:
        True if the file should be excluded, False otherwise
    """
    path_parts = Path(file_path).parts

    # Check if any directory in the path matches excluded directories
    for part in path_parts:
        if part in EXCLUDE_DIRS:
            return True

    # Check if it's a test file
    if is_test_file(file_path):
        return True

    return False


def is_source_file(file_path: str) -> bool:
    """
    Check if a file is a source code file.

    Args:
        file_path: Path to the file

    Returns:
        True if the file has a source code extension, False otherwise
    """
    ext = Path(file_path).suffix.lower()
    return ext in SOURCE_EXTENSIONS


def should_analyze_file(file_path: str) -> bool:
    """
    Check if a file should be analyzed for knowledge extraction.

    Combines all filtering rules:
    - Must be a source file
    - Must not be in an excluded directory
    - Must not be a test file

    Args:
        file_path: Path to the file

    Returns:
        True if the file should be analyzed, False otherwise
    """
    return is_source_file(file_path) and not should_exclude_path(file_path)


def get_exclusion_summary() -> str:
    """
    Get a human-readable summary of what files are excluded.

    Returns:
        A formatted string describing the exclusion rules
    """
    summary = "Files excluded from analysis:\n"
    summary += "  - Build/generated directories: dist, build, .next, node_modules, etc.\n"
    summary += "  - Test files and directories: *test*, *spec*, __tests__, etc.\n"
    summary += "  - IDE and cache: .vscode, .idea, .cache, etc.\n"
    summary += f"  - Total excluded directories: {len(EXCLUDE_DIRS)}\n"
    summary += f"  - Test patterns matched: {len(TEST_PATTERNS)}"
    return summary
