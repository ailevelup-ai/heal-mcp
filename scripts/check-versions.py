#!/usr/bin/env python3
"""
MCP Server Version Checker
Automatically checks all configured MCP servers for available updates
"""

import json
import subprocess
import sys
import re
from pathlib import Path
from typing import Dict, Optional, Tuple

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def get_npm_latest_version(package_name: str) -> Optional[str]:
    """Get latest version of npm package"""
    try:
        result = subprocess.run(
            ['npm', 'view', package_name, 'version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"  ⚠️  Error checking npm package {package_name}: {e}", file=sys.stderr)
    return None

def get_pypi_latest_version(package_name: str) -> Optional[str]:
    """Get latest version of PyPI package"""
    try:
        result = subprocess.run(
            ['pip', 'index', 'versions', package_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            # Parse output like "package-name (1.0.0)"
            match = re.search(r'\(([0-9.]+)\)', result.stdout.split('\n')[0])
            if match:
                return match.group(1)
    except Exception as e:
        print(f"  ⚠️  Error checking PyPI package {package_name}: {e}", file=sys.stderr)
    return None

def extract_package_name(args: list) -> Tuple[Optional[str], Optional[str]]:
    """Extract package name and type from MCP server args"""
    # Handle npx packages
    if 'npx' in args or args[0] == 'npx':
        for i, arg in enumerate(args):
            if arg == '-y' and i + 1 < len(args):
                package = args[i + 1]
                # Remove @latest suffix if present
                package = package.replace('@latest', '')
                return package, 'npm'
            elif not arg.startswith('-') and '@' in arg and '/' in arg:
                package = arg.replace('@latest', '')
                return package, 'npm'
    
    # Handle uvx packages
    elif 'uvx' in args or args[0] == 'uvx':
        for arg in args:
            if not arg.startswith('-') and not arg == 'uvx':
                package = arg.replace('@latest', '')
                return package, 'pypi'
    
    # Handle pnpm/npm direct packages
    elif 'pnpm' in args or 'npm' in args:
        # This is likely a local package, skip version check
        return None, 'local'
    
    return None, None

def compare_versions(current: str, latest: str) -> str:
    """Compare version strings and return status"""
    if current == latest:
        return 'up-to-date'
    
    # Simple version comparison (works for semantic versioning)
    def parse_version(v):
        return [int(x) for x in v.split('.') if x.isdigit()]
    
    try:
        current_parts = parse_version(current)
        latest_parts = parse_version(latest)
        
        if current_parts < latest_parts:
            return 'outdated'
        elif current_parts > latest_parts:
            return 'ahead'
    except:
        pass
    
    return 'unknown'

def check_config_file(config_path: Path, platform: str) -> Dict:
    """Check all MCP servers in a config file"""
    results = []
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Handle different config structures
        servers = {}
        if platform == 'claude-desktop':
            servers = config.get('mcpServers', {})
        elif platform == 'cursor':
            servers = config.get('mcpServers', {})
        elif platform == 'claude-code':
            # Claude Code has project-specific configs
            for project_path, project_data in config.get('projects', {}).items():
                servers.update(project_data.get('mcpServers', {}))
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}📦 {platform.upper()}{Colors.END}")
        print(f"Config: {config_path}")
        print(f"Servers found: {len(servers)}\n")
        
        for server_name, server_config in servers.items():
            command = server_config.get('command', '')
            args = server_config.get('args', [])
            
            package_name, package_type = extract_package_name([command] + args)
            
            if not package_name or package_type == 'local':
                print(f"  • {Colors.BOLD}{server_name}{Colors.END}")
                print(f"    Type: Local/Custom")
                print(f"    Command: {command}")
                results.append({
                    'server': server_name,
                    'status': 'local',
                    'platform': platform
                })
                continue
            
            # Check for latest version
            latest_version = None
            if package_type == 'npm':
                latest_version = get_npm_latest_version(package_name)
            elif package_type == 'pypi':
                latest_version = get_pypi_latest_version(package_name)
            
            # Determine current version from args
            current_version = 'latest'
            for arg in args:
                if '@' in arg and package_name in arg:
                    parts = arg.split('@')
                    if len(parts) > 1 and parts[-1] != 'latest':
                        current_version = parts[-1]
                        break
            
            # Display results
            print(f"  • {Colors.BOLD}{server_name}{Colors.END}")
            print(f"    Package: {package_name}")
            print(f"    Type: {package_type}")
            
            if latest_version:
                if current_version == 'latest':
                    print(f"    Version: {Colors.GREEN}@latest{Colors.END} (currently {latest_version})")
                    status = 'latest-tag'
                else:
                    comparison = compare_versions(current_version, latest_version)
                    if comparison == 'up-to-date':
                        print(f"    Version: {Colors.GREEN}{current_version}{Colors.END} ✓")
                        status = 'up-to-date'
                    elif comparison == 'outdated':
                        print(f"    Current: {Colors.YELLOW}{current_version}{Colors.END}")
                        print(f"    Latest:  {Colors.GREEN}{latest_version}{Colors.END}")
                        print(f"    {Colors.YELLOW}⚠️  UPDATE AVAILABLE{Colors.END}")
                        status = 'outdated'
                    else:
                        print(f"    Version: {current_version}")
                        print(f"    Latest: {latest_version}")
                        status = 'unknown'
            else:
                print(f"    Version: {current_version}")
                print(f"    {Colors.RED}❌ Could not check latest version{Colors.END}")
                status = 'check-failed'
            
            print()
            
            results.append({
                'server': server_name,
                'package': package_name,
                'current': current_version,
                'latest': latest_version,
                'status': status,
                'platform': platform
            })
    
    except FileNotFoundError:
        print(f"{Colors.YELLOW}⚠️  Config file not found: {config_path}{Colors.END}")
    except json.JSONDecodeError:
        print(f"{Colors.RED}❌ Invalid JSON in config: {config_path}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Error checking {platform}: {e}{Colors.END}")
    
    return results

def print_summary(all_results: list):
    """Print summary of all checks"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}📊 SUMMARY{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    outdated = [r for r in all_results if r.get('status') == 'outdated']
    up_to_date = [r for r in all_results if r.get('status') in ['up-to-date', 'latest-tag']]
    local = [r for r in all_results if r.get('status') == 'local']
    failed = [r for r in all_results if r.get('status') == 'check-failed']
    
    print(f"{Colors.GREEN}✓ Up to date:{Colors.END} {len(up_to_date)} servers")
    print(f"{Colors.YELLOW}⚠ Updates available:{Colors.END} {len(outdated)} servers")
    print(f"{Colors.BLUE}• Local/Custom:{Colors.END} {len(local)} servers")
    print(f"{Colors.RED}✗ Check failed:{Colors.END} {len(failed)} servers")
    
    if outdated:
        print(f"\n{Colors.BOLD}Updates Available:{Colors.END}")
        for result in outdated:
            print(f"  • {result['server']} ({result['platform']})")
            print(f"    {result['current']} → {result['latest']}")
    
    print()

def main():
    """Main entry point"""
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}🔍 MCP Server Version Checker{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    
    home = Path.home()
    all_results = []
    
    # Check Claude Desktop (macOS)
    claude_desktop_config = home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    if claude_desktop_config.exists():
        results = check_config_file(claude_desktop_config, 'claude-desktop')
        all_results.extend(results)
    
    # Check Cursor
    cursor_config = home / ".cursor" / "mcp.json"
    if cursor_config.exists():
        results = check_config_file(cursor_config, 'cursor')
        all_results.extend(results)
    
    # Check Claude Code
    claude_code_config = home / ".claude.json"
    if claude_code_config.exists():
        results = check_config_file(claude_code_config, 'claude-code')
        all_results.extend(results)
    
    # Print summary
    if all_results:
        print_summary(all_results)
    else:
        print(f"\n{Colors.YELLOW}⚠️  No MCP configurations found{Colors.END}\n")

if __name__ == "__main__":
    main()
