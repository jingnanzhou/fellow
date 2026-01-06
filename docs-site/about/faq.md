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
