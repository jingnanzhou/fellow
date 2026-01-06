# Fellow Plugin Installation Guide

**Fellow - Architectural Guardrails for Claude Code**

This guide explains how to install Fellow, a Claude Code plugin that automatically enriches every request to prevent architectural drift and enforce codebase consistency.

## Prerequisites

Before installing Fellow, ensure you have:

- **Claude Code CLI or VS Code Extension** - Fellow works with both!
- **Python 3.8 or higher** (for knowledge extraction agents)
- **Git** (optional, for cloning from source)

!!! tip "VS Code Users"
    Fellow works seamlessly with the Claude Code VS Code extension! Install the extension, then install Fellow via CLI. All features work identically with added visual benefits. See the [VS Code Integration Guide](docs-site/vscode.md) for details.

## Installation Methods

Fellow can be installed in three ways:

### Method 1: Install from Local Clone (Current - Until Published)

**Right now, Fellow is not yet in the official marketplace.** Install from a local clone:

```bash
# Step 1: Add as local marketplace
claude plugin marketplace add https://github.com/jingnanzhou/fellow.git

# Step 2: Install from local marketplace
claude plugin marketplace install fellow@local_marketplace

# Step 3: Verify installation
claude plugin list
```

**What happens:**
1. Claude Code registers the directory as a local marketplace
2. Reads the `plugin.json` manifest from the marketplace
3. Installs Fellow from the local marketplace
4. Enables Fellow automatically

**Verification:**
```bash
claude plugin list
# Should show: ✓ fellow (v2.1.0) - Semantic knowledge extraction...
```

### Method 2: Install from Marketplace (After Publishing)

**Once Fellow is published to a marketplace**, installation becomes simpler:

```bash
# Simple one-command installation
claude plugin install fellow

# Verify installation
claude plugin list
```

Claude Code will:
1. Download Fellow from the official marketplace
2. Install it automatically
3. Verify and enable automatically

### Method 3: Removing the Plugin

To uninstall Fellow:

```bash
# Step 1: Uninstall the plugin
claude plugin uninstall fellow@local_marketplace

# Step 2: Remove the marketplace
claude plugin marketplace remove local_marketplace
```

**What this does:**
1. Removes Fellow plugin from your Claude Code installation
2. Removes the local marketplace reference

## Verification

After installation, verify Fellow is loaded:

```bash
# List all installed plugins
/plugin list

# You should see:
# ✓ fellow@user (v2.1.0) - Semantic knowledge extraction and context enrichment
```

Verify Fellow commands are available:

```bash
# Check Fellow commands
/build-kb --help
/fellow --help
/toggle-hooks --help
```

Expected output:
```
Available Fellow commands:
  /build-kb      - Extract semantic knowledge from codebase
  /fellow        - Manual context-enriched coding
  /toggle-hooks  - Enable/disable automatic context enrichment
```

## Plugin Location and Structure

### Where Fellow is Installed

Claude Code copies Fellow to a **cache directory** for security verification:

| OS | Plugin Cache Location |
|----|----------------------|
| **macOS** | `~/.claude/cache/plugins/fellow/` |
| **Linux** | `~/.claude/cache/plugins/fellow/` |
| **Windows** | `%APPDATA%\ClaudeCode\cache\plugins\fellow\` |

### Plugin Configuration

Plugin settings are stored in:

| Scope | Location |
|-------|----------|
| **User-level** | `~/.claude/settings.json` (macOS/Linux)<br>`%APPDATA%\ClaudeCode\settings.json` (Windows) |
| **Project-level** | `.claude/settings.json` (in project root) |
| **Local development** | `.claude/settings.local.json` (gitignored) |

### Directory Structure

Fellow follows the standard Claude Code plugin structure:

```
fellow/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest (required)
│   └── hooks.json           # Hook configuration
├── commands/                 # Slash commands
│   ├── build-kb.md
│   ├── fellow.md
│   └── toggle-hooks.md
├── agents/                   # Extraction agents
│   ├── factual-knowledge-extractor.md
│   ├── procedural-knowledge-extractor.md
│   └── conceptual-knowledge-extractor.md
├── hooks/                    # Hook implementations
│   ├── enrich-context.sh
│   ├── enrich-context.py
│   └── logger.py
├── docs/                     # Documentation
│   ├── CHEAT_SHEET.md
│   └── INCREMENTAL_UPDATES.md
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## Configuration

### Default Configuration

Fellow comes pre-configured with sensible defaults:

- **Automatic enrichment**: Enabled via hooks
- **Logging**: Disabled by default (enable with `FELLOW_LOGGING=1`)
- **Detection confidence**: 0.7 threshold
- **Silent mode**: Disabled (shows enriched context)

### Customizing Fellow

