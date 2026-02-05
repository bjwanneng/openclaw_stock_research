#!/bin/bash
#
# OpenClaw 全自动部署脚本
# 用法: ./deploy_to_openclaw.sh [项目路径]
#
# 此脚本会自动检测项目代码是否存在:
# - 如果已存在，直接使用现有代码部署
# - 如果不存在，自动从 GitHub 克隆代码
#

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目信息
REPO_URL="https://github.com/bjwanneng/openclaw_stock_research.git"
PROJECT_NAME="openclaw_stock_research"

# 打印信息函数
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查系统依赖
check_dependencies() {
    print_step "检查系统依赖..."

    # 检查 Python 3
    if ! command -v python3 &> /dev/null; then
        print_error "未找到 Python3，请先安装 Python 3.9+"
        exit 1
    fi

    # 检查 Git
    if ! command -v git &> /dev/null; then
        print_error "未找到 Git，请先安装 Git"
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version 2>/dev/null | cut -d' ' -f2 | cut -d'.' -f1,2)
    print_info "Python 版本: $PYTHON_VERSION"
    print_info "系统依赖检查通过"
}

# 获取或下载项目代码
get_project_code() {
    print_step "获取项目代码..."

    # 如果用户提供了项目路径参数
    if [ -n "$1" ]; then
        PROJECT_PATH="$(cd "$1" && pwd)"
        print_info "使用指定的项目路径: $PROJECT_PATH"

        # 验证路径是否有效
        if [ ! -f "$PROJECT_PATH/SKILL.md" ]; then
            print_error "指定路径不是有效的项目目录（找不到 SKILL.md）"
            exit 1
        fi

        return
    fi

    # 检查当前目录是否已经是项目目录
    if [ -f "./SKILL.md" ] && [ -d "./src/openclaw_stock" ]; then
        PROJECT_PATH="$(pwd)"
        print_info "检测到当前目录已是项目目录: $PROJECT_PATH"
        return
    fi

    # 检查是否在父目录中存在项目
    if [ -f "../SKILL.md" ] && [ -d "../src/openclaw_stock" ]; then
        PROJECT_PATH="$(cd .. && pwd)"
        print_info "在父目录找到项目: $PROJECT_PATH"
        return
    fi

    # 尝试从 GitHub 克隆代码
    DEFAULT_CLONE_DIR="$HOME/$PROJECT_NAME"

    if [ -d "$DEFAULT_CLONE_DIR" ]; then
        print_warn "目录已存在: $DEFAULT_CLONE_DIR"
        read -p "是否覆盖？ (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$DEFAULT_CLONE_DIR"
        else
            print_info "使用现有目录: $DEFAULT_CLONE_DIR"
            PROJECT_PATH="$DEFAULT_CLONE_DIR"
            return
        fi
    fi

    print_info "从 GitHub 克隆代码..."
    print_info "仓库: $REPO_URL"
    git clone "$REPO_URL" "$DEFAULT_CLONE_DIR"

    if [ $? -eq 0 ]; then
        PROJECT_PATH="$DEFAULT_CLONE_DIR"
        print_info "代码克隆成功: $PROJECT_PATH"
    else
        print_error "代码克隆失败"
        exit 1
    fi
}

# 创建虚拟环境
setup_virtualenv() {
    print_step "设置虚拟环境..."

    cd "$PROJECT_PATH"

    if [ -d "venv" ]; then
        print_info "虚拟环境已存在，跳过创建"
    else
        print_info "创建 Python 虚拟环境..."
        python3 -m venv venv
        print_info "虚拟环境创建成功"
    fi

    # 激活虚拟环境并安装依赖
    print_info "激活虚拟环境并安装依赖..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -e .

    print_info "依赖安装完成"
}

# 配置环境变量
setup_env() {
    print_step "配置环境变量..."

    cd "$PROJECT_PATH"

    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_warn "已创建 .env 文件，请编辑配置必要的环境变量（特别是 AKSHARE_DATA_PATH）"
        else
            print_warn "找不到 .env.example，请手动创建 .env 文件"
        fi
    else
        print_info ".env 文件已存在"
    fi
}

