# Publishing to PyPI

This guide explains how to publish your fork of Robot Framework MCP Server to PyPI.

## Prerequisites

- PyPI account ([Sign up here](https://pypi.org/account/register/))
- PyPI API token ([Create here](https://pypi.org/manage/account/token/))
- Python 3.10+
- Build tools installed

## Step-by-Step Guide

### 1. Prepare Your Package

#### Update Package Name

Edit `pyproject.toml` to use a unique name (to avoid conflicts with the original package):

```toml
[project]
name = "robotframework-mcp-yourname"  # Change this!
version = "2.0.0"
description = "Your custom Robot Framework MCP Server"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
```

#### Update Package Metadata

Also update these fields in `pyproject.toml`:

```toml
[project.urls]
Homepage = "https://github.com/YOUR_USERNAME/robotframework-MCP"
Repository = "https://github.com/YOUR_USERNAME/robotframework-MCP.git"
Issues = "https://github.com/YOUR_USERNAME/robotframework-MCP/issues"
```

#### Update README

Update `README.md` to reflect your package name:

```bash
# Old
pip install robotframework-mcp

# New
pip install robotframework-mcp-yourname
```

### 2. Install Build Tools

```bash
pip install --upgrade build twine
```

### 3. Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build source distribution and wheel
python -m build
```

This creates two files in the `dist/` directory:
- `robotframework-mcp-yourname-2.0.0.tar.gz` (source distribution)
- `robotframework_mcp_yourname-2.0.0-py3-none-any.whl` (wheel)

### 4. Test on TestPyPI (Recommended)

Before publishing to the real PyPI, test on TestPyPI:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ robotframework-mcp-yourname
```

### 5. Upload to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your PyPI API token (starts with `pypi-`)

### 6. Verify Installation

```bash
# Install from PyPI
pip install robotframework-mcp-yourname

# Test it works
python -c "from src.server import main; print('Success!')"
```

## Automated Publishing with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: python -m twine upload dist/*
```

Add your PyPI API token to GitHub Secrets:
1. Go to your repository Settings
2. Secrets and variables → Actions
3. New repository secret
4. Name: `PYPI_API_TOKEN`
5. Value: Your PyPI API token

Now, whenever you create a GitHub release, it will automatically publish to PyPI!

## Version Management

### Semantic Versioning

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version (2.x.x): Breaking changes
- **MINOR** version (x.1.x): New features, backward compatible
- **PATCH** version (x.x.1): Bug fixes, backward compatible

### Updating Version

Update version in `pyproject.toml`:

```toml
[project]
version = "2.1.0"  # Increment this
```

Also update in:
- `src/__init__.py`
- `src/config.py` (ServerConfig.version)
- `package.json`

### Creating a Release

```bash
# Tag the release
git tag -a v2.1.0 -m "Release version 2.1.0"
git push origin v2.1.0

# Create GitHub release
# Go to GitHub → Releases → Create new release
```

## Troubleshooting

### Error: Package name already exists

Change your package name in `pyproject.toml` to something unique.

### Error: Invalid credentials

Make sure you're using:
- Username: `__token__`
- Password: Your full API token (including `pypi-` prefix)

### Error: File already exists

You can't re-upload the same version. Increment the version number.

### Error: Invalid distribution

Make sure your package structure is correct:
```
robotframework-MCP/
├── src/
│   ├── __init__.py
│   └── ...
├── pyproject.toml
├── README.md
└── LICENSE
```

## Best Practices

1. **Test Locally First**
   ```bash
   pip install -e .
   python -c "from src.server import main; main()"
   ```

2. **Use TestPyPI**
   Always test on TestPyPI before publishing to real PyPI

3. **Version Bumping**
   Use tools like `bump2version` to manage versions:
   ```bash
   pip install bump2version
   bump2version patch  # 2.0.0 → 2.0.1
   bump2version minor  # 2.0.1 → 2.1.0
   bump2version major  # 2.1.0 → 3.0.0
   ```

4. **Changelog**
   Keep `CHANGELOG.md` updated with each release

5. **Documentation**
   Update README with installation instructions for your package

## Resources

- [PyPI Documentation](https://packaging.python.org/tutorials/packaging-projects/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Semantic Versioning](https://semver.org/)
- [Python Packaging Guide](https://packaging.python.org/)

## Support

If you encounter issues:
1. Check [PyPI Help](https://pypi.org/help/)
2. Review [Packaging Troubleshooting](https://packaging.python.org/guides/analyzing-pypi-package-downloads/)
3. Ask on [Python Packaging Discourse](https://discuss.python.org/c/packaging/)
