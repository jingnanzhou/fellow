# Incremental Knowledge Base Updates

## Overview

Fellow supports incremental updates to the knowledge base, allowing you to efficiently update only the changed parts of your codebase instead of re-analyzing everything.

## How It Works

### Initial Build (Full Extraction)

```bash
/build-kb
```

Creates:
- `.fellow-data/semantic/factual_knowledge.json`
- `.fellow-data/semantic/procedural_knowledge.json`
- `.fellow-data/semantic/conceptual_knowledge.json`
- `.fellow-data/semantic/SEMANTIC_KNOWLEDGE_SUMMARY.md`
- `.fellow-data/semantic/extraction_metadata.json` (tracks extraction state)

### Incremental Update

```bash
/build-kb --update
# or simply
/build-kb
```

If knowledge base already exists, automatically performs incremental update:
1. Detects changed files (via git or file modification time)
2. Re-extracts knowledge only for changed files
3. Merges new knowledge with existing knowledge base
4. Updates metadata and summary

### Force Full Rebuild

```bash
/build-kb --full
```

Forces complete re-extraction even if knowledge base exists.

## Extraction Metadata Format

**File**: `.fellow-data/semantic/extraction_metadata.json`

```json
{
  "version": "2.0.0",
  "project_path": "/path/to/project",
  "last_full_extraction": "2026-01-05T10:00:00Z",
  "last_update": "2026-01-05T15:30:00Z",
  "extraction_method": "incremental",
  "git_info": {
    "commit_hash": "abc123def456",
    "branch": "main",
    "has_uncommitted_changes": false
  },
  "file_registry": {
    "src/main.py": {
      "last_analyzed": "2026-01-05T10:00:00Z",
      "hash": "sha256:abc123...",
      "size": 1234,
      "entities_extracted": ["MainClass", "ConfigLoader"],
      "workflows_extracted": ["startup_workflow"],
      "status": "analyzed"
    },
    "src/services/auth.py": {
      "last_analyzed": "2026-01-05T15:30:00Z",
      "hash": "sha256:def456...",
      "size": 2345,
      "entities_extracted": ["AuthService", "TokenValidator"],
      "workflows_extracted": ["authentication_flow"],
      "status": "analyzed"
    }
  },
  "statistics": {
    "total_files_analyzed": 25,
    "total_entities": 45,
    "total_workflows": 12,
    "last_update_duration_seconds": 15,
    "files_changed_since_last_update": 3
  }
}
```

## Change Detection Strategies

### 1. Git-Based (Preferred)

If project is a git repository:

```bash
# Detect changed files since last extraction
git diff --name-only <last_commit_hash> HEAD

# Detect uncommitted changes
git diff --name-only
git ls-files --others --exclude-standard
```

**Advantages**:
- Precise change tracking
- Handles renames and moves
- Integrates with version control
- Tracks deletions

### 2. File Modification Time

If not a git repository:

```bash
# Compare file modification times with last_analyzed timestamp
find . -name "*.py" -newer .fellow-data/semantic/extraction_metadata.json
```

**Advantages**:
- Works without git
- Simple and reliable
- Fast detection

### 3. File Hash Comparison

Calculate SHA-256 hash and compare with stored hashes:

```python
import hashlib

def file_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
```

**Advantages**:
- Most accurate
- Detects content changes even if mtime unchanged
- Cross-platform

## Incremental Extraction Process

### Phase 1: Change Detection

1. **Load metadata**: Read `extraction_metadata.json`
2. **Detect changes**:
   - Use git if available: `git diff --name-only <commit>`
   - Fall back to file modification time
   - Calculate hashes if needed
3. **Categorize changes**:
   - **Modified files**: Re-extract knowledge
   - **New files**: Extract knowledge
   - **Deleted files**: Remove from knowledge base
   - **Renamed files**: Update references

### Phase 2: Targeted Extraction

**For Modified/New Files**:

1. **Factual Knowledge**:
   - Extract entities from changed files
   - Update relationships involving these entities
   - Remove old entities from these files
   - Add new entities

2. **Procedural Knowledge**:
   - Re-analyze workflows starting from changed files
   - Update affected workflows
   - Remove workflows that no longer exist

3. **Conceptual Knowledge**:
   - Typically requires full re-analysis (architecture overview)
   - Or: Only update if architectural changes detected

### Phase 3: Knowledge Base Merge

**Merge Strategy**:

```python
# Pseudo-code for merge logic

def merge_factual_knowledge(existing, new_extraction, changed_files):
    # Remove entities from changed files
    existing_entities = [
        e for e in existing["entities"]
        if e["grounding"]["file"] not in changed_files
    ]

    # Add newly extracted entities
    updated_entities = existing_entities + new_extraction["entities"]

    # Update relationships
    updated_relationships = update_relationships(
        existing["entity_relationships"],
        new_extraction["entity_relationships"],
        changed_files
    )

    return {
        "metadata": update_metadata(existing["metadata"]),
        "entities": updated_entities,
        "entity_relationships": updated_relationships,
        "summary": recalculate_summary(updated_entities)
    }
```

**Conflict Resolution**:
- **Entity name conflicts**: Use file path + line number as unique identifier
- **Relationship updates**: Remove old, add new
- **Metadata merging**: Keep historical info, update current stats

