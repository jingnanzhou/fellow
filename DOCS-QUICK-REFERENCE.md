# Documentation Quick Reference

Quick commands for working with Fellow's MkDocs documentation.

## Prerequisites

```bash
# Ensure virtual environment is active
source ~/genai-env/bin/activate

# Ensure MkDocs is installed
uv pip install mkdocs mkdocs-material
```

## Daily Workflow

### Preview Changes Locally

```bash
cd /path/to/fellow
source ~/genai-env/bin/activate
mkdocs serve
```

Open: http://127.0.0.1:8000

Press `Ctrl+C` to stop.

### Deploy to GitHub Pages

```bash
cd /path/to/fellow
source ~/genai-env/bin/activate
mkdocs gh-deploy --force --clean
```

Site live at: https://jingnanzhou.github.io/fellow/

## Common Tasks

### Build Locally Only

```bash
mkdocs build --clean
# Output: site/
```

### Check for Errors

```bash
mkdocs build --strict
# Fails on any warnings
```

### Clean Everything

```bash
rm -rf site/
mkdocs build
```

## File Structure

```
fellow/
├── mkdocs.yml           # Configuration
├── docs-site/           # Source markdown files
│   ├── index.md        # Homepage (required!)
│   ├── quick-start.md
│   └── ...
└── site/               # Generated (don't edit!)
    ├── index.html
    └── ...
```

## Troubleshooting

### 404 Error

Check `mkdocs.yml` has:
```yaml
docs_dir: docs-site
```

### Missing index.html

Ensure `docs-site/index.md` exists.

### Module Not Found

```bash
source ~/genai-env/bin/activate
uv pip install mkdocs mkdocs-material
```

## Full Guide

See: **MKDOCS-DEPLOYMENT-GUIDE.md** for complete documentation.
