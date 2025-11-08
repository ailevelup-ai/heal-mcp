# MCP Error Codes and Solutions

Complete reference for Model Context Protocol error codes and their solutions.

## Error -32000: Connection Closed

**This is the most common MCP error.** It occurs when the connection between client and server terminates unexpectedly.

### Symptoms
- Server appears in configuration but no tools show
- Logs show "Starting new stdio process" followed immediately by "Client closed"
- Error message: "Failed to reload client: MCP error -32000: Connection closed"
- Previously working servers suddenly stop functioning

### Root Causes

#### 1. Windows npx Batch Script Issue (Most Common on Windows)
**Cause:** Windows cannot execute batch scripts without a command interpreter.

**Solution:** Wrap npx with cmd
```json
{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "package-name"]
}
```

See `reference/windows-issues.md` for complete Windows troubleshooting.

#### 2. Stdout Pollution (Most Common on macOS/Linux)
**Cause:** Server writes non-JSON-RPC data to stdout, corrupting the protocol stream.

**What breaks it:**
- `console.log()` statements in Node.js servers
- `print()` statements in Python servers (should use stderr)
- Any debug output going to stdout
- Welcome messages or startup banners

**Solution:** Audit server code and change all logging to stderr:
- Node.js: `console.error()` instead of `console.log()`
- Python: `sys.stderr.write()` instead of `print()`

**Testing:**
```bash
# Run server directly and check output
npx -y @modelcontextprotocol/server-name | cat

# Should see ONLY JSON-RPC messages like:
# {"jsonrpc":"2.0","method":"...","params":{...}}

# Should NOT see:
# - "Server starting..."
# - Debug messages
# - Plain text
```

#### 3. Server Process Exit
**Cause:** The server process terminates before establishing connection.

**Common reasons:**
- Missing dependencies
- Uncaught exceptions during startup
- Permission denied errors
- Port conflicts (for HTTP/SSE servers)

**Solution:** Test server independently:
```bash
# Should start and wait, not exit immediately
npx -y @modelcontextprotocol/server-filesystem ~/Desktop

# If it exits, check:
node --version  # Must be 18+
python3 --version  # Must be 3.10+
```

#### 4. Command Not Found
**Cause:** The specified command isn't in PATH or doesn't exist.

**Solution:**
- Verify installation: `which node`, `which python3`
- Use full paths: `/usr/local/bin/node`
- Check PATH in environment

#### 5. Invalid Configuration
**Cause:** Malformed JSON or missing required fields.

**Solution:** Run validation:
```bash
python3 ~/.claude/skills/heal_mcp/scripts/validate-config.py
```

## Error -32001: Request Timeout

**Cause:** Server took too long to respond to a request.

### Symptoms
- Operations start but never complete
- Loading indicators that never finish
- Timeout errors in logs

### Solutions

1. **Increase timeout in configuration:**
```json
{
  "command": "npx",
  "args": ["..."],
  "timeout": 30000  // 30 seconds
}
```

2. **Check server performance:**
- Is the operation computationally expensive?
- Are there network delays?
- Is the database/file system slow?

3. **Optimize server code:**
- Add caching
- Use async operations
- Index databases properly

## Error -32600: Invalid Request

**Cause:** Client sent a malformed JSON-RPC request.

### Symptoms
- Specific tools fail while others work
- Error messages about invalid parameters

### Solutions

1. **Check tool parameters:**
- Verify parameter types match schema
- Ensure required parameters are provided
- Check parameter names are correct

2. **Update client:**
- Older clients may have bugs
- Update Claude Desktop/Code/Cursor

## Error -32601: Method Not Found

**Cause:** Client requested a method the server doesn't implement.

### Symptoms
- Error about unknown method
- Tool appears but doesn't execute

### Solutions

1. **Verify server version:**
```bash
npm view @modelcontextprotocol/server-name version
```

2. **Check protocol version compatibility:**
- Server may be outdated
- Update: `npm install -g package-name@latest`

3. **Verify tool availability:**
```bash
npx @modelcontextprotocol/inspector node server.js
```

## Error -32602: Invalid Params

**Cause:** Request parameters don't match the method's schema.

### Symptoms
- Tool fails with parameter error
- Error messages about type mismatches

### Solutions

1. **Check parameter types:**
- String vs Number
- Array vs Object
- Required vs Optional

2. **Review server documentation:**
- Check expected parameter format
- Verify examples in README

