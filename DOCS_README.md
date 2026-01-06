# Fellow Documentation Website

This repository includes a comprehensive documentation website built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

## 🌐 Live Documentation

Once deployed, the documentation will be available at:
**https://jingnanzhou.github.io/fellow/**

## 📁 Documentation Structure

```
fellow/
├── mkdocs.yml                 # MkDocs configuration
├── docs-requirements.txt      # Python dependencies for docs
├── docs-site/                 # Documentation source files
│   ├── index.md              # Homepage
│   ├── quick-start.md        # Quick start guide
│   ├── getting-started/      # Getting started guides
│   ├── user-guide/           # User documentation
│   ├── features/             # Feature documentation
│   ├── use-cases/            # Use case examples
│   ├── best-practices/       # Best practices
│   ├── reference/            # Reference documentation
│   ├── contributing/         # Contributing guides
│   └── about/                # About pages
└── .github/workflows/docs.yml # Auto-deployment workflow
```

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Install dependencies:**

   ```bash
   pip install -r docs-requirements.txt
   ```

2. **Serve documentation locally:**

   ```bash
   mkdocs serve
   ```

3. **Open in browser:**

   Navigate to http://127.0.0.1:8000

   The site will auto-reload when you edit files.

### Build for Production

Build static HTML files:

```bash
mkdocs build
```

Output will be in the `site/` directory.

## 📝 Writing Documentation

### Creating a New Page

1. **Create a new markdown file** in the appropriate directory under `docs-site/`

   ```bash
   touch docs-site/user-guide/new-feature.md
   ```

2. **Add to navigation** in `mkdocs.yml`:

   ```yaml
   nav:
     - User Guide:
       - New Feature: user-guide/new-feature.md
   ```

3. **Write content** using markdown and extensions

### Markdown Extensions Available

Fellow's docs support many useful extensions:

#### Admonitions (Call-out Boxes)

```markdown
!!! note "Optional Title"
    This is a note admonition.

!!! tip
    This is a tip.

!!! warning
    This is a warning.

!!! danger
    This is a danger alert.

!!! success
    This is a success message.
```

#### Code Blocks with Syntax Highlighting

````markdown
```python
def hello_world():
    print("Hello, Fellow!")
```

```bash
/build-kb
```
````

#### Tabbed Content

```markdown
=== "Tab 1"

    Content for tab 1

=== "Tab 2"

    Content for tab 2
```

#### Task Lists

```markdown
- [x] Completed task
- [ ] Incomplete task
```

#### Keyboard Keys

```markdown
Press ++ctrl+alt+del++ to restart.
```

#### Highlighting

```markdown
==Highlight important text==
```

#### Diagrams (Mermaid)

````markdown
```mermaid
graph LR
    A[Start] --> B[Process]
    B --> C[End]
```
````

#### Emoji

```markdown
:rocket: :star: :heart:
```

### Material Design Cards

```markdown
<div class="grid cards" markdown>

-   :material-clock-fast: **Fast**

    ---

    Description here

-   :material-shield: **Secure**

    ---

    Description here

</div>
```

## 🚀 Deployment

### Automatic Deployment

Documentation is automatically deployed to GitHub Pages when:

1. **Changes are pushed to `main` branch**
2. **Changes are made to:**
   - `docs-site/**`
   - `mkdocs.yml`
   - `.github/workflows/docs.yml`

The GitHub Actions workflow (`.github/workflows/docs.yml`) handles building and deployment.

### Manual Deployment

Deploy manually:

```bash
mkdocs gh-deploy --force
```

This builds the site and pushes to the `gh-pages` branch.

### Setting Up GitHub Pages

1. **Go to repository settings**
2. **Navigate to "Pages"**
3. **Set source to "Deploy from a branch"**
4. **Select `gh-pages` branch**
5. **Save**

## 🎨 Theme Customization

### Colors

Edit `mkdocs.yml` to change theme colors:

```yaml
theme:
  palette:
    primary: indigo  # Change to: red, pink, purple, blue, etc.
    accent: indigo
```

### Logo and Favicon

Add custom logo and favicon:

```yaml
theme:
  logo: assets/logo.png
  favicon: assets/favicon.ico
```

Place files in `docs-site/assets/`

### Custom CSS

Add custom styles:

1. Create `docs-site/stylesheets/extra.css`
2. Add to `mkdocs.yml`:

   ```yaml
   extra_css:
     - stylesheets/extra.css
   ```

## 📊 Analytics

To enable Google Analytics:

1. **Get your GA4 property ID**
2. **Update `mkdocs.yml`:**

   ```yaml
   extra:
     analytics:
       provider: google
       property: G-XXXXXXXXXX  # Your property ID
   ```

## 🔍 Search

Search is automatically enabled and indexes:
- Page titles
- Headings
- Content

No configuration needed!

## 📱 Mobile Responsive

The theme is fully responsive and works great on:
- Desktop
- Tablet
- Mobile

## 🌙 Dark Mode

Dark mode is automatically available. Users can toggle with the moon/sun icon.

## ✅ Best Practices

### Documentation Structure

- **One topic per page** - Keep pages focused
- **Clear navigation** - Organize logically in `mkdocs.yml`
- **Use headings** - Structure content with H2 (##) and H3 (###)
- **Add examples** - Show don't tell
- **Link between pages** - Create a web of knowledge

### Writing Style

- **Active voice** - "Run this command" not "This command should be run"
- **Short paragraphs** - 2-4 sentences max
- **Bullet points** - Break up dense text
- **Code examples** - Always include working examples
- **Clear steps** - Number sequential instructions

### Commit Messages

When updating docs:

```bash
git commit -m "docs: add incremental updates guide"
git commit -m "docs: update installation instructions"
git commit -m "docs: fix typo in quick start"
```

## 🐛 Troubleshooting

### "Module not found" error

**Solution**: Install dependencies

```bash
pip install -r docs-requirements.txt
```

### "Page not found" after deployment

**Solution**: Check navigation in `mkdocs.yml` matches file paths exactly

### Images not showing

**Solution**: Place images in `docs-site/assets/` and reference as:

```markdown
![Alt text](assets/image.png)
```

### Site not updating on GitHub Pages

**Solution**: Check GitHub Actions workflow status

1. Go to "Actions" tab in GitHub
2. Check if deployment succeeded
3. Look for error messages

## 📚 Resources

- **MkDocs Documentation**: https://www.mkdocs.org/
- **Material Theme**: https://squidfunk.github.io/mkdocs-material/
- **Markdown Guide**: https://www.markdownguide.org/
- **Mermaid Diagrams**: https://mermaid.js.org/

## 🤝 Contributing to Docs

See [Contributing Documentation Guide](docs-site/contributing/documentation.md) for detailed guidelines on:

- Documentation standards
- Style guide
- Review process
- Building and testing

## 📞 Questions?

- **Documentation Issues**: Open an issue on GitHub
- **General Questions**: fellow@example.com
- **Pull Requests**: Welcome! Follow the contributing guide

---

<p align="center">
  <strong>Happy documenting! 📖</strong>
</p>
