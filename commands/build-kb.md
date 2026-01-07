---
description: Build or update semantic knowledge base for a target project with support for incremental updates
argument-hint: [project-path] [--full|--update]
---

# Build Knowledge Base

Extract comprehensive semantic knowledge from a codebase to enable intelligent coding context, architectural guardrails, and constraint enforcement.

**Supports Incremental Updates**: Only re-analyzes changed files for fast updates during active development.

## Objective

Analyze a target project and extract three types of knowledge:
1. **Factual Knowledge** - What entities, models, and data structures exist
2. **Procedural Knowledge** - How workflows and execution flows work
3. **Conceptual Knowledge** - What the overall architecture and design patterns are

Store this knowledge in the target project's `.fellow-data/semantic/` directory for use by coding assistants.

---

## Arguments

- **Project Path** (optional): Path to target project
  - If empty: Use current working directory
  - If provided: Use specified path

- **Mode Flags** (optional):
  - `--full`: Force complete re-extraction (ignore existing KB)
  - `--update`: Force incremental update (default if KB exists)
  - No flag: Auto-detect (full if no KB, incremental if KB exists)

---

## Execution Modes

### Mode 1: Full Extraction (Initial Build)

When: No knowledge base exists OR `--full` flag used

**Time**: 2-5 minutes for medium project

**Process**: Analyzes entire codebase from scratch

### Mode 2: Incremental Update (Fast)

When: Knowledge base exists AND (no flag OR `--update` flag)

**Time**: 5-30 seconds for typical changes (1-10 files)

**Process**:
1. Detects changed files (via git or file modification time)
2. Re-extracts knowledge only for changed files
3. Merges with existing knowledge base
4. Updates metadata

---

## Core Principles

- **Incremental Updates**: Only analyze changed files for efficiency
- **Change Detection**: Use git diff or file modification times
- **Parallel Extraction**: Run all three extraction agents simultaneously for speed
- **No Modification**: Only read and analyze - never modify target project code
- **Comprehensive Coverage**: Extract enough knowledge to understand the project deeply
- **Machine Readable**: Output structured JSON for programmatic use
- **Human Readable**: Generate comprehensive markdown documentation for developers
- **Metadata Tracking**: Track extraction state for incremental updates

---

## Execution Workflow

### Phase 0: Mode Detection

**Goal**: Determine extraction mode (full vs incremental)

**Actions**:
1. Check if `.fellow-data/semantic/` exists
2. If exists, check for `extraction_metadata.json`
3. Parse flags: `--full` or `--update`
4. Determine mode:
   - **Full mode**: If no KB OR `--full` flag
   - **Incremental mode**: If KB exists AND (no flag OR `--update` flag)
5. Report mode to user:
   ```
   Mode: Incremental Update (3 files changed since last extraction)
   ```
   or
   ```
   Mode: Full Extraction (initial build)
   ```

---

### Phase 1: Setup and Validation

**Goal**: Determine target project path and validate it exists

**Actions**:
1. Create todo list tracking all phases
2. Determine target path:
   - If $ARGUMENTS is empty: Use current working directory (pwd)
   - If $ARGUMENTS provided: Use that path
3. **CRITICAL: Convert to absolute path** using `realpath` or Python's `os.path.abspath()`
   - Example: `realpath <target-path>` or `python3 -c "import os; print(os.path.abspath('<target-path>'))"`
   - Store this as `TARGET_ABSOLUTE_PATH` - this will be used in all agent prompts
4. Validate target path exists and is a directory
5. Create output directory: `mkdir -p ${TARGET_ABSOLUTE_PATH}/.fellow-data/semantic/`
6. Report target path and mode to user

**Important**: The `TARGET_ABSOLUTE_PATH` variable must be used in all subsequent phases when launching agents or writing files. Never use relative paths.

---

### Phase 1.5: Change Detection (Incremental Mode Only)

**Goal**: Identify files that changed since last extraction

**CRITICAL**: This is an EXECUTABLE phase. You MUST run the change detection tool, not execute git commands manually.

**Actions**:

