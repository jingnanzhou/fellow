# Publishing Fellow to Claude Code Marketplace

This guide explains how to publish Fellow (or fork Fellow) to the Claude Code plugin marketplace for distribution.

## Overview

Claude Code has a marketplace system for distributing plugins. There are two types of marketplaces:

1. **Official Anthropic Marketplace** - Curated plugins vetted by Anthropic
2. **Custom Marketplaces** - Self-hosted plugin collections for teams/organizations

## Publishing to Official Marketplace

### Requirements

To be accepted into the official Claude Code marketplace, your plugin must meet these requirements:

**Technical Requirements:**
- ✅ Valid `plugin.json` manifest with all required fields
- ✅ Proper directory structure (`.claude-plugin/`, `commands/`, `agents/`, etc.)
- ✅ All components tested and working
- ✅ No security vulnerabilities
- ✅ Compatible with latest Claude Code version
- ✅ Documentation (README.md, usage examples)

**Quality Requirements:**
- ✅ Solves a real problem for Claude Code users
- ✅ Provides clear value over existing solutions
- ✅ Well-documented with examples
- ✅ Actively maintained
- ✅ Open source license (Apache 2.0, MIT, etc.)

### Submission Process

**Step 1: Prepare Your Plugin**

Ensure your plugin meets all requirements:

```bash
# Validate plugin structure
claude plugin validate .

# Test locally
claude --plugin-dir .

# Run your plugin's test suite
# (add tests if you don't have them)
```

**Step 2: Create GitHub Repository**

Fellow is already on GitHub at `github.com/jingnanzhou/fellow`

Ensure your repository includes:
- ✅ Clear README.md with installation and usage
- ✅ LICENSE file (Apache 2.0 for Fellow)
- ✅ CHANGELOG.md with version history
- ✅ CONTRIBUTING.md for contributors
- ✅ Examples and documentation
- ✅ GitHub releases for version tags

**Step 3: Submit to Anthropic**

Contact Anthropic to submit your plugin for official marketplace inclusion:

1. **Via GitHub**: Open an issue at `github.com/anthropics/claude-code` requesting marketplace addition
2. **Via Email**: Contact plugins@anthropic.com with:
   - Plugin name and description
   - GitHub repository URL
   - Why your plugin should be in the marketplace
   - Screenshots or demo video

**Step 4: Review Process**

Anthropic will review your plugin for:
- Security vulnerabilities
- Code quality
- Documentation completeness
- User value
- Uniqueness

**Expected timeline**: 2-4 weeks for review

**Step 5: Marketplace Listing**

Once approved, your plugin will be listed in the official marketplace:

```bash
# Users can install with:
/plugin install fellow

# Or discover it via:
/plugin search knowledge
/plugin search semantic
```

## Creating a Custom Marketplace

For teams or organizations that want to distribute plugins internally or publicly, you can create a custom marketplace.

### Custom Marketplace Structure

**Repository structure:**

```
my-claude-plugins/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace catalog
├── plugins/
│   ├── fellow/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── commands/
│   │   └── ...
│   ├── code-formatter/
│   │   └── ...
│   └── deployment-tools/
│       └── ...
├── README.md
└── LICENSE
```

### Create marketplace.json

**Location**: `.claude-plugin/marketplace.json`

```json
{
  "name": "my-company-tools",
  "description": "Internal Claude Code plugins for My Company",
  "owner": {
    "name": "My Company Engineering",
    "email": "eng@mycompany.com",
    "url": "https://github.com/mycompany"
  },
  "homepage": "https://docs.mycompany.com/claude-plugins",
  "plugins": [
    {
      "name": "fellow",
      "source": "./plugins/fellow",
      "description": "Semantic knowledge extraction and context enrichment",
      "version": "2.1.0",
      "author": {
        "name": "Jingnan Zhou",
        "email": "jingnan.zhou@example.com"
      },
      "license": "Apache-2.0",
      "keywords": ["knowledge", "semantic", "architecture", "context"]
    },
    {
      "name": "code-formatter",
      "source": "./plugins/code-formatter",
      "description": "Automatic code formatting for all languages",
      "version": "1.0.0",
      "author": {
        "name": "My Company"
      },
      "license": "MIT",
      "keywords": ["formatting", "style"]
    }
  ]
}
```

### Marketplace Plugin Sources

Plugins in your marketplace can come from three types of sources:

**1. Relative Path (plugins in same repo):**

```json
{
  "name": "fellow",
  "source": "./plugins/fellow"
}
```

**2. GitHub Repository:**

```json
{
  "name": "fellow",
  "source": {
    "source": "github",
    "repo": "jingnanzhou/fellow"
  }
}
```

**3. Git URL (any Git host):**

```json
{
  "name": "fellow",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/mycompany/fellow.git"
  }
}
```

### Publishing Your Custom Marketplace

**Step 1: Host on GitHub (Recommended)**

```bash
# Create repository
git init my-claude-plugins
cd my-claude-plugins

# Add marketplace.json
mkdir -p .claude-plugin
# (Create marketplace.json as shown above)

# Add plugins
mkdir -p plugins
git submodule add https://github.com/jingnanzhou/fellow.git plugins/fellow

# Commit and push
git add .
git commit -m "Initial marketplace setup"
git push origin main
```

