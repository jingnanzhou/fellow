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