Run the change detection tool:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/detect_changes.py <target-path>
```

**What the tool does**:
1. Loads extraction metadata from `.fellow-data/semantic/extraction_metadata.json`
2. Detects changes using git (preferred) or file comparison (fallback)
3. Categorizes files as modified, new, or deleted
4. Filters to only source code files
5. Reports changes or confirms KB is up-to-date

**Expected Output (Changes Detected)**:

```
🔍 Detecting changes using git...

📋 Files Changed Since Last Extraction:

  📝 Modified (2 files):
     • src/services/auth.py
     • src/api/routes.py

  ✨ New (1 files):
     • src/services/notification.py

  🗑️  Deleted (1 files):
     • src/utils/deprecated.py

📊 Total: 4 files to re-analyze
🔍 Detection method: git

📄 JSON Output:
{
  "status": "success",
  "mode": "incremental",
  "modified": ["src/services/auth.py", "src/api/routes.py"],
  "new": ["src/services/notification.py"],
  "deleted": ["src/utils/deprecated.py"],
  "total": 4,
  "detection_method": "git"
}
```

**Expected Output (No Changes)**:

```
✅ Knowledge base is up-to-date

   No files changed since last extraction
   Detection method: git

💡 Tip: Make code changes and run /fellow:build-kb again to update
```

**Important**:
- Replace `<target-path>` with the absolute path to the target project
- The tool automatically chooses between git and file comparison
- Parse the JSON output to get the list of changed files for extraction
- If `mode` is `"up_to_date"`, skip extraction and exit early
- Do NOT execute git commands manually

---

### Phase 2: Semantic Knowledge Extraction

**Goal**: Extract all three types of knowledge (full or incremental based on mode)

**CRITICAL REQUIREMENTS**:
1. Launch all three agents in parallel for maximum efficiency
2. **MUST use the absolute path** (`TARGET_ABSOLUTE_PATH` from Phase 1) in all agent prompts
3. Never use relative paths or placeholders like `<target-path>` in agent prompts
4. The agents MUST receive the actual absolute path (e.g., `/Users/jingnan.zhou/workspace/my-project`) not placeholders

**Example**: If the target project is at `/Users/jingnan.zhou/workspace/my-project`, the agent prompt should contain:
- ✅ CORRECT: "Extract factual knowledge from the project at /Users/jingnan.zhou/workspace/my-project. ... Save results to /Users/jingnan.zhou/workspace/my-project/.fellow-data/semantic/factual_knowledge.json"
- ❌ WRONG: "Extract factual knowledge from the project at <target-path>. ... Save results to <target-path>/.fellow-data/semantic/factual_knowledge.json"

#### Mode A: Full Extraction

**When**: No existing KB OR `--full` flag

**Actions**:
1. **CRITICAL**: Use the `TARGET_ABSOLUTE_PATH` from Phase 1 in all agent prompts below. Replace the placeholder `<target-path>` with the actual absolute path.

2. Launch three extraction agents simultaneously:

   **Agent 1: factual-knowledge-extractor**
   - Prompt: "Extract factual knowledge from the project at ${TARGET_ABSOLUTE_PATH}. Identify all significant entities, classes, data structures, and their relationships. Focus on the top 10-20 most important domain and technical entities. Save results to ${TARGET_ABSOLUTE_PATH}/.fellow-data/semantic/factual_knowledge.json using the Write tool with the full absolute path."

   **Agent 2: procedural-knowledge-extractor**
   - Prompt: "Extract procedural knowledge from the project at ${TARGET_ABSOLUTE_PATH}. Identify key workflows, execution flows, and call sequences. Focus on the 5-10 most important workflows (request handlers, background jobs, data pipelines). Save results to ${TARGET_ABSOLUTE_PATH}/.fellow-data/semantic/procedural_knowledge.json using the Write tool with the full absolute path."

   **Agent 3: conceptual-knowledge-extractor**
   - Prompt: "Extract conceptual knowledge from the project at ${TARGET_ABSOLUTE_PATH}. Identify the architecture style, layers, modules, design patterns, and architectural decisions. Save results to ${TARGET_ABSOLUTE_PATH}/.fellow-data/semantic/conceptual_knowledge.json using the Write tool with the full absolute path."

3. Wait for all three agents to complete
4. Verify all three JSON files were created successfully by checking if they exist:
   - `${TARGET_ABSOLUTE_PATH}/.fellow-data/semantic/factual_knowledge.json`
   - `${TARGET_ABSOLUTE_PATH}/.fellow-data/semantic/procedural_knowledge.json`
   - `${TARGET_ABSOLUTE_PATH}/.fellow-data/semantic/conceptual_knowledge.json`

#### Mode B: Incremental Extraction

**When**: KB exists AND (no flag OR `--update` flag) AND files changed

**Actions**:
1. **CRITICAL**: Use the `TARGET_ABSOLUTE_PATH` from Phase 1 in all agent prompts below. Replace the placeholder `<target-path>` with the actual absolute path.

2. Launch three extraction agents with file-specific prompts:

   **Agent 1: factual-knowledge-extractor (targeted)**
   - Prompt: "Extract factual knowledge from these CHANGED files in ${TARGET_ABSOLUTE_PATH}: [list of changed files]. Identify entities, classes, data structures and their relationships ONLY in these files. Save results to ${TARGET_ABSOLUTE_PATH}/.fellow-data/semantic/factual_knowledge_delta.json using the Write tool with the full absolute path."
   - Note: Output is temporary delta file

   **Agent 2: procedural-knowledge-extractor (targeted)**
   - Prompt: "Extract procedural knowledge from these CHANGED files in ${TARGET_ABSOLUTE_PATH}: [list of changed files]. Identify workflows that START or are SIGNIFICANTLY AFFECTED by functions in these files. Save results to ${TARGET_ABSOLUTE_PATH}/.fellow-data/semantic/procedural_knowledge_delta.json using the Write tool with the full absolute path."
   - Note: Output is temporary delta file

   **Agent 3: conceptual-knowledge-extractor (light analysis)**
   - Prompt: "Analyze architectural changes in ${TARGET_ABSOLUTE_PATH} considering these CHANGED files: [list of changed files]. If architectural patterns or layers changed, extract full conceptual knowledge. Otherwise, skip. Save results to ${TARGET_ABSOLUTE_PATH}/.fellow-data/semantic/conceptual_knowledge_delta.json using the Write tool with the full absolute path."
   - Note: May skip if no architectural changes

3. Wait for all agents to complete
4. Verify delta files were created successfully by checking if they exist

**Delta Files** (Temporary):
- `factual_knowledge_delta.json` - Entities from changed files only
- `procedural_knowledge_delta.json` - Workflows from changed files only
- `conceptual_knowledge_delta.json` - Architectural updates (if any)

---

### Phase 2.5: Knowledge Base Merge (Incremental Mode Only)

**Goal**: Merge extracted delta knowledge with existing knowledge base

**CRITICAL**: This is an EXECUTABLE phase. You MUST run the merge tool, not display implementation details.

**Actions**:

Run the knowledge merge tool:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/tools/merge_knowledge.py <target-path>
```

