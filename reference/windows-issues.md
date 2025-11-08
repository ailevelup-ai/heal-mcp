# Windows MCP Server Troubleshooting Guide

This document covers Windows-specific issues with MCP servers and their solutions.

## The Most Common Issue: npx Batch Script Failure

**Problem:** On Windows, npx is actually a batch script (.cmd file) rather than a native executable. When Claude Desktop, Claude Code, or Cursor try to execute `npx` directly, Windows cannot run batch scripts without explicitly invoking the command interpreter.

**Symptom:** 
- Server appears in configuration
- Logs show "Starting new stdio process"
- Immediately followed by "Client closed"
- Error: "MCP error -32000: Connection closed"
- No tools appear in the client

**Solution:** Wrap npx commands with cmd.exe interpreter.

### Before (doesn't work on Windows):
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\username\\Desktop"]
    }
  }
}
```

### After (works on Windows):
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\username\\Desktop"]
    }
  }
}
```

**How it works:**
- `cmd` invokes the Windows command interpreter
- `/c` tells cmd to execute the command and then exit
- `npx` and subsequent arguments are passed to cmd for execution
- cmd can properly execute batch scripts

## Alternative Solutions

### Solution 1: Global npm Installation

Instead of using npx, install the package globally and reference the installed script:

```bash
npm install -g @modelcontextprotocol/server-filesystem
```

Then find where it was installed:
```bash
npm root -g
```

Configure with the full path:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "node",
      "args": ["C:\\Users\\username\\AppData\\Roaming\\npm\\node_modules\\@modelcontextprotocol\\server-filesystem\\dist\\index.js", "C:\\Users\\username\\Desktop"]
    }
  }
}
```

**Advantages:**
- Faster startup (no package downloading)
- More reliable
- No batch script issues

**Disadvantages:**
- Must update manually
- Full path required

### Solution 2: Use PowerShell Instead of cmd

PowerShell can also execute batch scripts:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "powershell",
      "args": ["-Command", "npx", "-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\username\\Desktop"]
    }
  }
}
```

## Path Issues on Windows

Windows uses backslashes (`\`) in paths, but JSON requires escaping them as `\\`.

**Incorrect:**
```json
"args": ["C:\Users\username\Desktop"]
```

**Correct:**
```json
"args": ["C:\\Users\\username\\Desktop"]
```

**Alternative (forward slashes work in most cases):**
```json
"args": ["C:/Users/username/Desktop"]
```

## Environment Variable Issues

Windows environment variables use different syntax than Unix:

**Windows environment variable expansion:**
```json
{
  "env": {
    "USERPROFILE": "%USERPROFILE%"
  }
}
```

**Better approach - use explicit paths:**
```json
{
  "env": {
    "HOME_DIR": "C:\\Users\\username"
  }
}
```

## Common Windows-Specific Errors

### Error: "command not found"

**Cause:** Node.js or Python not in PATH

**Solution:**
1. Verify installation: Open cmd and type `node --version`
2. If not found, reinstall Node.js from https://nodejs.org
3. Check "Add to PATH" during installation
4. Restart terminal after installation

### Error: "ENOENT: no such file or directory"

**Cause:** Incorrect path or missing directory

**Solution:**
1. Verify the path exists: `dir C:\path\to\directory`
2. Use absolute paths, not relative
3. Escape backslashes: `C:\\Users\\...`
4. Or use forward slashes: `C:/Users/...`

### Error: "Access is denied"

**Cause:** Permission issues or file in use

**Solution:**
1. Run cmd as Administrator (right-click → Run as administrator)
2. Check antivirus isn't blocking execution
3. Ensure no other process is using the file
4. Check Windows Defender settings

## Configuration File Locations on Windows

**Claude Desktop:**
```
C:\Users\username\AppData\Roaming\Claude\claude_desktop_config.json
```

**Claude Code:**
```
C:\Users\username\.claude.json
```

**Cursor:**
```
C:\Users\username\.cursor\mcp.json
```

## Log File Locations on Windows

**Claude Desktop:**
```
C:\Users\username\AppData\Local\Claude\Logs\
```

**Cursor:**
```
C:\Users\username\AppData\Roaming\Cursor\logs\
```

## Testing on Windows

### Test npx directly:
```cmd
npx -y @modelcontextprotocol/server-filesystem C:\Users\username\Desktop
```

### Test with cmd wrapper:
```cmd
cmd /c npx -y @modelcontextprotocol/server-filesystem C:\Users\username\Desktop
```

### Test Node.js directly:
```cmd
node C:\path\to\server\index.js
```

## Complete Working Example for Windows

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "cmd",
      "args": [
        "/c",
        "npx",
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\username\\Documents"
      ]
    },
    "github": {
      "command": "cmd",
      "args": [
        "/c",
        "npx",
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here"
      }
    },
    "sqlite": {
      "command": "cmd",
      "args": [
        "/c",
        "uvx",
        "mcp-server-sqlite",
        "--db-path",
        "C:\\Users\\username\\databases\\mydata.db"
      ]
    }
  }
}
```

## Performance Optimization on Windows

### Cache npm packages globally:
```cmd
npm config set cache C:\npm-cache --global
```

### Use npm v7+ for faster installs:
```cmd
npm install -g npm@latest
```

### Disable npm update checks:
```cmd
npm config set update-notifier false
```

## Security Considerations

1. **Run as regular user, not Administrator** - Only use Administrator for installation
2. **Verify package authenticity** - Check @modelcontextprotocol scope on npm
3. **Use environment variables for secrets** - Never hardcode tokens
4. **Keep Node.js updated** - Security patches matter
5. **Review server code** - Especially for community servers

## Still Having Issues?

1. **Clear npm cache:**
   ```cmd
   npm cache clean --force
   ```

2. **Reinstall Node.js:**
   - Uninstall completely
   - Delete `C:\Users\username\AppData\Roaming\npm`
   - Reinstall from https://nodejs.org
   - Choose "Add to PATH" option

3. **Check Windows version:**
   - Windows 10 version 1909 or later recommended
   - Windows 11 fully supported

4. **Disable antivirus temporarily:**
   - Test if antivirus is blocking execution
   - Add npm/node to exclusions if needed

5. **Use Windows Terminal:**
   - Better than cmd.exe
   - Install from Microsoft Store
   - Better Unicode and path support
