"""
ak_market_tool wrapper for OpenClaw
项目代码位于: ~/.openclaw/workspace/openclaw_stock_research

此文件作为wrapper，用于将实际的ak_market_tool暴露给OpenClaw使用。
它处理了路径设置、环境变量加载和模块导入。
"""
import sys
import os

# 添加项目路径，确保能导入 openclaw_stock 模块
PROJECT_PATH = os.path.expanduser("~/.openclaw/workspace/openclaw_stock_research")
sys.path.insert(0, os.path.join(PROJECT_PATH, "src"))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv(os.path.join(PROJECT_PATH, ".env"))

# 导入实际的 tool
from openclaw_stock.tools.ak_market_tool import ak_market_tool

# 导出 tool 供 OpenClaw 使用
__all__ = ["ak_market_tool"]
