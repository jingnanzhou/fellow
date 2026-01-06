# Documentation Summary

This document provides an overview of all documentation resources for Fellow and how to work with them.

## 📚 Live Documentation Site

**Main Site:** https://jingnanzhou.github.io/fellow/

The documentation site is built with MkDocs Material and deployed to GitHub Pages.

### Available Pages

- **Home** - Overview and key features
- **Quick Start** - Getting started guide with two options (pre-build or auto-build)
- **Installation** - Complete installation instructions
- **CLI Installation** - How to install Claude Code CLI
- **VS Code** - VS Code extension integration guide
- **Getting Started** - Tutorial section
- **User Guide** - Commands and usage
- **Features** - Incremental updates and more
- **Use Cases** - Usage scenarios
- **Reference** - Cheat sheet and configuration
- **About** - License and FAQ

## 📝 Documentation Source Files

### Location

All documentation source files are in: **`docs-site/`**

```
docs-site/
├── index.md              # Homepage
├── quick-start.md        # Quick start guide
├── installation.md       # Installation instructions
├── cli-installation.md   # CLI installation guide
├── vscode.md            # VS Code integration
├── getting-started/
│   └── overview.md
├── user-guide/
│   └── commands/
│       └── overview.md
├── features/
│   └── incremental-updates.md
├── use-cases/
│   └── overview.md
├── reference/
│   └── cheat-sheet.md
└── about/
    ├── faq.md
    └── license.md
```

### Editing Documentation

1. Edit markdown files in `docs-site/`
2. Preview locally: `mkdocs serve`
3. Deploy: `mkdocs gh-deploy --force --clean`

## 🛠️ Working with MkDocs

### Quick Commands

```bash
# Preview locally
source ~/genai-env/bin/activate
mkdocs serve
# Visit: http://127.0.0.1:8000

# Deploy to GitHub Pages
mkdocs gh-deploy --force --clean
# Live at: https://jingnanzhou.github.io/fellow/
```

### Documentation Guides

1. **[MKDOCS-DEPLOYMENT-GUIDE.md](MKDOCS-DEPLOYMENT-GUIDE.md)**
   - Complete guide for regenerating and publishing documentation
   - Prerequisites, setup, troubleshooting
   - From scratch instructions
   - ~450 lines, comprehensive

2. **[DOCS-QUICK-REFERENCE.md](DOCS-QUICK-REFERENCE.md)**
   - Quick reference card
   - Common commands
   - Daily workflow
   - ~100 lines, concise

## 📖 Other Documentation Files

### Installation & Setup

- **[README.md](README.md)** - Main project documentation
- **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation guide
- **[HOW-TO-INSTALL-NOW.md](HOW-TO-INSTALL-NOW.md)** - Current installation method (local clone)
- **[PUBLISHING-TO-MARKETPLACE.md](PUBLISHING-TO-MARKETPLACE.md)** - Guide for publishing to Claude marketplace

### Features & Guides

- **[AUTO-BUILD-FEATURE.md](AUTO-BUILD-FEATURE.md)** - Auto-build enhancement documentation
- **[ENHANCEMENT-AUTO-BUILD-SUMMARY.md](ENHANCEMENT-AUTO-BUILD-SUMMARY.md)** - Auto-build implementation summary
- **[MESSAGE-DISPLAY-MECHANISM.md](MESSAGE-DISPLAY-MECHANISM.md)** - How hooks/commands display messages

### Quick References

- **[docs/CHEAT_SHEET.md](docs/CHEAT_SHEET.md)** - Command reference
- **[docs/INCREMENTAL_UPDATES.md](docs/INCREMENTAL_UPDATES.md)** - Incremental update guide

### Command Documentation

Located in `commands/`:
- **[build-kb.md](commands/build-kb.md)** - Knowledge base building
- **[fellow.md](commands/fellow.md)** - Context enrichment command
- **[toggle-hooks.md](commands/toggle-hooks.md)** - Hook management

### Agent Documentation

Located in `agents/`:
- **[factual-knowledge-extractor.md](agents/factual-knowledge-extractor.md)** - Entity extraction
- **[procedural-knowledge-extractor.md](agents/procedural-knowledge-extractor.md)** - Workflow extraction
- **[conceptual-knowledge-extractor.md](agents/conceptual-knowledge-extractor.md)** - Architecture extraction

## 🔧 Configuration Files

### MkDocs Configuration

**File:** `mkdocs.yml`

