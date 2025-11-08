#!/usr/bin/env python3
"""
Smart Dependency Installer for MCP Servers
Auto-detects and offers to install missing dependencies
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class DependencyChecker:
    """Check and install dependencies"""
    
    def __init__(self):
        self.findings = {
            'node': None,
            'npm': None,
            'npx': None,
            'python3': None,
            'pip3': None,
            'uv': None,
            'uvx': None,
            'homebrew': None
        }
    
    def check_all(self):
        """Check all dependencies"""
        print(f"{Colors.BOLD}{Colors.BLUE}Checking system dependencies...{Colors.END}\n")
        
        # Node.js ecosystem
        self.findings['node'] = self._check_command('node', '--version')
        self.findings['npm'] = self._check_command('npm', '--version')
        self.findings['npx'] = self._check_command('npx', '--version')
        
        # Python ecosystem
        self.findings['python3'] = self._check_command('python3', '--version')
        self.findings['pip3'] = self._check_command('pip3', '--version')
        self.findings['uv'] = self._check_command('uv', '--version')
        self.findings['uvx'] = self._check_command('uvx', '--version')
        
        # Package managers
        self.findings['homebrew'] = self._check_command('brew', '--version')
        
        self._print_status()
    
    def _check_command(self, command: str, version_flag: str) -> Optional[str]:
        """Check if a command exists and get its version"""
        try:
            result = subprocess.run(
                [command, version_flag],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n')[0]
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None
    
    def _print_status(self):
        """Print dependency status"""
        print(f"{Colors.BOLD}Node.js Ecosystem:{Colors.END}")
        self._print_item('Node.js', self.findings['node'], required=True)
        self._print_item('npm', self.findings['npm'], required=True)
        self._print_item('npx', self.findings['npx'], required=True)
        
        print(f"\n{Colors.BOLD}Python Ecosystem:{Colors.END}")
        self._print_item('Python 3', self.findings['python3'], required=False)
        self._print_item('pip3', self.findings['pip3'], required=False)
        self._print_item('uv', self.findings['uv'], required=False)
        self._print_item('uvx', self.findings['uvx'], required=False)
        
        print(f"\n{Colors.BOLD}Package Managers:{Colors.END}")
        self._print_item('Homebrew', self.findings['homebrew'], required=False)
        print()
    
    def _print_item(self, name: str, version: Optional[str], required: bool):
        """Print a single dependency item"""
        if version:
            print(f"  {Colors.GREEN}✓{Colors.END} {name:12} {version}")
        else:
            icon = f"{Colors.RED}✗{Colors.END}" if required else f"{Colors.YELLOW}○{Colors.END}"
            status = "Missing" if required else "Optional"
            print(f"  {icon} {name:12} {status}")
    
    def get_missing_critical(self) -> List[str]:
        """Get list of missing critical dependencies"""
        missing = []
        if not self.findings['node']:
            missing.append('node')
        if not self.findings['npm']:
            missing.append('npm')
        if not self.findings['npx']:
            missing.append('npx')
        return missing
    
    def install_missing(self):
        """Offer to install missing dependencies"""
        missing = self.get_missing_critical()
        
        if not missing:
            print(f"{Colors.GREEN}All critical dependencies are installed!{Colors.END}\n")
            return True
        
        print(f"\n{Colors.BOLD}{Colors.RED}Missing critical dependencies:{Colors.END}")
        for dep in missing:
            print(f"  • {dep}")
        
        print(f"\n{Colors.BOLD}Installation options:{Colors.END}")
        
        # Check if Homebrew is available
        if self.findings['homebrew']:
            print(f"\n{Colors.GREEN}Homebrew detected!{Colors.END}")
            if self._confirm("Install Node.js via Homebrew?"):
                return self._install_via_homebrew()
        else:
            print(f"\n{Colors.YELLOW}Homebrew not detected.{Colors.END}")
            print(f"For the best experience, install Homebrew first:")
            print(f"  {Colors.CYAN}/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"{Colors.END}")
            
            if self._confirm("Would you like installation instructions?"):
                self._print_manual_instructions()
        
        return False
    
    def _install_via_homebrew(self) -> bool:
        """Install Node.js via Homebrew"""
        print(f"\n{Colors.CYAN}Installing Node.js...{Colors.END}")
        
        try:
            subprocess.run(['brew', 'install', 'node'], check=True)
            print(f"{Colors.GREEN}✓ Node.js installed successfully!{Colors.END}")
            
            # Verify installation
            self.findings['node'] = self._check_command('node', '--version')
            self.findings['npm'] = self._check_command('npm', '--version')
            self.findings['npx'] = self._check_command('npx', '--version')
            
            print(f"\n{Colors.BOLD}Verifying installation:{Colors.END}")
            self._print_item('Node.js', self.findings['node'], required=True)
            self._print_item('npm', self.findings['npm'], required=True)
            self._print_item('npx', self.findings['npx'], required=True)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}✗ Installation failed: {e}{Colors.END}")
            return False
    
    def _print_manual_instructions(self):
        """Print manual installation instructions"""
        print(f"\n{Colors.BOLD}Manual Installation Instructions:{Colors.END}\n")
        
        print(f"{Colors.BOLD}Option 1: Using Homebrew (Recommended){Colors.END}")
        print(f"  1. Install Homebrew:")
        print(f"     {Colors.CYAN}/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"{Colors.END}")
        print(f"  2. Install Node.js:")
        print(f"     {Colors.CYAN}brew install node{Colors.END}")
        
        print(f"\n{Colors.BOLD}Option 2: Using Official Installer{Colors.END}")
        print(f"  1. Visit: https://nodejs.org/")
        print(f"  2. Download the LTS version")
        print(f"  3. Run the installer")
        
        print(f"\n{Colors.BOLD}Option 3: Using nvm (Node Version Manager){Colors.END}")
        print(f"  1. Install nvm:")
        print(f"     {Colors.CYAN}curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash{Colors.END}")
        print(f"  2. Install Node.js:")
        print(f"     {Colors.CYAN}nvm install --lts{Colors.END}")
        print()
    
    def _confirm(self, message: str) -> bool:
        """Ask user for confirmation"""
        while True:
            response = input(f"{Colors.YELLOW}{message} (y/n): {Colors.END}").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            print(f"{Colors.RED}Please enter 'y' or 'n'{Colors.END}")
    
    def offer_optional_installs(self):
        """Offer to install optional dependencies"""
        print(f"\n{Colors.BOLD}Optional Dependencies:{Colors.END}\n")
        
        # Python
        if not self.findings['python3']:
            if self._confirm("Install Python 3 (for Python-based MCP servers)?"):
                self._install_python()
        
        # uv (Python package manager)
        if not self.findings['uv'] and self.findings['python3']:
            if self._confirm("Install uv (fast Python package manager for MCP servers)?"):
                self._install_uv()
    
    def _install_python(self):
        """Install Python via Homebrew"""
        if not self.findings['homebrew']:
            print(f"{Colors.YELLOW}Homebrew required. Install it first.{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}Installing Python 3...{Colors.END}")
        try:
            subprocess.run(['brew', 'install', 'python3'], check=True)
            print(f"{Colors.GREEN}✓ Python 3 installed successfully!{Colors.END}")
            self.findings['python3'] = self._check_command('python3', '--version')
            self.findings['pip3'] = self._check_command('pip3', '--version')
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}✗ Installation failed: {e}{Colors.END}")
    
    def _install_uv(self):
        """Install uv"""
        print(f"\n{Colors.CYAN}Installing uv...{Colors.END}")
        try:
            subprocess.run(['pip3', 'install', 'uv'], check=True)
            print(f"{Colors.GREEN}✓ uv installed successfully!{Colors.END}")
            self.findings['uv'] = self._check_command('uv', '--version')
            self.findings['uvx'] = self._check_command('uvx', '--version')
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}✗ Installation failed: {e}{Colors.END}")

def main():
    """Main entry point"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}🔧 Smart Dependency Installer for MCP Servers{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")
    
    checker = DependencyChecker()
    checker.check_all()
    
    # Install critical dependencies
    if not checker.install_missing():
        print(f"\n{Colors.YELLOW}Please install the missing dependencies and run this script again.{Colors.END}\n")
        return
    
    # Offer optional dependencies
    checker.offer_optional_installs()
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}Setup complete!{Colors.END}")
    print(f"\nNext steps:")
    print(f"  1. Restart your terminal to ensure PATH is updated")
    print(f"  2. Verify installation: {Colors.CYAN}node --version && npm --version{Colors.END}")
    print(f"  3. Configure your MCP servers")
    print(f"  4. Run health check: {Colors.CYAN}python3 ~/.claude/skills/heal_mcp/scripts/health-dashboard.py{Colors.END}")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Operation cancelled by user{Colors.END}\n")
        sys.exit(0)