**What the tool does**:
1. Loads existing knowledge base and delta files
2. Merges factual knowledge (removes entities from changed files, adds new entities)
3. Merges procedural knowledge (updates workflows affected by changed files)
4. Merges conceptual knowledge (applies architectural changes if detected)
5. Writes merged knowledge base files
6. Cleans up delta files
7. Reports merge statistics

**Expected Output**:

```
📦 Loading existing knowledge base...
📦 Loading delta knowledge...
🔄 Merging knowledge for 3 changed files...
💾 Writing merged knowledge base...
🧹 Cleaning up delta files...

✅ Knowledge Base Updated (Incremental)

📊 Merge Statistics:

  Factual Knowledge:
    • Entities removed: 3 (from changed files)
    • Entities added: 5 (new extraction)
    • Relationships updated: 8

  Procedural Knowledge:
    • Workflows updated: 2
    • Workflows added: 1

  Conceptual Knowledge:
    • Status: No architectural changes

📁 Knowledge base location: /path/to/project/.fellow-data/semantic/
```

**Important**:
- Replace `<target-path>` with the absolute path to the target project
- The tool reads changed files from `extraction_metadata.json`
- Delta files are automatically cleaned up after merge
- Do NOT display the tool's source code or implementation details

---

### Phase 3: Validation and Summary Statistics

