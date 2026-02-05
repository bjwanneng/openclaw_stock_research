#!/bin/bash
#
# OpenClaw 部署脚本
# 用法: ./deploy_to_openclaw.sh [项目路径]
# 如果不指定项目路径，默认使用当前目录
#

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取项目路径
if [ -z "$1" ]; then
    PROJECT_PATH="$(pwd)"
    echo -e "${BLUE}使用当前目录作为项目路径: $PROJECT_PATH${NC}"
else
    PROJECT_PATH="$(cd "$1" && pwd)"
    echo -e "${BLUE}使用指定项目路径: $PROJECT_PATH${NC}"
fi

# 检查项目目录结构
if [ ! -f "$PROJECT_PATH/SKILL.md" ]; then
    echo -e "${RED}错误: 找不到 SKILL.md，请确保在项目根目录运行此脚本${NC}"
    exit 1
fi

if [ ! -d "$PROJECT_PATH/src/openclaw_stock/tools" ]; then
    echo -e "${RED}错误: 找不到 src/openclaw_stock/tools 目录${NC}"
    exit 1
fi

# OpenClaw 工作区路径
OPENCLAW_WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
CUSTOM_TOOLS_DIR="$OPENCLAW_WORKSPACE/custom_tools"
SKILLS_DIR="$OPENCLAW_WORKSPACE/skills/stock-research"

# 检查 OpenClaw 工作区是否存在
if [ ! -d "$OPENCLAW_WORKSPACE" ]; then
    echo -e "${YELLOW}警告: OpenClaw 工作区不存在，正在创建: $OPENCLAW_WORKSPACE${NC}"
    mkdir -p "$OPENCLAW_WORKSPACE"
fi

# 确保项目目录链接存在
PROJECT_LINK="$OPENCLAW_WORKSPACE/openclaw_stock_research"
if [ -L "$PROJECT_LINK" ]; then
    rm "$PROJECT_LINK"
fi

# 创建软链接指向项目
ln -sf "$PROJECT_PATH" "$PROJECT_LINK"
echo -e "${GREEN}✓ 创建项目软链接: $PROJECT_LINK -> $PROJECT_PATH${NC}"

# 创建 custom_tools 目录并复制 wrapper 文件
mkdir -p "$CUSTOM_TOOLS_DIR"

# 检查 wrapper 文件是否存在
WRAPPER_DIR="$PROJECT_PATH/deploy/openclaw_wrappers"
if [ -f "$WRAPPER_DIR/ak_market_tool.py" ]; then
    cp "$WRAPPER_DIR/ak_market_tool.py" "$CUSTOM_TOOLS_DIR/"
    echo -e "${GREEN}✓ 复制 wrapper: ak_market_tool.py${NC}"
else
    echo -e "${YELLOW}警告: 找不到 ak_market_tool.py wrapper，跳过${NC}"
fi

if [ -f "$WRAPPER_DIR/web_quote_validator.py" ]; then
    cp "$WRAPPER_DIR/web_quote_validator.py" "$CUSTOM_TOOLS_DIR/"
    echo -e "${GREEN}✓ 复制 wrapper: web_quote_validator.py${NC}"
else
    echo -e "${YELLOW}警告: 找不到 web_quote_validator.py wrapper，跳过${NC}"
fi

# 创建 skills 目录并复制 SKILL.md
mkdir -p "$SKILLS_DIR"
if [ -f "$PROJECT_PATH/SKILL.md" ]; then
    cp "$PROJECT_PATH/SKILL.md" "$SKILLS_DIR/"
    echo -e "${GREEN}✓ 复制 SKILL.md${NC}"
fi

# 复制 .env 文件
if [ -f "$PROJECT_PATH/.env" ]; then
    cp "$PROJECT_PATH/.env" "$OPENCLAW_WORKSPACE/"
    echo -e "${GREEN}✓ 复制 .env 文件${NC}"
else
    echo -e "${YELLOW}警告: 找不到 .env 文件，请确保已创建${NC}"
fi

echo ""
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}  部署完成！${NC}"
echo -e "${GREEN}=====================================${NC}"
echo ""
echo "下一步:"
echo "  1. 编辑 ~/.openclaw/config.json 添加 tools 和 skills 配置"
echo "  2. 确保 python_path 指向正确的虚拟环境"
echo "  3. 测试工具是否能正常运行"
echo ""
echo "配置示例:"
echo '  "tools": ['
echo '    {'
echo '      "name": "ak_market_tool",'
echo '      "path": "~/.openclaw/workspace/custom_tools/ak_market_tool.py",'
echo '      "enabled": true'
echo '    },'
echo '    {'
echo '      "name": "web_quote_validator",'
echo '      "path": "~/.openclaw/workspace/custom_tools/web_quote_validator.py",'
echo '      "enabled": true'
echo '    }'
echo '  ]'
