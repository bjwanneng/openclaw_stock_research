"""
ak_market_tool wrapper for OpenClaw

此文件作为wrapper，用于将实际的ak_market_tool暴露给OpenClaw使用。
它处理了路径设置、环境变量加载和模块导入。

路径解析逻辑：
1. 首先尝试从当前wrapper文件位置推导项目路径
2. 如果失败，尝试从环境变量 OPENCLAW_PROJECT_PATH 获取
3. 如果仍失败，使用默认路径 ~/.openclaw/workspace/openclaw_stock_research
"""
import sys
import os

def _get_project_path() -> str:
    """
    智能检测项目路径

    尝试多种方式找到项目根目录：
    1. 从当前文件位置推导（通过软链接找到实际项目）
    2. 从环境变量获取
    3. 使用默认路径
    """
    # 方式1: 尝试从当前文件位置推导
    try:
        # 获取当前wrapper文件的路径
        wrapper_path = os.path.abspath(__file__)

        # 如果这是一个软链接，获取真实路径
        if os.path.islink(wrapper_path):
            wrapper_path = os.path.realpath(wrapper_path)

        # 从路径推导：custom_tools/ak_market_tool.py -> 项目根目录
        # 或者通过软链接: workspace/openclaw_stock_research
        custom_tools_dir = os.path.dirname(wrapper_path)
        workspace_dir = os.path.dirname(custom_tools_dir)
        project_link = os.path.join(workspace_dir, "openclaw_stock_research")

        # 如果软链接存在，使用它指向的实际路径
        if os.path.islink(project_link):
            real_project_path = os.path.realpath(project_link)
            if os.path.exists(real_project_path):
                return real_project_path

        # 如果软链接不存在但 openclaw_stock_research 目录存在
        if os.path.isdir(project_link):
            return project_link

    except Exception:
        pass  # 如果推导失败，继续尝试其他方式

    # 方式2: 从环境变量获取
    env_path = os.environ.get("OPENCLAW_PROJECT_PATH")
    if env_path and os.path.exists(env_path):
        return os.path.abspath(env_path)

    # 方式3: 使用默认路径
    default_path = os.path.expanduser("~/.openclaw/workspace/openclaw_stock_research")
    if os.path.exists(default_path):
        return default_path

    # 如果都找不到，抛出错误
    raise RuntimeError(
        "无法找到项目路径。请确保：\n"
        "1. 项目已正确部署到 ~/.openclaw/workspace/openclaw_stock_research\n"
        "2. 或设置环境变量 OPENCLAW_PROJECT_PATH 指向项目根目录"
    )

# 获取项目路径
try:
    PROJECT_PATH = _get_project_path()
except RuntimeError as e:
    print(f"[ERROR] {e}")
    sys.exit(1)

# 添加项目路径到 Python 路径
sys.path.insert(0, os.path.join(PROJECT_PATH, "src"))

# 加载环境变量
try:
    from dotenv import load_dotenv
    env_path = os.path.join(PROJECT_PATH, ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv 未安装时跳过

# 导入实际的 tool
try:
    from openclaw_stock.tools.ak_market_tool import ak_market_tool
except ImportError as e:
    print(f"[ERROR] 无法导入 ak_market_tool: {e}")
    print(f"[INFO] 项目路径: {PROJECT_PATH}")
    print(f"[INFO] Python 路径: {sys.path}")
    raise

# 导出 tool 供 OpenClaw 使用
__all__ = ["ak_market_tool"]
