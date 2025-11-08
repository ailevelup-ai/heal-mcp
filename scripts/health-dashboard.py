#!/usr/bin/env python3
"""
MCP Health Dashboard
Provides a comprehensive overview of all MCP servers across all platforms
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ServerHealth:
    """Represents health status of an MCP server"""
    def __init__(self, name: str, platform: str):
        self.name = name
        self.platform = platform
        self.config_valid = False
        self.command_exists = False
        self.dependencies_met = False
        self.latest_version = None
        self.current_version = None
        self.errors = []
        self.warnings = []
        
    def is_healthy(self) -> bool:
        """Check if server is completely healthy"""
        return (self.config_valid and 
                self.command_exists and 
                self.dependencies_met and 
                len(self.errors) == 0)
    
    def get_status_icon(self) -> str:
        """Get status icon for display"""
        if self.is_healthy():
            return f"{Colors.GREEN}✓{Colors.END}"
        elif len(self.errors) > 0:
            return f"{Colors.RED}✗{Colors.END}"
        else:
            return f"{Colors.YELLOW}⚠{Colors.END}"
    
    def get_status_text(self) -> str:
        """Get human-readable status"""
        if self.is_healthy():
            return f"{Colors.GREEN}Healthy{Colors.END}"
        elif len(self.errors) > 0:
            return f"{Colors.RED}Failed{Colors.END}"
        else:
            return f"{Colors.YELLOW}Warning{Colors.END}"

def check_command_exists(command: str) -> bool:
    """Check if a command is available"""
    try:
        subprocess.run(
            ['which', command],
            capture_output=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

def check_node_version() -> Optional[str]:
    """Get Node.js version"""
    try:
        result = subprocess.run(
            ['node', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def check_python_version() -> Optional[str]:
    """Get Python version"""
    try:
        result = subprocess.run(
            ['python3', '--version'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().replace('Python ', '')
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def analyze_config(config_path: Path, platform: str) -> List[ServerHealth]:
    """Analyze a configuration file and return health status for each server"""
    servers = []
    
    try:
        with open(config_path) as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        return []
    except FileNotFoundError:
        return []
    
    # Get the mcpServers section
    mcp_servers = config.get('mcpServers', {})
    
    for server_name, server_config in mcp_servers.items():
        health = ServerHealth(server_name, platform)
        
        # Check basic config validity
        if 'command' in server_config:
            health.config_valid = True
        else:
            health.errors.append("Missing 'command' field")
        
        # Check if command exists
        command = server_config.get('command', '')
        if command:
            if command == 'npx':
                health.command_exists = check_command_exists('npx')
                if not health.command_exists:
                    health.errors.append("npx not found")
            elif command == 'uvx':
                health.command_exists = check_command_exists('uvx')
                if not health.command_exists:
                    health.errors.append("uvx not found")
            elif command == 'node':
                health.command_exists = check_command_exists('node')
                if not health.command_exists:
                    health.errors.append("node not found")
            elif command == 'python3':
                health.command_exists = check_command_exists('python3')
                if not health.command_exists:
                    health.errors.append("python3 not found")
            else:
                # Check if command is a path
                cmd_path = Path(command)
                if cmd_path.exists():
                    health.command_exists = True
                else:
                    health.command_exists = check_command_exists(command)
                    if not health.command_exists:
                        health.warnings.append(f"Command '{command}' not found in PATH")
        
        # Check for environment variables
        env = server_config.get('env', {})
        for key, value in env.items():
            if not value or value == '':
                health.warnings.append(f"Environment variable '{key}' is empty")
        
        # Check args for common issues
        args = server_config.get('args', [])
        if command == 'npx' and '-y' not in args:
            health.warnings.append("Consider adding '-y' flag to npx command")
        
        servers.append(health)
    
    return servers

def print_dashboard_header():
    """Print dashboard header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}🏥 MCP Health Dashboard{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")
    
    # System dependencies
    print(f"{Colors.BOLD}System Dependencies:{Colors.END}")
    node_version = check_node_version()
    python_version = check_python_version()
    
    if node_version:
        print(f"  Node.js: {Colors.GREEN}✓{Colors.END} {node_version}")
    else:
        print(f"  Node.js: {Colors.RED}✗{Colors.END} Not found")
    
    if python_version:
        print(f"  Python:  {Colors.GREEN}✓{Colors.END} {python_version}")
    else:
        print(f"  Python:  {Colors.RED}✗{Colors.END} Not found")
    
    print(f"  npx:     {Colors.GREEN}✓{Colors.END}" if check_command_exists('npx') else f"  npx:     {Colors.RED}✗{Colors.END}")
    print(f"  uvx:     {Colors.GREEN}✓{Colors.END}" if check_command_exists('uvx') else f"  uvx:     {Colors.YELLOW}○{Colors.END} Optional")
    print()

def print_platform_section(platform: str, servers: List[ServerHealth]):
    """Print a platform section"""
    if not servers:
        return
    
    print(f"{Colors.BOLD}{Colors.CYAN}{platform.upper()}:{Colors.END}")
    print(f"{Colors.CYAN}{'─'*80}{Colors.END}")
    
    # Summary
    healthy = sum(1 for s in servers if s.is_healthy())
    failed = sum(1 for s in servers if len(s.errors) > 0)
    warnings = sum(1 for s in servers if len(s.warnings) > 0 and len(s.errors) == 0)
    
    print(f"  Total: {len(servers)} servers | ", end='')
    print(f"{Colors.GREEN}{healthy} healthy{Colors.END} | ", end='')
    if warnings > 0:
        print(f"{Colors.YELLOW}{warnings} warnings{Colors.END} | ", end='')
    if failed > 0:
        print(f"{Colors.RED}{failed} failed{Colors.END}")
    else:
        print()
    
    print()
    
    # Server details
    for server in servers:
        print(f"  {server.get_status_icon()} {Colors.BOLD}{server.name}{Colors.END}")
        print(f"     Status: {server.get_status_text()}")
        
        if not server.config_valid:
            print(f"     Config: {Colors.RED}Invalid{Colors.END}")
        else:
            print(f"     Config: {Colors.GREEN}Valid{Colors.END}")
        
        if not server.command_exists:
            print(f"     Command: {Colors.RED}Not found{Colors.END}")
        else:
            print(f"     Command: {Colors.GREEN}Available{Colors.END}")
        
        if server.errors:
            print(f"     {Colors.RED}Errors:{Colors.END}")
            for error in server.errors:
                print(f"       • {error}")
        
        if server.warnings:
            print(f"     {Colors.YELLOW}Warnings:{Colors.END}")
            for warning in server.warnings:
                print(f"       • {warning}")
        
        print()
    
    print()

def print_summary(all_servers: List[ServerHealth]):
    """Print overall summary"""
    if not all_servers:
        print(f"{Colors.YELLOW}No MCP servers found in any configuration{Colors.END}\n")
        return
    
    total = len(all_servers)
    healthy = sum(1 for s in all_servers if s.is_healthy())
    failed = sum(1 for s in all_servers if len(s.errors) > 0)
    warnings = sum(1 for s in all_servers if len(s.warnings) > 0 and len(s.errors) == 0)
    
    print(f"{Colors.BOLD}{'─'*80}{Colors.END}")
    print(f"{Colors.BOLD}Overall Summary:{Colors.END}")
    print(f"  Total servers: {total}")
    print(f"  {Colors.GREEN}Healthy: {healthy} ({healthy*100//total}%){Colors.END}")
    if warnings > 0:
        print(f"  {Colors.YELLOW}Warnings: {warnings} ({warnings*100//total}%){Colors.END}")
    if failed > 0:
        print(f"  {Colors.RED}Failed: {failed} ({failed*100//total}%){Colors.END}")
    
    print(f"\n{Colors.BOLD}Recommendations:{Colors.END}")
    if failed > 0:
        print(f"  • Run: {Colors.CYAN}python3 ~/.claude/skills/heal_mcp/scripts/interactive-repair.py{Colors.END}")
    elif warnings > 0:
        print(f"  • Review warnings and consider updating configurations")
    else:
        print(f"  • {Colors.GREEN}All systems operational!{Colors.END}")
    
    print()

def main():
    """Main entry point"""
    print_dashboard_header()
    
    home = Path.home()
    all_servers = []
    
    # Check Claude Desktop (macOS)
    claude_desktop_config = home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    if claude_desktop_config.exists():
        servers = analyze_config(claude_desktop_config, 'Claude Desktop')
        print_platform_section('Claude Desktop', servers)
        all_servers.extend(servers)
    
    # Check Cursor
    cursor_config = home / ".cursor" / "mcp.json"
    if cursor_config.exists():
        servers = analyze_config(cursor_config, 'Cursor')
        print_platform_section('Cursor', servers)
        all_servers.extend(servers)
    
    # Check Claude Code
    claude_code_config = home / ".claude.json"
    if claude_code_config.exists():
        servers = analyze_config(claude_code_config, 'Claude Code')
        print_platform_section('Claude Code', servers)
        all_servers.extend(servers)
    
    # Print summary
    print_summary(all_servers)

if __name__ == "__main__":
    main()
