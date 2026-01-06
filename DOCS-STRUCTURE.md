# Documentation Structure

Visual overview of Fellow's documentation organization.

## 🌐 Live Documentation Site

```
https://jingnanzhou.github.io/fellow/
├── Home (index.md)
├── Quick Start (quick-start.md)
├── Installation (installation.md)
├── CLI Installation (cli-installation.md)
├── VS Code (vscode.md)
├── Getting Started/
│   └── Overview
├── User Guide/
│   └── Commands/
│       └── Overview
├── Features/
│   └── Incremental Updates
├── Use Cases/
│   └── Overview
├── Reference/
│   └── Cheat Sheet
└── About/
    ├── FAQ
    └── License
```

**Deployed from:** `docs-site/` directory
**Configuration:** `mkdocs.yml`
**Deployment:** GitHub Pages (`gh-pages` branch)

---

## 📁 Documentation Files Organization

```
fellow/
│
├── 📘 User Documentation
│   ├── README.md                          # Main project overview
│   ├── INSTALLATION.md                    # Complete installation guide
│   ├── HOW-TO-INSTALL-NOW.md             # Current installation method
│   ├── PUBLISHING-TO-MARKETPLACE.md       # Publishing guide
│   └── docs/
│       ├── CHEAT_SHEET.md                # Command reference
│       └── INCREMENTAL_UPDATES.md        # Incremental update guide
│
├── 🌐 Documentation Site Source
│   ├── mkdocs.yml                         # MkDocs configuration
│   └── docs-site/                         # Site source files
│       ├── index.md                       # Homepage
│       ├── quick-start.md
│       ├── installation.md
│       ├── cli-installation.md
│       ├── vscode.md
│       ├── getting-started/
│       │   └── overview.md
│       ├── user-guide/
│       │   └── commands/
│       │       └── overview.md
│       ├── features/
│       │   └── incremental-updates.md
│       ├── use-cases/
│       │   └── overview.md
│       ├── reference/
│       │   └── cheat-sheet.md
│       └── about/
│           ├── faq.md
│           └── license.md
│
├── 🔧 Documentation Guides (For Contributors)
│   ├── MKDOCS-DEPLOYMENT-GUIDE.md        # Complete deployment guide
│   ├── DOCS-QUICK-REFERENCE.md           # Quick command reference
│   ├── DOCUMENTATION-SUMMARY.md          # Overview (what you're reading)
│   └── DOCS-STRUCTURE.md                 # This file
│
├── 💡 Feature Documentation
│   ├── AUTO-BUILD-FEATURE.md             # Auto-build feature docs
│   ├── ENHANCEMENT-AUTO-BUILD-SUMMARY.md # Auto-build summary
│   └── MESSAGE-DISPLAY-MECHANISM.md      # Hook/command messages
│
├── ⚙️ Command Documentation
│   └── commands/
│       ├── build-kb.md                   # /build-kb command
│       ├── fellow.md                     # /fellow command
│       └── toggle-hooks.md               # /toggle-hooks command
│
└── 🤖 Agent Documentation
    └── agents/
        ├── factual-knowledge-extractor.md      # Entity extraction
        ├── procedural-knowledge-extractor.md   # Workflow extraction
        └── conceptual-knowledge-extractor.md   # Architecture extraction
```

---

## 🎯 Documentation by Audience

### For End Users (Installing/Using Fellow)