Key settings:
```yaml
site_name: Fellow
site_url: https://jingnanzhou.github.io/fellow
docs_dir: docs-site        # IMPORTANT: Points to source directory
theme:
  name: material
```

### Plugin Configuration

**File:** `.claude-plugin/plugin.json`

Defines:
- Plugin metadata
- Commands
- Hooks
- Agents

## 🚀 Deployment Workflow

### Method 1: Quick Deploy (Most Common)

```bash
# 1. Activate virtual environment
source ~/genai-env/bin/activate

# 2. Navigate to project
cd /path/to/fellow

# 3. Deploy
mkdocs gh-deploy --force --clean
```

### Method 2: Test Then Deploy

```bash
# 1. Activate environment
source ~/genai-env/bin/activate

# 2. Test locally
mkdocs serve
# Open http://127.0.0.1:8000 and verify changes

# 3. Deploy
mkdocs gh-deploy --force --clean
```

### Method 3: From Scratch

See **[MKDOCS-DEPLOYMENT-GUIDE.md](MKDOCS-DEPLOYMENT-GUIDE.md)** for complete from-scratch instructions.

## 📋 Checklist for Documentation Updates

- [ ] Edit markdown files in `docs-site/`
- [ ] Test locally with `mkdocs serve`
- [ ] Verify all links work
- [ ] Check for broken references
- [ ] Deploy with `mkdocs gh-deploy --force --clean`
- [ ] Wait 1-2 minutes for GitHub Pages to update
- [ ] Verify changes at https://jingnanzhou.github.io/fellow/
- [ ] Commit and push source changes to main branch

## 🔍 Finding Documentation

### By Topic

- **Installation:** README.md, INSTALLATION.md, docs-site/installation.md
- **Quick Start:** README.md, docs-site/quick-start.md
- **Commands:** commands/*.md, docs-site/user-guide/commands/overview.md
- **Features:** docs-site/features/*, AUTO-BUILD-FEATURE.md
- **Deployment:** MKDOCS-DEPLOYMENT-GUIDE.md, DOCS-QUICK-REFERENCE.md
- **Contributing:** CONTRIBUTING.md

### By Format

- **Web (HTML):** https://jingnanzhou.github.io/fellow/
- **Markdown (Source):** docs-site/*.md, *.md files in root
- **Command Specs:** commands/*.md (command documentation)
- **Agent Specs:** agents/*.md (agent documentation)

## 🆘 Troubleshooting

### Common Issues

1. **404 Error on GitHub Pages**
   - Check `mkdocs.yml` has `docs_dir: docs-site`
   - Verify index.html was generated in `site/`
   - Redeploy with `--force --clean` flags

2. **Missing Pages**
   - Check file exists in `docs-site/`
   - Verify path in `mkdocs.yml` nav section
   - Rebuild and redeploy

3. **Module Not Found**
   - Activate virtual environment: `source ~/genai-env/bin/activate`
   - Install dependencies: `uv pip install mkdocs mkdocs-material`

4. **Old Content Showing**
   - Hard refresh browser: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
   - Wait 2-5 minutes for GitHub Pages cache
   - Redeploy with `--force` flag

See **[MKDOCS-DEPLOYMENT-GUIDE.md](MKDOCS-DEPLOYMENT-GUIDE.md)** for complete troubleshooting guide.

## 📦 Documentation Dependencies

```txt
mkdocs>=1.5.3
mkdocs-material>=9.5.3
pymdown-extensions>=10.7
mkdocs-minify-plugin>=0.8.0
```

Install with:
```bash
source ~/genai-env/bin/activate
uv pip install mkdocs mkdocs-material
```

## 🔗 Key Links

- **Live Site:** https://jingnanzhou.github.io/fellow/
- **GitHub Repository:** https://github.com/jingnanzhou/fellow
- **GitHub Pages Settings:** https://github.com/jingnanzhou/fellow/settings/pages
- **Issues:** https://github.com/jingnanzhou/fellow/issues

## 📚 Documentation Resources

### Internal Guides
- MKDOCS-DEPLOYMENT-GUIDE.md - Complete deployment guide
- DOCS-QUICK-REFERENCE.md - Quick command reference
- DOCUMENTATION-SUMMARY.md - This file

### External Resources
- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages](https://pages.github.com/)

---

**Last Updated:** 2026-01-05
**Site URL:** https://jingnanzhou.github.io/fellow/
**Repository:** https://github.com/jingnanzhou/fellow
