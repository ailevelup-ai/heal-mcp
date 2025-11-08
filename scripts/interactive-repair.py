#!/usr/bin/env python3
"""
Interactive MCP Server Repair Tool
Provides step-by-step guided repairs for MCP server issues
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class BackupManager:
    """Manages configuration backups"""
    
    def __init__(self):
        self.backup_dir = Path.home() / ".claude" / "skills" / "heal_mcp" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, config_path: Path) -> Path:
        """Create a timestamped backup of a config file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        platform_name = self._get_platform_name(config_path)
        backup_subdir = self.backup_dir / timestamp
        backup_subdir.mkdir(exist_ok=True)
        
        backup_path = backup_subdir / f"{platform_name}_config.json"
        shutil.copy2(config_path, backup_path)
        
        # Save metadata
        metadata = {
            "original_path": str(config_path),
            "backup_time": timestamp,
            "platform": platform_name
        }
        metadata_path = backup_subdir / f"{platform_name}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return backup_path
    
    def _get_platform_name(self, config_path: Path) -> str:
        """Determine platform from config path"""
        path_str = str(config_path)
        if "Claude/claude_desktop_config" in path_str:
            return "claude-desktop"
        elif ".cursor" in path_str:
            return "cursor"
        elif ".claude.json" in path_str:
            return "claude-code"
        return "unknown"
    
    def list_backups(self) -> List[Dict]:
        """List all available backups"""
        backups = []
        for backup_dir in sorted(self.backup_dir.iterdir(), reverse=True):
            if not backup_dir.is_dir():
                continue
            
            for metadata_file in backup_dir.glob("*_metadata.json"):
                try:
                    with open(metadata_file) as f:
                        metadata = json.load(f)
                        metadata['backup_dir'] = backup_dir
                        backups.append(metadata)
                except:
                    pass
        
        return backups
    
    def restore_backup(self, backup_dir: Path, platform: str) -> bool:
        """Restore a backup"""
        config_file = backup_dir / f"{platform}_config.json"
        metadata_file = backup_dir / f"{platform}_metadata.json"
        
        if not config_file.exists() or not metadata_file.exists():
            return False
        
        with open(metadata_file) as f:
            metadata = json.load(f)
        
        original_path = Path(metadata['original_path'])
        
        # Create backup of current state before restoring
        if original_path.exists():
            current_backup = self.create_backup(original_path)
            print(f"  {Colors.YELLOW}Created backup of current state{Colors.END}")
        
        # Restore
        shutil.copy2(config_file, original_path)
        return True

