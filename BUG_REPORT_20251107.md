# Bug Report: MCP Server Update Script

## Summary
The `update-configs.py` script in the heal_mcp skill was causing malformed package names due to incorrect string replacement logic.

## The Bug

### Root Cause
The script used partial string replacement with `.replace()` method:

```python
args[i] = args[i].replace(update_info['old'], update_info['new'])
```

With UPDATES dictionary having:
```python
'aws-kb-retrieval': {
    'old': 'modelcontextprotocol/server-aws-kb-retrieval',  # Missing @ prefix!
    'new': '@modelcontextprotocol/server-aws-kb-retrieval@0.6.2'
}
```

### What Happened
Starting with: `@modelcontextprotocol/server-aws-kb-retrieval@0.6.2`

1. Found substring: `modelcontextprotocol/server-aws-kb-retrieval`
2. Replaced with: `@modelcontextprotocol/server-aws-kb-retrieval@0.6.2`
3. Result: `@@modelcontextprotocol/server-aws-kb-retrieval@0.6.2@0.6.2`

The replacement kept the existing `@` prefix and `@0.6.2` suffix, then inserted the full new package name in between.

## Symptoms
- Package names had double `@@` prefixes
- Version numbers were duplicated: `@0.6.2@0.6.2`
- MCP servers failed to connect with errors like:
  - "spawn npx ENOENT" 
  - "Server disconnected"
  - "Could not connect"

## Affected Servers
- aws-kb-retrieval
- filesystem
- github
- sequential-thinking

## The Fix

### Changed Approach
Instead of partial string replacement, now uses **direct replacement**:

```python
# Find the package name argument
for i, arg in enumerate(args):
    if arg.startswith('-'):
        continue
    
    # If it looks like a package name
    if '@' in arg or '/' in arg:
        old_arg = args[i]
        args[i] = update_info['new']  # Direct replacement!
        break
```

### Updated UPDATES Dictionary
Removed the 'old' pattern entirely - now only needs 'new':

```python
'aws-kb-retrieval': {
    'new': '@modelcontextprotocol/server-aws-kb-retrieval@0.6.2'
}
```

## Testing
Verified the fix by:
1. Running the updated script
2. Checking configuration files show correct package names
3. Restarting Claude Desktop
4. Confirming no MCP connection errors

## Prevention
- Added comments explaining the replacement logic
- Used exact matching instead of substring replacement
- Simplified UPDATES dictionary to reduce error potential

## Related Files
- `/Users/hotbots/.claude/skills/heal_mcp/scripts/update-configs.py` - Fixed script
- `/Users/hotbots/.claude/skills/heal_mcp/scripts/auto-update-servers.sh` - Wrapper script
- Backups saved to: `/Users/hotbots/.claude/skills/heal_mcp/backups/`

## Date
November 7, 2025
