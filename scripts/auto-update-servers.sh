#!/bin/bash

# Auto-update MCP servers across all platforms
# Part of the heal_mcp skill

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BOLD}${BLUE}============================================================${NC}"
echo -e "${BOLD}${BLUE}🔄 MCP Server Auto-Updater${NC}"
echo -e "${BOLD}${BLUE}============================================================${NC}"
echo ""

# Backup directory
BACKUP_DIR="$HOME/.claude/skills/heal_mcp/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo -e "${BOLD}📦 Step 1: Creating backups...${NC}"

# Backup Claude Desktop config
CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
if [ -f "$CLAUDE_CONFIG" ]; then
    cp "$CLAUDE_CONFIG" "$BACKUP_DIR/claude_desktop_config.json"
    echo -e "${GREEN}✓${NC} Backed up Claude Desktop config"
fi

# Backup Cursor config
CURSOR_CONFIG="$HOME/.cursor/mcp.json"
if [ -f "$CURSOR_CONFIG" ]; then
    cp "$CURSOR_CONFIG" "$BACKUP_DIR/cursor_mcp.json"
    echo -e "${GREEN}✓${NC} Backed up Cursor config"
fi

# Backup Claude Code config
CLAUDE_CODE_CONFIG="$HOME/.claude.json"
if [ -f "$CLAUDE_CODE_CONFIG" ]; then
    cp "$CLAUDE_CODE_CONFIG" "$BACKUP_DIR/claude_code.json"
    echo -e "${GREEN}✓${NC} Backed up Claude Code config"
fi

echo -e "${GREEN}✓${NC} All configs backed up to: ${BACKUP_DIR}"
echo ""

echo -e "${BOLD}🔄 Step 2: Updating configuration files...${NC}"
echo ""

# Now run the Python config updater
python3 "$(dirname $0)/update-configs.py"

echo ""
echo -e "${BOLD}${GREEN}============================================================${NC}"
echo -e "${BOLD}${GREEN}✅ Update Complete!${NC}"
echo -e "${BOLD}${GREEN}============================================================${NC}"
echo ""
echo -e "${BOLD}Next steps:${NC}"
echo -e "  1. ${BOLD}Restart Claude Desktop${NC} (⌘Q then reopen)"
echo -e "  2. ${BOLD}Restart Cursor${NC}"
echo -e "  3. Test your servers"
echo ""
echo -e "${GREEN}✓${NC} Backups saved to: ${BACKUP_DIR}"
echo -e "${YELLOW}⚠️${NC}  If anything breaks, restore with:"
echo -e "     cp $BACKUP_DIR/* ~/Library/Application\\ Support/Claude/"
echo ""
