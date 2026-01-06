# Using Fellow in VS Code

Fellow works seamlessly with the Claude Code VS Code extension, providing the same powerful semantic knowledge extraction and automatic context enrichment in a visual IDE environment.

## Quick Start

### 1. Install Claude Code CLI

!!! warning "CLI Required for Plugin Installation"
    The VS Code extension does NOT include the `claude` CLI command. You need to install the CLI separately to install plugins!

**Install Claude Code CLI first:**

=== "macOS"
    ```bash
    # Using Homebrew
    brew install claude

    # Verify installation
    claude --version
    ```

=== "Linux"
    ```bash
    # Using installer script
    curl -fsSL https://code.claude.com/install.sh | sh

    # Verify installation
    claude --version
    ```

=== "Windows"
    ```powershell
    # Using winget
    winget install Anthropic.ClaudeCode

    # Verify installation
    claude --version
    ```

**Or download from:** https://code.claude.com

### 2. Install VS Code Extension

After installing the CLI, install the VS Code extension:

**From VS Code:**
1. Open Extensions view (`Cmd+Shift+X` or `Ctrl+Shift+X`)
2. Search for "Claude Code"
3. Click "Install"

**Or from command line:**
```bash
code --install-extension anthropic.claude-code
```

### 3. Install Fellow Plugin

Now install Fellow using the Claude Code CLI (from step 1):

!!! warning "Fellow Not Yet Published"
    Fellow is not yet in the official marketplace. Install from local clone:

```bash
# Clone Fellow repository
git clone https://github.com/jingnanzhou/fellow.git
cd fellow

# Install from current directory
claude plugin add ./

# Verify installation
claude plugin list
```

!!! note "CLI Required for Plugin Installation"
    You need the Claude Code CLI to install plugins. Once installed, plugins are automatically available in the VS Code extension.

!!! tip "After Publishing"
    Once Fellow is published, installation will be simpler: `claude plugin add fellow`

### 4. Start Using Fellow

Open the Claude Code panel in VS Code and start coding:

```
# Build knowledge base for your project
/build-kb

# Start coding with automatic enrichment
"Add validation to the user registration endpoint"
```

Fellow automatically enriches your requests with context, just like in the CLI!

## How It Works

### Shared Configuration

The VS Code extension and CLI share the same plugin system:

```
~/.claude/
├── settings.json               # Shared settings
└── cache/
    └── plugins/
        └── fellow/            # Plugin files

your-project/
├── .fellow-data/              # Knowledge base
│   ├── semantic/              # Same location as CLI
│   └── logs/
└── .claude/
    └── settings.json          # Project settings
```

**Key Points:**
- Plugins installed via CLI are automatically available in VS Code
- Knowledge bases work identically in both environments
- Settings from `.claude/settings.json` apply to both
- Hooks work the same way (automatic enrichment)

### Fellow Features in VS Code

All Fellow features work in VS Code:

| Feature | CLI | VS Code | Notes |
|---------|-----|---------|-------|
| **Commands** | ✅ | ✅ | `/build-kb`, `/fellow`, `/toggle-hooks` |
| **Automatic Enrichment** | ✅ | ✅ | Hooks work identically |
| **Knowledge Base** | ✅ | ✅ | Same `.fellow-data/` location |
| **Incremental Updates** | ✅ | ✅ | Same speed (10-20 seconds) |
| **Logging** | ✅ | ✅ | Same format and location |

## Using Fellow Commands

### Build Knowledge Base

Build or update your knowledge base:

```bash
# First time - full extraction (2-5 minutes)
/build-kb

# After code changes - incremental update (10-20 seconds)
/build-kb --update

# Force full rebuild
/build-kb --full
```

**Output in VS Code:**
- Progress shown in Claude panel
- Extraction results displayed
- Knowledge base created in `.fellow-data/semantic/`

### Automatic Enrichment

Fellow automatically enriches coding requests:

```
# Just type your request naturally:
"Add caching to the tool listing API"

# Fellow automatically:
# 1. Detects this is a coding request
# 2. Loads relevant knowledge from KB
# 3. Enriches with entities, workflows, constraints
# 4. Passes to Claude for implementation
```

