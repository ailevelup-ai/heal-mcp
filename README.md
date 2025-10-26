# 🏥 heal-mcp: MCP Server Diagnostic & Repair Skill

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)]()
[![Claude Skills](https://img.shields.io/badge/Claude-Skills-brightgreen.svg)]()

> A comprehensive Claude Code skill for diagnosing, repairing, and managing Model Context Protocol (MCP) servers across Claude Desktop, Claude Code, and Cursor.

## 🎯 What is heal-mcp?

`heal-mcp` is an advanced diagnostic and repair skill that Claude can use to troubleshoot MCP server issues. It provides systematic workflows, automated scripts, and interactive tools to keep your MCP servers healthy and running smoothly.

### Key Features

- **🏥 Health Dashboard**: Real-time status of all MCP servers across all platforms
- **🔧 Interactive Repair**: Step-by-step guided fixes with automatic backups
- **📦 Smart Dependency Installer**: Auto-detect and install missing dependencies
- **🔄 Server Migration**: Easily copy/move servers between platforms
- **💾 Automatic Backups**: Every operation creates timestamped restore points
- **📊 Version Checker**: Find outdated servers and update them
- **✅ Config Validator**: Validate JSON syntax and MCP structure

## 🚀 Quick Start

### Installation

1. Clone this repository to Claude's skills directory:

```bash
git clone https://github.com/ailevelup-ai/heal-mcp.git ~/.claude/skills/heal-mcp
```

2. Make scripts executable:

```bash
chmod +x ~/.claude/skills/heal-mcp/scripts/*.sh
chmod +x ~/.claude/skills/heal-mcp/scripts/*.py
```

3. Verify installation:

```bash
python3 ~/.claude/skills/heal-mcp/scripts/health-dashboard.py
```

### Usage

Simply ask Claude in natural language:

- "My MCP servers aren't connecting"
- "Can you check my MCP server health?"
- "I need to migrate my GitHub MCP server from Claude Desktop to Cursor"
- "Help me update all my outdated MCP servers"

Claude will automatically load this skill and guide you through the appropriate workflow.

## 🛠️ Tools & Scripts

### Health Dashboard (`health-dashboard.py`)
Comprehensive overview of all MCP servers:
```bash
python3 ~/.claude/skills/heal-mcp/scripts/health-dashboard.py
```

Shows:
- System dependencies status
- All configured servers by platform
- Health indicators (✓ healthy, ⚠ warnings, ✗ failed)
- Recommendations for fixes

### Interactive Repair (`interactive-repair.py`)
Guided repair workflow:
```bash
python3 ~/.claude/skills/heal-mcp/scripts/interactive-repair.py
```

Features:
- Automatic issue detection
- User-confirmed fixes
- Backup before changes
- Restore capability

### Version Checker (`check-versions.py`)
Find outdated MCP servers:
```bash
python3 ~/.claude/skills/heal_mcp/scripts/check-versions.py
```

Checks:
- npm packages for latest versions
- PyPI packages for Python servers
- Provides update recommendations

### Config Validator (`validate-config.py`)
Validate MCP configurations:
```bash
python3 ~/.claude/skills/heal_mcp/scripts/validate-config.py
```

Validates:
- JSON syntax
- Required fields
- Command availability
- Common misconfigurations

### Dependency Installer (`install-dependencies.py`)
Install missing dependencies:
```bash
python3 ~/.claude/skills/heal_mcp/scripts/install-dependencies.py
```

Installs:
- Node.js (via Homebrew)
- Python 3
- uv/uvx
- Other MCP requirements

### Server Migration (`migrate-servers.py`)
Move servers between platforms:
```bash
python3 ~/.claude/skills/heal_mcp/scripts/migrate-servers.py
```

Operations:
- Copy servers (keeps original)
- Move servers (removes from source)
- Sync all servers between platforms

### Auto-Update (`auto-update-servers.sh`)
Automatically update server versions:
```bash
~/.claude/skills/heal_mcp/scripts/auto-update-servers.sh
```

Updates:
- Backs up all configs
- Updates package versions
- Provides rollback instructions

## 📚 Supported Platforms

| Platform | Config Location | Notes |
|----------|----------------|-------|
| **Claude Desktop** | `~/Library/Application Support/Claude/claude_desktop_config.json` | macOS only |
| **Claude Code** | `~/.claude.json` (user)<br>`.mcp.json` (project) | Cross-platform |
| **Cursor** | `~/.cursor/mcp.json` (global)<br>`.cursor/mcp.json` (project) | Cross-platform |

## 🔍 Common Issues & Solutions

### Error -32000: MCP Server Connection Failed

**Causes:**
- Server binary not found
- Missing dependencies
- Wrong command path
- Port conflicts

**Solution:**
```bash
python3 ~/.claude/skills/heal_mcp/scripts/health-dashboard.py
```
Then follow recommendations.

### npx Not Working on Windows

**Issue:** Windows requires `cmd /c npx` wrapper

**Solution:** The interactive repair tool will detect and fix this automatically.

### Empty Environment Variables

**Issue:** Server requires env vars like API keys

**Solution:** Interactive repair will prompt you to fill in missing values.

### Server Shows Up But No Tools

**Causes:**
- Server version mismatch
- Missing tool permissions
- Server not fully initialized

**Solution:**
```bash
python3 ~/.claude/skills/heal_mcp/scripts/check-versions.py
```
Update if outdated.

## 🎓 How It Works

When you mention an MCP issue to Claude:

1. **Detection**: Claude identifies this is an MCP-related problem
2. **Skill Loading**: The heal-mcp skill is loaded
3. **Diagnosis**: Claude uses the appropriate diagnostic script
4. **Guided Repair**: Claude walks you through fixing issues
5. **Verification**: Health check confirms the fix worked

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repo
git clone https://github.com/ailevelup-ai/heal-mcp.git
cd heal-mcp

# Make scripts executable
chmod +x scripts/*.sh scripts/*.py

# Run tests
python3 scripts/validate-config.py
python3 scripts/health-dashboard.py
```

## 📄 License

Copyright (C) 2025 SSage Software Inc  
5550 Glades Rd St 500-1160  
Boca Raton, FL 33431

This project is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0) with additional permissions for free use by:

- ✅ Educational institutions and students
- ✅ Non-profit organizations
- ✅ Personal use
- ✅ Commercial use by companies with annual revenue below $1,000,000 USD

For commercial use by companies with $1M+ annual revenue, please contact licensing@ssagesoftware.com for a commercial license.

See [LICENSE](LICENSE) for the full license text.

## 🙏 Acknowledgments

Built for the Claude ecosystem to make MCP server management effortless.

Special thanks to:
- Anthropic for Claude and MCP
- The MCP community for server development
- Contributors and users of this skill

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ailevelup-ai/heal-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ailevelup-ai/heal-mcp/discussions)
- **Email**: licensing@ssagesoftware.com

## 🗺️ Roadmap

- [ ] Windows support enhancement
- [ ] Linux support
- [ ] Automated server updates
- [ ] MCP marketplace integration
- [ ] Web UI for configuration management
- [ ] Docker containerized testing
- [ ] CI/CD for skill validation

---

Made with ❤️ by [SSage Software Inc](https://ssagesoftware.com)
