<div align="center">

# Fellow - Architectural Guardrails for Claude Code

**Enrich Claude Code requests to prevent architectural drift and enforce codebase consistency. Claude Code plugin that works in both the CLI and VS Code extension.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-purple.svg)](https://claude.com/code)

[Quick Start](#quick-start) · [Installation](#installation) · [Documentation](https://jingnanzhou.github.io/fellow/) · [Contributing](CONTRIBUTING.md)

</div>

---

## Overview

Fellow helps Claude understand your codebase by extracting three types of knowledge:

1. **Factual Knowledge** - What entities, models, and data structures exist
2. **Procedural Knowledge** - How workflows and execution flows work
3. **Conceptual Knowledge** - What the overall architecture and design patterns are

This knowledge enables intelligent coding assistance with:
- Context-aware code suggestions
- Architectural boundary enforcement
- Constraint checking
- Pattern-consistent implementations

## Installation

```bash
# Step 1: Add as local marketplace
claude plugin marketplace add https://github.com/jingnanzhou/fellow.git

# Step 2: Install from local marketplace
claude plugin install fellow@local_marketplace

# Step 3: Verify installation
claude plugin list
```

**Works in both CLI and VS Code!** Fellow automatically works with the Claude Code VS Code extension.

### Removing the Plugin

To uninstall Fellow:

```bash
# Step 1: Uninstall the plugin
claude plugin uninstall fellow@local_marketplace

# Step 2: Remove the marketplace
claude plugin marketplace remove local_marketplace
```

**See [INSTALLATION.md](INSTALLATION.md) for comprehensive installation guide.**

### Requirements

- **Claude Code CLI or VS Code Extension** - Fellow works with both!
- **Python 3.8+** - For knowledge extraction (standard library only, no packages required)
- **Git** - Optional, for cloning from source

### VS Code Users

Fellow works seamlessly with the Claude Code VS Code extension:

1. Install Claude Code extension in VS Code
2. Install Fellow: `/plugin install fellow`
3. All Fellow features work identically with visual benefits!

See [VS Code Integration Guide](docs-site/vscode.md) for details.

### Quick Reference

After installation:
- **Commands Available:** `/build-kb`, `/fellow`, `/toggle-hooks`
- **Hooks Status:** Use `/toggle-hooks status` to check
- **Cheat Sheet:** See [docs/CHEAT_SHEET.md](docs/CHEAT_SHEET.md) for all commands

## Quick Start

```bash
# Option 1: Build knowledge base first (recommended)
/build-kb

# Option 2: Start coding immediately (auto-build)
# Fellow will offer to build KB automatically when needed!
"Add authentication to the user endpoint"

# Check if automatic enrichment is enabled (default: on)
/toggle-hooks status

# Start coding naturally - context is automatically enriched!
"Add validation to the registration form"

# Optional: Use manual enrichment with /fellow
/fellow Add caching to the API

# Optional: Update KB after code changes (incremental, fast)
/build-kb --update
```

**✨ New: Auto-Build Feature**

If you forget to build the knowledge base, Fellow will:
- Detect it's missing when you make a coding request
- Inform you it will take 2-5 minutes
- Offer to build it automatically
- Then proceed with your request!

No more confusing errors - Fellow guides you through the process.

**📖 New to Fellow?** Check out the [Cheat Sheet](docs/CHEAT_SHEET.md) for a quick reference guide!

## Usage

### Step 1: Build Knowledge Base

Extract semantic knowledge from a target project:

```bash
# Build KB for current project (default)
/build-kb

# Build KB for specific project
/build-kb /path/to/project

# Build KB for relative path
/build-kb ../my-project

# Force full re-extraction (ignore existing KB)
/build-kb --full

# Incremental update (only re-analyze changed files)
/build-kb --update
```

**What it does:**
- Launches three extraction agents in parallel
- Analyzes the target project comprehensively
- Creates `.fellow-data/semantic/` directory in target project
- Saves three JSON files (for machine consumption):
  - `factual_knowledge.json` - Entities and relationships
  - `procedural_knowledge.json` - Workflows and execution flows
  - `conceptual_knowledge.json` - Architecture and design patterns
- Generates comprehensive markdown summary (for human readers):
  - `SEMANTIC_KNOWLEDGE_SUMMARY.md` - Human-readable documentation
- Tracks file changes in `extraction_metadata.json` for incremental updates

**Modes:**
- **Full Extraction**: Analyzes entire codebase (2-5 minutes for typical projects)
- **Incremental Update**: Only re-analyzes changed files (10-20 seconds, 10-20x faster)
  - Detects changes via git diff, file hashes, or modification times
  - Merges new knowledge with existing KB
  - Perfect for active development workflows

**Time:**
- Full extraction: 2-5 minutes (first time or with `--full`)
- Incremental update: 10-20 seconds (subsequent updates)

### Step 2: Context-Enriched Coding

Fellow automatically enriches your coding requests with semantic knowledge from the knowledge base.

#### Automatic Mode (Default - via Hooks)

Once you've built a knowledge base with `/build-kb`, Fellow automatically intercepts coding requests and enriches them with context:

```bash
# Simply write your coding request naturally - no special command needed!
Add a POST endpoint for user registration

# Refactor existing code
Refactor the payment processing to use the Strategy pattern

# Add features with constraints
Add caching to the tool listing API with 60-second TTL

# Fix or enhance
Add validation to the user registration form
```

**How it works:**
- Hook automatically detects coding requests (keywords: add, create, implement, fix, etc.)
- Loads semantic knowledge from `.fellow-data/semantic/` in current directory or parent directories
- Enriches your request with:
  - Relevant entities (with locations and purposes)
  - Relevant workflows (existing patterns to follow)
  - Architectural guardrails (constraints that apply)
  - Architecture style and design patterns
- Passes enriched context to Claude transparently
- Non-coding requests pass through unchanged

**Hook Configuration:**
- Enabled by default via `.claude-plugin/hooks.json`
- Toggle on/off: Use `/toggle-hooks on|off|status`
- Confidence threshold: 0.7 (configurable)
- Silent mode: false (shows enriched context)
- See Hook Configuration section below for customization

#### Manual Mode (Optional - via /fellow command)

You can also explicitly use the `/fellow` command:

```bash
# Explicit context enrichment
/fellow Add a POST endpoint for user registration
```

This is useful when:
- You want to force context enrichment even for ambiguous requests
- The hook doesn't detect your request as a coding task
- You're testing the knowledge base

**Guardrails Applied:**
- Architecture boundaries (layer dependencies, module isolation)
- Design patterns (follow established patterns)
- Security constraints (auth, validation, sanitization)
- Performance constraints (caching, pooling, optimization)
- Consistency rules (naming, structure, error handling)

## Knowledge Base Structure

The knowledge base is stored in the target project at `.fellow-data/semantic/`:

### factual_knowledge.json
```json
{
  "metadata": { ... },
  "entities": [
    {
      "name": "User",
      "type": "class",
      "attributes": [...],
      "methods": [...],
      "relationships": [...],
      "grounding": { "file": "...", "line_start": 10, "line_end": 50 }
    }
  ],
  "entity_relationships": [...],
  "summary": { ... }
}
```

### procedural_knowledge.json
```json
{
  "metadata": { ... },
  "workflows": [
    {
      "name": "user_authentication",
      "type": "request_handler",
      "entry_point": { "function": "...", "file": "...", "line": 123 },
      "steps": [...],
      "data_flow": { ... },
      "control_flow": { ... }
    }
  ],
  "summary": { ... }
}
```

### conceptual_knowledge.json
```json
{
  "metadata": { ... },
  "architecture_style": { "primary": "Layered Architecture", ... },
  "layers": [...],
  "modules": [...],
  "design_patterns": [...],
  "design_decisions": [...],
  "constraints": [...]
}
```

### SEMANTIC_KNOWLEDGE_SUMMARY.md
Comprehensive human-readable documentation including:
- **Project Overview** - Core capabilities and technology stack
- **Architecture Evolution** - Transformation story with metrics
- **System Architecture** - Layered architecture with detailed descriptions
- **Core Entities** - Key entities with purposes and design patterns
- **Key Workflows** - Complete workflows with step-by-step flows
- **Design Patterns** - Patterns used with benefits and trade-offs
- **Design Decisions** - Major decisions with rationale and alternatives
- **Architectural Constraints** - Constraints organized by category
- **Key Metrics** - Code quality, performance, and pattern usage metrics

**Use Cases:**
- Onboarding new developers to the codebase
- Architecture reviews and documentation
- Understanding design decisions and trade-offs
- Quick reference for codebase structure

## Hook Configuration

Fellow uses Claude Code's hook system to automatically intercept and enrich coding requests.

### Default Configuration

The hook is defined in `.claude-plugin/hooks.json`:

```json
{
  "hooks": [
    {
      "name": "fellow-context-enrichment",
      "type": "user-prompt-submit",
      "description": "Automatically enriches coding requests with semantic knowledge",
      "enabled": true,
      "script": "./hooks/enrich-context.sh",
      "config": {
        "detect_coding_requests": true,
        "auto_load_kb": true,
        "silent_mode": false,
        "logging_enabled": true,
        "min_confidence": 0.7,
        "keywords": [
          "add", "create", "implement", "build", "write", "fix", "refactor",
          "update", "modify", "change", "enhance", "improve", "optimize",
          "delete", "remove", "test", "debug", "validate", "endpoint",
          "function", "class", "method", "service", "component", "module"
        ]
      }
    }
  ]
}
```

### Customization Options

**Enable/Disable Hook:**
```json
"enabled": false  // Disable automatic enrichment
```

**Adjust Detection Confidence:**
```json
"min_confidence": 0.5  // Lower = more aggressive detection (more false positives)
"min_confidence": 0.9  // Higher = conservative detection (may miss some requests)
```

**Silent Mode:**
```json
"silent_mode": true  // Hide enriched context, only apply guardrails
```

**Enable Logging:**
```json
"logging_enabled": true  // Log all enrichment events to .fellow-data/logs/
```

**Add Custom Keywords:**
```json
"keywords": [
  "add", "create", ...,
  "scaffold", "generate", "migrate"  // Add your own keywords
]
```

### Hook Behavior

**Detected as Coding Request (enriched):**
- "Add a new authentication endpoint"
- "Refactor the payment service to use Strategy pattern"
- "Fix the validation bug in user registration"
- "Implement caching for tool listing API"

**Not Detected (pass through):**
- "What is the architecture of this project?"
- "Show me the user authentication workflow"
- "How does the payment processing work?"
- "List all the design patterns used"

### Logging

Fellow can log all enrichment events for debugging and analysis.

**Log Location:**
- Project logs: `.fellow-data/logs/` (in target project directory)
- Fallback: `fellow/.fellow-data/logs/` (in Fellow plugin directory)

**Log Files Created:**
- `enrichment_YYYY-MM-DD.jsonl` - Machine-readable JSON logs (one line per event)
- `enrichment_YYYY-MM-DD.log` - Human-readable logs with full context

**Enabling Logging:**

Method 1: Edit `.claude-plugin/hooks.json`:
```json
{
  "hooks": [{
    "config": {
      "logging_enabled": true
    }
  }]
}
```

Method 2: Environment variable:
```bash
export FELLOW_LOGGING=1
```

**Log Contents:**

Each enrichment event logs:
- **Original prompt** - User's original coding request
- **Detection results** - Whether detected as coding request, intent, confidence
- **Knowledge base** - Whether KB found, path
- **Enrichment stats** - Number of entities, workflows, constraints found
- **Enriched prompt** - Full context that was added
- **Source** - Whether from hook or /fellow command
- **Timestamp** - When enrichment occurred

**Example Log Entry (Human-Readable):**
```
================================================================================
[2026-01-05 18:15:08] HOOK
================================================================================
Original Prompt (42 chars):
Add validation to the OAuth token endpoint

Detection:
  - Coding Request: True
  - Intent: create
  - Confidence: 1.00

Knowledge Base:
  - Found: True
  - Path: /path/to/project/.fellow-data/semantic

Enrichment:
  - Entities: 5
  - Workflows: 3
  - Constraints: 8
  - Enriched Length: 2743 chars

Enriched Prompt:
[full enriched context shown here]
```

**Use Cases:**
- Debug why certain entities/workflows were retrieved
- Analyze detection accuracy
- Understand what context is being added
- Track usage patterns
- Troubleshoot hook behavior

### Enabling/Disabling Hooks

**Using the Toggle Command (Recommended):**

```bash
# Check current status
/toggle-hooks status

# Disable automatic enrichment
/toggle-hooks off

# Re-enable automatic enrichment
/toggle-hooks on
```

**Manual Configuration:**

Alternatively, edit `.claude-plugin/hooks.json` directly:

```json
{
  "hooks": [
    {
      "name": "fellow-context-enrichment",
      "enabled": false,  // Change to true/false
      ...
    }
  ]
}
```

**When Disabled:**
- All requests pass through unchanged
- Use `/fellow` command for explicit enrichment when needed

## Architecture

### Plugin Components

**Commands** (`commands/`):
- `build-kb.md` - Orchestrates knowledge extraction with incremental updates (Step 1)
- `fellow.md` - Manual context-enriched coding (Step 2, optional)
- `toggle-hooks.md` - Enable/disable automatic context enrichment hooks

**Agents** (`agents/`):
- `factual-knowledge-extractor` - Extracts entities and models
- `procedural-knowledge-extractor` - Extracts workflows
- `conceptual-knowledge-extractor` - Extracts architecture

**Hooks** (`hooks/`):
- `enrich-context.sh` - Shell wrapper for hook execution
- `enrich-context.py` - Automatic coding request detection and enrichment

**Documentation** (`docs/`):
- `INCREMENTAL_UPDATES.md` - Incremental update feature documentation
- `CHEAT_SHEET.md` - Quick reference guide for all commands and features

### How It Works

**Step 1: Knowledge Base Extraction (`/build-kb`)**
1. **Command Invocation**: User runs `/build-kb [path] [--full|--update]`
2. **Path Resolution**: Determines target project (current dir or specified path)
3. **Mode Detection**: Decides between full extraction or incremental update
4. **Change Detection** (incremental only): Identifies modified files via git/hash/mtime
5. **Parallel Extraction**: Launches three agents simultaneously
6. **Knowledge Merge** (incremental only): Merges new knowledge with existing KB
7. **Knowledge Storage**: Saves JSON to `.fellow-data/semantic/`
8. **Metadata Tracking**: Updates `extraction_metadata.json` with file hashes
9. **Markdown Generation**: Creates comprehensive human-readable summary
10. **Summary**: Reports extraction statistics

**Step 2: Context-Enriched Coding (Automatic via Hooks)**
1. **Request Interception**: Hook intercepts user prompt before Claude processes it
2. **Coding Detection**: Analyzes prompt for coding keywords and intent
3. **Knowledge Base Discovery**: Searches upward for `.fellow-data/semantic/`
4. **Knowledge Loading**: Loads factual, procedural, and conceptual JSON files
5. **Relevance Scoring**: Scores entities and workflows by relevance to prompt
6. **Constraint Filtering**: Identifies applicable architectural constraints
7. **Context Enrichment**: Generates enriched prompt with entities, workflows, guardrails
8. **Transparent Execution**: Passes enriched prompt to Claude for processing
9. **Pass-Through**: Non-coding requests pass through unchanged

**Step 2: Context-Enriched Coding (Manual via `/fellow`)**
1. **Explicit Command**: User runs `/fellow <coding request>`
2. **Knowledge Loading**: Loads semantic KB from `.fellow-data/semantic/`
3. **Intent Analysis**: Analyzes the coding request (create, modify, fix, etc.)
4. **Knowledge Retrieval**: Finds relevant entities, workflows, patterns
5. **Constraint Extraction**: Identifies applicable architectural constraints
6. **Guardrail Generation**: Creates specific coding guardrails
7. **Task Execution**: Executes with full architectural awareness

### Design Principles

- **Non-Invasive**: Only reads code, never modifies it
- **Language Agnostic**: Works with any programming language
- **Parallel Processing**: Runs extractions concurrently for speed
- **Machine Readable**: Structured JSON output for programmatic use
- **Human Readable**: Comprehensive markdown documentation for developers
- **Grounded**: All knowledge linked to source code locations

## Roadmap

### ✅ Step 1: Knowledge Base Extraction (Complete)
- Build semantic knowledge base from any project
- Extract factual, procedural, and conceptual knowledge
- Store as structured JSON and human-readable markdown
- **Incremental updates** - Only re-analyze changed files (10-20x faster)
- File change tracking via git diff, hashes, or modification times
- Smart merge logic for updated knowledge

### ✅ Step 2: Automatic Context Enrichment (Complete)
- **Hook-based automatic enrichment** - No manual command needed
- Transparent coding request detection
- Automatic knowledge base discovery
- Relevance-based entity and workflow retrieval
- Constraint filtering by intent type
- Pass-through for non-coding requests
- Optional manual `/fellow` command for explicit enrichment

### 🚧 Step 3: Advanced Features (Future)
- Knowledge base querying (search entities, workflows, patterns)
- Cross-project knowledge sharing
- Custom constraint definitions
- Integration with external documentation systems
- Real-time knowledge synchronization
- Team collaboration features

## Examples

### Enabling/Disabling Automatic Enrichment

```bash
# Check if hooks are enabled
/toggle-hooks status
```

Output:
```
✅ Fellow hooks are ENABLED
   Coding requests will be automatically enriched with context

To disable: /toggle-hooks off
```

```bash
# Temporarily disable for testing
/toggle-hooks off
```

Output:
```
❌ Fellow hooks DISABLED
   Automatic enrichment is now off
   Use /fellow command for explicit enrichment when needed
```

```bash
# Re-enable when ready
/toggle-hooks on
```

Output:
```
✅ Fellow hooks ENABLED
   Coding requests will now be automatically enriched with context
```

### Building KB for a Python Project
```bash
cd /path/to/my-python-project
/build-kb
```

Output:
```
✓ Knowledge base built successfully!

Target Project: /path/to/my-python-project

Extracted Knowledge:
- Factual: 15 entities, 24 relationships
- Procedural: 8 workflows, 3 patterns
- Conceptual: 4 layers, 12 modules, 5 design patterns

Output Location: /path/to/my-python-project/.fellow-data/semantic/

Files Created:
- factual_knowledge.json (machine-readable entities)
- procedural_knowledge.json (machine-readable workflows)
- conceptual_knowledge.json (machine-readable architecture)
- SEMANTIC_KNOWLEDGE_SUMMARY.md (human-readable comprehensive summary)
```

### Building KB for a Different Project
```bash
# While working on project A, analyze project B
/build-kb /path/to/project-b
```

### Complete Workflow Example

**Scenario**: Working on an e-commerce project

```bash
# Step 1: Build knowledge base
cd /path/to/ecommerce-project
/build-kb
```

Output:
```
✓ Knowledge base built successfully!

Target Project: /path/to/ecommerce-project

Extracted Knowledge:
- Factual: 24 entities, 38 relationships
- Procedural: 12 workflows, 6 patterns
- Conceptual: 4 layers, 8 modules, 8 design patterns

Output Location: .fellow-data/semantic/
```

```bash
# Step 2: Use context-enriched coding
/fellow Add a POST endpoint for creating orders with items and payment info
```

Output:
```
📋 Context Loaded from Knowledge Base

Relevant Entities: 5 entities found
  - Order (core entity with relationships to User, OrderItem, Payment)
  - OrderService (service layer, handles order creation workflow)
  - PaymentProcessor (handles payment validation and processing)
  - ValidationService (input validation)
  - AuthService (authentication and authorization)

Relevant Workflows: 2 workflows found
  - Order creation workflow (existing pattern to follow)
  - Payment processing workflow (integration points)

Applicable Constraints: 6 constraints apply
  - Security: Authentication required for order creation
  - Validation: Order items must be validated against inventory
  - Performance: Use connection pooling for database operations
  - Architectural: API layer cannot directly access database
  - Data validation: Payment info must be validated and sanitized
  - Resource management: Transaction must be properly committed/rolled back

Key Guardrails:
- MUST authenticate user via AuthService before processing
- MUST validate order items using ValidationService
- MUST use OrderService (service layer) - do not access database directly
- MUST handle payment through PaymentProcessor
- MUST use transaction for order and payment (all-or-nothing)
- SHOULD follow existing API response format (Order entity structure)

[Proceeds with implementation following these guardrails...]
```

**Result**: The endpoint is implemented following existing patterns, respecting architectural boundaries, and maintaining consistency with the codebase.

## Documentation

### Documentation Site

**📚 Full documentation available at:** **https://jingnanzhou.github.io/fellow/**

The documentation site includes comprehensive guides for installation, usage, best practices, and more.

### Quick References

- **[Cheat Sheet](docs/CHEAT_SHEET.md)** - Quick reference for all commands, workflows, and troubleshooting
- **[Incremental Updates Guide](docs/INCREMENTAL_UPDATES.md)** - How incremental updates work and performance details
- **[Docs Quick Reference](DOCS-QUICK-REFERENCE.md)** - Quick commands for deploying documentation

### Core Documentation

- **[README.md](README.md)** - Complete overview and usage guide (this file)
- **[INSTALLATION.md](INSTALLATION.md)** - Complete installation guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[LICENSE](LICENSE)** - Apache 2.0 license

### For Documentation Contributors

- **[MkDocs Deployment Guide](MKDOCS-DEPLOYMENT-GUIDE.md)** - Complete guide for regenerating and publishing documentation
- **[Docs Quick Reference](DOCS-QUICK-REFERENCE.md)** - Quick commands for documentation workflow

### Command Documentation

Located in `commands/`:
- `build-kb.md` - Knowledge base extraction command (full + incremental)
- `fellow.md` - Manual context enrichment command
- `toggle-hooks.md` - Hook management command

### Agent Documentation

Located in `agents/`:
- `factual-knowledge-extractor.md` - Entity extraction agent
- `procedural-knowledge-extractor.md` - Workflow extraction agent
- `conceptual-knowledge-extractor.md` - Architecture extraction agent

## Contributing

Fellow is designed to be:
- **Extensible**: Add new extraction agents easily
- **Customizable**: Modify extraction logic per project needs
- **Composable**: Use extracted knowledge in various workflows

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

Created by Jingnan Zhou, 2026.

## Version History

**2.1.0** - Automatic enrichment, incremental updates, and logging (Current)
- **Hook-based automatic context enrichment** - No `/fellow` command needed
- Automatic coding request detection (keywords, entities, imperative mood)
- Transparent knowledge base discovery and loading
- Pass-through for non-coding requests
- **Incremental knowledge base updates** - 10-20x faster
- Change detection via git diff, file hashes, or modification times
- Smart merge logic for updated entities and workflows
- File registry tracking in `extraction_metadata.json`
- **Comprehensive logging system** - Logs all enrichment events
- Logs original prompts, enriched context, detection results, KB stats
- Both JSON and human-readable log formats
- Optional manual `/fellow` command for explicit enrichment
- `/toggle-hooks` command for easy enable/disable

**2.0.0** - Context-enriched coding
- Added `/fellow` command for context-enriched coding
- Intent analysis (create, modify, fix, validate, test, document)
- Knowledge retrieval from KB (entities, workflows, patterns)
- Constraint extraction and guardrail generation
- Architectural awareness during implementation

**1.0.0** - Knowledge base extraction
- Initial release with `/build-kb` command
- Parallel extraction of factual, procedural, and conceptual knowledge
- JSON output for machine consumption
- Markdown summary for human readers