**You'll see:**
```
📋 Context from Knowledge Base

**Relevant Entities:**
- CacheService (class): Redis-based caching
- ToolRepository (class): Data access layer

**Architectural Guardrails:**
- [Performance] Use Redis for caching
- [Architecture] Set TTL to 60 seconds
- [Pattern] Use cache-aside pattern

[Implementation follows...]
```

### Manual Enrichment

Force enrichment even for ambiguous requests:

```bash
/fellow Add error handling to the API
```

### Manage Hooks

Control automatic enrichment:

```bash
# Check status
/toggle-hooks status

# Disable temporarily
/toggle-hooks off

# Re-enable
/toggle-hooks on
```

## Visual Benefits of VS Code

### 1. Inline Diffs

**CLI:** Text-based diffs in terminal
**VS Code:** Visual inline diffs with highlighting

**Benefits:**
- See changes in context of your file
- Click to accept/reject changes
- Multiple files shown in tabs
- Syntax highlighting preserved

### 2. File Selection

**VS Code Advantage:** @-mention files from editor

```
# In CLI:
/fellow Add auth to src/api/users.py

# In VS Code:
"Add auth to this endpoint"
# (with users.py file selected or @-mentioned)
```

### 3. Integrated Workflow

**No context switching:**
- Edit code in VS Code
- Ask Fellow for help in panel
- Review diffs inline
- Accept changes with click
- Continue coding

**vs CLI workflow:**
- Edit in editor
- Switch to terminal
- Review text diffs
- Switch back to editor
- Apply changes manually

### 4. Multiple Conversations

**VS Code allows:**
- Multiple Claude conversations in tabs
- Keep context of different tasks
- Switch between conversations easily

## Configuration

### Project-Level Settings

Create `.claude/settings.json` in your project:

```json
{
  "enabledPlugins": {
    "fellow@user": true
  },
  "pluginSettings": {
    "fellow": {
      "autoUpdate": true,
      "logLevel": "info"
    }
  }
}
```

### Customize Fellow Behavior

Edit Fellow's hook configuration:

**Location:** `~/.claude/cache/plugins/fellow/.claude-plugin/hooks.json`

```json
{
  "hooks": [{
    "name": "fellow-context-enrichment",
    "enabled": true,
    "config": {
      "min_confidence": 0.7,
      "silent_mode": false,
      "logging_enabled": false
    }
  }]
}
```

**Recommended settings for VS Code:**

=== "Visual Learner"
    ```json
    {
      "min_confidence": 0.7,
      "silent_mode": false,
      "logging_enabled": true
    }
    ```
    See full context in panel + logs for review

=== "Experienced User"
    ```json
    {
      "min_confidence": 0.7,
      "silent_mode": false,
      "logging_enabled": false
    }
    ```
    Standard enrichment without logging overhead

=== "Conservative"
    ```json
    {
      "min_confidence": 0.9,
      "silent_mode": false,
      "logging_enabled": false
    }
    ```
    Only very obvious coding requests enriched

### Enable Logging

To see what context Fellow is adding:

```bash
export FELLOW_LOGGING=1
```

Logs appear in:
```
.fellow-data/logs/
├── enrichment_2026-01-05.jsonl    # Machine-readable
└── enrichment_2026-01-05.log      # Human-readable
```

## Workflow Examples

### Example 1: New Feature with Visual Review

**Scenario:** Add a new API endpoint

1. **Build knowledge base:**
   ```
   /build-kb
   ```

2. **Request feature:**
   ```
   "Add a POST endpoint for creating orders with items and payment info"
   ```

3. **Review in VS Code:**
   - Fellow enriches with Order entities, payment workflows, constraints
   - Claude generates code
   - See inline diffs with syntax highlighting
   - Click "Accept" on each change
   - Files updated automatically

4. **Update knowledge base:**
   ```
   /build-kb --update
   ```

### Example 2: Refactoring with Context

**Scenario:** Refactor authentication logic

1. **Select code in editor:**
   - Highlight authentication code in `auth.py`

2. **Request refactoring:**
   ```
   "Refactor this to use the Strategy pattern"
   ```

3. **Fellow provides context:**
   - Loads existing auth patterns
   - Shows current architecture
   - Applies security constraints

4. **Review changes:**
   - Visual diff shows before/after
   - Accept changes with confidence

### Example 3: Multi-Project Setup

**Scenario:** Working on multiple projects

