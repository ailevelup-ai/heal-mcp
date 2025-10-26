# heal_mcp - MCP Server Diagnostic & Repair Skill

> A comprehensive diagnostic and repair toolkit for Model Context Protocol (MCP) servers across Claude Desktop, Claude Code, and Cursor.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey)](https://github.com/ailevelup-ai/heal-mcp)

## 🎯 Overview

`heal_mcp` is a powerful skill for Claude that helps you diagnose, repair, and manage MCP servers across multiple platforms. It provides automated health checks, guided repairs, dependency management, and server migration tools.

### Key Features

- 🏥 **Health Dashboard** - Comprehensive overview of all MCP servers
- 🔧 **Interactive Repair** - Step-by-step guided fixes with automatic backups
- 📦 **Dependency Installer** - Auto-detect and install missing dependencies
- 🔄 **Server Migration** - Copy/move servers between platforms
- 📋 **Configuration Templates** - Pre-built configs for popular servers
- 💾 **Automatic Backups** - Safe repairs with rollback capability

## 🚀 Quick Start

### Installation

1. Clone this repository into your Claude skills directory:

```bash
cd ~/.claude/skills
git clone https://github.com/ailevelup-ai/heal-mcp.git
```

2. Make scripts executable:

```bash
chmod +x ~/.claude/skills/heal-mcp/scripts/*.py
```

3. Run health check:

```bash
python3 ~/.claude/skills/heal-mcp/scripts/health-dashboard.py
```

### Basic Usage

#### Check MCP Server Health
```bash
python3 ~/.claude/skills/heal-mcp/scripts/health-dashboard.py
```

#### Fix Issues Interactively
```bash
python3 ~/.claude/skills/heal-mcp/scripts/interactive-repair.py
```

#### Install Missing Dependencies
```bash
python3 ~/.claude/skills/heal-mcp/scripts/install-dependencies.py
```

#### Migrate Servers Between Platforms
```bash
python3 ~/.claude/skills/heal-mcp/scripts/migrate-servers.py
```

## 📚 Documentation

### Supported Platforms

- **Claude Desktop** (macOS, Windows, Linux)
- **Claude Code** (Command-line tool)
- **Cursor** (IDE)

### Tools Included

#### Diagnostic Tools
- `health-dashboard.py` - Comprehensive health check
- `check-versions.py` - Check for outdated servers
- `validate-config.py` - Validate JSON configurations
- `check-dependencies.sh` - Verify system dependencies

#### Repair Tools
- `interactive-repair.py` - Guided repair workflow
- `install-dependencies.py` - Dependency installer
- `auto-update-servers.sh` - Update outdated servers

#### Migration Tools
- `migrate-servers.py` - Move/copy servers between platforms
- `update-configs.py` - Batch configuration updates

### Configuration Templates

Pre-built templates for popular MCP servers:
- Filesystem
- GitHub
- Brave Search
- SQLite
- PostgreSQL
- Puppeteer

## 🎓 Use Cases

### Scenario 1: New MCP Setup
```bash
# Install dependencies
python3 scripts/install-dependencies.py

# Use templates to configure servers
cat templates/github.json
# Add to your config, replacing <PLACEHOLDERS>

# Verify setup
python3 scripts/health-dashboard.py
```

### Scenario 2: Troubleshooting Connection Issues
```bash
# Run diagnostics
python3 scripts/health-dashboard.py

# Identify issues and get guided fixes
python3 scripts/interactive-repair.py
```

### Scenario 3: Moving from Desktop to Cursor
```bash
# Launch migration tool
python3 scripts/migrate-servers.py

# Select: Copy from Claude Desktop to Cursor
# Your servers are now available in both platforms
```

## 🛠️ Requirements

### System Dependencies
- Python 3.8 or higher
- Node.js 18.0+ (for most MCP servers)
- npm / npx
- Optional: Python 3.10+ for uvx-based servers

### Installation
The `install-dependencies.py` script can help install these automatically on macOS via Homebrew.

## 📖 How It Works

### Health Dashboard
Scans all MCP configurations and checks:
- ✅ Configuration validity (JSON syntax)
- ✅ Command availability (npx, uvx, node, etc.)
- ✅ System dependencies (Node.js, Python)
- ✅ Environment variable completeness
- ✅ Common configuration issues

### Interactive Repair
Provides guided fixes for:
- Missing `-y` flags on npx commands
- Empty environment variables
- Invalid JSON syntax
- Missing command fields
- Path issues

All repairs create automatic backups with rollback capability.

### Server Migration
Supports three operations:
- **Copy**: Duplicate server to another platform
- **Move**: Transfer server and remove from source
- **Sync**: Copy all servers from source to destination

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contributions
- Add more configuration templates
- Support for additional platforms
- Automated monitoring features
- Performance metrics
- Web dashboard interface
- Additional diagnostic checks

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for the [Model Context Protocol](https://modelcontextprotocol.io)
- Inspired by the MCP community's troubleshooting needs
- Tested with [Claude](https://claude.ai) by Anthropic

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ailevelup-ai/heal-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ailevelup-ai/heal-mcp/discussions)
- **MCP Documentation**: https://modelcontextprotocol.io

## 🗺️ Roadmap

- [ ] v2.1: Automated monitoring with cron jobs
- [ ] v2.2: Email/Slack notifications
- [ ] v2.3: Performance metrics tracking
- [ ] v3.0: Web dashboard interface
- [ ] v3.1: Cloud config sync

## ⭐ Star History

If you find this useful, please consider giving it a star! It helps others discover the tool.

---

**Made with ❤️ for the MCP community**
