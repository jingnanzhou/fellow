# Quick Start Guide

**Fellow - Architectural Guardrails for Claude Code**

Get up and running with Fellow in 5 minutes. Fellow automatically enriches every Claude Code request to prevent architectural drift and enforce codebase consistency.

## Prerequisites

- Claude Code CLI installed
- A code project to analyze
- Python 3.8+ (for knowledge extraction)

## Step 1: Install Fellow

!!! warning "Fellow Not Yet Published"
    Fellow is not yet in the official marketplace. Use local installation for now.

**Clone and install Fellow:**

```bash
# Clone repository
git clone https://github.com/jingnanzhou/fellow.git
cd fellow

# Install from current directory
claude plugin add ./
```

**Verify installation:**

```bash
# Check Fellow is installed
claude plugin list

# You should see:
# ✓ fellow (v2.1.0) - Semantic knowledge extraction...
```

!!! tip "Alternative: Direct Git URL"
    You can also install directly: `claude plugin add https://github.com/jingnanzhou/fellow.git`

    Once published to the marketplace, installation will be simpler: `claude plugin add fellow`

## Step 2: Build Your First Knowledge Base

You have two options:

### Option A: Build Explicitly (Recommended)

```bash
# Go to your project directory
cd /path/to/your/project

# Build the knowledge base (first time: 2-5 minutes)
/build-kb
```

### Option B: Auto-Build on First Use

!!! tip "New: Auto-Build Feature"
    You can skip building the KB upfront! When you make your first coding request, Fellow will detect the missing KB and offer to build it automatically.

    ```
    You: "Add authentication to the endpoint"

    Fellow: ⚠️ Knowledge base not found. Build now (2-5 min)? (y/n)
    ```

    Just say "yes" and Fellow builds it for you!

### What Happens During Extraction

Fellow will:

1. **Analyze your codebase** - Scans all source files
2. **Extract entities** - Finds classes, functions, services, models
3. **Map workflows** - Traces execution flows and integration patterns
4. **Identify patterns** - Discovers your architectural patterns
5. **Capture constraints** - Extracts security, performance, and validation rules

### Output

After extraction completes, you'll see:

```
✓ Knowledge base built successfully!

Mode: Full Extraction
Target Project: /path/to/your-project

Extracted Knowledge:
- Factual: 45 entities, 67 relationships
- Procedural: 12 workflows, 8 patterns
- Conceptual: 4 layers, 9 modules, 10 design patterns

Output Location: /path/to/your-project/.fellow-data/semantic/

Files Created:
- factual_knowledge.json (machine-readable entities)
- procedural_knowledge.json (machine-readable workflows)
- conceptual_knowledge.json (machine-readable architecture)
- SEMANTIC_KNOWLEDGE_SUMMARY.md (human-readable comprehensive summary)
- extraction_metadata.json (tracks extraction state)

Time: 3 minutes 15 seconds
```

## Step 3: Verify Automatic Enrichment

Check if hooks are enabled (they are by default):

```bash
/toggle-hooks status
```

Expected output:

```
✅ Fellow hooks are ENABLED
   Coding requests will be automatically enriched with context

To disable: /toggle-hooks off
```

## Step 4: Try Your First Enriched Request

Just type a coding request naturally:

```
Add validation to the user registration endpoint
```

### What Fellow Does Automatically

1. **Detects coding intent** - Recognizes this as a code modification request
2. **Loads knowledge base** - Retrieves relevant knowledge from `.fellow-data/semantic/`
3. **Finds relevant entities** - Identifies UserModel, ValidationService, etc.
4. **Retrieves workflows** - Finds your existing registration workflow
5. **Applies constraints** - Loads security and validation rules
6. **Enriches context** - Prepends all this information to your request

### What You'll See

```
📋 **Context from Knowledge Base**

**Relevant Entities:**
- **UserModel** (class): User entity with validation rules
  Location: `src/models/user.py`
- **ValidationService** (class): Centralized validation logic
  Location: `src/services/validation.py`
- **RegistrationHandler** (class): Handles user registration workflow
  Location: `src/handlers/registration.py`

**Relevant Workflows:**
- **User Registration Flow**: Complete user registration with validation
  Entry: `src/handlers/registration.py`

**Architectural Guardrails (MUST follow):**
- [Security] Passwords must be hashed with bcrypt
- [Validation] Email format must match RFC 5322
- [Architecture] Use ValidationService for all input validation
- [Data] User emails must be unique (database constraint)

**Architecture Style:** Service-Oriented Architecture

---

**User Request:**
Add validation to the user registration endpoint
```

Claude Code now has full context about YOUR codebase and will suggest code that follows YOUR patterns!

## Step 5: Update Knowledge Base After Changes

After making code changes, update your knowledge base incrementally:

```bash
/build-kb --update
```

