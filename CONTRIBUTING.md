# Contributing to Fellow

**Fellow - Architectural Guardrails for Claude Code**

Thank you for your interest in contributing to Fellow! Fellow automatically enriches every Claude Code request to prevent architectural drift and enforce codebase consistency.

This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the problem
- **Expected behavior** vs **actual behavior**
- **Screenshots** if applicable
- **Environment details**: Claude Code version, OS, project type
- **Knowledge base files** if relevant (anonymized if needed)

Use the bug report template when creating an issue.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use cases** - why would this be useful?
- **Proposed solution** - how might this work?
- **Alternatives considered**
- **Examples** from other tools if applicable

Use the feature request template when creating an issue.

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
6. **Push to your fork**
7. **Open a Pull Request**

### Contributing Documentation

Documentation improvements are always welcome! This includes:

- README enhancements
- Command documentation
- Agent documentation
- Examples and tutorials
- Knowledge base format documentation

### Contributing Examples

Real-world examples help others understand how to use Fellow:

- Add examples to the `examples/` directory
- Include a README explaining the example
- Test the example before submitting
- Anonymize any sensitive information

## Development Setup

### Prerequisites

- Claude Code (latest version)
- Git
- A project to test with (or use the examples)

### Installation for Development

1. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/fellow.git
   cd fellow
   ```

2. **Create a test project** (or use existing):
   ```bash
   # Example: Clone a test project
   git clone https://github.com/example/test-project ../test-project
   ```

3. **Test the plugin**:
   ```bash
   # In Claude Code, load the fellow plugin
   # Point it to your cloned fellow directory

   # Test knowledge extraction
   cd ../test-project
   /build-kb

   # Verify outputs in .fellow-data/semantic/
   ls -la .fellow-data/semantic/
   ```

### Testing Changes

#### Test /build-kb Command

```bash
# Navigate to a test project
cd /path/to/test-project

# Run knowledge extraction
/build-kb

# Verify all 4 files created:
# - factual_knowledge.json
# - procedural_knowledge.json
# - conceptual_knowledge.json
# - SEMANTIC_KNOWLEDGE_SUMMARY.md

# Validate JSON structure
cat .fellow-data/semantic/factual_knowledge.json | python -m json.tool > /dev/null
cat .fellow-data/semantic/procedural_knowledge.json | python -m json.tool > /dev/null
cat .fellow-data/semantic/conceptual_knowledge.json | python -m json.tool > /dev/null

# Review markdown summary
less .fellow-data/semantic/SEMANTIC_KNOWLEDGE_SUMMARY.md
```

#### Test /fellow Command

```bash
# Ensure KB exists
/build-kb

# Test context-enriched coding
/fellow Add authentication endpoint with JWT validation

# Verify:
# - Context is loaded from KB
# - Relevant entities/workflows identified
# - Guardrails generated
# - Implementation follows architectural patterns
```

### Adding New Extraction Agents

If you're adding a new type of knowledge extraction:

1. Create agent file in `agents/` directory
2. Follow the existing agent structure (frontmatter + instructions)
3. Define clear extraction objectives
4. Specify JSON output format
5. Add to `/build-kb` command workflow
6. Update README.md

**Agent Template**:

```markdown
---
name: your-knowledge-extractor
description: Brief description of what this extracts
tools: Glob, Grep, Read, Write, TodoWrite
model: sonnet
color: blue
---

# Your Knowledge Extraction Agent

## Objective

[Clear statement of what this extracts]

## What to Extract

[Detailed instructions]

## Analysis Process

[Step-by-step process]

## Output Format

[JSON schema]

## Execution Instructions

[How the agent should run]
```

## Submitting Changes

### Pull Request Process

1. **Update documentation** if you've changed functionality
2. **Add tests/examples** if applicable
3. **Follow the style guidelines**
4. **Write clear commit messages**
5. **Fill out the PR template completely**
6. **Link related issues**

### Commit Message Guidelines

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:

```
feat(build-kb): add support for TypeScript projects

- Add TypeScript-specific entity extraction
- Handle TSX files in conceptual analysis
- Update documentation

Closes #123
```

```
fix(fellow): correct entity matching for nested classes

Entity matching was failing for classes defined inside other classes.
Updated the matching algorithm to handle nested structures.

Fixes #456
```

### Code Review Process

1. **Automated checks** must pass (if configured)
2. **At least one maintainer** must approve
3. **All conversations** must be resolved
4. **Documentation** must be updated
5. **Examples** should be added for new features

## Style Guidelines

### Markdown Files

- Use ATX-style headers (`#`, `##`, `###`)
- Include a table of contents for long documents
- Use code blocks with language specification
- Use relative links for internal references
- Keep lines under 100 characters when reasonable

### Command Files

- Clear frontmatter with description and argument-hint
- Structured sections with clear headers
- Step-by-step execution instructions
- Error handling guidance
- Usage examples

### Agent Files

- Detailed extraction objectives
- Clear analysis process
- Comprehensive output format specification
- Grounding requirements (file, line numbers)
- Examples throughout

### JSON Output

- Valid JSON structure
- Descriptive field names
- Include metadata section
- Include summary section
- Link all knowledge to source code (grounding)

## Community

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

### Recognition

Contributors are recognized in:
- CHANGELOG.md for their contributions
- README.md contributors section (if added)
- Release notes

## Questions?

Don't hesitate to ask questions by opening an issue or discussion. We're here to help!

## License

By contributing to Fellow, you agree that your contributions will be licensed under the Apache License 2.0.

Thank you for contributing! 🎉
