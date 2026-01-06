# Installation

**Fellow - Architectural Guardrails for Claude Code**

This guide explains how to install Fellow, a Claude Code plugin that automatically enriches every request to prevent architectural drift and enforce codebase consistency.

## Prerequisites

Before installing Fellow, ensure you have:

- **Claude Code CLI** - **Required for plugin installation** (even for VS Code users!)
- **Python 3.8 or higher** (for knowledge extraction agents)
- **Git** (optional, for cloning from source)

!!! warning "CLI Required for Plugin Installation"
    The VS Code extension does NOT include the `claude` CLI command. You must install the Claude Code CLI separately to install plugins, even if you only plan to use VS Code.

    **[Install Claude Code CLI →](cli-installation.md)**

!!! tip "VS Code Users"
    Fellow works seamlessly with the [Claude Code VS Code extension](vscode.md)! But you still need the CLI to install Fellow first. After CLI installation via marketplace commands, Fellow automatically works in both CLI and VS Code.

## Installation Methods

Choose the installation method that fits your needs:

### Method 1: Local Clone (Current - Required Until Published)

**Required right now** since Fellow is not yet in the official marketplace.

**Best for:** Everyone (current only option)

```bash
# Step 1: Add as local marketplace
claude plugin marketplace add https://github.com/jingnanzhou/fellow.git

# Step 2: Install from local marketplace
claude plugin marketplace install fellow@local_marketplace

# Step 3: Verify
claude plugin list
```

**What this does:**
- Registers the GitHub repository as a local marketplace
- Reads `plugin.json` from the repository
- Installs Fellow from local marketplace
- Enables Fellow automatically

**Pros:**
- ✅ Works immediately (no official marketplace needed)
- ✅ No cloning needed - installs directly from GitHub
- ✅ Simple and fast installation
- ✅ Works in both CLI and VS Code

### Method 2: From Marketplace (After Publishing - Future)

**Will work after** Fellow is published to the official Claude Code marketplace.

```bash
# Simple one-command installation
claude plugin install fellow

# Verify installation
claude plugin list
```

**When available:**
- After Anthropic reviews and approves Fellow
- Expected timeline: 2-4 weeks after submission

**Pros (when available):**
- ✅ Simple one-command installation
- ✅ Automatic updates available
- ✅ Verified and tested releases
- ✅ Security-checked by Claude Code

### Method 3: Removing the Plugin

To uninstall Fellow:

```bash
# Step 1: Uninstall the plugin
claude plugin uninstall fellow@local_marketplace

# Step 2: Remove the marketplace
claude plugin marketplace remove local_marketplace
```

**What this does:**
- Removes Fellow plugin from Claude Code
- Removes the local marketplace reference

## Verify Installation

After installing Fellow, verify it's working correctly:

```bash
# List installed plugins
claude plugin list
```

You should see:
```
✓ fellow@local_marketplace (v2.1.0) - Semantic knowledge extraction and context enrichment
```

Verify Fellow commands are available:

```bash
# These commands should now work:
/build-kb --help
/toggle-hooks status
```

## Where is Fellow Installed?

Claude Code copies Fellow to a **secure cache directory** for verification:

| Operating System | Plugin Cache Location |
|-----------------|----------------------|
| **macOS** | `~/.claude/cache/plugins/fellow/` |
| **Linux** | `~/.claude/cache/plugins/fellow/` |
| **Windows** | `%APPDATA%\ClaudeCode\cache\plugins\fellow\` |

!!! note "Why a cache directory?"
    Claude Code copies plugins to a cache for security verification. This ensures plugins can't modify themselves after installation.

### Plugin Configuration

Plugin settings are stored separately from plugin files:

| Configuration Scope | Location (macOS/Linux) | Location (Windows) |
|-------------------|------------------------|-------------------|
| **User-level** | `~/.claude/settings.json` | `%APPDATA%\ClaudeCode\settings.json` |
| **Project-level** | `.claude/settings.json` | `.claude/settings.json` |
| **Local** | `.claude/settings.local.json` | `.claude/settings.local.json` |

## Post-Installation Setup

### 1. Verify Python

Fellow requires Python 3.8+ for knowledge extraction:

```bash
python3 --version
```

Expected output: `Python 3.8.0` or higher

!!! tip "No additional dependencies needed"
    Fellow uses only Python standard library modules. No `pip install` required!

### 2. Check Hook Status

Fellow's automatic enrichment hooks are enabled by default:

```bash
/toggle-hooks status
```

Expected output:
```
✅ Fellow hooks are ENABLED
   Coding requests will be automatically enriched with context