# 部署到 OpenClaw
deploy_to_openclaw() {
    print_step "部署到 OpenClaw..."

    OPENCLAW_WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
    CUSTOM_TOOLS_DIR="$OPENCLAW_WORKSPACE/custom_tools"
    SKILLS_DIR="$OPENCLAW_WORKSPACE/skills/stock-research"

    print_info "OpenClaw 工作区: $OPENCLAW_WORKSPACE"

    # 创建工作区目录
    mkdir -p "$OPENCLAW_WORKSPACE"
    mkdir -p "$CUSTOM_TOOLS_DIR"
    mkdir -p "$SKILLS_DIR"

    # 创建项目链接
    PROJECT_LINK="$OPENCLAW_WORKSPACE/openclaw_stock_research"
    if [ -L "$PROJECT_LINK" ]; then
        rm "$PROJECT_LINK"
    fi
    ln -sf "$PROJECT_PATH" "$PROJECT_LINK"
    print_info "创建项目链接: $PROJECT_LINK -> $PROJECT_PATH"

    # 复制 wrapper 文件
    print_info "复制 wrapper 文件..."
    WRAPPER_DIR="$PROJECT_PATH/deploy/openclaw_wrappers"

    if [ -f "$WRAPPER_DIR/ak_market_tool.py" ]; then
        cp "$WRAPPER_DIR/ak_market_tool.py" "$CUSTOM_TOOLS_DIR/"
        print_info "✓ ak_market_tool.py"
    else
        print_warn "✗ 找不到 ak_market_tool.py wrapper"
    fi

    if [ -f "$WRAPPER_DIR/web_quote_validator.py" ]; then
        cp "$WRAPPER_DIR/web_quote_validator.py" "$CUSTOM_TOOLS_DIR/"
        print_info "✓ web_quote_validator.py"
    else
        print_warn "✗ 找不到 web_quote_validator.py wrapper"
    fi

    # 复制 SKILL.md
    if [ -f "$PROJECT_PATH/SKILL.md" ]; then
        cp "$PROJECT_PATH/SKILL.md" "$SKILLS_DIR/"
        print_info "✓ SKILL.md"
    fi

    # 复制 .env 文件
    if [ -f "$PROJECT_PATH/.env" ]; then
        cp "$PROJECT_PATH/.env" "$OPENCLAW_WORKSPACE/"
        print_info "✓ .env 文件"
    fi

    print_info "部署完成！"
}

# 验证部署
verify_deployment() {
    print_step "验证部署..."

    cd "$PROJECT_PATH"
    source venv/bin/activate

    print_info "测试 ak_market_tool 导入..."
    if python -c "from openclaw_stock.tools.ak_market_tool import ak_market_tool" 2>/dev/null; then
        print_info "✓ ak_market_tool 加载成功"
    else
        print_warn "✗ ak_market_tool 加载失败"
    fi

    print_info "测试 web_quote_validator 导入..."
    if python -c "from openclaw_stock.tools.web_quote_validator import web_quote_validator_tool" 2>/dev/null; then
        print_info "✓ web_quote_validator 加载成功"
    else
        print_warn "✗ web_quote_validator 加载失败"
    fi
}

# 打印完成信息
print_completion() {
    echo ""
    echo -e "${GREEN}=====================================${NC}"
    echo -e "${GREEN}     部署完成！                      ${NC}"
    echo -e "${GREEN}=====================================${NC}"
    echo ""
    echo "项目路径: $PROJECT_PATH"
    echo "OpenClaw 工作区: $HOME/.openclaw/workspace"
    echo ""
    echo "下一步:"
    echo "  1. 编辑 .env 文件配置环境变量:"
    echo "     vim $PROJECT_PATH/.env"
    echo ""
    echo "  2. 配置 OpenClaw config.json:"
    echo "     vim ~/.openclaw/config.json"
    echo ""
    echo "  3. 测试工具:"
    echo "     cd $PROJECT_PATH"
    echo "     source venv/bin/activate"
    echo "     python -c \"from openclaw_stock.tools.ak_market_tool import ak_market_tool; print('OK')\""
    echo ""
}

# 主函数
main() {
    print_step "开始部署 OpenClaw 投研分析系统..."
    print_info "仓库: $REPO_URL"
    echo ""

    # 检查依赖
    check_dependencies
    echo ""

    # 获取项目代码
    get_project_code "$1"
    echo ""

    # 设置虚拟环境
    setup_virtualenv
    echo ""

    # 配置环境变量
    setup_env
    echo ""

    # 部署到 OpenClaw
    deploy_to_openclaw
    echo ""

    # 验证部署
    verify_deployment
    echo ""

    # 打印完成信息
    print_completion
}

# 执行主函数
main "$@"
