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

# Step 3: Install Fellow from current directory
claude plugin add ./

# Step 4: Verify installation
claude plugin list
```

**Expected output:**
```
✓ fellow (v2.1.0) - Semantic knowledge extraction and context enrichment
```

**What this does:**
1. `claude plugin add ./` reads the `.claude-plugin/plugin.json` file
2. Copies the entire `fellow/` directory to `~/.claude/cache/plugins/fellow/`
3. Registers Fellow in `~/.claude/settings.json`
4. Enables Fellow automatically

**Where you can put the clone:**
- Anywhere on your machine! Examples:
  - `~/projects/fellow`
  - `/opt/claude-plugins/fellow`
  - `C:\Users\YourName\plugins\fellow` (Windows)
- The location doesn't matter because Claude Code **copies** it to the plugin cache

### Method 2: Install Directly from Git URL

If you don't want to manually clone, let Claude Code do it:

```bash
# Claude Code will clone and install automatically
claude plugin add https://github.com/jingnanzhou/fellow.git

# Verify
claude plugin list
```

**What this does:**
1. Claude Code clones the repository to a temporary location
2. Reads the plugin manifest
3. Copies to `~/.claude/cache/plugins/fellow/`
4. Registers and enables Fellow

**Advantage:** No manual git clone needed!

### Method 3: Temporary Testing (No Installation)

If you just want to test Fellow without installing:

```bash
# Clone repository
git clone https://github.com/jingnanzhou/fellow.git
cd fellow

# Run Claude with Fellow for this session only
claude --plugin-dir ./fellow
```

**What this does:**
- Loads Fellow for the current session only
- Does NOT copy to plugin cache
- Does NOT persist after you close Claude
- Useful for testing or development

---

## Understanding Plugin Installation

### Where Does Fellow Get Installed?

After running `claude plugin add ./`, Fellow is copied to:

| OS | Location |
|----|----------|
| **macOS** | `~/.claude/cache/plugins/fellow/` |
| **Linux** | `~/.claude/cache/plugins/fellow/` |
| **Windows** | `%APPDATA%\ClaudeCode\cache\plugins\fellow\` |

**Important:** The original clone location doesn't matter after installation! Claude Code copies Fellow to its own plugin cache.

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

# 5. Install Fellow
claude plugin add ./
# Claude Code processes the plugin...

# 6. Verify it's installed
claude plugin list
# Output: ✓ fellow (v2.1.0) - Semantic knowledge extraction...

# 7. Test Fellow commands
claude /build-kb --help
# Should show help for /build-kb command

# 8. You can now delete the clone if you want!
cd ..
rm -rf fellow
# Fellow still works because it was copied to ~/.claude/cache/plugins/fellow/
```

---

## After Publishing (Future)

**Once Fellow is published to the official Claude Code marketplace** (expected: 2-4 weeks after submission), installation becomes simpler:

```bash
# Just one command!
claude plugin add fellow

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
claude plugin add ./

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
claude plugin add ./
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
claude plugin add ./  # Reinstall

# Method 2: If you deleted the clone
git clone https://github.com/jingnanzhou/fellow.git
cd fellow
claude plugin add ./  # Reinstall
```

---

## Common Questions

### Q: Where should I clone Fellow?

**A:** Anywhere you want! The location doesn't matter because `claude plugin add ./` **copies** Fellow to the plugin cache. You can even delete the clone after installation.

**Examples:**
```bash
# Home directory
cd ~
git clone https://github.com/jingnanzhou/fellow.git
cd fellow && claude plugin add ./

# Projects folder
cd ~/projects
git clone https://github.com/jingnanzhou/fellow.git
cd fellow && claude plugin add ./

# Temporary location (then delete)
cd /tmp
git clone https://github.com/jingnanzhou/fellow.git
cd fellow && claude plugin add ./
cd .. && rm -rf fellow  # Delete after installing
```

### Q: Can I install without cloning?

**A:** Yes! Use the Git URL method:
```bash
claude plugin add https://github.com/jingnanzhou/fellow.git
```

### Q: How do I uninstall Fellow?

**A:**
```bash
# Remove Fellow
claude plugin remove fellow

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

### Q: Will `/plugin install fellow` work now?

**A:** No, not until Fellow is published to the marketplace. Use `claude plugin add ./` from a local clone instead.

---

## Summary

**Current Installation (Required Now):**
```bash
git clone https://github.com/jingnanzhou/fellow.git
cd fellow
claude plugin add ./
```

**Future Installation (After Publishing):**
```bash
claude plugin add fellow
```

**Key Points:**
- Clone location doesn't matter (it gets copied)
- Works in both CLI and VS Code
- Can delete clone after installing
- Update by re-cloning and re-installing

---

**Ready to install Fellow? Follow Method 1 above!**