To disable: /toggle-hooks off
```

### 3. Build Your First Knowledge Base

Navigate to a project and extract knowledge:

```bash
cd /path/to/your-project
/build-kb
```

This creates `.fellow-data/semantic/` with your project's knowledge base.

## Configuration

### Default Settings

Fellow comes pre-configured with sensible defaults:

- ✅ **Automatic enrichment**: Enabled
- ✅ **Hook detection confidence**: 0.7 threshold
- ✅ **Silent mode**: Disabled (shows enriched context)
- ✅ **Logging**: Disabled (enable with `FELLOW_LOGGING=1`)

### Customizing Fellow

To customize Fellow's behavior, edit the hook configuration:

**Location**: Find it in Claude Code's plugin cache at:
- macOS/Linux: `~/.claude/cache/plugins/fellow/.claude-plugin/hooks.json`
- Windows: `%APPDATA%\ClaudeCode\cache\plugins\fellow\.claude-plugin\hooks.json`

**Configuration options:**

```json
{
  "hooks": [{
    "name": "fellow-context-enrichment",
    "enabled": true,
    "config": {
      "min_confidence": 0.7,
      "silent_mode": false,
      "logging_enabled": false,
      "keywords": ["add", "create", "implement", ...]
    }
  }]
}
```

**Settings explained:**

| Setting | Values | Description |
|---------|--------|-------------|
| `enabled` | `true`/`false` | Enable/disable automatic enrichment |
| `min_confidence` | `0.5` - `1.0` | Detection threshold (higher = stricter) |
| `silent_mode` | `true`/`false` | Hide enriched context from display |
| `logging_enabled` | `true`/`false` | Log all enrichment events |
| `keywords` | Array of strings | Keywords for coding request detection |

**Recommended settings by use case:**

=== "Learning Fellow"
    ```json
    {
      "min_confidence": 0.7,
      "silent_mode": false,
      "logging_enabled": true
    }
    ```
    **Best for:** Understanding how Fellow works

=== "Production Use"
    ```json
    {
      "min_confidence": 0.7,
      "silent_mode": false,
      "logging_enabled": false
    }
    ```
    **Best for:** Daily development work

=== "Conservative"
    ```json
    {
      "min_confidence": 0.9,
      "silent_mode": false,
      "logging_enabled": false
    }
    ```
    **Best for:** Only enrich very obvious coding requests

=== "Aggressive"
    ```json
    {
      "min_confidence": 0.5,
      "silent_mode": false,
      "logging_enabled": true
    }
    ```
    **Best for:** Maximum enrichment, log to verify accuracy

### Enable Logging

To see what context Fellow is adding:

**Method 1: Environment variable**
```bash
export FELLOW_LOGGING=1
```

**Method 2: Edit hooks.json**
```json
{
  "config": {
    "logging_enabled": true
  }
}
```

Logs will be created in your project at:
```
.fellow-data/logs/
├── enrichment_2026-01-05.jsonl    # Machine-readable
└── enrichment_2026-01-05.log      # Human-readable
```

## Troubleshooting

### Plugin Not Found

**Symptom**: `/build-kb` command not recognized

**Solutions:**

1. Verify installation:
   ```bash
   /plugin list
   ```

2. Reinstall Fellow:
   ```bash
   /plugin uninstall fellow
   /plugin install fellow
   ```

3. Check plugin cache exists:
   ```bash
   ls ~/.claude/cache/plugins/
   # Should show "fellow" directory
   ```

### Commands Not Working

**Symptom**: Commands execute but no output

**Solutions:**

1. Check Python availability:
   ```bash
   which python3
   python3 --version
   ```

2. Verify plugin structure:
   ```bash
   ls ~/.claude/cache/plugins/fellow/
   # Should show: .claude-plugin/, commands/, agents/, hooks/
   ```

3. Check script permissions:
   ```bash
   ls -la ~/.claude/cache/plugins/fellow/hooks/enrich-context.sh
   # Should have execute permission (-rwxr-xr-x)
   ```

### Hooks Not Intercepting

**Symptom**: Coding requests not automatically enriched

**Solutions:**

1. Check hook status:
   ```bash
   /toggle-hooks status
   ```

2. Verify hooks are enabled in config:
   ```bash
   cat ~/.claude/cache/plugins/fellow/.claude-plugin/hooks.json
   # Look for "enabled": true
   ```

3. Use explicit command instead:
   ```bash
   /fellow Add authentication to the endpoint
   ```

4. Enable logging to debug:
   ```bash
   export FELLOW_LOGGING=1
   # Check logs in .fellow-data/logs/
   ```

### Knowledge Base Not Found

**Symptom**: "Knowledge base not found" error

**Solution:**

Build the knowledge base first:

```bash
cd /path/to/your-project
/build-kb

# Verify it was created
ls .fellow-data/semantic/
# Should show JSON files
```

### Python Import Errors

**Symptom**: "ModuleNotFoundError" when running commands

**Solution:**

Fellow uses only Python standard library. If you see import errors:

1. Update Python to 3.8+:
   ```bash
   python3 --version
   ```

2. Check Python path:
   ```bash
   which python3
   ```

3. Reinstall Python if necessary

## Updating Fellow

To update to the latest version:

```bash
# Check current version
/plugin list

# Update Fellow
/plugin update fellow

# Verify new version installed
/plugin list
```

## Uninstalling Fellow

To completely remove Fellow:

```bash
# Step 1: Uninstall the plugin
claude plugin uninstall fellow@local_marketplace

# Step 2: Remove the marketplace
claude plugin marketplace remove local_marketplace

# Optional: Remove knowledge bases from projects
# (These are in your project directories at .fellow-data/)
```

## Multiple Projects

Fellow works seamlessly across multiple projects. Each project gets its own knowledge base:

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
"Add feature X"  # Uses project-a's knowledge base

# Coding in Project B
cd /path/to/project-b
"Add feature Y"  # Uses project-b's knowledge base
```

Fellow automatically discovers and loads the correct knowledge base based on your current directory.

## Next Steps

After installation:

1. **[Quick Start Guide](quick-start.md)** - Build your first knowledge base
2. **[Commands Overview](user-guide/commands/overview.md)** - Learn all Fellow commands
3. **[Cheat Sheet](reference/cheat-sheet.md)** - Quick reference for all features
4. **[FAQ](about/faq.md)** - Common questions answered

## Getting Help

- **Documentation**: https://jingnanzhou.github.io/fellow/
- **GitHub Issues**: https://github.com/jingnanzhou/fellow/issues
- **Email**: fellow@example.com

---

<p align="center">
  <strong>Installation complete! Ready to code with Fellow.</strong>
</p>
