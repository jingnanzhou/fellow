#!/bin/bash
#
# Fellow Documentation Migration Script
#
# This script helps migrate existing documentation to the new MkDocs structure.
#

set -e

echo "==============================================="
echo "Fellow Documentation Migration"
echo "==============================================="
echo ""

# Create docs-site directory structure
echo "Creating documentation structure..."

mkdir -p docs-site/{getting-started,user-guide/{commands,hooks,knowledge-base,logging},features,use-cases,best-practices,reference,contributing,about,assets}

echo "✓ Created directory structure"
echo ""

# Copy and adapt existing documentation
echo "Migrating existing documentation..."

# Copy CHEAT_SHEET.md to reference/
if [ -f "docs/CHEAT_SHEET.md" ]; then
    cp docs/CHEAT_SHEET.md docs-site/reference/cheat-sheet.md
    echo "✓ Migrated: Cheat Sheet"
fi

# Copy INCREMENTAL_UPDATES.md to features/
if [ -f "docs/INCREMENTAL_UPDATES.md" ]; then
    cp docs/INCREMENTAL_UPDATES.md docs-site/features/incremental-updates.md
    echo "✓ Migrated: Incremental Updates"
fi

# Copy MARKETING_BENEFITS.md (can be used for marketing site, not docs)
if [ -f "docs/MARKETING_BENEFITS.md" ]; then
    mkdir -p marketing
    cp docs/MARKETING_BENEFITS.md marketing/MARKETING_BENEFITS.md
    echo "✓ Copied: Marketing Benefits (to marketing/ folder)"
fi

# Create placeholder files for main sections
echo ""
echo "Creating placeholder pages..."

# Create overview pages
cat > docs-site/getting-started/overview.md << 'EOF'
# Getting Started Overview

Welcome to Fellow! This guide will help you get up and running quickly.

## What You'll Learn

- [x] How to install Fellow
- [x] How to build your first knowledge base
- [x] How to use automatic enrichment
- [x] How to update your knowledge base

## Quick Links

- [First Knowledge Base](first-kb.md) - Step-by-step guide
- [Automatic Mode](automatic-mode.md) - Using hooks
- [Manual Mode](manual-mode.md) - Using /fellow command

## Prerequisites

Before getting started, make sure you have:

- Claude Code CLI installed
- Python 3.8+ installed
- A code project to analyze

## Next Steps

Ready to begin? Start with [building your first knowledge base](first-kb.md).
EOF

cat > docs-site/user-guide/commands/overview.md << 'EOF'
# Commands Overview

Fellow provides three main commands for knowledge base management and context enrichment.

## Available Commands

### `/build-kb` - Build Knowledge Base

Extract semantic knowledge from your codebase.

**[Learn more →](build-kb.md)**

### `/fellow` - Manual Enrichment

Explicitly enrich a coding request with semantic knowledge.

**[Learn more →](fellow.md)**

### `/toggle-hooks` - Manage Hooks

Enable or disable automatic context enrichment.

**[Learn more →](toggle-hooks.md)**

## Quick Command Reference

| Command | Purpose | Speed |
|---------|---------|-------|
| `/build-kb` | Initial extraction | 2-5 min |
| `/build-kb --update` | Incremental update | 10-20 sec |
| `/build-kb --full` | Force rebuild | 2-5 min |
| `/fellow <request>` | Manual enrichment | Instant |
| `/toggle-hooks status` | Check hook status | Instant |
| `/toggle-hooks on` | Enable hooks | Instant |
| `/toggle-hooks off` | Disable hooks | Instant |
EOF

cat > docs-site/use-cases/overview.md << 'EOF'
# Use Cases Overview

Fellow solves real problems for real development teams. Here are the most common use cases.

## Common Scenarios

### 🚀 Fast-Growing Startups

Maintain architectural consistency while scaling from 5 to 50 engineers.

**[Read more →](startups.md)**

### 🏢 Enterprise Modernization

Safely evolve legacy systems with AI assistance and architectural guardrails.

**[Read more →](enterprise.md)**

### 🏥 Legacy System Migration

Extract knowledge from 10+ year old codebases and migrate safely.

**[Read more →](legacy-migration.md)**

### 🔓 Open Source Projects

Maintain consistency across distributed contributors.

**[Read more →](open-source.md)**

### 👋 Onboarding New Developers

Cut onboarding time from 12 weeks to 3 weeks.