!!! success "Incremental Updates"
    Incremental updates are **10-20x faster** than full extraction:

    - **Full extraction**: 2-5 minutes
    - **Incremental update**: 10-20 seconds

    Fellow detects changed files and only re-extracts those files.

Expected output:

```
✓ Knowledge base updated successfully!

Mode: Incremental Update
Target Project: /path/to/your-project

Files Changed: 2 files
- Modified: src/models/user.py
- Modified: src/services/validation.py

Knowledge Updates:
- Factual: 2 entities updated
- Procedural: 1 workflow updated
- Conceptual: No architectural changes

Time: 12 seconds (15x faster than full extraction)
```

## Common First-Time Scenarios

### Scenario 1: Large Codebase

!!! info "First extraction takes longer for large codebases"
    - Small project (< 10K LOC): 1-2 minutes
    - Medium project (10-50K LOC): 2-3 minutes
    - Large project (50-200K LOC): 3-5 minutes
    - Very large (200K+ LOC): 5-10 minutes

    **This is a one-time cost**. Subsequent incremental updates take 10-20 seconds.

### Scenario 2: "Knowledge base not found"

If you try enriched coding without building the KB first:

```
❌ Knowledge base not found
Please run /build-kb first to extract semantic knowledge
```

**Solution**: Run `/build-kb` in your project directory.

### Scenario 3: Non-Coding Request

If you ask a question (not a coding request):

```
"What is the architecture of this project?"
```

Fellow recognizes this isn't a coding request and **passes through unchanged**. No enrichment is added.

### Scenario 4: Multiple Projects

Fellow automatically loads the correct knowledge base based on your current directory:

```bash
# Project A
cd /path/to/project-a
/build-kb
# Creates .fellow-data/ in project-a

# Project B
cd /path/to/project-b
/build-kb
# Creates .fellow-data/ in project-b

# Coding in Project A
cd /path/to/project-a
"Add feature X"  # Uses project-a knowledge base

# Coding in Project B
cd /path/to/project-b
"Add feature Y"  # Uses project-b knowledge base
```

## Troubleshooting

### Issue: "Hook not intercepting my requests"

**Check 1**: Verify hooks are enabled

```bash
/toggle-hooks status
```

**Check 2**: Is your request a coding request?

Fellow detects coding keywords like:
- add, create, implement, build
- update, modify, refactor
- fix, debug, resolve
- delete, remove

Questions like "What is..." or "Show me..." are not detected as coding requests.

**Solution**: Use `/fellow` command explicitly:

```bash
/fellow Add feature X
```

### Issue: "Knowledge base seems outdated"

**Solution**: Run incremental update:

```bash
/build-kb --update
```

Or force full rebuild:

```bash
/build-kb --full
```

### Issue: "Extraction is taking a long time"

This is normal for first extraction. Grab a coffee ☕

**Tips to speed up**:
- Exclude unnecessary directories (node_modules, vendor, etc.) - we detect these automatically
- Use incremental updates for subsequent extractions

## Next Steps

<div class="grid cards" markdown>

-   :material-school: **Learn All Commands**

    ---

    Explore all Fellow commands and options.

    [:octicons-arrow-right-24: User Guide](user-guide/commands/overview.md)

-   :material-cog: **Configure Hooks**

    ---

    Customize automatic enrichment behavior.

    [:octicons-arrow-right-24: Hook Configuration](user-guide/hooks/configuration.md)

-   :material-book-open: **Understand Output**

    ---

    Learn what each knowledge file contains.

    [:octicons-arrow-right-24: Knowledge Base Structure](user-guide/knowledge-base/structure.md)

-   :material-file-document: **Read Cheat Sheet**

    ---

    Quick reference for all commands and features.

    [:octicons-arrow-right-24: Cheat Sheet](reference/cheat-sheet.md)

</div>

## Best Practices for First-Time Users

1. **Start with a small project** - Test Fellow on a manageable codebase first
2. **Review the generated summary** - Check `.fellow-data/semantic/SEMANTIC_KNOWLEDGE_SUMMARY.md`
3. **Try different request types** - Test create, modify, fix, refactor commands
4. **Enable logging** - See what context is being added (`export FELLOW_LOGGING=1`)
5. **Update incrementally** - Use `/build-kb --update` after code changes

## What to Explore Next

- **[Features Overview](features/automatic-enrichment.md)** - Understand how automatic enrichment works
- **[Use Cases](use-cases/overview.md)** - See how teams use Fellow
- **[Best Practices](best-practices/overview.md)** - Learn optimal workflows
- **[FAQ](about/faq.md)** - Common questions answered

---

<p align="center">
  <strong>Ready to code 10x faster?</strong><br>
  Start with <code>/build-kb</code> and let Fellow transform your AI coding experience.
</p>