**Goal**: Ensure extraction succeeded and gather statistics

**Actions**:
1. Check that all three JSON files exist:
   - `<target-path>/.fellow-data/semantic/factual_knowledge.json`
   - `<target-path>/.fellow-data/semantic/procedural_knowledge.json`
   - `<target-path>/.fellow-data/semantic/conceptual_knowledge.json`

2. Read each file and extract summary statistics:
   - Factual: Number of entities extracted
   - Procedural: Number of workflows extracted
   - Conceptual: Architecture style identified

---

### Phase 4: Generate Human-Readable Summary

**Goal**: Create comprehensive markdown documentation for human readers

**Actions**:
1. Read all three JSON files:
   - factual_knowledge.json
   - procedural_knowledge.json
   - conceptual_knowledge.json

2. Generate comprehensive markdown summary including:
   - **Project Overview**: Core capabilities, technology stack, purpose
   - **Architecture Evolution**: Transformation story with metrics
   - **System Architecture**: Layered architecture with component descriptions
   - **Core Entities**: Key entities with purposes and patterns (from factual knowledge)
   - **Key Workflows**: Complete workflows with step-by-step flows (from procedural knowledge)
   - **Design Patterns**: Patterns used with benefits and trade-offs (from conceptual knowledge)
   - **Design Decisions**: Major decisions with rationale and alternatives (from conceptual knowledge)
   - **Architectural Constraints**: Constraints organized by category (from conceptual knowledge)
   - **Key Metrics**: Code quality, refactoring impact, performance metrics

3. Write to `<target-path>/.fellow-data/semantic/SEMANTIC_KNOWLEDGE_SUMMARY.md`

---

### Phase 5: Metadata Tracking

**Goal**: Track extraction state for future incremental updates

**Actions**:

1. **Collect File Information**:
   ```python
   # For each source file analyzed
   file_registry = {}
   for file_path in analyzed_files:
       file_registry[file_path] = {
           "last_analyzed": current_timestamp(),
           "hash": calculate_sha256(file_path),
           "size": get_file_size(file_path),
           "entities_extracted": get_entities_from_file(file_path),
           "workflows_extracted": get_workflows_from_file(file_path),
           "status": "analyzed"
       }
   ```

2. **Collect Git Information** (if available):

   Run the git info tool:

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/tools/git_info.py <target-path>
   ```

   This collects:
   - Current commit hash
   - Current branch name
   - Uncommitted changes status
   - Parse the JSON output for inclusion in metadata

3. **Create Metadata Structure**:
   ```json
   {
     "version": "2.0.0",
     "project_path": "/absolute/path/to/project",
     "last_full_extraction": "2026-01-05T10:00:00Z",
     "last_update": "2026-01-05T10:00:00Z",
     "extraction_method": "full",
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
         "entities_extracted": ["MainClass"],
         "workflows_extracted": ["startup"],
         "status": "analyzed"
       }
     },
     "statistics": {
       "total_files_analyzed": 25,
       "total_entities": 45,
       "total_workflows": 12,
       "extraction_duration_seconds": 180
     }
   }
   ```

4. **Write Metadata File**:
   - Save to `<target-path>/.fellow-data/semantic/extraction_metadata.json`

5. **Update on Incremental**:
   ```python
   # For incremental updates
   metadata["last_update"] = current_timestamp()
   metadata["extraction_method"] = "incremental"
   metadata["git_info"]["commit_hash"] = new_commit_hash

   # Update file registry for changed files
   for changed_file in changed_files:
       metadata["file_registry"][changed_file] = {
           "last_analyzed": current_timestamp(),
           "hash": new_hash,
           ...
       }

   # Update statistics
   metadata["statistics"]["files_changed_since_last_update"] = len(changed_files)
   metadata["statistics"]["entities_added"] = entities_added
   metadata["statistics"]["entities_removed"] = entities_removed
   ```

---

### Phase 6: Report Completion

**Goal**: Inform user of successful extraction

**For Full Extraction**:
```
✓ Knowledge base built successfully!