**Start Here:**
1. **README.md** - Overview and quick start
2. **INSTALLATION.md** - How to install
3. **docs-site/** (via https://jingnanzhou.github.io/fellow/) - Complete guides

**Quick References:**
- docs/CHEAT_SHEET.md - Command reference
- docs/INCREMENTAL_UPDATES.md - Update guide

**Features:**
- AUTO-BUILD-FEATURE.md - Auto-build capability
- MESSAGE-DISPLAY-MECHANISM.md - How messages work

### For Contributors (Developing Fellow)

**Start Here:**
1. **CONTRIBUTING.md** - Contribution guidelines
2. **commands/*.md** - Command specifications
3. **agents/*.md** - Agent specifications

**Development:**
- Command docs in `commands/`
- Agent docs in `agents/`
- Feature docs in root

### For Documentation Maintainers

**Start Here:**
1. **DOCS-QUICK-REFERENCE.md** - Quick commands
2. **MKDOCS-DEPLOYMENT-GUIDE.md** - Complete guide
3. **DOCUMENTATION-SUMMARY.md** - Overview

**Working with Docs:**
- Edit: `docs-site/*.md`
- Config: `mkdocs.yml`
- Deploy: `mkdocs gh-deploy --force --clean`
- View: https://jingnanzhou.github.io/fellow/

---

## 🔄 Documentation Workflow

### Creating New Documentation

```
1. Write markdown file
   ├── For site: docs-site/new-page.md
   └── For reference: new-doc.md (root)

2. Update navigation (if for site)
   └── Edit mkdocs.yml nav section

3. Test locally
   └── mkdocs serve

4. Deploy
   └── mkdocs gh-deploy --force --clean

5. Commit source
   └── git add . && git commit -m "Add documentation"
```

### Updating Existing Documentation

```
1. Edit file
   ├── Site docs: docs-site/*.md
   └── Reference: *.md

2. Test locally (if site doc)
   └── mkdocs serve

3. Deploy (if site doc)
   └── mkdocs gh-deploy --force --clean

4. Commit
   └── git add . && git commit -m "Update docs"
```

---

## 📋 Documentation Types

### 1. User-Facing Documentation

**Location:** docs-site/ (deployed to web)
**Format:** Markdown → HTML via MkDocs
**Audience:** End users
**Examples:** Installation guide, quick start, tutorials

### 2. Reference Documentation

**Location:** Root *.md files, docs/ directory
**Format:** Markdown (GitHub-rendered)
**Audience:** Users reading on GitHub
**Examples:** README, INSTALLATION.md, CHEAT_SHEET.md

### 3. Developer Documentation

**Location:** commands/, agents/
**Format:** Markdown specifications
**Audience:** Contributors, Claude Code
**Examples:** Command specs, agent specs

### 4. Internal Documentation

**Location:** Root *.md files
**Format:** Markdown
**Audience:** Developers, maintainers
**Examples:** Feature docs, deployment guides

---

## 🚀 Quick Actions

### Deploy Documentation

```bash
source ~/genai-env/bin/activate
mkdocs gh-deploy --force --clean
```

### Preview Documentation

```bash
source ~/genai-env/bin/activate
mkdocs serve
# Visit: http://127.0.0.1:8000
```

### Check Documentation

```bash
mkdocs build --strict  # Fail on warnings
```

### Find Documentation

- **Online:** https://jingnanzhou.github.io/fellow/
- **Source:** docs-site/*.md
- **Reference:** *.md files in root
- **Commands:** commands/*.md
- **Agents:** agents/*.md

---

## 📊 Documentation Statistics

### Documentation Site
- **Pages:** ~15 (and growing)
- **Sections:** 7 major sections
- **Format:** MkDocs Material
- **URL:** https://jingnanzhou.github.io/fellow/

### Reference Documentation
- **Root .md files:** ~15 files
- **Command docs:** 3 files
- **Agent docs:** 3 files
- **Total lines:** ~5,000+ lines

---

## 🔗 Key Resources

### Guides
- **[MKDOCS-DEPLOYMENT-GUIDE.md](MKDOCS-DEPLOYMENT-GUIDE.md)** - How to deploy docs
- **[DOCS-QUICK-REFERENCE.md](DOCS-QUICK-REFERENCE.md)** - Quick commands
- **[DOCUMENTATION-SUMMARY.md](DOCUMENTATION-SUMMARY.md)** - Complete overview

### Configuration
- **mkdocs.yml** - Site configuration
- **.claude-plugin/plugin.json** - Plugin configuration

### Live Sites
- **Documentation:** https://jingnanzhou.github.io/fellow/
- **Repository:** https://github.com/jingnanzhou/fellow

---

**This structure enables:**
- ✅ Easy navigation for users
- ✅ Clear separation of concerns
- ✅ Simple contribution workflow
- ✅ Automated deployment
- ✅ Version control for everything
