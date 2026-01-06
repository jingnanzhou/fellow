# Fellow - Quick Reference Cheat Sheet

**Fellow - Architectural Guardrails for Claude Code**

A quick reference guide for using Fellow, the Claude Code plugin that automatically enriches every request to prevent architectural drift and enforce codebase consistency.

---

## Core Commands

### `/build-kb` - Build Knowledge Base

Extract semantic knowledge from your project.

```bash
# Initial build (full extraction)
/build-kb

# Build for specific project
/build-kb /path/to/project

# Force full re-extraction
/build-kb --full

# Incremental update (only changed files)
/build-kb --update
```

**Time:**
- Full: 2-5 minutes
- Incremental: 10-20 seconds (10-20x faster)

**Output Location:** `.fellow-data/semantic/`

---

### `/fellow` - Manual Context Enrichment

Explicitly enrich a coding request with semantic knowledge.

```bash
/fellow Add authentication to the user endpoint
/fellow Refactor payment processing to use Strategy pattern
/fellow Add rate limiting to the API
```

**Use when:**
- Hooks are disabled
- You want forced enrichment
- Testing the knowledge base

---

### `/toggle-hooks` - Enable/Disable Automatic Enrichment

Control whether Fellow automatically intercepts coding requests.

```bash
# Check status
/toggle-hooks status

# Disable automatic enrichment
/toggle-hooks off

# Enable automatic enrichment
/toggle-hooks on
```

---

## Automatic Mode (Default)

When hooks are **enabled** (default), Fellow automatically enriches coding requests.

### How It Works

1. You type a coding request naturally
2. Fellow detects it's a coding request
3. Loads semantic knowledge from KB
4. Enriches your request with context
5. Passes enriched context to Claude

### Example

**You type:**
```
Add validation to the authentication endpoint
```

**Fellow automatically enriches with:**
- Relevant entities (AuthService, ValidationService)
- Relevant workflows (authentication flow)
- Architectural constraints (security, validation rules)
- Design patterns in use

**Result:** Claude implements with full architectural awareness

### Detected as Coding Requests

- "Add a new feature"
- "Refactor the payment service"
- "Fix the validation bug"
- "Implement caching"
- "Create an endpoint"
- "Update the authentication"

### Not Detected (Pass Through)

- "What is the architecture?"
- "Show me the workflows"
- "How does this work?"
- "List the design patterns"

---

## Knowledge Base Structure

### Files Created in `.fellow-data/semantic/`

| File | Purpose | Format |
|------|---------|--------|
| `factual_knowledge.json` | Entities and relationships | JSON (machine) |
| `procedural_knowledge.json` | Workflows and execution flows | JSON (machine) |
| `conceptual_knowledge.json` | Architecture and patterns | JSON (machine) |
| `SEMANTIC_KNOWLEDGE_SUMMARY.md` | Comprehensive summary | Markdown (human) |
| `extraction_metadata.json` | File tracking for incremental updates | JSON (metadata) |

### Logs in `.fellow-data/logs/`

| File | Purpose | Format |
|------|---------|--------|
| `enrichment_YYYY-MM-DD.log` | Human-readable enrichment logs | Text |
| `enrichment_YYYY-MM-DD.jsonl` | Machine-readable logs | JSON Lines |

---

## Configuration

### Hook Configuration (`.claude-plugin/hooks.json`)

```json
{
  "hooks": [{
    "enabled": true,              // Enable/disable automatic enrichment
    "config": {
      "logging_enabled": true,    // Enable enrichment logging
      "silent_mode": false,       // Hide enriched context output
      "min_confidence": 0.7       // Detection confidence threshold (0.0-1.0)
    }
  }]
}
```

### Enable Logging

**Method 1:** Edit `hooks.json`
```json
"logging_enabled": true
```

**Method 2:** Environment variable
```bash
export FELLOW_LOGGING=1
```

---

## Common Workflows

### Daily Development Workflow

```bash
# Day 1: Initial setup
/build-kb

# Your coding request (automatic enrichment)
Add user authentication with JWT tokens

# Day 2: After making changes
/build-kb --update

# Continue coding with enriched context
Refactor the authentication service
```

### Testing Without Enrichment

```bash
# Disable hooks temporarily
/toggle-hooks off

# Code without enrichment
[your coding work]

# Re-enable when ready
/toggle-hooks on
```

### Periodic Full Refresh

```bash
# Monthly full rebuild (recommended)
/build-kb --full
```

### Working on Multiple Projects

```bash
# Build KB for project A
cd /path/to/project-a
/build-kb

# Build KB for project B
cd /path/to/project-b
/build-kb

# Fellow automatically loads correct KB based on current directory
```