**Step 2: Share with Team**

Users add your marketplace:

```bash
# Add marketplace by GitHub repo
/plugin marketplace add mycompany/claude-plugins

# Or by full URL
/plugin marketplace add https://github.com/mycompany/claude-plugins.git

# List available plugins
/plugin search

# Install plugins
/plugin install fellow@my-company-tools
/plugin install code-formatter@my-company-tools
```

**Step 3: Team Distribution via Settings**

For automatic team distribution, add to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "my-company-tools": {
      "source": {
        "source": "github",
        "repo": "mycompany/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "fellow@my-company-tools": true,
    "code-formatter@my-company-tools": true
  }
}
```

Commit this to your project repo - team members automatically get plugins!

## Enterprise Marketplace Control

For enterprises, administrators can restrict which marketplaces users can access:

**Enterprise managed settings:**

```json
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "mycompany/approved-plugins"
    }
  ]
}
```

This prevents users from adding untrusted marketplaces.

## Versioning and Updates

### Semantic Versioning

Follow semantic versioning (semver) for Fellow releases:

- **Major version (2.0.0 → 3.0.0)**: Breaking changes
- **Minor version (2.1.0 → 2.2.0)**: New features, backward compatible
- **Patch version (2.1.0 → 2.1.1)**: Bug fixes, backward compatible

### Creating Releases

**Step 1: Update version in plugin.json**

```json
{
  "name": "fellow",
  "version": "2.2.0",
  ...
}
```

**Step 2: Update CHANGELOG.md**

```markdown
## [2.2.0] - 2026-01-15

### Added
- New feature X
- Enhancement Y

### Fixed
- Bug fix Z

### Changed
- Improved performance of ABC
```

**Step 3: Create Git tag**

```bash
git tag -a v2.2.0 -m "Release v2.2.0: Feature X and Bug Fix Z"
git push origin v2.2.0
```

**Step 4: Create GitHub Release**

1. Go to GitHub repository
2. Click "Releases" → "Draft a new release"
3. Select tag `v2.2.0`
4. Title: "Fellow v2.2.0"
5. Description: Copy from CHANGELOG.md
6. Publish release

### Update Distribution

**Official Marketplace**: Anthropic automatically picks up new releases

**Custom Marketplace**: Update marketplace.json:

```json
{
  "plugins": [
    {
      "name": "fellow",
      "version": "2.2.0",  // Update version
      ...
    }
  ]
}
```

## Marketing Your Plugin

### Documentation Website

Fellow has a comprehensive documentation website at `https://jingnanzhou.github.io/fellow/` built with MkDocs Material.

**Create your own docs site:**

```bash
# Install MkDocs Material
pip install mkdocs-material

# Build documentation
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### README.md Best Practices

Your README should include:

1. **What it does** (one-sentence summary)
2. **Why it's useful** (problem it solves)
3. **Quick start** (5-minute getting started)
4. **Installation** (clear instructions)
5. **Examples** (real-world usage)
6. **Screenshots/GIFs** (visual demonstrations)
7. **Documentation link** (comprehensive docs)
8. **Contributing guide** (how to help)
9. **License** (open source license)

### Promoting Your Plugin

**GitHub:**
- Add topics/tags: `claude-code`, `plugin`, `semantic-analysis`
- Create demo videos or GIFs
- Write detailed examples in README

**Social Media:**
- Announce on Twitter/X
- Share on Reddit (r/ClaudeDev, r/programming)
- Post on Hacker News

**Blogging:**
- Write a launch blog post
- Create tutorial blog posts
- Share use cases and case studies

**Community:**
- Answer questions on GitHub issues
- Respond to feedback quickly
- Build a community around your plugin

## Maintenance Best Practices

**Regular updates:**
- Fix bugs promptly
- Respond to issues within 48 hours
- Keep up with Claude Code updates
- Test with new Claude Code versions

**Documentation:**
- Keep README.md current
- Update CHANGELOG.md with every release
- Maintain comprehensive docs site
- Add examples for new features

**Community:**
- Welcome contributions
- Review pull requests promptly
- Thank contributors
- Build a CONTRIBUTORS.md file

## Fellow's Publishing Checklist

For publishing Fellow specifically:

- [x] Create GitHub repository: `github.com/jingnanzhou/fellow`
- [x] Add LICENSE (Apache 2.0)
- [x] Add CONTRIBUTING.md
- [x] Create comprehensive README.md
- [x] Create documentation website (MkDocs)
- [x] Add CHANGELOG.md
- [ ] Create GitHub releases for versions
- [ ] Submit to Anthropic for official marketplace
- [ ] Create demo video/screenshots
- [ ] Write launch blog post
- [ ] Set up issue templates
- [ ] Add CI/CD for testing
- [ ] Create plugin validation tests

## Getting Help

For questions about publishing:

- **Claude Code Plugin Documentation**: https://code.claude.com/docs/en/plugins.md
- **Marketplace Documentation**: https://code.claude.com/docs/en/plugin-marketplaces.md
- **Community Forum**: https://github.com/anthropics/claude-code/discussions
- **Email**: plugins@anthropic.com

---

**Ready to share Fellow with the world!**
