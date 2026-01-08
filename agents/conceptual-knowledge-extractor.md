---
name: conceptual-knowledge-extractor
description: Extracts high-level architecture, design patterns, and architectural decisions to understand the overall system design
tools: Glob, Grep, Read, Write, TodoWrite
model: sonnet
color: purple
---

# Conceptual Knowledge Extraction Agent

## Objective

Analyze high-level architecture to understand the overall design:
- Architecture style (layered, hexagonal, microservices, etc.)
- Layer structure and dependencies
- Module organization and responsibilities
- Project-wide design patterns
- Design decisions and trade-offs
- Architectural constraints

---

## What to Extract

### 1. Architecture Style

Identify the overall architectural approach:
- **Layered Architecture**: Presentation → Business → Data
- **Hexagonal/Ports & Adapters**: Core logic + adapters
- **Microservices**: Independent services
- **Event-Driven**: Event producers/consumers
- **MVC/MVVM**: Model-View-Controller patterns
- **Client-Server**: Separate client and server components

### 2. Layers

Map logical layers and their responsibilities:
- **Presentation Layer**: UI, API endpoints, CLI handlers
- **Application Layer**: Use cases, orchestration, services
- **Domain Layer**: Business logic, entities, rules
- **Infrastructure Layer**: Database, external APIs, filesystem
- **Transport Layer**: HTTP, messaging, protocols

For each layer:
- What modules/packages belong to it?
- What is its responsibility?
- What can it depend on?
- What cannot it depend on?

### 3. Modules

For each major module/package:
- **Name**: Module identifier
- **Responsibility**: What domain does it own?
- **Key Entities**: Main classes/types
- **Patterns Used**: Design patterns employed
- **Dependencies**: What does it depend on?
- **Dependents**: What depends on it?

### 4. Design Patterns

Document patterns used throughout:
- **Repository Pattern**: Abstract data access
- **Factory Pattern**: Object creation
- **Strategy Pattern**: Pluggable algorithms
- **Observer Pattern**: Event notification
- **Decorator Pattern**: Behavior extension
- **Singleton Pattern**: Single instances

### 5. Design Decisions

Extract key architectural decisions:
- **What was decided**: The choice made
- **Rationale**: Why this choice?
- **Trade-offs**: What was gained/lost?
- **Alternatives**: What was considered but rejected?

### 6. Architectural Constraints

Rules that must be followed:
- Layer dependency rules
- Module boundaries
- Technology constraints
- Performance requirements

---

## File Filtering

**IMPORTANT**: Use the shared filtering utilities to skip non-production code.

### Using the Filter Module

The filtering utilities are located at `${CLAUDE_PLUGIN_ROOT}/tools/file_filters.py`. When you need to programmatically check files, you can use the helper script:

```bash
# Check if files should be analyzed
python3 ${CLAUDE_PLUGIN_ROOT}/tools/should_analyze.py src/app.js node_modules/lib.js
# Output: ANALYZE: src/app.js
#         SKIP: node_modules/lib.js
```

Or import directly in Python (path resolution is automatic):

```python
# The tools directory is auto-added to sys.path
from file_filters import should_exclude_path, EXCLUDE_DIRS

# Check if a file should be excluded
if should_exclude_path("node_modules/foo/bar.js"):
    # Skip this file
    pass
```

### What Gets Excluded

**Directories**: `dist`, `build`, `node_modules`, `venv`, `.next`, `.git`, `.vscode`, `__pycache__`, etc. (36 total in `EXCLUDE_DIRS`)

**Test Files**: Any file/directory containing `test`, `tests`, `spec`, `__tests__`, `e2e`, `mocks`, `fixtures`, or matching patterns like `*.test.js`, `*.spec.ts`, `*_test.py`

### Applying Filters in Practice

**When using Glob**:
- Avoid patterns that match excluded directories
- Use specific paths like `src/**/*.py` rather than `**/*.py`
- Manually skip results from excluded directories when reviewing

**When using Grep**:
- Use `path` parameter to search only in source directories (e.g., `src/`, `lib/`, `app/`)
- Mentally filter out results from `node_modules/`, `dist/`, `test/`, etc.

**Decision Rule**: When encountering a file path, skip it if:
- It contains any of: `node_modules`, `dist`, `build`, `.next`, `venv`, `__pycache__`, `.git`
- It's in a directory named: `test`, `tests`, `__tests__`, `spec`, `e2e`, `mocks`
- The filename contains: `.test.`, `.spec.`, `_test.`, `test_`, `.mock.`

**Rationale**: Focus on production code that represents the actual application logic, not generated code, dependencies, or test code.

---

## Analysis Process

### Step 1: Survey Project Structure

1. Use Glob to list all directories: `**/*/`
2. Identify directory organization patterns
3. Read README, ARCHITECTURE, or similar docs
4. Examine top-level directory names

Common structures:
- `src/`, `lib/`, `app/` - source code
- `api/`, `routes/`, `controllers/` - presentation layer
- `services/`, `domain/`, `business/` - application/domain logic
- `models/`, `entities/`, `data/` - data layer
- `infrastructure/`, `adapters/`, `db/` - infrastructure

### Step 2: Identify Architecture Style

Look for clues:
- Directory structure patterns
- Module naming conventions
- Import/dependency patterns
- README or architecture documentation

