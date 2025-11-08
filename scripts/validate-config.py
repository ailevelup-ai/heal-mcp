#!/usr/bin/env python3
"""
MCP Configuration Validator
Validates JSON configuration files for Claude Desktop, Claude Code, and Cursor
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def find_config_files() -> List[Path]:
    """Find all MCP configuration files on the system"""
    configs = []
    home = Path.home()
    
    # Claude Desktop (macOS)
    claude_desktop = home / "Library/Application Support/Claude/claude_desktop_config.json"
    if claude_desktop.exists():
        configs.append(("Claude Desktop", claude_desktop))
    
    # Claude Code user scope
    claude_code_user = home / ".claude.json"
    if claude_code_user.exists():
        configs.append(("Claude Code (User)", claude_code_user))
    
    # Cursor global
    cursor_global = home / ".cursor/mcp.json"
    if cursor_global.exists():
        configs.append(("Cursor (Global)", cursor_global))
    
    # Check current directory for project configs
    project_claude = Path(".mcp.json")
    if project_claude.exists():
        configs.append(("Claude Code (Project)", project_claude))
    
    project_cursor = Path(".cursor/mcp.json")
    if project_cursor.exists():
        configs.append(("Cursor (Project)", project_cursor))
    
    return configs

def validate_json_syntax(config_path: Path) -> Tuple[bool, str, Dict]:
    """Validate JSON syntax and return parsed config"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return True, "Valid JSON syntax", config
    except json.JSONDecodeError as e:
        return False, f"JSON syntax error at line {e.lineno}, column {e.colno}: {e.msg}", None
    except Exception as e:
        return False, f"Error reading file: {str(e)}", None

def validate_mcp_structure(config: Dict, platform: str) -> List[str]:
    """Validate MCP server configuration structure"""
    issues = []
    
    # Check for mcpServers key
    if "mcpServers" not in config:
        issues.append("Missing 'mcpServers' root key")
        return issues
    
    servers = config["mcpServers"]
    if not isinstance(servers, dict):
        issues.append("'mcpServers' must be an object/dictionary")
        return issues
    
    # Validate each server
    for server_name, server_config in servers.items():
        if not isinstance(server_config, dict):
            issues.append(f"Server '{server_name}': configuration must be an object")
            continue
        
        # Check required fields
        if "command" not in server_config:
            issues.append(f"Server '{server_name}': missing required 'command' field")
        
        if "args" in server_config:
            if not isinstance(server_config["args"], list):
                issues.append(f"Server '{server_name}': 'args' must be an array")
        
        if "env" in server_config:
            if not isinstance(server_config["env"], dict):
                issues.append(f"Server '{server_name}': 'env' must be an object")
        
        # Check command executability
        command = server_config.get("command", "")
        if command and command not in ["npx", "uvx", "node", "python", "python3", "docker", "cmd"]:
            # Check if it's a full path
            if not os.path.isfile(command):
                issues.append(f"Server '{server_name}': command '{command}' not found in PATH")
    
    return issues

def check_common_issues(config: Dict, platform: str) -> List[str]:
    """Check for common configuration issues"""
    warnings = []
    
    servers = config.get("mcpServers", {})
    
    for server_name, server_config in servers.items():
        command = server_config.get("command", "")
        args = server_config.get("args", [])
        
        # Windows npx issue
        if sys.platform == "win32" and command == "npx":
            warnings.append(
                f"Server '{server_name}': Windows detected with npx command. "
                f"Consider wrapping with cmd: 'command': 'cmd', 'args': ['/c', 'npx', ...]"
            )
        
        # Missing -y flag for npx
        if command == "npx" and "-y" not in args:
            warnings.append(
                f"Server '{server_name}': npx without -y flag may prompt for installation"
            )
        
        # Scoped package names with uvx
        if command == "uvx":
            for arg in args:
                if arg.startswith("@") and "/" in arg:
                    warnings.append(
                        f"Server '{server_name}': uvx with scoped package '{arg}' may fail. "
                        f"Consider using npx instead"
                    )
        
        # Environment variables
        env = server_config.get("env", {})
        for key, value in env.items():
            if value and len(value) < 10 and not value.startswith("${"):
                warnings.append(
                    f"Server '{server_name}': env variable '{key}' looks suspicious. "
                    f"Ensure it's not a hardcoded secret"
                )
    
    return warnings

def print_results(platform: str, config_path: Path, valid: bool, message: str, 
                 config: Dict, issues: List[str], warnings: List[str]):
    """Print validation results"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}Platform: {platform}{Colors.END}")
    print(f"{Colors.BOLD}Config: {config_path}{Colors.END}")
    print(f"{'='*60}")
    
    # JSON syntax
    if valid:
        print(f"{Colors.GREEN}✓ {message}{Colors.END}")
    else:
        print(f"{Colors.RED}✗ {message}{Colors.END}")
        return
    
    # Structure validation
    if not issues:
        print(f"{Colors.GREEN}✓ Configuration structure is valid{Colors.END}")
    else:
        print(f"{Colors.RED}✗ Configuration issues found:{Colors.END}")
        for issue in issues:
            print(f"  {Colors.RED}• {issue}{Colors.END}")
    
    # Warnings
    if warnings:
        print(f"{Colors.YELLOW}⚠ Warnings:{Colors.END}")
        for warning in warnings:
            print(f"  {Colors.YELLOW}• {warning}{Colors.END}")
    
    # Server summary
    if config and "mcpServers" in config:
        servers = config["mcpServers"]
        print(f"\n{Colors.BOLD}Servers configured: {len(servers)}{Colors.END}")
        for server_name in servers.keys():
            print(f"  • {server_name}")

def main():
    """Main validation function"""
    print(f"{Colors.BOLD}{Colors.BLUE}MCP Configuration Validator{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    # Find all config files
    config_files = find_config_files()
    
    if not config_files:
        print(f"{Colors.YELLOW}No MCP configuration files found.{Colors.END}")
        print("\nSearched locations:")
        print("  • ~/Library/Application Support/Claude/claude_desktop_config.json")
        print("  • ~/.claude.json")
        print("  • ~/.cursor/mcp.json")
        print("  • .mcp.json (current directory)")
        print("  • .cursor/mcp.json (current directory)")
        return 1
    
    all_valid = True
    
    # Validate each config file
    for platform, config_path in config_files:
        valid, message, config = validate_json_syntax(config_path)
        
        issues = []
        warnings = []
        if valid and config:
            issues = validate_mcp_structure(config, platform)
            warnings = check_common_issues(config, platform)
        
        print_results(platform, config_path, valid, message, config, issues, warnings)
        
        if not valid or issues:
            all_valid = False
    
    # Final summary
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    if all_valid:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All configurations are valid!{Colors.END}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Some configurations have issues{Colors.END}")
        print(f"\nFix the issues above and run this script again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
