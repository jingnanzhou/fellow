# MkDocs Deployment Guide

Complete guide for regenerating and publishing Fellow's documentation site to GitHub Pages.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Local Development](#local-development)
4. [Deploying to GitHub Pages](#deploying-to-github-pages)
5. [Troubleshooting](#troubleshooting)
6. [Configuration Reference](#configuration-reference)

---

## Prerequisites

### Required Software

1. **Python 3.8+**
   ```bash
   python3 --version
   ```

2. **uv** (Fast Python package installer)
   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Git**
   ```bash
   git --version
   ```

4. **Virtual Environment** (recommended: use existing `~/genai-env`)
   ```bash
   # Check if genai-env exists
   ls ~/genai-env/bin/activate
   ```

---

## Initial Setup

### Step 1: Activate Virtual Environment

```bash
# Activate your existing virtual environment
source ~/genai-env/bin/activate

# You should see (genai-env) in your prompt
```

### Step 2: Install MkDocs Dependencies

```bash
# Navigate to Fellow project directory
cd /path/to/fellow

# Install MkDocs and Material theme
uv pip install mkdocs mkdocs-material

# Or install from requirements file (if you create one)
uv pip install -r docs-requirements.txt
```

**docs-requirements.txt** (optional, for reproducibility):
```txt
mkdocs>=1.5.3
mkdocs-material>=9.5.3
pymdown-extensions>=10.7
mkdocs-minify-plugin>=0.8.0
```

### Step 3: Verify Installation

```bash
# Check MkDocs is installed
mkdocs --version

# Should output something like:
# mkdocs, version 1.5.3
```

---

## Local Development

### Build and Preview Locally

```bash
# Navigate to project root
cd /path/to/fellow

# Activate virtual environment if not already active
source ~/genai-env/bin/activate

# Build the documentation locally
mkdocs build

# This creates a 'site/' directory with the static HTML
```

### Test Local Site

```bash
# Serve the documentation locally with live reload
mkdocs serve

# Open browser to: http://127.0.0.1:8000
# The site will auto-reload when you edit docs-site/*.md files
```

**Tips:**
- Press `Ctrl+C` to stop the local server
- Any changes to `docs-site/*.md` files will auto-reload
- Check for warnings/errors in terminal output

### Clean Build

```bash
# Remove old build artifacts
rm -rf site/

# Rebuild from scratch
mkdocs build --clean
```

---

## Deploying to GitHub Pages

### Method 1: Quick Deploy (Recommended)

```bash
# Activate virtual environment
source ~/genai-env/bin/activate

# Navigate to project root
cd /path/to/fellow

# Deploy to GitHub Pages (one command!)
mkdocs gh-deploy --force --clean
```

**What this does:**
1. Builds the documentation to `site/`
2. Creates/updates `gh-pages` branch
3. Pushes to GitHub
4. Site goes live at: https://jingnanzhou.github.io/fellow/

**Flags:**
- `--force`: Force push to gh-pages (overwrites existing)
- `--clean`: Clean site directory before building

### Method 2: Step-by-Step Deploy

```bash
# Step 1: Build locally
mkdocs build --clean

# Step 2: Check output
ls -la site/
# Verify index.html exists

# Step 3: Deploy to gh-pages
mkdocs gh-deploy --force
```

### Method 3: Manual Deploy (Advanced)

```bash
# Build the site
mkdocs build --clean

# Create/checkout gh-pages branch
git checkout gh-pages || git checkout --orphan gh-pages

# Remove old files
git rm -rf .

# Copy new files
cp -r site/* .

# Commit and push
git add .
git commit -m "Deploy documentation"
git push origin gh-pages

# Return to main branch
git checkout main
```

---

## Complete Workflow from Scratch

If you need to start completely from scratch:

### Step 1: Clean Everything

```bash
# Navigate to project
cd /path/to/fellow

# Remove old build artifacts
rm -rf site/

# Remove gh-pages branch locally (optional)
git branch -D gh-pages

# Remove gh-pages branch on GitHub (CAREFUL!)
# git push origin --delete gh-pages
```

### Step 2: Verify Configuration

```bash
# Check mkdocs.yml exists and is correct
cat mkdocs.yml | head -20
```

**Critical settings in mkdocs.yml:**
```yaml
site_name: Fellow
site_url: https://jingnanzhou.github.io/fellow
docs_dir: docs-site  # IMPORTANT: Must match your docs directory!
```

### Step 3: Verify Documentation Files

```bash
# Check docs-site directory exists
ls -la docs-site/

# Should see:
# index.md
# quick-start.md
# installation.md
# cli-installation.md
# vscode.md
# ... etc
```

### Step 4: Fresh Build

```bash
# Activate environment
source ~/genai-env/bin/activate

# Clean build
mkdocs build --clean

# Verify index.html was created
ls -la site/index.html
```

### Step 5: Deploy

```bash
# Deploy to GitHub Pages
mkdocs gh-deploy --force --clean
```

### Step 6: Enable GitHub Pages (First Time Only)

1. Go to: https://github.com/jingnanzhou/fellow/settings/pages
2. Under "Source", select: **Deploy from a branch**
3. Under "Branch", select: **gh-pages** and **/ (root)**
4. Click **Save**

### Step 7: Verify Deployment

```bash
# Check gh-pages branch exists
git fetch origin
git branch -r | grep gh-pages

# Check gh-pages branch content
git ls-tree --name-only origin/gh-pages

# Should see:
# index.html
# 404.html
# assets/
# ... etc
```

### Step 8: Access Site

Wait 1-2 minutes for GitHub Pages to propagate, then visit:

**https://jingnanzhou.github.io/fellow/**

---

## Troubleshooting

### Issue 1: 404 Error on GitHub Pages

**Symptoms:**
- Site deployed but shows 404 error
- No index.html in gh-pages branch

**Cause:** Missing `docs_dir` in mkdocs.yml

**Fix:**
```bash
# Check mkdocs.yml
grep docs_dir mkdocs.yml

# Should show:
# docs_dir: docs-site

# If missing, add it:
echo "docs_dir: docs-site" >> mkdocs.yml

# Redeploy
mkdocs gh-deploy --force --clean
```

### Issue 2: "Documentation file not found" Warnings

**Symptoms:**
```
WARNING - A reference to 'some-page.md' is included in the 'nav'
          configuration, but is not found in the documentation files.
```

**Cause:** Navigation in mkdocs.yml references pages that don't exist yet

**Fix:** Either:
1. Create the missing pages in `docs-site/`
2. Remove references from `nav:` section in mkdocs.yml

**Non-Critical:** These warnings don't prevent deployment, just create placeholder links

### Issue 3: No index.html Generated

**Symptoms:**
- `mkdocs build` completes but no index.html

**Cause:** No index.md in docs directory

**Fix:**
```bash
# Check if index.md exists
ls docs-site/index.md

# If missing, create it:
cat > docs-site/index.md << 'EOF'
# Welcome to Fellow

Fellow documentation homepage.
EOF

# Rebuild
mkdocs build --clean
```

### Issue 4: Permission Denied on gh-deploy

**Symptoms:**
```
ERROR   -  Failed to push to GitHub
Permission denied (publickey)
```

**Cause:** Git authentication not configured

**Fix:**
```bash
# Check git remote
git remote -v

# Should use HTTPS or SSH you have access to
# If using HTTPS, you may need a personal access token
# If using SSH, verify your SSH key is added to GitHub

# Test GitHub connection
ssh -T git@github.com
```

### Issue 5: Old Content Still Showing

**Symptoms:**
- Deployed new version but old content still shows

**Cause:** Browser cache or GitHub Pages cache

**Fix:**
```bash
# Hard refresh browser: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

# Force rebuild with --force flag
mkdocs gh-deploy --force --clean

# Wait 2-5 minutes for GitHub Pages to update
```

### Issue 6: Python Module Not Found

**Symptoms:**
```
ModuleNotFoundError: No module named 'mkdocs'
```

**Cause:** Virtual environment not activated or dependencies not installed

**Fix:**
```bash
# Activate virtual environment
source ~/genai-env/bin/activate

# Reinstall dependencies
uv pip install mkdocs mkdocs-material

# Verify installation
mkdocs --version
```

---

## Configuration Reference

### Critical Files

**mkdocs.yml** - Main configuration
```yaml
site_name: Fellow
site_url: https://jingnanzhou.github.io/fellow
docs_dir: docs-site        # Source directory
site_dir: site             # Build output (default)
theme:
  name: material
```

**docs-site/** - Documentation source files
```
docs-site/
├── index.md              # Homepage (required!)
├── quick-start.md
├── installation.md
├── about/
│   ├── faq.md
│   └── license.md
└── ... other pages
```

**site/** - Generated static site (auto-generated, don't edit!)
```
site/
├── index.html            # Generated from index.md
├── quick-start/
│   └── index.html
└── ... other pages
```

### Key mkdocs.yml Settings

```yaml
# Essential
site_name: Fellow                                    # Site title
site_url: https://jingnanzhou.github.io/fellow      # Base URL
docs_dir: docs-site                                  # Source directory

# Repository
repo_name: jingnanzhou/fellow
repo_url: https://github.com/jingnanzhou/fellow

# Theme
theme:
  name: material                                     # Material Design theme
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.tabs                                # Top-level tabs
    - navigation.instant                             # Fast loading
    - search.suggest                                 # Search suggestions

# Navigation (optional but recommended)
nav:
  - Home: index.md
  - Quick Start: quick-start.md
  - Installation: installation.md
  # ... more pages
```

---

## Automation with GitHub Actions (Optional)

For automatic deployment on every push:

**Create:** `.github/workflows/docs.yml`
```yaml
name: Deploy Documentation

on:
  push:
    branches:
      - main
    paths:
      - 'docs-site/**'
      - 'mkdocs.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: 3.x

      - run: pip install mkdocs mkdocs-material

      - run: mkdocs gh-deploy --force --clean
```

**Benefits:**
- Automatic deployment on every push to main
- No manual deployment needed
- Consistent build environment

---

## Quick Reference

### Common Commands

```bash
# Preview locally
mkdocs serve

# Build locally
mkdocs build

# Clean build
mkdocs build --clean

# Deploy to GitHub Pages
mkdocs gh-deploy --force --clean

# Check for errors
mkdocs build --strict
```

### File Locations

- Configuration: `mkdocs.yml`
- Source docs: `docs-site/*.md`
- Generated site: `site/` (don't commit!)
- GitHub Pages: `gh-pages` branch

### URLs

- Local preview: http://127.0.0.1:8000
- Production site: https://jingnanzhou.github.io/fellow/
- GitHub Pages settings: https://github.com/jingnanzhou/fellow/settings/pages

---

## Best Practices

1. **Always activate virtual environment first**
   ```bash
   source ~/genai-env/bin/activate
   ```

2. **Test locally before deploying**
   ```bash
   mkdocs serve
   # Check http://127.0.0.1:8000
   ```

3. **Use clean builds for production**
   ```bash
   mkdocs gh-deploy --force --clean
   ```

4. **Don't commit site/ directory**
   - Already in .gitignore
   - Generated fresh each build

5. **Keep docs-site/ organized**
   - Use subdirectories for sections
   - Match navigation structure in mkdocs.yml

6. **Review warnings**
   - Missing page warnings are OK if pages are planned
   - Fix broken internal links

---

## Summary: Deploy in 3 Steps

For quick reference, here's the minimal deployment workflow:

```bash
# 1. Activate environment
source ~/genai-env/bin/activate

# 2. Navigate to project
cd /path/to/fellow

# 3. Deploy!
mkdocs gh-deploy --force --clean
```

**That's it!** Your documentation will be live at:
**https://jingnanzhou.github.io/fellow/**

---

**Last Updated:** 2026-01-05
**MkDocs Version:** 1.5.3+
**Material Theme:** 9.5.3+
