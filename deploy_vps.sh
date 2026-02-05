#!/bin/bash

# OpenClaw 投研分析系统 - VPS 一键部署脚本
# 使用方法: ./deploy_vps.sh [WORKSPACE_PATH]

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 获取工作区路径
WORKSPACE="${1:-$HOME/.openclaw/workspace}"
REPO_URL="https://github.com/bjwanneng/openclaw-stock-research.git"

print_info "开始部署 OpenClaw 投研分析系统..."
print_info "工作区路径: $WORKSPACE"

# 1. 检查依赖
print_info "检查系统依赖..."
if ! command -v python3 &> /dev/null; then
    print_error "未找到 Python3，请先安装 Python 3.9+"
    exit 1
fi

if ! command -v git &> /dev/null; then
    print_error "未找到 Git，请先安装 Git"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
print_info "Python 版本: $PYTHON_VERSION"

# 2. 创建工作区
print_info "创建工作区目录..."
mkdir -p "$WORKSPACE"/{custom_tools,skills/stock-research,data}
print_info "工作区创建完成"

# 3. 克隆仓库
PROJECT_DIR="$WORKSPACE/openclaw-stock-research"
if [ -d "$PROJECT_DIR" ]; then
    print_warn "项目目录已存在，尝试更新..."
    cd "$PROJECT_DIR"
    git pull origin main || print_warn "更新失败，使用现有代码"
else
    print_info "克隆项目仓库..."
    git clone "$REPO_URL" "$PROJECT_DIR" || {
        print_error "克隆失败，请检查仓库地址和网络连接"
        exit 1
    }
fi

# 4. 创建虚拟环境并安装依赖
print_info "创建 Python 虚拟环境..."
cd "$PROJECT_DIR"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

print_info "激活虚拟环境并安装依赖..."
source venv/bin/activate
pip install --upgrade pip
pip install -e .

# 5. 配置环境变量
print_info "配置环境变量..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_warn "请编辑 .env 文件配置必要的环境变量，特别是 AKSHARE_DATA_PATH"
    fi
fi

# 设置默认环境变量
export AKSHARE_DATA_PATH="${AKSHARE_DATA_PATH:-$WORKSPACE/data}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"

# 6. 创建符号链接
print_info "创建 OpenClaw 符号链接..."
ln -sf "$PROJECT_DIR"/src/openclaw_stock/tools/ak_market_tool.py "$WORKSPACE"/custom_tools/
ln -sf "$PROJECT_DIR"/src/openclaw_stock/tools/web_quote_validator.py "$WORKSPACE"/custom_tools/
ln -sf "$PROJECT_DIR"/SKILL.md "$WORKSPACE"/skills/stock-research/

# 7. 验证部署
print_info "验证部署..."

# 测试导入
if python -c "from openclaw_stock.tools.ak_market_tool import ak_market_tool" 2>/dev/null; then
    print_info "✓ ak_market_tool 导入成功"
else
    print_error "✗ ak_market_tool 导入失败"
fi

if python -c "from openclaw_stock.tools.web_quote_validator import web_quote_validator_tool" 2>/dev/null; then
    print_info "✓ web_quote_validator_tool 导入成功"
else
    print_error "✗ web_quote_validator_tool 导入失败"
fi

# 8. 完成
print_info ""
print_info "=========================================="
print_info "部署完成！"
print_info "=========================================="
print_info ""
print_info "目录结构:"
print_info "  $WORKSPACE/"
print_info "  ├── custom_tools/          # 工具脚本"
print_info "  ├── skills/stock-research/ # 技能定义"
print_info "  ├── openclaw-stock-research/ # 项目源码"
print_info "  └── data/                  # 数据缓存"
print_info ""
print_info "下一步:"
print_info "  1. 编辑 .env 文件: vim $PROJECT_DIR/.env"
print_info "  2. 激活虚拟环境: source $PROJECT_DIR/venv/bin/activate"
print_info "  3. 测试工具: python -c \"from openclaw_stock.tools.ak_market_tool import ak_market_tool; print('OK')\""
print_info ""
print_info "更新代码:"
print_info "  cd $PROJECT_DIR && git pull && pip install -e ."
print_info ""
