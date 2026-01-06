# Installing Claude Code CLI

This guide explains how to install the Claude Code CLI, which is required for installing and managing plugins like Fellow.

## Why Install the CLI?

!!! important "CLI Required for Plugins"
    Even if you only plan to use VS Code, you **need the Claude Code CLI** to install plugins. The VS Code extension does not include plugin installation capabilities.

**What you need the CLI for:**
- ✅ Installing plugins (like Fellow)
- ✅ Managing plugin configuration
- ✅ Configuring MCP servers
- ✅ Using Claude Code in terminal

**What you don't need the CLI for:**
- Using the VS Code extension for basic conversations
- Code generation and editing in VS Code
- @-mentioning files in VS Code

## Installation by Operating System

### macOS

**Method 1: Homebrew (Recommended)**

```bash
# Install using Homebrew
brew install claude

# Verify installation
claude --version
```

**Method 2: Download Installer**

1. Visit https://code.claude.com
2. Download the macOS installer
3. Run the `.pkg` installer
4. Verify installation:
   ```bash
   claude --version
   ```

### Linux

**Method 1: Install Script (Recommended)**

```bash
# Download and run installer
curl -fsSL https://code.claude.com/install.sh | sh

# Verify installation
claude --version
```

**Method 2: Manual Download**

1. Visit https://code.claude.com
2. Download the Linux installer for your distribution
3. Follow installation instructions
4. Verify installation:
   ```bash
   claude --version
   ```

### Windows

**Method 1: winget**

```powershell
# Install using Windows Package Manager
winget install Anthropic.ClaudeCode

# Verify installation
claude --version
```

**Method 2: Download Installer**

1. Visit https://code.claude.com
2. Download the Windows installer
3. Run the `.exe` installer
4. Verify installation in PowerShell:
   ```powershell
   claude --version
   ```

## Verification

After installation, verify the CLI is working:

```bash
# Check version
claude --version

# Check help
claude --help

# Try listing plugins (should be empty initially)
claude plugin list
```

Expected output:
```
Claude Code CLI v1.2.3
```

## Post-Installation Setup

### Authentication

The first time you run Claude Code, you'll need to authenticate:

```bash
# Start Claude Code (will prompt for authentication)
claude

# Or authenticate explicitly
claude auth login
```

Follow the prompts to authenticate with your Anthropic account.

### Configuration

Claude Code stores configuration in:

| OS | Location |
|----|----------|
| **macOS/Linux** | `~/.claude/settings.json` |
| **Windows** | `%APPDATA%\ClaudeCode\settings.json` |

### Plugin Directory

Installed plugins are stored in:

| OS | Location |
|----|----------|
| **macOS/Linux** | `~/.claude/cache/plugins/` |
| **Windows** | `%APPDATA%\ClaudeCode\cache\plugins\` |

## Installing Fellow After CLI Setup

Once the CLI is installed, you can install Fellow:

```bash
# Clone Fellow repository
git clone https://github.com/jingnanzhou/fellow.git
cd fellow

# Add as local marketplace
claude plugin marketplace add ./

# Install Fellow from local marketplace
claude plugin marketplace install fellow@local_marketplace

# Verify Fellow is installed
claude plugin list
```

See the [Installation Guide](installation.md) for detailed Fellow installation instructions.

## Using with VS Code

After installing the CLI and Fellow:

1. **Install VS Code extension:**
   - Open VS Code
   - Go to Extensions (`Cmd+Shift+X` or `Ctrl+Shift+X`)
   - Search "Claude Code"
   - Click Install

2. **Fellow automatically works in VS Code:**
   - No additional setup needed!
   - All Fellow commands available in VS Code
   - Hooks work identically

See the [VS Code Integration Guide](vscode.md) for details.

## Troubleshooting

### Issue: "claude: command not found"

**Problem:** The CLI is not in your PATH

**Solution (macOS/Linux):**
```bash
# Check if claude is installed
which claude

# If not found, add to PATH (example for bash)
echo 'export PATH="$PATH:/usr/local/bin"' >> ~/.bashrc
source ~/.bashrc

# Or for zsh
echo 'export PATH="$PATH:/usr/local/bin"' >> ~/.zshrc
source ~/.zshrc
```

**Solution (Windows):**
1. Search for "Environment Variables" in Start menu
2. Edit "Path" variable
3. Add Claude Code installation directory
4. Restart terminal

### Issue: Permission denied

**Problem:** Insufficient permissions during installation

**Solution (macOS/Linux):**
```bash
# Use sudo for system-wide installation
sudo brew install claude

# Or use user-local installation
brew install claude --user
```

### Issue: Version outdated

**Problem:** Old version of Claude Code CLI

**Solution:**
```bash
# macOS (Homebrew)
brew upgrade claude

# Linux
curl -fsSL https://code.claude.com/install.sh | sh

# Windows
winget upgrade Anthropic.ClaudeCode
```

## Updating Claude Code CLI

To update to the latest version:

### macOS
```bash
brew upgrade claude
```

### Linux
```bash
curl -fsSL https://code.claude.com/install.sh | sh
```

### Windows
```powershell
winget upgrade Anthropic.ClaudeCode
```

## Uninstalling

To remove Claude Code CLI:

### macOS
```bash
brew uninstall claude
```

### Linux
```bash
# Remove binary
sudo rm /usr/local/bin/claude

# Remove configuration (optional)
rm -rf ~/.claude
```

### Windows
```powershell
# Uninstall via Windows Settings
# Or use winget
winget uninstall Anthropic.ClaudeCode
```

## Next Steps

After installing the CLI:

1. **[Install Fellow](installation.md)** - Install the Fellow plugin
2. **[Quick Start Guide](quick-start.md)** - Build your first knowledge base
3. **[VS Code Integration](vscode.md)** - Use Fellow in VS Code (optional)

## Resources

- **Claude Code Website**: https://code.claude.com
- **CLI Documentation**: https://code.claude.com/docs/en/cli.md
- **Installation Help**: https://code.claude.com/docs/en/installation.md

---

<p align="center">
  <strong>CLI installed? Ready to install Fellow!</strong>
</p>
