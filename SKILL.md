---
name: heal-mcp
description: Diagnose and repair Model Context Protocol (MCP) server connection issues across Claude Desktop, Claude Code, and Cursor. Use when MCP servers fail to connect, tools don't appear, connection errors occur, or when troubleshooting MCP error -32000, npx issues, configuration problems, or dependency conflicts.
---

# MCP Server Diagnostic and Repair Skill

This skill provides systematic diagnosis and repair of MCP server issues across all three platforms: Claude Desktop, Claude Code, and Cursor.

## When to Use This Skill

Automatically trigger this skill when users mention:
- MCP servers not connecting or disconnecting
- Tools not appearing in Claude/Cursor
- MCP error codes (especially -32000)
- "npx not working" or Windows MCP issues
- Configuration file problems
- Dependency or version conflicts
- Server startup failures
- Wanting to migrate servers between platforms
- Needing a health check of all MCP servers
- Installing missing dependencies

## New Enhanced Features (v2.0)

### 🏥 Health Dashboard
Get a comprehensive overview of all MCP servers across all platforms:
- Visual status indicators (✓ healthy, ⚠ warnings, ✗ failed)
- System dependency checks (Node.js, Python, npm, uvx)
- Per-platform breakdowns
- Overall health summary with recommendations

### 🔧 Interactive Repair Mode
Step-by-step guided repairs with:
- **Automatic backups** before any changes
- User confirmation for each fix
- Smart issue detection (missing flags, empty env vars, etc.)
- Rollback capability if something goes wrong
- Clear success/failure feedback

### 📦 Smart Dependency Installer
Auto-detect and install missing dependencies:
- Detects Homebrew and uses it for installations
- Installs Node.js, Python, uv, and other dependencies
- Provides manual installation instructions as fallback
- Verifies successful installation
- Offers to install optional dependencies

### 🔄 Server Migration Helper
Easily move servers between platforms:
- **Copy** servers (keeps original)
- **Move** servers (removes from source)
- **Sync** all servers from one platform to another
- Platform options: Claude Desktop ↔ Claude Code ↔ Cursor
- Automatic backup before migrations

### 💾 Automatic Backup System
Every operation creates timestamped backups:
- Stored in `~/.claude/skills/heal_mcp/backups/`
- Includes metadata (timestamp, platform, original path)
- Easy restore via interactive-repair.py
- Multiple restore points available

## Diagnostic Workflow

Follow this systematic approach from simple to complex:

### 1. Identify the Platform and Issue

First, determine:
- Which platform? (Claude Desktop, Claude Code, or Cursor)
- What's the symptom? (no connection, no tools, error message, etc.)
- Which specific MCP server is affected?

### 2. Check Basic Configuration

**For Claude Desktop (macOS):**
- Config file: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Logs: `~/Library/Logs/Claude/mcp*.log`

**For Claude Code:**
- Use: `claude mcp list` to see configured servers
- Check: `~/.claude.json` (user scope) or `.mcp.json` (project scope)

**For Cursor:**
- Config: `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project)
- Settings UI: Cursor Settings → MCP
- Logs: Check Output panel with MCP selected

### 3. Run Validation Script

Execute the validation script to check configuration syntax:

```bash
python3 ~/.claude/skills/heal_mcp/scripts/validate-config.py
```

This checks:
- JSON syntax validity
- Required fields present
- Path existence
- Command availability

### 4. Test Server Independence

Before diagnosing client issues, verify the server itself works:

```bash
# For npx-based servers:
npx -y @modelcontextprotocol/server-filesystem ~/Desktop

# For uvx-based servers:
uvx mcp-server-sqlite --db-path ~/test.db
```

The server should start without errors and wait for input. If it exits immediately or shows errors, the problem is with the server installation, not configuration.

### 5. Check Common Issues

**Windows npx failures (most common on Windows):**
- Symptom: Immediate "Connection closed" errors
- Solution: Wrap with cmd interpreter

**Stdout pollution:**
- Symptom: Connection works briefly then fails
- Check: Server code for console.log() statements
- Solution: Change to console.error() for all logging

**Missing dependencies:**
- Node.js version: Must be 18.0.0+
- Python version: Must be 3.10+ (3.13 recommended for uvx)
- Check with dependency script

**Environment variables:**
- API keys not reaching server
- Solution: Add explicit env block in config

### 6. Analyze Log Files

Read the appropriate log file and look for:
- "Starting new stdio process" followed immediately by "Client closed" = server won't start
- "MCP error -32000" = connection closed unexpectedly
- Stack traces showing the exact failure point
- The exact command that was executed

### 7. Use MCP Inspector

For definitive testing:

```bash
npx @modelcontextprotocol/inspector node path/to/server.js
```

Opens web interface at http://localhost:6274 showing:
- Whether server starts successfully
- Available tools and resources
- Raw JSON-RPC messages
- Protocol violations

### 8. Check GitHub for Known Issues

Search the official repository:
- https://github.com/modelcontextprotocol/servers/issues
- Search for exact error messages
- Check closed issues for solutions
- Verify you're using the latest version

## Platform-Specific Fixes

### macOS Issues
- iCloud sync conflicts: Move config files out of iCloud directories
- Permission errors: `chmod +x` on executable files
- Path issues: Use full absolute paths, not relative or tilde

### Windows Issues
- **Critical:** Wrap npx commands with cmd interpreter
- Change from: `"command": "npx"`
- Change to: `"command": "cmd"`, `"args": ["/c", "npx", "-y", "package"]`

### Common Configuration Patterns

**Correct npx server (macOS/Linux):**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    }
  }
}
```

