# How to Install Fellow Right Now

## Important: Fellow is Not Yet Published

**The documentation previously showed `/plugin install fellow`, but this only works AFTER Fellow is published to the Claude Code marketplace.**

Right now, Fellow needs to be installed from a local clone or Git URL.

---

## Current Installation Methods

### Method 1: Direct Install (Recommended)

This is the most straightforward way to install Fellow right now:

```bash
# Step 1: Add as local marketplace
claude plugin marketplace add https://github.com/jingnanzhou/fellow.git

# Step 2: Install from local marketplace
claude plugin  install fellow@local_marketplace

# Step 3: Verify installation
claude plugin list
```

**Expected output:**
```
✓ fellow@local_marketplace (v2.1.0) - Semantic knowledge extraction and context enrichment
```

**What this does:**
1. `claude plugin marketplace add https://github.com/jingnanzhou/fellow.git` registers the GitHub repository as a local marketplace
2. `claude plugin  install fellow@local_marketplace` installs Fellow from that marketplace
3. Registers Fellow in `~/.claude/settings.json`
4. Enables Fellow automatically

**Works in both CLI and VS Code!** Fellow automatically works with the Claude Code VS Code extension.

### Method 2: Removing the Plugin

To uninstall Fellow:

```bash
# Step 1: Uninstall the plugin
claude plugin uninstall fellow@local_marketplace

# Step 2: Remove the marketplace
claude plugin marketplace remove local_marketplace
```

**What this does:**
1. Removes Fellow plugin from Claude Code
2. Removes the local marketplace reference

---

## Understanding Plugin Installation

### Where Does Fellow Get Installed?

After running the marketplace install commands, Fellow is installed to:

| OS | Location |
|----|----------|
| **macOS** | `~/.claude/cache/plugins/fellow/` |
| **Linux** | `~/.claude/cache/plugins/fellow/` |
| **Windows** | `%APPDATA%\ClaudeCode\cache\plugins\fellow\` |

**Important:** The original clone location doesn't matter after installation! Claude Code installs Fellow from the marketplace to its own plugin cache.

### Configuration is Registered In

```
~/.claude/settings.json         # User-level settings (macOS/Linux)
%APPDATA%\ClaudeCode\settings.json   # User-level settings (Windows)
```

**Example `settings.json` after installation:**
```json
{
  "enabledPlugins": {
    "fellow": true
  }
}
```

---

## Step-by-Step Example

Let's walk through a complete installation:

**Scenario:** You want to install Fellow on macOS/Linux

```bash
# 1. Add Fellow as local marketplace
claude plugin marketplace add https://github.com/jingnanzhou/fellow.git
# Output: Marketplace 'local_marketplace' added successfully

# 2. Install Fellow from local marketplace
claude plugin  install fellow@local_marketplace
# Output: Installing fellow@local_marketplace...

# 3. Verify it's installed
claude plugin list
# Output: ✓ fellow@local_marketplace (v2.1.0) - Semantic knowledge extraction...

# 4. Test Fellow commands
claude /build-kb --help
# Should show help for /build-kb command
```

---

## After Publishing (Future)

**Once Fellow is published to the official Claude Code marketplace**, installation becomes simpler:

```bash
# Simple one-command installation
claude plugin install fellow

# Verify installation
claude plugin list
```

This will work after:
1. Submitting Fellow to Anthropic for review
2. Anthropic approves and adds to official marketplace
3. Marketplace is updated with Fellow

---

## VS Code Users

**Good news:** The same installation process works for VS Code!

```bash
# Step 1: Install Claude Code VS Code extension
# (Search "Claude Code" in VS Code Extensions)

# Step 2: Install Fellow via CLI (same as above)
claude plugin marketplace add https://github.com/jingnanzhou/fellow.git
claude plugin  install fellow@local_marketplace

# Step 3: Fellow is now available in VS Code automatically!
```

**Important:** Plugins must be installed via the CLI, but they work automatically in both CLI and VS Code extension.

---

## Troubleshooting

### Issue: "claude: command not found"

**Problem:** Claude Code CLI is not installed or not in PATH

**Solution:**
```bash
# Check if Claude Code is installed
which claude

# If not found, install Claude Code CLI first
# Visit: https://code.claude.com/docs/en/installation.md
```

### Issue: "Repository not found"

**Problem:** GitHub URL is incorrect or network issue

**Solution:**
```bash
# Verify the GitHub URL is correct
# https://github.com/jingnanzhou/fellow.git

# Check your network connection
curl -I https://github.com

# Try again
claude plugin marketplace add https://github.com/jingnanzhou/fellow.git
claude plugin  install fellow@local_marketplace
```

### Issue: Plugin installed but commands don't work

**Problem:** Claude Code might not have loaded the plugin properly

**Solution:**
```bash
# Restart Claude Code (if running)
# Then verify installation
claude plugin list

# Try running a command
claude /build-kb --help
```

### Issue: Want to update Fellow to latest version

**Solution:**
```bash
# Remove the old marketplace and reinstall
claude plugin marketplace remove local_marketplace
claude plugin marketplace add https://github.com/jingnanzhou/fellow.git
claude plugin  install fellow@local_marketplace
```

---

## Common Questions

### Q: Do I need to clone the repository?

**A:** No! The simplified installation method installs directly from the GitHub URL. You don't need to clone the repository locally.

### Q: Can I install without Git?

**A:** The Claude Code CLI handles the Git operations automatically when you use the GitHub URL. You don't need to run git commands yourself.

### Q: How do I uninstall Fellow?

**A:**
```bash
# Uninstall Fellow
claude plugin uninstall fellow@local_marketplace

# Remove the marketplace
claude plugin marketplace remove local_marketplace

# Verify it's gone
claude plugin list
```

### Q: How do I check if Fellow is installed?

**A:**
```bash
# List all plugins
claude plugin list

# Try a Fellow command
claude /build-kb --help
```

### Q: Will `claude plugin install fellow` work now?

**A:** No, not until Fellow is published to the official marketplace. Use the local marketplace method (`claude plugin marketplace add https://github.com/jingnanzhou/fellow.git` then `claude plugin  install fellow@local_marketplace`) instead.

---

## Summary

**Current Installation (Required Now):**
```bash
claude plugin marketplace add https://github.com/jingnanzhou/fellow.git
claude plugin  install fellow@local_marketplace
claude plugin list
```

**Future Installation (After Publishing):**
```bash
claude plugin install fellow
```

**Key Points:**
- No cloning needed - install directly from GitHub URL
- Works in both CLI and VS Code
- Update by removing and re-adding marketplace
- Simple and fast installation

---

**Ready to install Fellow? Follow Method 1 above!**
