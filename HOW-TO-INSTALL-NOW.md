# How to Install Fellow Right Now

## Important: Fellow is Not Yet Published

**The documentation previously showed `/plugin install fellow`, but this only works AFTER Fellow is published to the Claude Code marketplace.**

Right now, Fellow needs to be installed from a local clone or Git URL.

---

## Current Installation Methods

### Method 1: Clone and Install (Recommended)

This is the most straightforward way to install Fellow right now:

```bash
# Step 1: Clone Fellow repository to your local machine
git clone https://github.com/jingnanzhou/fellow.git

# Step 2: Navigate into the directory
cd fellow

# Step 3: Add as local marketplace
claude plugin marketplace add ./

# Step 4: Install from local marketplace
claude plugin marketplace install fellow@local_marketplace

# Step 5: Verify installation
claude plugin list
```

**Expected output:**
```
✓ fellow@local_marketplace (v2.1.0) - Semantic knowledge extraction and context enrichment
```

**What this does:**
1. `claude plugin marketplace add ./` registers the directory as a local marketplace
2. `claude plugin marketplace install fellow@local_marketplace` installs Fellow from that marketplace
3. Registers Fellow in `~/.claude/settings.json`
4. Enables Fellow automatically

**Where you can put the clone:**
- Anywhere on your machine! Examples:
  - `~/projects/fellow`
  - `/opt/claude-plugins/fellow`
  - `C:\Users\YourName\plugins\fellow` (Windows)
- The location doesn't matter because Claude Code installs it from the marketplace

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
# 1. Navigate to where you want to clone (anywhere is fine)
cd ~/Downloads

# 2. Clone Fellow
git clone https://github.com/jingnanzhou/fellow.git
# Output: Cloning into 'fellow'...

# 3. Enter the directory
cd fellow

# 4. Check the structure (optional)
ls -la
# You should see:
# - .claude-plugin/
# - commands/
# - agents/
# - hooks/
# - README.md
# - etc.

# 5. Add as local marketplace
claude plugin marketplace add ./
# Claude Code registers the marketplace...

# 6. Install Fellow from local marketplace
claude plugin marketplace install fellow@local_marketplace
# Claude Code installs the plugin...

# 7. Verify it's installed
claude plugin list
# Output: ✓ fellow@local_marketplace (v2.1.0) - Semantic knowledge extraction...

# 8. Test Fellow commands
claude /build-kb --help
# Should show help for /build-kb command

# 9. You can now delete the clone if you want!
cd ..
rm -rf fellow
# Fellow still works because it was installed to ~/.claude/cache/plugins/fellow/
```

---

## After Publishing (Future)

**Once Fellow is published to the official Claude Code marketplace** (expected: 2-4 weeks after submission), installation becomes simpler:

```bash
# Just one command!
claude plugin install fellow

# No cloning needed!
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
git clone https://github.com/jingnanzhou/fellow.git
cd fellow
claude plugin marketplace add ./
claude plugin marketplace install fellow@local_marketplace

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

### Issue: "Not a valid plugin directory"

**Problem:** You're not in the Fellow directory, or the plugin structure is incorrect

**Solution:**
```bash
# Make sure you're in the fellow directory
cd /path/to/fellow

# Verify .claude-plugin exists
ls .claude-plugin/plugin.json

# If it exists, try again
claude plugin marketplace add ./
claude plugin marketplace install fellow@local_marketplace
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
# Method 1: If you kept the clone
cd /path/to/fellow
git pull origin main
claude plugin marketplace install fellow@local_marketplace  # Reinstall

# Method 2: If you deleted the clone
git clone https://github.com/jingnanzhou/fellow.git
cd fellow
claude plugin marketplace add ./
claude plugin marketplace install fellow@local_marketplace
```

---

## Common Questions

### Q: Where should I clone Fellow?

**A:** Anywhere you want! The location doesn't matter because the marketplace install commands install Fellow to the plugin cache. You can even delete the clone after installation.

**Examples:**
```bash
# Home directory
cd ~
git clone https://github.com/jingnanzhou/fellow.git
cd fellow
claude plugin marketplace add ./
claude plugin marketplace install fellow@local_marketplace

# Projects folder
cd ~/projects
git clone https://github.com/jingnanzhou/fellow.git
cd fellow
claude plugin marketplace add ./
claude plugin marketplace install fellow@local_marketplace

# Temporary location (then delete)
cd /tmp
git clone https://github.com/jingnanzhou/fellow.git
cd fellow
claude plugin marketplace add ./
claude plugin marketplace install fellow@local_marketplace
cd .. && rm -rf fellow  # Delete after installing
```

### Q: Can I install without cloning?

**A:** Not currently. You need to clone the repository and install via local marketplace. After Fellow is published to the official marketplace, you'll be able to install directly with `claude plugin install fellow`.

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

**A:** No, not until Fellow is published to the official marketplace. Use the local marketplace method (`claude plugin marketplace add ./` then `claude plugin marketplace install fellow@local_marketplace`) from a local clone instead.

---

## Summary

**Current Installation (Required Now):**
```bash
git clone https://github.com/jingnanzhou/fellow.git
cd fellow
claude plugin marketplace add ./
claude plugin marketplace install fellow@local_marketplace
```

**Future Installation (After Publishing):**
```bash
claude plugin install fellow
```

**Key Points:**
- Clone location doesn't matter (it gets copied)
- Works in both CLI and VS Code
- Can delete clone after installing
- Update by re-cloning and re-installing

---

**Ready to install Fellow? Follow Method 1 above!**