## Error -32603: Internal Error

**Cause:** Server encountered an unexpected error during execution.

### Symptoms
- Stack traces in logs
- Random failures
- Inconsistent behavior

### Solutions

1. **Check server logs:**
- Look for exceptions
- Identify the failing operation
- Check for null/undefined errors

2. **Report to server maintainer:**
- Include full stack trace
- Provide reproduction steps
- Share configuration

## Connection Errors (Non-JSON-RPC)

### "ENOENT: no such file or directory"
**Cause:** File or directory path doesn't exist.

**Solution:**
- Verify path exists
- Use absolute paths
- Check permissions

### "EACCES: permission denied"
**Cause:** Insufficient permissions to access file/directory.

**Solution:**
```bash
chmod +x /path/to/server
chmod 755 /path/to/directory
```

### "EADDRINUSE: address already in use"
**Cause:** Port is already taken (HTTP/SSE servers only).

**Solution:**
- Change port in configuration
- Kill process using the port
- Use different server instance

### "Cannot find module"
**Cause:** Missing npm/pip package.

**Solution:**
```bash
# For npm
npm install -g package-name

# For Python
pip install package-name
# or
uvx package-name
```

## Diagnostic Workflow for Error -32000

Use this systematic approach:

### Step 1: Verify Basic Configuration
```bash
# Check JSON syntax
python3 ~/.claude/skills/heal_mcp/scripts/validate-config.py
```

### Step 2: Test Server Independence
```bash
# Should start without errors
npx -y @modelcontextprotocol/server-name args
```

### Step 3: Check Logs
- macOS: `~/Library/Logs/Claude/mcp-server-NAME.log`
- Windows: `%LOCALAPPDATA%\Claude\Logs\mcp-server-NAME.log`

Look for:
- Command that was executed
- Immediate exit vs timeout
- Error messages

### Step 4: Platform-Specific Checks

**Windows:**
- Is npx wrapped with cmd?
- Are paths escaped properly?

**macOS/Linux:**
- Any stdout pollution?
- Permissions correct?

### Step 5: Use MCP Inspector
```bash
npx @modelcontextprotocol/inspector node server.js
```

Opens http://localhost:6274 for interactive testing.

## Preventing Errors

### Best Practices

1. **Always use absolute paths**
   ```json
   "args": ["/Users/username/Desktop"]  // Good
   "args": ["~/Desktop"]  // May fail
   "args": ["./Desktop"]  // Will fail
   ```

2. **Validate JSON before saving**
   - Use a JSON validator
   - Run validation script
   - Check for trailing commas

3. **Test servers independently first**
   - Run command in terminal
   - Verify it starts successfully
   - Check output format

4. **Keep dependencies updated**
   ```bash
   npm update -g
   uv tool upgrade --all
   ```

5. **Monitor logs regularly**
   - Check for warnings
   - Look for deprecation notices
   - Identify patterns

6. **Use environment variables for secrets**
   ```json
   {
     "env": {
       "API_KEY": "${API_KEY}"  // Good
       // "API_KEY": "sk-1234..."  // Bad - hardcoded
     }
   }
   ```

## Getting Help

If errors persist:

1. **Search GitHub Issues:**
   - https://github.com/modelcontextprotocol/servers/issues
   - Search for exact error message
   - Check closed issues for solutions

2. **Use MCP Inspector:**
   - Isolates server testing
   - Shows raw protocol messages
   - Identifies protocol violations

3. **Check Community Resources:**
   - Awesome Claude Skills: https://github.com/travisvn/awesome-claude-skills
   - MCP Documentation: https://modelcontextprotocol.io
   - Claude Documentation: https://docs.claude.com

4. **Provide Complete Information:**
   - Exact error message
   - Platform (Windows/macOS/Linux)
   - Client (Claude Desktop/Code/Cursor)
   - Server name and version
   - Configuration (redact secrets)
   - Relevant log excerpts

## Quick Reference

| Error | Most Likely Cause | First Action |
|-------|------------------|--------------|
| -32000 | Connection failed | Check Windows npx wrapping |
| -32001 | Timeout | Increase timeout setting |
| -32600 | Invalid request | Check parameter types |
| -32601 | Method not found | Update server version |
| -32602 | Invalid params | Review parameter schema |
| -32603 | Internal error | Check server logs |
| ENOENT | Path not found | Use absolute paths |
| EACCES | Permission denied | Fix file permissions |