**Correct npx server (Windows):**
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", "C:\\path\\to\\dir"]
    }
  }
}
```

**With environment variables:**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

## Scripts Available

This skill includes comprehensive helper scripts in the `scripts/` directory:

### Diagnostic Tools
- `health-dashboard.py` - **NEW!** Comprehensive health check of all MCP servers across all platforms
- `check-versions.py` - Check for outdated MCP server versions
- `validate-config.py` - Validates JSON configuration files
- `check-dependencies.sh` - Verifies Node.js, Python, npm, uvx installation

### Repair Tools
- `interactive-repair.py` - **NEW!** Step-by-step guided repair with automatic backups
- `install-dependencies.py` - **NEW!** Smart installer for missing dependencies (Node.js, Python, uv, etc.)
- `auto-update-servers.sh` - Automatically update outdated MCP servers

### Migration Tools
- `migrate-servers.py` - **NEW!** Copy/move servers between platforms (Desktop ↔ Code ↔ Cursor)
- `update-configs.py` - Batch update configurations across platforms

### Quick Start Commands

**Run health check dashboard:**
```bash
python3 ~/.claude/skills/heal_mcp/scripts/health-dashboard.py
```

**Start interactive repair:**
```bash
python3 ~/.claude/skills/heal_mcp/scripts/interactive-repair.py
```

**Install missing dependencies:**
```bash
python3 ~/.claude/skills/heal_mcp/scripts/install-dependencies.py
```

**Migrate servers between platforms:**
```bash
python3 ~/.claude/skills/heal_mcp/scripts/migrate-servers.py
```

## Reference Documentation

Detailed platform-specific guides in `reference/`:

- `windows-issues.md` - Comprehensive Windows troubleshooting
- `log-patterns.md` - Common log patterns and their meanings
- `error-codes.md` - MCP error codes and solutions
- `platform-configs.md` - Complete configuration examples

## Repair Workflow

When issues are identified:

1. **Present findings clearly** - Explain what was found and why it's problematic
2. **Suggest specific fixes** - Provide exact changes needed
3. **Show corrected configuration** - Display the fixed config in an artifact
4. **Get user approval** - Never modify files without permission
5. **Verify the fix** - Re-run diagnostics after changes

## Version Checking

Check for latest versions:

```bash
# For npm packages:
npm view @modelcontextprotocol/server-filesystem version

# For Python packages:
pip index versions mcp-server-sqlite

# For GitHub releases:
curl -s "https://api.github.com/repos/modelcontextprotocol/servers/releases/latest" | jq -r ".tag_name"
```

## Emergency Diagnostics

If nothing else works:

1. **Clear caches:**
   ```bash
   npm cache clean --force
   uv cache clean
   ```

2. **Reinstall globally:**
   ```bash
   npm install -g @modelcontextprotocol/server-filesystem
   ```

3. **Use Docker (most reliable):**
   ```json
   {
     "command": "docker",
     "args": ["run", "-i", "--rm", "mcp-server:latest"]
   }
   ```

## Success Criteria

A properly functioning MCP server shows:
- ✅ Server appears in configuration
- ✅ Logs show "Client connected successfully"
- ✅ Tools appear in the client interface
- ✅ Tools execute without errors
- ✅ No error -32000 messages

## Additional Resources

- Official docs: https://modelcontextprotocol.io
- Server repository: https://github.com/modelcontextprotocol/servers
- Claude Code docs: https://docs.claude.com/en/docs/claude-code/mcp
- Cursor docs: https://docs.cursor.com/context/mcp

---

Remember: Most MCP issues fall into predictable categories. Work systematically through this checklist rather than jumping to complex solutions. The majority of problems are Windows npx issues, stdout pollution, or simple configuration syntax errors.