### Phase 4: Metadata Update

```json
{
  "last_update": "2026-01-05T15:30:00Z",
  "extraction_method": "incremental",
  "git_info": {
    "commit_hash": "new_commit_hash"
  },
  "file_registry": {
    // Update entries for changed files
    "src/services/auth.py": {
      "last_analyzed": "2026-01-05T15:30:00Z",
      "hash": "new_hash",
      "status": "analyzed"
    }
  },
  "statistics": {
    "files_changed_since_last_update": 3,
    "entities_added": 2,
    "entities_removed": 1,
    "entities_updated": 1,
    "workflows_updated": 1
  }
}
```

## Performance Comparison

### Full Extraction
- **Time**: 2-5 minutes for medium project (10K-50K LOC)
- **Analyzes**: All files
- **CPU Usage**: High
- **Use Case**: Initial build, major refactoring

### Incremental Update
- **Time**: 5-30 seconds for typical changes (1-10 files)
- **Analyzes**: Only changed files
- **CPU Usage**: Low
- **Use Case**: Regular development, minor changes

### Speedup Example

```
Project: 100 files, 20K LOC
Change: Modified 3 files (~300 LOC)

Full extraction: 180 seconds
Incremental update: 15 seconds
Speedup: 12x faster
```

## Usage Patterns

### Continuous Development

```bash
# Day 1: Initial extraction
/build-kb

# Day 2: After changing 5 files
/build-kb  # Auto-detects changes, incremental update (10 seconds)

# Day 3: After refactoring module
/build-kb  # Incremental (15 seconds)

# Week 2: Major restructuring
/build-kb --full  # Full rebuild (3 minutes)
```

### CI/CD Integration

```yaml
# .github/workflows/update-kb.yml
name: Update Knowledge Base

on:
  push:
    branches: [main]

jobs:
  update-kb:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0  # Full history for git-based detection

      - name: Update Knowledge Base
        run: |
          # Incremental update
          /build-kb

          # Commit changes if knowledge base updated
          git add .fellow-data/semantic/
          git commit -m "Update knowledge base [skip ci]"
          git push
```

### Team Workflow

```bash
# Team member A: Makes changes and updates KB
git pull
# ... make changes ...
/build-kb  # Incremental update
git add .fellow-data/semantic/
git commit -m "feat: Add user service + update KB"
git push

# Team member B: Pulls changes
git pull
# KB is already up-to-date from team member A
# Can immediately use /fellow command with current context
```

## Limitations

### When Incremental Updates May Not Suffice

1. **Major Refactoring**: Renaming entities, moving files
   - **Solution**: Force full rebuild with `--full`

2. **Relationship Changes**: When unchanged files now depend on changed files
   - **Solution**: Enhanced relationship tracking (future improvement)

3. **Architectural Changes**: Layer restructuring, pattern changes
   - **Solution**: Conceptual knowledge always does targeted re-analysis

4. **Git History Lost**: After rebasing, squashing commits
   - **Solution**: Fall back to hash-based detection

### Handling Edge Cases

**Deleted Files**:
```bash
# Detected by: git diff shows deletions
# Action: Remove entities with grounding to deleted files
# Update: Relationships involving deleted entities
```

**Renamed Files**:
```bash
# Detected by: git diff --find-renames
# Action: Update grounding locations
# Preserve: Entity knowledge (same content, new location)
```

**Moved Code Within File**:
```bash
# Detected by: File hash changed
# Action: Re-extract entire file
# Update: Line numbers in grounding
```

## Future Enhancements

### Smart Relationship Inference

Track entity usage across files:
```json
{
  "entity": "AuthService",
  "defined_in": "src/services/auth.py",
  "used_in": [
    "src/api/routes.py",
    "src/middleware/auth.py",
    "src/services/user.py"
  ]
}
```

When `AuthService` changes, re-analyze usage files too.

### Parallel Incremental Extraction

```bash
# Extract changed files in parallel
changed_files = detect_changes()
parallel_extract(changed_files, num_workers=4)
```

### Watch Mode (Future)

```bash
/build-kb --watch

# Continuously monitors file changes
# Auto-updates knowledge base in background
# Useful for active development
```

## Best Practices

1. **Commit KB to Git**: Track knowledge base evolution with code
2. **Regular Full Rebuilds**: Monthly or after major refactoring
3. **Use Git Tags**: Tag commits after full extraction for easy reference
4. **Review Incremental Changes**: Check what changed in KB after extraction
5. **CI/CD Integration**: Auto-update KB on main branch commits

## Troubleshooting

### KB Out of Sync

```bash
# Symptoms: /fellow command returns outdated context
# Solution: Force full rebuild
/build-kb --full
```

### Metadata Corrupted

```bash
# Symptoms: extraction_metadata.json invalid or missing
# Solution: Delete and rebuild
rm .fellow-data/semantic/extraction_metadata.json
/build-kb
```

### Large Incremental Updates

```bash
# If incremental update takes > 1 minute
# Consider forcing full rebuild for consistency
/build-kb --full
```

## Conclusion

Incremental updates make Fellow practical for active development by reducing update time from minutes to seconds. The knowledge base stays synchronized with your code without the overhead of full re-extraction.