def print_header():
    """Print tool header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}🔧 Interactive MCP Server Repair Tool{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

def get_user_choice(prompt: str, options: List[str], allow_skip: bool = True) -> Optional[str]:
    """Get user choice from a list of options"""
    print(f"\n{Colors.BOLD}{prompt}{Colors.END}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    if allow_skip:
        print(f"  0. Skip this fix")
    
    while True:
        try:
            choice = input(f"\n{Colors.CYAN}Enter choice: {Colors.END}").strip()
            if choice == '0' and allow_skip:
                return None
            
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
            
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")
        except (ValueError, KeyboardInterrupt):
            print(f"\n{Colors.YELLOW}Operation cancelled{Colors.END}")
            return None

def confirm_action(message: str) -> bool:
    """Ask user to confirm an action"""
    while True:
        response = input(f"\n{Colors.YELLOW}{message} (y/n): {Colors.END}").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print(f"{Colors.RED}Please enter 'y' or 'n'{Colors.END}")

def find_issues(config_path: Path) -> List[Dict]:
    """Find all issues in a configuration"""
    issues = []
    
    try:
        with open(config_path) as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        issues.append({
            'type': 'syntax',
            'severity': 'critical',
            'description': f'JSON syntax error: {e}',
            'fix': 'Manual correction required'
        })
        return issues
    
    mcp_servers = config.get('mcpServers', {})
    
    for server_name, server_config in mcp_servers.items():
        # Check for missing command
        if 'command' not in server_config:
            issues.append({
                'type': 'config',
                'severity': 'critical',
                'server': server_name,
                'description': 'Missing "command" field',
                'fix': 'add_command'
            })
        
        # Check for npx without -y flag
        command = server_config.get('command', '')
        args = server_config.get('args', [])
        
        if command == 'npx' and '-y' not in args:
            issues.append({
                'type': 'config',
                'severity': 'warning',
                'server': server_name,
                'description': 'npx command missing -y flag (may cause prompts)',
                'fix': 'add_npx_flag',
                'current_args': args
            })
        
        # Check for empty environment variables
        env = server_config.get('env', {})
        for key, value in env.items():
            if not value or value == '':
                issues.append({
                    'type': 'config',
                    'severity': 'warning',
                    'server': server_name,
                    'description': f'Environment variable "{key}" is empty',
                    'fix': 'set_env_var',
                    'env_key': key
                })
    
    return issues

def apply_fix(config_path: Path, issue: Dict, backup_mgr: BackupManager) -> bool:
    """Apply a fix for an issue"""
    # Create backup first
    print(f"\n{Colors.CYAN}Creating backup...{Colors.END}")
    backup_path = backup_mgr.create_backup(config_path)
    print(f"  {Colors.GREEN}✓{Colors.END} Backup saved to: {backup_path}")
    
    with open(config_path) as f:
        config = json.load(f)
    
    server_name = issue.get('server')
    fix_type = issue.get('fix')
    
    if fix_type == 'add_npx_flag':
        # Add -y flag to npx
        server_config = config['mcpServers'][server_name]
        args = server_config.get('args', [])
        
        if '-y' not in args:
            # Insert -y as first argument
            args.insert(0, '-y')
            server_config['args'] = args
            
            print(f"\n{Colors.GREEN}Applied fix:{Colors.END}")
            print(f"  Added '-y' flag to npx command for {server_name}")
    
    elif fix_type == 'set_env_var':
        # Set environment variable
        server_config = config['mcpServers'][server_name]
        env_key = issue.get('env_key')
        
        print(f"\n{Colors.YELLOW}Environment variable '{env_key}' needs a value{Colors.END}")
        env_value = input(f"Enter value for {env_key}: ").strip()
        
        if not env_value:
            print(f"{Colors.YELLOW}Skipping empty value{Colors.END}")
            return False
        
        if 'env' not in server_config:
            server_config['env'] = {}
        
        server_config['env'][env_key] = env_value
        print(f"\n{Colors.GREEN}Applied fix:{Colors.END}")
        print(f"  Set {env_key} = {env_value[:10]}..." if len(env_value) > 10 else f"  Set {env_key} = {env_value}")
    
    # Write updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return True

def repair_workflow(config_path: Path):
    """Interactive repair workflow"""
    backup_mgr = BackupManager()
    
    print(f"\n{Colors.BOLD}Analyzing: {Colors.CYAN}{config_path}{Colors.END}\n")
    
    issues = find_issues(config_path)
    
    if not issues:
        print(f"{Colors.GREEN}✓ No issues found! Configuration looks good.{Colors.END}\n")
        return
    
    # Categorize issues
    critical = [i for i in issues if i['severity'] == 'critical']
    warnings = [i for i in issues if i['severity'] == 'warning']
    
    print(f"{Colors.BOLD}Issues found:{Colors.END}")
    if critical:
        print(f"  {Colors.RED}Critical: {len(critical)}{Colors.END}")
    if warnings:
        print(f"  {Colors.YELLOW}Warnings: {len(warnings)}{Colors.END}")
    
    print()
    
    # Show issues and offer fixes
    for i, issue in enumerate(issues, 1):
        severity_color = Colors.RED if issue['severity'] == 'critical' else Colors.YELLOW
        severity_icon = "✗" if issue['severity'] == 'critical' else "⚠"
        
        print(f"\n{severity_color}{severity_icon} Issue {i}/{len(issues)}{Colors.END}")
        print(f"  Server: {Colors.BOLD}{issue.get('server', 'N/A')}{Colors.END}")
        print(f"  Problem: {issue['description']}")
        
        if issue['fix'] in ['add_npx_flag', 'set_env_var']:
            if confirm_action(f"Apply automatic fix?"):
                if apply_fix(config_path, issue, backup_mgr):
                    print(f"  {Colors.GREEN}✓ Fix applied successfully{Colors.END}")
                else:
                    print(f"  {Colors.YELLOW}Fix skipped{Colors.END}")
        else:
            print(f"  {Colors.RED}Manual fix required:{Colors.END} {issue['fix']}")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}Repair session complete!{Colors.END}\n")
    print(f"Next steps:")
    print(f"  1. Restart your MCP client (Claude Desktop/Code/Cursor)")
    print(f"  2. Test the affected servers")
    print(f"  3. Run: {Colors.CYAN}python3 ~/.claude/skills/heal_mcp/scripts/health-dashboard.py{Colors.END}")
    print()

def main_menu():
    """Display main menu"""
    while True:
        print(f"\n{Colors.BOLD}What would you like to do?{Colors.END}")
        print(f"  1. Repair Claude Desktop configuration")
        print(f"  2. Repair Cursor configuration")
        print(f"  3. Repair Claude Code configuration")
        print(f"  4. View/Restore backups")
        print(f"  5. Exit")
        
        choice = input(f"\n{Colors.CYAN}Enter choice: {Colors.END}").strip()
        
        home = Path.home()
        
        if choice == '1':
            config_path = home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
            if config_path.exists():
                repair_workflow(config_path)
            else:
                print(f"{Colors.RED}Configuration file not found{Colors.END}")
        
        elif choice == '2':
            config_path = home / ".cursor" / "mcp.json"
            if config_path.exists():
                repair_workflow(config_path)
            else:
                print(f"{Colors.RED}Configuration file not found{Colors.END}")
        
        elif choice == '3':
            config_path = home / ".claude.json"
            if config_path.exists():
                repair_workflow(config_path)
            else:
                print(f"{Colors.RED}Configuration file not found{Colors.END}")
        
        elif choice == '4':
            backup_mgr = BackupManager()
            backups = backup_mgr.list_backups()
            
            if not backups:
                print(f"\n{Colors.YELLOW}No backups found{Colors.END}")
                continue
            
            print(f"\n{Colors.BOLD}Available backups:{Colors.END}")
            for i, backup in enumerate(backups, 1):
                print(f"  {i}. {backup['platform']} - {backup['backup_time']}")
            
            print(f"  0. Cancel")
            
            try:
                idx = int(input(f"\n{Colors.CYAN}Select backup to restore: {Colors.END}").strip())
                if idx == 0:
                    continue
                
                if 1 <= idx <= len(backups):
                    backup = backups[idx - 1]
                    if confirm_action(f"Restore {backup['platform']} backup from {backup['backup_time']}?"):
                        if backup_mgr.restore_backup(backup['backup_dir'], backup['platform']):
                            print(f"{Colors.GREEN}✓ Backup restored successfully{Colors.END}")
                        else:
                            print(f"{Colors.RED}Failed to restore backup{Colors.END}")
            except (ValueError, IndexError):
                print(f"{Colors.RED}Invalid choice{Colors.END}")
        
        elif choice == '5':
            print(f"\n{Colors.GREEN}Goodbye!{Colors.END}\n")
            break
        
        else:
            print(f"{Colors.RED}Invalid choice. Please try again.{Colors.END}")

def main():
    """Main entry point"""
    print_header()
    main_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Operation cancelled by user{Colors.END}\n")
        sys.exit(0)