Edit Fellow's hook configuration to customize behavior:

**Location**: `~/.claude/cache/plugins/fellow/.claude-plugin/hooks.json`

```json
{
  "hooks": [{
    "name": "fellow-context-enrichment",
    "enabled": true,
    "config": {
      "min_confidence": 0.7,     // Adjust detection sensitivity
      "silent_mode": false,       // Hide/show enriched context
      "logging_enabled": false,   // Enable/disable logging
      "keywords": [               // Customize detection keywords
        "add", "create", "implement", ...
      ]
    }
  }]
}
```

**Recommended settings by use case:**

| Use Case | min_confidence | silent_mode | logging_enabled |
|----------|----------------|-------------|-----------------|
| **Learning Fellow** | 0.7 | false | true |
| **Production use** | 0.7 | false | false |
| **Conservative detection** | 0.9 | false | false |
| **Aggressive detection** | 0.5 | false | true |

### Project-Level Configuration

You can configure Fellow per-project by creating `.claude/settings.json`:

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

## Enabling Python Dependencies

Fellow's extraction agents require Python 3.8+. No additional dependencies are needed - Fellow uses only Python standard library modules.

Verify Python is available:

```bash
python3 --version
# Should output: Python 3.8.0 or higher
```

## Troubleshooting

### Issue: Plugin not found

**Symptom**: `/build-kb` command not recognized

**Solutions**:

1. **Verify installation**:
   ```bash
   /plugin list
   ```

2. **Reinstall Fellow**:
   ```bash
   /plugin uninstall fellow
   /plugin install fellow
   ```

3. **Check plugin cache**:
   ```bash
   ls ~/.claude/cache/plugins/
   # Should show "fellow" directory
   ```

### Issue: Commands not working

**Symptom**: Commands execute but no output or errors

**Solutions**:

1. **Check Python availability**:
   ```bash
   which python3
   python3 --version
   ```

2. **Verify plugin structure**:
   ```bash
   ls ~/.claude/cache/plugins/fellow/
   # Should show: .claude-plugin/, commands/, agents/, hooks/
   ```

3. **Check permissions**:
   ```bash
   # Make sure hook scripts are executable
   ls -la ~/.claude/cache/plugins/fellow/hooks/
   # enrich-context.sh should have execute permission
   ```

### Issue: Hooks not intercepting requests

**Symptom**: Coding requests not automatically enriched

**Solutions**:

1. **Check hook status**:
   ```bash
   /toggle-hooks status
   ```

2. **Verify hooks are enabled**:
   ```bash
   cat ~/.claude/cache/plugins/fellow/.claude-plugin/hooks.json
   # "enabled": true
   ```

3. **Check detection keywords**:
   - Make sure your request uses coding keywords (add, create, fix, etc.)
   - Use `/fellow` command to force enrichment

4. **Enable logging to debug**:
   ```bash
   export FELLOW_LOGGING=1
   # Check logs in target project's .fellow-data/logs/
   ```

### Issue: Knowledge base not found

**Symptom**: "Knowledge base not found" error when coding

**Solution**:

```bash
# Build knowledge base first
cd /path/to/your/project
/build-kb

# Verify KB was created
ls .fellow-data/semantic/
# Should show: factual_knowledge.json, procedural_knowledge.json, etc.
```

### Issue: Python import errors

**Symptom**: "ModuleNotFoundError" when running /build-kb

**Solution**:

Fellow uses only Python standard library. If you see import errors:

1. **Update Python**:
   ```bash
   python3 --version
   # Must be 3.8 or higher
   ```

2. **Check Python path**:
   ```bash
   which python3
   # Should point to valid Python 3.8+ installation
   ```

## Uninstalling Fellow

To remove Fellow completely:

```bash
# Step 1: Uninstall the plugin
claude plugin uninstall fellow@local_marketplace

# Step 2: Remove the marketplace
claude plugin marketplace remove local_marketplace

# Optional: Remove any generated knowledge bases
# These are in your project directories at .fellow-data/
```

## Updating Fellow

To update to the latest version:

```bash
# Check current version
/plugin list

# Update Fellow
/plugin update fellow

# Verify new version
/plugin list
```

## Next Steps

After installation:

1. **Read the Quick Start Guide**: `docs-site/quick-start.md`
2. **Build your first knowledge base**: `/build-kb`
3. **Try automatic enrichment**: Just type a coding request!
4. **Check the Cheat Sheet**: `docs/CHEAT_SHEET.md`

## Getting Help

- **Documentation**: https://jingnanzhou.github.io/fellow/
- **Issues**: https://github.com/jingnanzhou/fellow/issues
- **Email**: fellow@example.com

---

**Installation complete! Ready to start coding with Fellow.**