```bash
# Project A
cd /workspace/api-service
/build-kb

# Work on Project A in VS Code
# Fellow uses api-service knowledge base

# Project B
cd /workspace/web-app
/build-kb

# Switch to Project B in VS Code
# Fellow automatically uses web-app knowledge base
```

Fellow automatically discovers the correct knowledge base based on your current workspace!

## Keyboard Shortcuts

Useful VS Code shortcuts for Claude + Fellow:

| Shortcut | Action |
|----------|--------|
| `Cmd+Shift+P` (macOS)<br>`Ctrl+Shift+P` (Windows/Linux) | Open command palette |
| Type `/build-kb` | Build knowledge base |
| Type `/toggle-hooks status` | Check hook status |
| `Cmd+K Cmd+I` | Open Claude inline chat |
| `Cmd+'` | Toggle Claude panel |

## Troubleshooting

### Issue: Fellow commands not available

**Solution:**

1. Verify Fellow is installed:
   ```bash
   /plugin list
   ```

2. Restart VS Code:
   - Close and reopen VS Code
   - Plugins should load automatically

3. Check VS Code extension is enabled:
   - Extensions view → "Claude Code" → Ensure enabled

### Issue: Knowledge base not found in VS Code

**Solution:**

Make sure you're in the correct workspace:

1. Check current directory in VS Code:
   - Terminal → `pwd` (macOS/Linux) or `cd` (Windows)

2. Build KB for this workspace:
   ```
   /build-kb
   ```

3. Verify KB was created:
   ```bash
   ls .fellow-data/semantic/
   ```

### Issue: Hooks not working in VS Code

**Solution:**

1. Check hook status:
   ```
   /toggle-hooks status
   ```

2. Verify hooks are enabled:
   ```bash
   cat ~/.claude/cache/plugins/fellow/.claude-plugin/hooks.json
   # "enabled": true
   ```

3. Enable logging to debug:
   ```bash
   export FELLOW_LOGGING=1
   ```

4. Try explicit command:
   ```
   /fellow Add feature X
   ```

### Issue: Slow first-time extraction

**Expected behavior:**

- First extraction: 2-5 minutes (same as CLI)
- Incremental updates: 10-20 seconds

This is normal! Grab a coffee while Fellow analyzes your codebase.

## Best Practices for VS Code

### 1. Use Visual Diffs

Take advantage of VS Code's visual diff view:
- Review each change carefully
- See changes in context
- Accept/reject selectively

### 2. Organize Conversations

Keep conversations focused:
- One conversation per feature/task
- Use tabs for parallel work
- Archive completed conversations

### 3. Leverage @-mentions

Use @-mentions for precise context:
```
"Add validation to @src/api/users.py on lines 45-67"
```

### 4. Update KB Regularly

After significant changes:
```
/build-kb --update
```

Keep Fellow's knowledge current for best results.

### 5. Use Logging During Learning

Enable logging while learning Fellow:
```bash
export FELLOW_LOGGING=1
```

See what context is being added, then disable once confident.

## Comparison: CLI vs VS Code

### When to Use CLI

**Best for:**
- Quick terminal-based workflows
- Scripting and automation
- Server/remote environments
- Preference for keyboard-only interaction

### When to Use VS Code Extension

**Best for:**
- Visual code review
- IDE-integrated workflow
- Multi-file changes
- Learning Fellow (visual feedback)
- Teams familiar with VS Code

### Use Both!

Many developers use both:
- **VS Code** for feature development (visual diffs)
- **CLI** for quick updates and scripts
- Conversations and knowledge bases are shared!

## Next Steps

Now that you know how to use Fellow in VS Code:

1. **[Quick Start Guide](quick-start.md)** - Build your first knowledge base
2. **[Commands Overview](user-guide/commands/overview.md)** - Learn all Fellow commands
3. **[Cheat Sheet](reference/cheat-sheet.md)** - Quick reference
4. **[Best Practices](best-practices/overview.md)** - Optimize your workflow

## Resources

- **Claude Code VS Code Extension**: [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)
- **VS Code Extension Docs**: https://code.claude.com/docs/en/vs-code.md
- **Fellow Documentation**: https://jingnanzhou.github.io/fellow/
- **GitHub**: https://github.com/jingnanzhou/fellow

---

<p align="center">
  <strong>Fellow + VS Code = Visual AI coding with your architecture</strong>
</p>
