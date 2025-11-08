# MCP Server Configuration Templates

This directory contains pre-built configuration templates for popular MCP servers.

## How to Use Templates

1. Choose a template from this directory
2. Copy the server configuration block
3. Replace any placeholder values (shown in `<UPPERCASE>`)
4. Add to your MCP configuration file
5. Restart your client

## Available Templates

### filesystem.json
Basic filesystem access for a directory

### github.json
GitHub integration with authentication

### brave-search.json
Web search via Brave Search API

### postgres.json
PostgreSQL database access

### aws.json
AWS services integration

### puppeteer.json
Browser automation with Puppeteer

### sqlite.json
SQLite database access

## Configuration File Locations

**Claude Desktop (macOS):**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Cursor:**
```
~/.cursor/mcp.json
```

**Claude Code:**
```
~/.claude.json
```

## Common Placeholders

- `<YOUR_TOKEN>` - Your personal access token
- `<YOUR_API_KEY>` - Your API key
- `<PATH_TO_DIRECTORY>` - Absolute path to a directory
- `<DATABASE_PATH>` - Path to database file
- `<CONNECTION_STRING>` - Database connection string

## Platform-Specific Notes

### macOS/Linux
- Use `npx` as the command
- Add `-y` flag to auto-accept installations
- Use absolute paths (starting with `/`)

### Windows
- Wrap npx with cmd: `"command": "cmd", "args": ["/c", "npx", "-y", ...]`
- Use Windows-style paths: `C:\\Users\\...`
