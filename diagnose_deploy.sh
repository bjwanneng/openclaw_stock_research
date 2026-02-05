#!/bin/bash
# 部署问题诊断脚本

echo "=========================================="
echo "  OpenClaw 部署问题诊断"
echo "=========================================="
echo ""

# 1. 检查当前目录
echo "[1/6] 检查当前工作目录..."
echo "  当前目录: $(pwd)"
echo "  目录内容:"
ls -la | head -10
echo ""

# 2. 检查 pyproject.toml
echo "[2/6] 检查 pyproject.toml..."
if [ -f "pyproject.toml" ]; then
    echo "  [OK] pyproject.toml 存在"
    echo "  文件大小: $(stat -c%s pyproject.toml) bytes"
    echo "  前5行内容:"
    head -5 pyproject.toml
else
    echo "  [ERROR] pyproject.toml 不存在!"
    echo "  这会导致 'pip install -e .' 失败"
fi
echo ""

# 3. 检查 src 目录
echo "[3/6] 检查 src 目录结构..."
if [ -d "src" ]; then
    echo "  [OK] src 目录存在"
    echo "  子目录:"
    find src -maxdepth 2 -type d | head -10
else
    echo "  [ERROR] src 目录不存在!"
fi
echo ""

# 4. 检查 git 状态
echo "[4/6] 检查 git 状态..."
if [ -d ".git" ]; then
    echo "  [OK] 是 git 仓库"
    echo "  当前分支: $(git branch --show-current)"
    echo "  最近提交:"
    git log --oneline -3
    echo ""
    echo "  pyproject.toml 是否在版本控制中:"
    git ls-files pyproject.toml || echo "  [WARNING] pyproject.toml 未添加到 git!"
else
    echo "  [WARNING] 不是 git 仓库"
fi
echo ""

# 5. 检查 Python 环境
echo "[5/6] 检查 Python 环境..."
echo "  Python 版本: $(python3 --version)"
echo "  pip 版本: $(pip --version)"
echo "  是否可导入 hatchling:"
python3 -c "import hatchling; print('    [OK] hatchling 可导入')" 2>/dev/null || echo "    [WARNING] hatchling 未安装"
echo ""

# 6. 尝试安装测试
echo "[6/6] 尝试安装测试 (模拟)..."
echo "  如果运行: pip install -e ."
echo "  可能会出现以下错误:"
echo ""
echo "  常见错误1: ERROR: file:///... does not appear to be a Python project"
echo "  原因: pyproject.toml 缺失或格式错误"
echo ""
echo "  常见错误2: ValueError: Unable to determine which files to ship"
echo "  原因: [build.targets.wheel] 配置缺失"
echo ""

echo "=========================================="
echo "  诊断建议:"
echo "=========================================="
echo ""
if [ ! -f "pyproject.toml" ]; then
    echo "[紧急] pyproject.toml 文件缺失!"
    echo "  解决: 从 GitHub 重新克隆代码，或手动创建 pyproject.toml"
    echo ""
fi

echo "1. 确认 GitHub 上的代码是最新版本"
echo "   git pull origin main"
echo ""
echo "2. 确认 pyproject.toml 在 git 中"
echo "   git ls-files pyproject.toml"
echo ""
echo "3. 如果文件缺失，重新克隆:"
echo "   rm -rf /root/openclaw_stock_research"
echo "   git clone https://github.com/bjwanneng/openclaw_stock_research.git /root/openclaw_stock_research"
echo ""
echo "=========================================="