---

## Troubleshooting

### "Knowledge base not found"

**Problem:** No KB exists for current project

**Solution:**
```bash
/build-kb
```

### "No changes detected"

**Problem:** Running incremental update but no files changed

**Solution:** This is normal - KB is already up to date

### Hook not working

**Check 1:** Is hook enabled?
```bash
/toggle-hooks status
```

**Check 2:** Is logging enabled to debug?
```bash
export FELLOW_LOGGING=1
# Check logs in .fellow-data/logs/
```

**Check 3:** Is it a coding request?
- Try using `/fellow` explicitly to force enrichment

### Logs too large

**Solution:** Logs are rotated daily. Old logs can be deleted:
```bash
rm .fellow-data/logs/enrichment_2026-01-*.log
rm .fellow-data/logs/enrichment_2026-01-*.jsonl
```

---

## Best Practices

### ✅ DO

- Run `/build-kb` after initial setup
- Run `/build-kb --update` after significant code changes
- Use automatic mode (hooks enabled) for daily work
- Check logs when debugging enrichment behavior
- Exclude `.fellow-data/` from git (add to `.gitignore`)

### ❌ DON'T

- Commit `.fellow-data/` to version control
- Run `/build-kb --full` every time (use incremental)
- Disable hooks unless you have a specific reason
- Ignore enriched context suggestions

---

## Quick Stats

| Metric | Value |
|--------|-------|
| **Full extraction time** | 2-5 minutes |
| **Incremental update time** | 10-20 seconds |
| **Speedup (incremental)** | 10-20x faster |
| **KB size** | 100-500 KB per project |
| **Log size** | ~3-5 KB per enrichment event |
| **Confidence threshold** | 0.7 (default, configurable) |

---

## Integration with Git

### Recommended `.gitignore` Entry

Add to your project's `.gitignore`:

```gitignore
# Fellow - Knowledge Base and Logs
.fellow-data/
```

**Rationale:**
- `.fellow-data/` contains generated files
- Large files (KB + logs)
- Project-specific and should be regenerated locally
- Not suitable for version control

---

## Advanced Usage

### Custom Confidence Threshold

Lower = more aggressive detection (more false positives)
Higher = conservative detection (may miss requests)

```json
"min_confidence": 0.5  // Aggressive
"min_confidence": 0.7  // Default
"min_confidence": 0.9  // Conservative
```

### Silent Mode

Hide enriched context, only apply guardrails:

```json
"silent_mode": true
```

### Analyze Logs

```bash
# View human-readable logs
cat .fellow-data/logs/enrichment_2026-01-05.log

# Parse JSON logs
cat .fellow-data/logs/enrichment_2026-01-05.jsonl | jq '.'

# Count enrichment events
wc -l .fellow-data/logs/enrichment_2026-01-05.jsonl

# Find specific prompts
grep "authentication" .fellow-data/logs/enrichment_2026-01-05.log
```

---

## Version Info

**Current Version:** 2.1.0

**Features:**
- ✅ Automatic context enrichment (hooks)
- ✅ Incremental knowledge base updates
- ✅ Comprehensive logging
- ✅ Manual enrichment command
- ✅ Hook enable/disable toggle

---

## Getting Help

- **Full Documentation:** `README.md`
- **Incremental Updates:** `docs/INCREMENTAL_UPDATES.md`
- **Contributing:** `CONTRIBUTING.md`
- **Issues:** https://github.com/jingnanzhou/fellow/issues

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                    FELLOW QUICK COMMANDS                    │
├─────────────────────────────────────────────────────────────┤
│ /build-kb              Build knowledge base (full)          │
│ /build-kb --update     Update KB (incremental, fast)        │
│ /build-kb --full       Force complete rebuild               │
├─────────────────────────────────────────────────────────────┤
│ /fellow <request>      Manual enrichment                    │
├─────────────────────────────────────────────────────────────┤
│ /toggle-hooks status   Check hook status                    │
│ /toggle-hooks on       Enable automatic enrichment          │
│ /toggle-hooks off      Disable automatic enrichment         │
├─────────────────────────────────────────────────────────────┤
│ AUTOMATIC MODE: Just type coding requests naturally!        │
│ Fellow auto-enriches: "Add auth endpoint" → enriched        │
├─────────────────────────────────────────────────────────────┤
│ LOGS: .fellow-data/logs/enrichment_YYYY-MM-DD.log           │
│ KB:   .fellow-data/semantic/*.json                          │
└─────────────────────────────────────────────────────────────┘
```
