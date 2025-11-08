# Contributing to heal_mcp

Thank you for considering contributing to heal_mcp! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **System information** (OS, Python version, Node.js version)
- **Configuration files** (sanitized, no tokens/keys)
- **Log outputs** or error messages

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - why this would be useful
- **Proposed solution** - how you envision it working
- **Alternatives considered** - other approaches you've thought about

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear messages (`git commit -m 'Add feature: description'`)
6. Push to your fork (`git push origin feature/your-feature-name`)
7. Open a Pull Request

#### Pull Request Guidelines

- **One feature per PR** - Keep PRs focused
- **Update documentation** - Update README.md and SKILL.md if needed
- **Add tests** - If adding new functionality
- **Follow existing code style** - Match the project's conventions
- **Update ENHANCEMENTS.md** - Document significant changes

### Code Style

- **Python**: Follow PEP 8 guidelines
- **Shell scripts**: Use shellcheck for linting
- **JSON**: Use 2-space indentation
- **Comments**: Write clear, helpful comments
- **Error handling**: Always handle errors gracefully

### Testing Your Changes

Before submitting a PR:

1. Test on your local machine
2. Run the health dashboard: `python3 scripts/health-dashboard.py`
3. Test interactive repair: `python3 scripts/interactive-repair.py`
4. Verify no breaking changes to existing functionality

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 18.0+
- Git

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/heal-mcp.git
cd heal-mcp

# Make scripts executable
chmod +x scripts/*.py scripts/*.sh

# Test installation
python3 scripts/health-dashboard.py
```

## Project Structure

```
heal-mcp/
├── SKILL.md              # Main skill documentation
├── scripts/              # All executable scripts
│   ├── health-dashboard.py
│   ├── interactive-repair.py
│   └── ...
├── templates/            # Configuration templates
├── reference/            # Reference documentation
└── backups/              # Auto-generated backups (gitignored)
```

## Adding New Features

### Adding a New Script

1. Create script in `scripts/` directory
2. Make it executable: `chmod +x scripts/your-script.py`
3. Add usage instructions to README.md
4. Update SKILL.md with new capability
5. Add to ENHANCEMENTS.md

### Adding a New Template

1. Create JSON file in `templates/` directory
2. Use `<PLACEHOLDER>` format for user-replaceable values
3. Update `templates/README.md` with description
4. Add example usage to main README.md

### Adding New Platform Support

When adding support for a new platform:

1. Update `ConfigManager` in relevant scripts
2. Add platform detection logic
3. Add configuration path
4. Test thoroughly on the target platform
5. Update documentation

## Documentation

Good documentation is crucial! When contributing:

- Update README.md for user-facing changes
- Update SKILL.md for skill behavior changes
- Add code comments for complex logic
- Include examples for new features

## Questions?

Feel free to:
- Open an issue with the `question` label
- Start a discussion in GitHub Discussions
- Check existing issues and discussions

## Recognition

Contributors will be:
- Listed in the project's contributors
- Acknowledged in release notes
- Credited in the README if making significant contributions

Thank you for contributing to heal_mcp! 🎉