Mode: Full Extraction
Target Project: /path/to/project

Extracted Knowledge:
- Factual: 45 entities, 67 relationships
- Procedural: 12 workflows, 8 patterns
- Conceptual: 4 layers, 9 modules, 10 design patterns

Output Location: /path/to/project/.fellow-data/semantic/

Files Created:
- factual_knowledge.json (machine-readable entities)
- procedural_knowledge.json (machine-readable workflows)
- conceptual_knowledge.json (machine-readable architecture)
- SEMANTIC_KNOWLEDGE_SUMMARY.md (human-readable comprehensive summary)
- extraction_metadata.json (tracks extraction state)

Time: 3 minutes 15 seconds
Next: Use `/build-kb` to update after code changes (incremental)
```

**For Incremental Update**:
```
✓ Knowledge base updated successfully!

Mode: Incremental Update
Target Project: /path/to/project

Files Changed: 4 files
- Modified: src/services/auth.py, src/api/routes.py
- New: src/services/notification.py
- Deleted: src/utils/deprecated.py

Knowledge Updates:
- Factual: 3 entities removed, 5 entities added, 8 relationships updated
- Procedural: 2 workflows updated, 1 workflow added
- Conceptual: No architectural changes

Output Location: /path/to/project/.fellow-data/semantic/

Files Updated:
- factual_knowledge.json (updated)
- procedural_knowledge.json (updated)
- conceptual_knowledge.json (unchanged)
- SEMANTIC_KNOWLEDGE_SUMMARY.md (regenerated)
- extraction_metadata.json (updated)

Time: 15 seconds (12x faster than full extraction)
Tip: Use `/build-kb --full` to force complete re-extraction if needed
```

**For No Changes**:
```
✓ Knowledge base is up-to-date

Mode: Incremental Update Check
Target Project: /path/to/project

No files changed since last extraction
Last extracted: 2026-01-05T10:00:00Z (2 hours ago)

Knowledge base location: /path/to/project/.fellow-data/semantic/

Tip: Make code changes and run `/build-kb` again to update
```

Mark all todos complete.

---

### Phase 7: Update .gitignore

**Goal**: Ensure `.fellow-data/` is excluded from git

**Actions**:

1. Check if target project is a git repository:
   ```bash
   cd <target-path>
   if [ -d .git ]; then
     # It's a git repo
   fi
   ```

2. If git repository, ensure `.fellow-data/` is in `.gitignore`:
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/hooks/gitignore_helper.py <target-path>
   ```

3. The helper script will:
   - Check if `.gitignore` exists
   - Check if `.fellow-data/` is already present
   - If not present, add it with a comment
   - If `.gitignore` doesn't exist, create it

**Output**:
```
✓ Added .fellow-data/ to .gitignore
```

Or:
```
ℹ️  .fellow-data/ already in .gitignore
```

Or:
```
ℹ️  Not a git repository - skipping .gitignore update
```

**Rationale**:
- `.fellow-data/` contains generated files (knowledge base, logs)
- These files are project-specific and large
- Should not be committed to version control
- Each developer should generate their own KB locally
- Logs are for debugging and should not be shared

**Note**: This is a courtesy feature. If the script fails, don't block the build-kb command.

---

## Error Handling

If any agent fails:
1. Report which agent failed
2. Check if partial output was created
3. Suggest re-running or investigating the error
4. Do NOT proceed if critical knowledge is missing

---

## Usage Examples

### Initial Build

```bash
# Build KB for current project (first time - full extraction)
/build-kb

# Build KB for specific project
/build-kb /path/to/other/project

# Build KB for relative path
/build-kb ../my-project
```

### Incremental Updates

