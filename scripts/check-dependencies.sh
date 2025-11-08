#!/bin/bash
# MCP Dependency Checker
# Verifies that all required dependencies are installed for MCP servers

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${BOLD}${BLUE}MCP Dependency Checker${NC}"
echo -e "${BLUE}==========================================${NC}\n"

ALL_OK=true

# Check Node.js
echo -e "${BOLD}Checking Node.js...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
    echo -e "${GREEN}✓ Node.js found: $NODE_VERSION${NC}"
    
    if [ "$NODE_MAJOR" -lt 18 ]; then
        echo -e "${RED}✗ Node.js version must be 18.0.0 or higher${NC}"
        echo -e "${YELLOW}  Current: $NODE_VERSION, Required: v18.0.0+${NC}"
        ALL_OK=false
    else
        echo -e "${GREEN}  Version OK (≥18.0.0)${NC}"
    fi
else
    echo -e "${RED}✗ Node.js not found${NC}"
    echo -e "${YELLOW}  Install from: https://nodejs.org${NC}"
    ALL_OK=false
fi

# Check npm
echo -e "\n${BOLD}Checking npm...${NC}"
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓ npm found: v$NPM_VERSION${NC}"
else
    echo -e "${RED}✗ npm not found (should be included with Node.js)${NC}"
    ALL_OK=false
fi

# Check npx
echo -e "\n${BOLD}Checking npx...${NC}"
if command -v npx &> /dev/null; then
    NPX_VERSION=$(npx --version)
    echo -e "${GREEN}✓ npx found: v$NPX_VERSION${NC}"
else
    echo -e "${RED}✗ npx not found (should be included with Node.js)${NC}"
    ALL_OK=false
fi

# Check Python
echo -e "\n${BOLD}Checking Python...${NC}"
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
fi

if [ -n "$PYTHON_CMD" ]; then
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
    
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
        echo -e "${YELLOW}⚠ Python version should be 3.10+ for best compatibility${NC}"
        echo -e "${YELLOW}  Current: $PYTHON_VERSION, Recommended: 3.13+${NC}"
    else
        echo -e "${GREEN}  Version OK (≥3.10)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Python not found${NC}"
    echo -e "${YELLOW}  Required for Python-based MCP servers${NC}"
    echo -e "${YELLOW}  Install from: https://python.org${NC}"
fi

# Check pip
echo -e "\n${BOLD}Checking pip...${NC}"
if command -v pip3 &> /dev/null || command -v pip &> /dev/null; then
    PIP_CMD=$(command -v pip3 &> /dev/null && echo "pip3" || echo "pip")
    PIP_VERSION=$($PIP_CMD --version | awk '{print $2}')
    echo -e "${GREEN}✓ pip found: $PIP_VERSION${NC}"
else
    if [ -n "$PYTHON_CMD" ]; then
        echo -e "${YELLOW}⚠ pip not found${NC}"
        echo -e "${YELLOW}  Install with: $PYTHON_CMD -m ensurepip --upgrade${NC}"
    fi
fi

# Check uv and uvx
echo -e "\n${BOLD}Checking uv/uvx...${NC}"
if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version | awk '{print $2}')
    echo -e "${GREEN}✓ uv found: $UV_VERSION${NC}"
    
    if command -v uvx &> /dev/null; then
        echo -e "${GREEN}✓ uvx found${NC}"
    else
        echo -e "${YELLOW}⚠ uvx not found (should be included with uv)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ uv/uvx not found${NC}"
    echo -e "${YELLOW}  Recommended for Python MCP servers${NC}"
    echo -e "${YELLOW}  Install: curl -LsSf https://astral.sh/uv/install.sh | sh${NC}"
fi

# Check Docker (optional)
echo -e "\n${BOLD}Checking Docker (optional)...${NC}"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
    echo -e "${GREEN}✓ Docker found: $DOCKER_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ Docker not found (optional)${NC}"
    echo -e "${YELLOW}  Useful for containerized MCP servers${NC}"
    echo -e "${YELLOW}  Install from: https://docker.com${NC}"
fi

# Check PATH
echo -e "\n${BOLD}Checking PATH configuration...${NC}"
echo -e "${BLUE}Current PATH:${NC}"
echo "$PATH" | tr ':' '\n' | sed 's/^/  /'

# Check common MCP server packages
echo -e "\n${BOLD}Checking for globally installed MCP packages...${NC}"

# npm global packages
if command -v npm &> /dev/null; then
    echo -e "${BLUE}npm global packages:${NC}"
    npm list -g --depth=0 2>/dev/null | grep "@modelcontextprotocol" || echo -e "${YELLOW}  No @modelcontextprotocol packages found${NC}"
fi

# uv tools
if command -v uv &> /dev/null; then
    echo -e "\n${BLUE}uv global tools:${NC}"
    uv tool list 2>/dev/null | grep "mcp" || echo -e "${YELLOW}  No MCP tools found${NC}"
fi

# Final summary
echo -e "\n${BOLD}=========================================${NC}"
if [ "$ALL_OK" = true ]; then
    echo -e "${GREEN}${BOLD}✓ All required dependencies are installed!${NC}"
    echo -e "${GREEN}Your system is ready for MCP servers.${NC}"
    exit 0
else
    echo -e "${RED}${BOLD}✗ Some required dependencies are missing${NC}"
    echo -e "${YELLOW}Install the missing dependencies above.${NC}"
    exit 1
fi
