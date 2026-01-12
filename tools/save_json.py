#!/usr/bin/env python3
"""
JSON File Saver Utility

This utility safely saves JSON data to files, handling directory creation
and proper error handling. Used by extraction agents to save knowledge base files.

Usage:
    python3 save_json.py <output_path> '<json_data>'

    Or import in Python:
    from save_json import save_json
    save_json(data, output_path)
"""

import json
import os
import sys
from pathlib import Path


def save_json(data, output_path, indent=2):
    """
    Save JSON data to a file with proper error handling.

    Args:
        data: Python dict/list to save as JSON
        output_path: Absolute path where to save the file
        indent: JSON indentation (default: 2)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Convert to Path object for easier manipulation
        output_path = Path(output_path).resolve()

        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write JSON file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)

        print(f"✓ Saved JSON to: {output_path}")
        return True

    except Exception as e:
        print(f"✗ Error saving JSON to {output_path}: {e}", file=sys.stderr)
        return False


def load_and_update_json(output_path, update_func):
    """
    Load existing JSON, update it with a function, and save back.
    Useful for incremental updates.

    Args:
        output_path: Path to JSON file
        update_func: Function that takes data dict and returns updated dict

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        output_path = Path(output_path).resolve()

        # Load existing data if file exists
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}

        # Apply update function
        data = update_func(data)

        # Save updated data
        return save_json(data, output_path)

    except Exception as e:
        print(f"✗ Error updating JSON at {output_path}: {e}", file=sys.stderr)
        return False


def main():
    """CLI interface for saving JSON."""
    if len(sys.argv) < 3:
        print("Usage: python3 save_json.py <output_path> '<json_data>'")
        print("Example: python3 save_json.py /path/to/output.json '{\"key\": \"value\"}'")
        sys.exit(1)

    output_path = sys.argv[1]
    json_data = sys.argv[2]

    try:
        # Parse JSON string
        data = json.loads(json_data)

        # Save to file
        if save_json(data, output_path):
            sys.exit(0)
        else:
            sys.exit(1)

    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