```bash
# After making code changes (auto-detects incremental mode)
/build-kb

# Explicitly request incremental update
/build-kb --update

# Force full rebuild even if KB exists
/build-kb --full
```

### Typical Development Workflow

```bash
# Day 1: Initial setup
cd /path/to/my-project
/build-kb
# Output: Full extraction (3 minutes)

# Day 2: After changing 3 files
/build-kb
# Output: Incremental update (15 seconds)
# - Detected 3 changed files
# - Updated entities and workflows

# Week 2: After major refactoring
/build-kb --full
# Output: Full re-extraction (3 minutes)
# - Ensures KB is fully consistent
```

### Team Collaboration

```bash
# Team member A: Makes changes and updates KB
git pull
# ... make changes to code ...
/build-kb  # Incremental update
git add .fellow-data/semantic/
git commit -m "feat: Add notification service + update KB"
git push

# Team member B: Pulls changes
git pull
# KB is already up-to-date!
# Can immediately use /fellow command
```

---

## Notes

### Performance

- **Full Extraction**: 2-5 minutes for medium project (10K-50K LOC)
  - Analyzes entire codebase
  - All three agents run in parallel

- **Incremental Update**: 5-30 seconds for typical changes (1-10 files)
  - Only analyzes changed files
  - 10-20x faster than full extraction
  - Merges with existing knowledge base

### Output Files

Generates 5 files in `.fellow-data/semantic/`:
- `factual_knowledge.json` - Machine-readable entities (Step 2 of Fellow plugin)
- `procedural_knowledge.json` - Machine-readable workflows (Step 2 of Fellow plugin)
- `conceptual_knowledge.json` - Machine-readable architecture (Step 2 of Fellow plugin)
- `SEMANTIC_KNOWLEDGE_SUMMARY.md` - Human-readable documentation
- `extraction_metadata.json` - Tracks extraction state for incremental updates ⭐ NEW

### Incremental Update Benefits

- **Speed**: Update in seconds instead of minutes
- **Efficiency**: Only re-analyze what changed
- **Automatic**: Detects changes via git or file modification times
- **Safe**: Merges carefully to maintain consistency
- **Smart**: Skips extraction if no files changed

### Best Practices

1. **Initial Build**: Always run full extraction first: `/build-kb`
2. **Regular Updates**: Run `/build-kb` after code changes (auto-incremental)
3. **Commit KB**: Check in `.fellow-data/semantic/` to git for team sharing
4. **Periodic Full Rebuild**: Monthly or after major refactoring: `/build-kb --full`
5. **CI/CD Integration**: Auto-update KB on main branch commits

### When to Use Full vs Incremental

**Use Full Extraction** (`--full`):
- Initial KB creation
- After major refactoring or restructuring
- When renaming many files or moving code
- Monthly maintenance (ensure consistency)
- When metadata is corrupted

**Use Incremental Update** (default):
- Regular development (most common)
- After changing a few files
- Quick context updates
- Active development sessions

### Limitations

- **Git Required** (Optional): Incremental updates work best with git for precise change detection
- **Without Git**: Falls back to file modification times (still works)
- **Architectural Changes**: May trigger broader re-analysis
- **File Renames**: Detected in git, treated as delete+add otherwise

### Troubleshooting

**KB seems out of sync**:
```bash
/build-kb --full  # Force complete rebuild
```

**Metadata corrupted**:
```bash
rm .fellow-data/semantic/extraction_metadata.json
/build-kb  # Will do full extraction
```

**Incremental taking too long**:
```bash
# If many files changed, consider full rebuild
/build-kb --full
```

### Safety

- **Read-Only**: Never modifies target project code
- **Non-Invasive**: Only analyzes and extracts knowledge
- **Safe to Re-run**: Can run multiple times without issues
- **Separate Storage**: KB stored in `.fellow-data/` (easy to gitignore or commit)

### Target Projects

- **Plugin Directory**: The fellow plugin itself is separate
- **Target Projects**: Any project you want to analyze
- **Multiple Projects**: Can analyze different projects from same plugin