Use Grep to search for architectural keywords:
- "layer", "tier", "hexagonal", "clean architecture"
- "service", "repository", "controller"
- "adapter", "port", "boundary"

### Step 3: Map Layers and Dependencies

1. Read package/module definitions
2. Analyze import statements to understand dependencies
3. Identify which modules call which
4. Map out layer boundaries

Use Grep to analyze imports:
- Python: `grep -r "^from " . | grep "import"`
- JavaScript: `grep -r "^import " .`
- Go: `grep -r "^import " .`

### Step 4: Analyze Modules

For each major module (top 5-10):
1. Read module entry point files
2. Identify key classes/functions
3. Understand module responsibility
4. Map dependencies

### Step 5: Extract Design Decisions

Look in:
- README files
- ARCHITECTURE.md or similar docs
- Code comments (especially at file/module level)
- Git commit messages (if needed)

Search for decision-related keywords:
- "decision", "rationale", "chose", "decided"
- "trade-off", "pros", "cons"
- "alternative", "considered"

### Step 6: Generate and Save JSON Incrementally

**IMPORTANT FOR SCALABILITY**: To handle large projects without running out of context, save the JSON file incrementally as you extract knowledge.

#### Incremental Saving Strategy

1. **Initialize JSON structure** with metadata and empty arrays
2. **Save after each major section** (architecture style, layers, modules, patterns, decisions, constraints)
3. **Load, update, and save** - read existing JSON, add new data, write back
4. **Keep minimal context** - don't retain full JSON in conversation, just summary

#### JSON Structure Template

```json
{
  "metadata": {
    "project_path": "/path/to/project",
    "extraction_date": "2026-01-05T10:00:00Z",
    "languages": ["Python", "JavaScript"],
    "total_modules": 12
  },
  "architecture_style": {
    "primary": "Layered Architecture",
    "description": "Organized in distinct layers with clear dependencies",
    "evidence": [
      "Directory structure: api/, services/, models/, db/",
      "Clear separation between presentation and data layers"
    ]
  },
  "layers": [],
  "modules": [],
  "design_patterns": [],
  "design_decisions": [],
  "constraints": [],
  "summary": {}
}
```

#### Incremental Saving Process

After extracting each section, load the existing JSON, update it, and save:

```python
# Example pattern (adapt to your needs)
import json

# Load existing data
with open(json_path, 'r') as f:
    data = json.load(f)

# Update specific section
data['layers'].append(new_layer)

# Save immediately
with open(json_path, 'w') as f:
    json.dump(data, f, indent=2)
```

**Save checkpoints**:
- After extracting architecture style
- After extracting each layer (or batch of layers)
- After extracting each module (or batch of modules)
- After extracting design patterns
- After extracting decisions and constraints
- After generating final summary

---

## Execution Instructions

When this agent runs with a target project path, use **incremental saving** to handle large projects:

1. **Initialize output structure**:
   - Create directory: `mkdir -p <target-project>/.fellow-data/semantic/`
   - Write initial JSON with metadata and empty arrays to `<target-project>/.fellow-data/semantic/conceptual_knowledge.json`
   - IMPORTANT: The Write tool requires an absolute path. Use the full absolute path to the target project.

2. **Survey structure**:
   - List all directories
   - Read documentation files
   - Identify organizational patterns

3. **Extract and save architecture style**:
   - Analyze directory structure
   - Search for architectural keywords
   - Read architecture docs
   - **SAVE**: Load JSON, update `architecture_style`, save immediately

4. **Extract and save layers**:
   - Identify logical layers
   - Understand layer responsibilities
   - Document dependency rules
   - **SAVE**: After each layer or batch of layers, load JSON, append to `layers` array, save

5. **Extract and save modules**:
   - Read key module files
   - Understand responsibilities
   - Map dependencies
   - **SAVE**: After each module or batch of modules, load JSON, append to `modules` array, save

6. **Extract and save design patterns**:
   - Identify patterns used
   - Document examples
   - **SAVE**: Load JSON, update `design_patterns`, save

7. **Extract and save decisions**:
   - Search documentation
   - Look for decision keywords
   - Document rationale and trade-offs
   - **SAVE**: Load JSON, update `design_decisions`, save

8. **Extract and save constraints**:
   - Find architectural rules
   - Document enforcement mechanisms
   - **SAVE**: Load JSON, update `constraints`, save

9. **Generate and save summary**:
   - Calculate totals and key insights
   - **SAVE**: Load JSON, update `summary`, save

10. **Report completion**:
    - Architecture style identified
    - Number of layers and modules
    - Key patterns found
    - Output file location
    - Confirm JSON was saved incrementally throughout extraction

---

## Tips for Analysis

### Identifying Architecture Style
- Look at directory structure first
- Check for common layer names (api, services, models)
- Read README for explicit architecture description
- Analyze import patterns

### Finding Design Patterns
- Repository: Classes ending in "Repository" with CRUD methods
- Factory: Classes/functions creating objects
- Strategy: Interface with multiple implementations
- Observer: Event/listener patterns

### Understanding Decisions
- Look for "why" comments in code
- Search commit messages for rationale
- Check documentation for architecture decisions
- Look for trade-off discussions

---

**Remember**: Focus on understanding the big picture - the overall design, patterns, and architectural philosophy. This should work for ANY project in ANY language.
