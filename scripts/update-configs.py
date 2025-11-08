#!/usr/bin/env python3
"""
Auto-update MCP server versions in configuration files
Part of the heal_mcp skill - FIXED VERSION
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Server version updates to apply
# FIXED: Now uses exact package name matching instead of partial replacement
UPDATES = {
    'claude-desktop': {
        'aws-kb-retrieval': {
            'new': '@modelcontextprotocol/server-aws-kb-retrieval@0.6.2'
        },
        'filesystem': {
            'new': '@modelcontextprotocol/server-filesystem@2025.8.21'
        },
        'github': {
            'new': '@modelcontextprotocol/server-github@2025.4.8'
        },
        'sequential-thinking': {
            'new': '@modelcontextprotocol/server-sequential-thinking@2025.7.1'
        }
    },
    'cursor': {
        'sequentialthinking': {
            'new': '@modelcontextprotocol/server-sequential-thinking@2025.7.1'
        },
        'bravesearch': {
            'new': '@modelcontextprotocol/server-brave-search@0.6.2'
        },
        'desktop-commander': {
            'new': '@wonderwhy-er/desktop-commander@0.2.19'
        }
    },
    'claude-code': {
        'aws-kb-retrieval': {
            'new': '@modelcontextprotocol/server-aws-kb-retrieval@0.6.2'
        },
        'mcp-installer': {
            'new': '@anaisbetts/mcp-installer@0.5.0'
        },
        'github': {
            'new': '@modelcontextprotocol/server-github@2025.4.8'
        },
        'puppeteer': {
            'new': '@modelcontextprotocol/server-puppeteer@2025.5.12'
        },
        'stripe': {
            'new': '@stripe/mcp@0.2.5'
        }
    }
}

def update_config_file(config_path: Path, platform: str, updates: Dict) -> Tuple[int, List[str]]:
    """Update a single config file with new versions"""
    
    if not config_path.exists():
        print(f"{Colors.YELLOW}⚠️  Config not found: {config_path}{Colors.END}")
        return 0, []
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}✗ Failed to parse {config_path}: {e}{Colors.END}")
        return 0, []
    
    # Get the mcpServers section
    if platform == 'claude-code':
        # Claude Code stores servers in projects
        servers_updated = 0
        updated_server_list = []
        
        for project_path, project_config in config.get('projects', {}).items():
            servers = project_config.get('mcpServers', {})
            count, srv_list = update_servers_dict(servers, updates, platform)
            servers_updated += count
            updated_server_list.extend(srv_list)
        
        if servers_updated > 0:
            try:
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                print(f"{Colors.GREEN}✓ Updated {config_path}{Colors.END}")
            except Exception as e:
                print(f"{Colors.RED}✗ Failed to write {config_path}: {e}{Colors.END}")
                return 0, []
        
        return servers_updated, updated_server_list
    else:
        servers = config.get('mcpServers', {})
        count, srv_list = update_servers_dict(servers, updates, platform)
        
        if count > 0:
            try:
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                print(f"{Colors.GREEN}✓ Updated {config_path}{Colors.END}")
            except Exception as e:
                print(f"{Colors.RED}✗ Failed to write {config_path}: {e}{Colors.END}")
                return 0, []
        
        return count, srv_list

def update_servers_dict(servers: Dict, updates: Dict, platform: str) -> Tuple[int, List[str]]:
    """Update servers in a dictionary"""
    updated_count = 0
    updated_servers = []
    
    for server_name, update_info in updates.items():
        if server_name not in servers:
            continue
            
        server_config = servers[server_name]
        
        # Check if this server uses npx with a package name
        if server_config.get('command') in ['npx', 'uvx']:
            args = server_config.get('args', [])
            
            # Find the package name argument (usually after -y flag)
            for i, arg in enumerate(args):
                # Skip flags
                if arg.startswith('-'):
                    continue
                
                # Check if this looks like a package name (contains @ or /)
                if '@' in arg or '/' in arg:
                    old_arg = args[i]
                    # FIXED: Direct replacement instead of partial string matching
                    args[i] = update_info['new']
                    
                    print(f"  {Colors.BLUE}→{Colors.END} {Colors.BOLD}{server_name}{Colors.END}")
                    print(f"    {old_arg}")
                    print(f"    {Colors.GREEN}→ {args[i]}{Colors.END}")
                    
                    updated_count += 1
                    updated_servers.append(server_name)
                    break
    
    return updated_count, updated_servers

def main():
    """Main entry point"""
    print(f"{Colors.BOLD}{Colors.BLUE}🔧 Updating MCP Server Configurations{Colors.END}")
    print()
    
    home = Path.home()
    total_updates = 0
    all_updated_servers = []
    
    # Update Claude Desktop
    print(f"{Colors.BOLD}{Colors.BLUE}📦 CLAUDE DESKTOP{Colors.END}")
    claude_desktop_config = home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    count, servers = update_config_file(claude_desktop_config, 'claude-desktop', UPDATES['claude-desktop'])
    total_updates += count
    all_updated_servers.extend([(s, 'claude-desktop') for s in servers])
    print()
    
    # Update Cursor
    print(f"{Colors.BOLD}{Colors.BLUE}📦 CURSOR{Colors.END}")
    cursor_config = home / ".cursor" / "mcp.json"
    count, servers = update_config_file(cursor_config, 'cursor', UPDATES['cursor'])
    total_updates += count
    all_updated_servers.extend([(s, 'cursor') for s in servers])
    print()
    
    # Update Claude Code
    print(f"{Colors.BOLD}{Colors.BLUE}📦 CLAUDE CODE{Colors.END}")
    claude_code_config = home / ".claude.json"
    count, servers = update_config_file(claude_code_config, 'claude-code', UPDATES['claude-code'])
    total_updates += count
    all_updated_servers.extend([(s, 'claude-code') for s in servers])
    print()
    
    # Summary
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    if total_updates > 0:
        print(f"{Colors.GREEN}✓ Updated {total_updates} servers across {len(set(s[1] for s in all_updated_servers))} platforms{Colors.END}")
        print()
        print(f"{Colors.BOLD}Updated servers:{Colors.END}")
        for server, platform in all_updated_servers:
            print(f"  • {server} ({platform})")
    else:
        print(f"{Colors.YELLOW}⚠️  No updates were applied{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")

if __name__ == "__main__":
    main()