**[Read more →](onboarding.md)**

## By Role

### For Developers

- Save 2-3 hours/week on context explanation
- Get architecturally-correct suggestions instantly
- Learn codebase patterns faster

### For Engineering Managers

- Onboard developers 70% faster
- Scale team without losing quality
- Reduce senior developer bottlenecks

### For Tech Leads

- Enforce architectural standards automatically
- Reduce code review time by 50%
- Preserve tribal knowledge

### For CTOs

- Move fast without breaking architecture
- Safe AI for legacy systems
- Competitive advantage through velocity + quality
EOF

echo "✓ Created overview pages"
echo ""

# Create reference symlinks or copies
if [ ! -f "docs-site/about/license.md" ]; then
    echo "# License" > docs-site/about/license.md
    echo "" >> docs-site/about/license.md
    echo "Fellow is licensed under the Apache License 2.0." >> docs-site/about/license.md
    echo "" >> docs-site/about/license.md
    cat LICENSE >> docs-site/about/license.md 2>/dev/null || echo "See LICENSE file in repository root."
    echo "✓ Created: License page"
fi

# Create FAQ placeholder
cat > docs-site/about/faq.md << 'EOF'
# Frequently Asked Questions

## General

### What is Fellow?

Fellow is a semantic knowledge extraction and context enrichment plugin for Claude Code. It extracts patterns, workflows, and constraints from your codebase and automatically enriches AI coding requests with relevant context.

### How is Fellow different from Copilot?

Copilot suggests code based on general patterns. Fellow makes AI understand YOUR specific codebase - YOUR patterns, YOUR constraints, YOUR architecture.

### Is Fellow free?

Yes! Fellow is open source under Apache 2.0 license. Free for individuals, teams, and commercial use.

## Installation & Setup

### How do I install Fellow?

Clone the repository - Claude Code will auto-detect it. See [Installation Guide](../installation.md).

### How long does the first extraction take?

2-5 minutes for most projects. Large codebases (200K+ LOC) may take 5-10 minutes.

### Can I use Fellow on multiple projects?

Yes! Each project gets its own knowledge base in `.fellow-data/semantic/`.

## Usage

### Do I need to use a special command every time?

No! By default, hooks are enabled. Fellow automatically enriches coding requests. No manual commands needed.

### What if I want to disable automatic enrichment?

Run `/toggle-hooks off`. You can still use `/fellow` for manual enrichment.

### How do I keep the knowledge base current?

Run `/build-kb --update` after code changes. Takes 10-20 seconds (incremental update).

## Troubleshooting

### Fellow isn't enriching my requests

Check if hooks are enabled: `/toggle-hooks status`. Make sure your request uses coding keywords (add, create, fix, etc.).

### Knowledge base seems outdated

Run `/build-kb --update` to incrementally update based on code changes.

### Can I see what context is being added?

Enable logging: `export FELLOW_LOGGING=1`. Check `.fellow-data/logs/`.

## Privacy & Security

### Where is my code sent?

Nowhere! Fellow runs entirely locally. Your code never leaves your machine.

### What data does Fellow collect?

None. Fellow is open source - audit the code yourself.

### Can I use Fellow on private/proprietary codebases?

Yes! Everything runs locally. No data transmission.

## Advanced

### Can I customize the extraction?

Yes! You can modify extraction agents in `agents/` directory. See [Contributing Guide](../contributing/overview.md).

### Does Fellow support my programming language?

Fellow is language-agnostic. It analyzes code structure regardless of language.

### Can I integrate with CI/CD?

Yes! Run `/build-kb --update` in your CI pipeline. See [CI/CD Integration](../best-practices/cicd.md).

## Still Have Questions?

- **GitHub Issues**: [Report bugs or ask questions](https://github.com/jingnanzhou/fellow/issues)
- **Email**: fellow@example.com
- **Documentation**: Browse this site for detailed guides
EOF

echo "✓ Created: FAQ page"
echo ""

echo "==============================================="
echo "Migration Complete!"
echo "==============================================="
echo ""
echo "Next steps:"
echo "1. Review migrated files in docs-site/"
echo "2. Install dependencies: pip install -r docs-requirements.txt"
echo "3. Preview locally: mkdocs serve"
echo "4. Deploy: mkdocs gh-deploy"
echo ""
echo "Documentation structure created at: docs-site/"
echo "Configuration file: mkdocs.yml"
echo ""
echo "Happy documenting! 📖"
