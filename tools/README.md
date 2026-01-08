# Fellow Tools

This directory contains utility scripts used by the Fellow plugin for knowledge base extraction and management.

## File Filtering System

All tools use a shared filtering system to exclude non-production code from analysis.

### Core Module: `file_filters.py`

Provides centralized filtering logic used across all tools and agents:

- **36 excluded directories**: `node_modules`, `dist`, `build`, `.next`, `venv`, etc.
- **Test file patterns**: Detects test files by path and filename patterns
- **Reusable functions**: `should_exclude_path()`, `is_test_file()`, `should_analyze_file()`

### Import Path Resolution

All Python tools automatically add the `tools/` directory to `sys.path`, ensuring imports work regardless of where they're invoked from:

```python
# This works from any directory
python3 /path/to/fellow/tools/detect_changes.py /target/project

# The script automatically handles imports
from file_filters import should_exclude_path
```

**How it works**:
```python
# Each tool includes this at the top
SCRIPT_DIR = Path(__file__).parent.resolve()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
```

## Available Tools

### `file_filters.py` - Shared Filtering Utilities
Core module with filtering functions and exclusion rules.

**Usage**:
```python
from file_filters import should_exclude_path, EXCLUDE_DIRS

if should_exclude_path("node_modules/lib.js"):
    # Skip this file
    pass
```

### `detect_changes.py` - Change Detection
Detects files that changed since last KB extraction for incremental updates.

**Usage**:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/detect_changes.py <target-path>
```

**What it does**:
- Loads extraction metadata
- Uses git or file comparison to detect changes
- Filters to only source code files (excludes build/test files)
- Reports modified, new, and deleted files

### `should_analyze.py` - File Analysis Checker
Helper script to check if files should be analyzed.

**Usage**:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/should_analyze.py src/app.js test/app.test.js node_modules/lib.js

# Output:
# ANALYZE: src/app.js
# SKIP: test/app.test.js
# SKIP: node_modules/lib.js
```

**Returns**:
- Exit code 0: All files should be analyzed
- Exit code 1: At least one file should be skipped

### `merge_knowledge.py` - Knowledge Base Merger
Merges delta knowledge with existing KB for incremental updates.

**Usage**:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/merge_knowledge.py <target-path>
```

### `git_info.py` - Git Metadata Collection
Collects git repository information for KB metadata tracking.

**Usage**:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/git_info.py <target-path>
```

### `toggle_hooks.py` - Hook Management
Manages Fellow plugin hooks (enable/disable automatic enrichment).

**Usage**:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/toggle_hooks.py [on|off|status]
```

## Testing

All tools have been tested to work from different working directories:

```bash
# Works from anywhere
cd /tmp
python3 /Users/you/fellow/tools/detect_changes.py /some/project

# Imports are automatically resolved
cd /Users/you/fellow
python3 tools/detect_changes.py /some/project

# Using ${CLAUDE_PLUGIN_ROOT} variable
python3 ${CLAUDE_PLUGIN_ROOT}/tools/detect_changes.py <target>
```

## What Gets Filtered Out

**Build & Generated**:
- `dist`, `build`, `out`, `target`, `bin`
- `.next`, `.nuxt`, `.output`
- `coverage`, `.nyc_output`

**Dependencies**:
- `node_modules`, `bower_components`, `vendor`
- `venv`, `.venv`, `env`, `__pycache__`

**Tests**:
- Directories: `test`, `tests`, `__tests__`, `spec`, `e2e`, `mocks`, `fixtures`
- Files: `*.test.js`, `*.spec.ts`, `*_test.py`, etc.

**IDE & VCS**:
- `.git`, `.svn`, `.hg`
- `.idea`, `.vscode`, `.vs`
- `.cache`, `tmp`, `temp`

## For Agent Developers

When building extraction agents, use the filtering utilities:

1. **Reference the helper script**: `${CLAUDE_PLUGIN_ROOT}/tools/should_analyze.py`
2. **Apply decision rules**: Skip files containing `node_modules`, `dist`, `test`, etc.
3. **Use path parameters**: When using Grep, specify paths like `src/` to avoid excluded dirs
4. **Trust the system**: The change detection tool already applies filters, so delta extractions receive pre-filtered file lists

## Maintenance

To add new exclusion patterns:

1. Edit `EXCLUDE_DIRS` or `TEST_PATTERNS` in `file_filters.py`
2. All tools automatically inherit the new rules
3. No changes needed to individual tools or agents

This ensures consistency across the entire Fellow system.
