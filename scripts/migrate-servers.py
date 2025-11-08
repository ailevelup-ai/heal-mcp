#!/usr/bin/env python3
"""
MCP Server Migration Helper
Migrate MCP server configurations between platforms
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class ConfigManager:
    """Manage MCP configurations across platforms"""
    
    def __init__(self):
        home = Path.home()
        self.configs = {
            'claude-desktop': home / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",
            'cursor': home / ".cursor" / "mcp.json",
            'claude-code': home / ".claude.json"
        }
        
        self.backup_dir = home / ".claude" / "skills" / "heal_mcp" / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def load_config(self, platform: str) -> Optional[Dict]:
        """Load configuration for a platform"""
        config_path = self.configs.get(platform)
        if not config_path or not config_path.exists():
            return None
        
        try:
            with open(config_path) as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None
    
    def save_config(self, platform: str, config: Dict) -> bool:
        """Save configuration for a platform"""
        config_path = self.configs.get(platform)
        if not config_path:
            return False
        
        # Create backup first
        if config_path.exists():
            self._create_backup(platform)
        
        # Ensure directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return True
    
    def _create_backup(self, platform: str):
        """Create backup of current config"""
        config_path = self.configs[platform]
        if not config_path.exists():
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_subdir = self.backup_dir / timestamp
        backup_subdir.mkdir(exist_ok=True)
        
        backup_path = backup_subdir / f"{platform}_config.json"
        shutil.copy2(config_path, backup_path)
    
    def get_servers(self, platform: str) -> Dict:
        """Get all servers from a platform"""
        config = self.load_config(platform)
        if not config:
            return {}
        
        return config.get('mcpServers', {})
    
    def list_all_servers(self) -> Dict[str, List[str]]:
        """List all servers across all platforms"""
        all_servers = {}
        
        for platform in self.configs.keys():
            servers = self.get_servers(platform)
            if servers:
                all_servers[platform] = list(servers.keys())
        
        return all_servers

def print_header():
    """Print header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}🔄 MCP Server Migration Helper{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

def print_servers(all_servers: Dict[str, List[str]]):
    """Print all servers organized by platform"""
    if not all_servers:
        print(f"{Colors.YELLOW}No MCP servers found on any platform{Colors.END}\n")
        return
    
    for platform, servers in all_servers.items():
        print(f"{Colors.BOLD}{Colors.CYAN}{platform.upper()}:{Colors.END}")
        for i, server in enumerate(servers, 1):
            print(f"  {i}. {server}")
        print()

def confirm_action(message: str) -> bool:
    """Ask user to confirm"""
    while True:
        response = input(f"{Colors.YELLOW}{message} (y/n): {Colors.END}").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print(f"{Colors.RED}Please enter 'y' or 'n'{Colors.END}")

def select_platform(manager: ConfigManager, prompt: str, exclude: Optional[str] = None) -> Optional[str]:
    """Let user select a platform"""
    platforms = [p for p in manager.configs.keys() if p != exclude]
    
    print(f"\n{Colors.BOLD}{prompt}{Colors.END}")
    for i, platform in enumerate(platforms, 1):
        print(f"  {i}. {platform}")
    print(f"  0. Cancel")
    
    while True:
        try:
            choice = int(input(f"\n{Colors.CYAN}Enter choice: {Colors.END}").strip())
            if choice == 0:
                return None
            if 1 <= choice <= len(platforms):
                return platforms[choice - 1]
            print(f"{Colors.RED}Invalid choice{Colors.END}")
        except ValueError:
            print(f"{Colors.RED}Please enter a number{Colors.END}")

def select_server(servers: List[str], prompt: str) -> Optional[str]:
    """Let user select a server"""
    print(f"\n{Colors.BOLD}{prompt}{Colors.END}")
    for i, server in enumerate(servers, 1):
        print(f"  {i}. {server}")
    print(f"  0. Cancel")
    
    while True:
        try:
            choice = int(input(f"\n{Colors.CYAN}Enter choice: {Colors.END}").strip())
            if choice == 0:
                return None
            if 1 <= choice <= len(servers):
                return servers[choice - 1]
            print(f"{Colors.RED}Invalid choice{Colors.END}")
        except ValueError:
            print(f"{Colors.RED}Please enter a number{Colors.END}")

def migrate_server(manager: ConfigManager, source_platform: str, dest_platform: str, server_name: str) -> bool:
    """Migrate a server from one platform to another"""
    # Load source config
    source_config = manager.load_config(source_platform)
    if not source_config:
        print(f"{Colors.RED}Could not load source configuration{Colors.END}")
        return False
    
    # Get server config
    source_servers = source_config.get('mcpServers', {})
    if server_name not in source_servers:
        print(f"{Colors.RED}Server '{server_name}' not found in {source_platform}{Colors.END}")
        return False
    
    server_config = source_servers[server_name]
    
    # Load destination config
    dest_config = manager.load_config(dest_platform)
    if not dest_config:
        dest_config = {'mcpServers': {}}
    
    if 'mcpServers' not in dest_config:
        dest_config['mcpServers'] = {}
    
    # Check if server already exists
    if server_name in dest_config['mcpServers']:
        print(f"\n{Colors.YELLOW}Server '{server_name}' already exists in {dest_platform}{Colors.END}")
        if not confirm_action("Overwrite existing server?"):
            return False
    
    # Add server to destination
    dest_config['mcpServers'][server_name] = server_config
    
    # Save destination config
    if manager.save_config(dest_platform, dest_config):
        print(f"\n{Colors.GREEN}✓ Successfully migrated '{server_name}' from {source_platform} to {dest_platform}{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}Failed to save destination configuration{Colors.END}")
        return False

def copy_server(manager: ConfigManager, source_platform: str, dest_platform: str, server_name: str) -> bool:
    """Copy a server (keeps original)"""
    return migrate_server(manager, source_platform, dest_platform, server_name)

def move_server(manager: ConfigManager, source_platform: str, dest_platform: str, server_name: str) -> bool:
    """Move a server (removes from source)"""
    # First copy it
    if not migrate_server(manager, source_platform, dest_platform, server_name):
        return False
    
    # Then remove from source
    source_config = manager.load_config(source_platform)
    if source_config and 'mcpServers' in source_config:
        if server_name in source_config['mcpServers']:
            del source_config['mcpServers'][server_name]
            manager.save_config(source_platform, source_config)
            print(f"{Colors.GREEN}✓ Removed from {source_platform}{Colors.END}")
    
    return True

def sync_all_servers(manager: ConfigManager, source_platform: str, dest_platform: str) -> bool:
    """Sync all servers from source to destination"""
    source_servers = manager.get_servers(source_platform)
    
    if not source_servers:
        print(f"{Colors.YELLOW}No servers found in {source_platform}{Colors.END}")
        return False
    
    print(f"\n{Colors.BOLD}This will sync {len(source_servers)} servers from {source_platform} to {dest_platform}{Colors.END}")
    print(f"{Colors.YELLOW}Servers in destination: {len(manager.get_servers(dest_platform))}{Colors.END}")
    
    if not confirm_action("Continue?"):
        return False
    
    dest_config = manager.load_config(dest_platform) or {'mcpServers': {}}
    if 'mcpServers' not in dest_config:
        dest_config['mcpServers'] = {}
    
    # Copy all servers
    for server_name, server_config in source_servers.items():
        dest_config['mcpServers'][server_name] = server_config
        print(f"  {Colors.GREEN}✓{Colors.END} {server_name}")
    
    # Save
    if manager.save_config(dest_platform, dest_config):
        print(f"\n{Colors.GREEN}✓ Successfully synced all servers{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}Failed to save configuration{Colors.END}")
        return False

def main_menu():
    """Main menu"""
    manager = ConfigManager()
    
    while True:
        print(f"\n{Colors.BOLD}What would you like to do?{Colors.END}")
        print(f"  1. View all servers")
        print(f"  2. Copy a server to another platform")
        print(f"  3. Move a server to another platform")
        print(f"  4. Sync all servers between platforms")
        print(f"  5. Exit")
        
        choice = input(f"\n{Colors.CYAN}Enter choice: {Colors.END}").strip()
        
        if choice == '1':
            all_servers = manager.list_all_servers()
            print()
            print_servers(all_servers)
        
        elif choice in ['2', '3']:
            operation = 'copy' if choice == '2' else 'move'
            
            # Select source platform
            source = select_platform(manager, "Select source platform:")
            if not source:
                continue
            
            # Select server
            servers = list(manager.get_servers(source).keys())
            if not servers:
                print(f"{Colors.YELLOW}No servers found in {source}{Colors.END}")
                continue
            
            server = select_server(servers, "Select server:")
            if not server:
                continue
            
            # Select destination platform
            dest = select_platform(manager, "Select destination platform:", exclude=source)
            if not dest:
                continue
            
            # Perform operation
            if operation == 'copy':
                copy_server(manager, source, dest, server)
            else:
                move_server(manager, source, dest, server)
        
        elif choice == '4':
            # Select platforms
            source = select_platform(manager, "Select source platform:")
            if not source:
                continue
            
            dest = select_platform(manager, "Select destination platform:", exclude=source)
            if not dest:
                continue
            
            sync_all_servers(manager, source, dest)
        
        elif choice == '5':
            print(f"\n{Colors.GREEN}Goodbye!{Colors.END}\n")
            break
        
        else:
            print(f"{Colors.RED}Invalid choice{Colors.END}")

def main():
    """Main entry point"""
    print_header()
    main_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Operation cancelled{Colors.END}\n")
