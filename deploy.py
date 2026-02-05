#!/usr/bin/env python3
"""
OpenClaw 投研分析系统部署脚本

此脚本用于将开发完成的工具和技能部署到 OpenClaw 工作区。

使用方法:
    python deploy.py [--workspace PATH]

参数:
    --workspace: OpenClaw 工作区路径，默认为 ~/.openclaw/workspace
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Optional


def get_default_workspace() -> Path:
    """获取默认的 OpenClaw 工作区路径"""
    home = Path.home()
    return home / ".openclaw" / "workspace"


def ensure_dir(path: Path) -> None:
    """确保目录存在"""
    path.mkdir(parents=True, exist_ok=True)
    print(f"  创建目录: {path}")


def copy_file(src: Path, dst: Path, overwrite: bool = True) -> bool:
    """复制文件"""
    if dst.exists() and not overwrite:
        print(f"  跳过(已存在): {dst}")
        return False

    try:
        shutil.copy2(src, dst)
        print(f"  复制文件: {src} -> {dst}")
        return True
    except Exception as e:
        print(f"  错误: 复制文件失败 {src}: {e}")
        return False


def copy_dir(src: Path, dst: Path, ignore_patterns: Optional[list] = None) -> bool:
    """复制目录"""
    try:
        if ignore_patterns:
            ignore = shutil.ignore_patterns(*ignore_patterns)
            shutil.copytree(src, dst, ignore=ignore, dirs_exist_ok=True)
        else:
            shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"  复制目录: {src} -> {dst}")
        return True
    except Exception as e:
        print(f"  错误: 复制目录失败 {src}: {e}")
        return False


def create_openclaw_config(workspace: Path) -> None:
    """创建 OpenClaw 配置文件示例"""
    config_content = '''{
  "version": "1.0.0",
  "skills": [
    {
      "name": "StockAnalystPro",
      "display_name": "股票投研分析专家",
      "description": "专业A股/港股投研分析，提供实时行情、历史数据、基本面分析和深度研报生成",
      "path": "skills/stock-research/SKILL.md",
      "entry": "skills/stock-research/research_flow.py",
      "enabled": true,
      "tags": ["stock", "finance", "research", "a-share", "hk-stock"]
    }
  ],
  "tools": [
    {
      "name": "ak_market_tool",
      "display_name": "AkShare市场数据引擎",
      "description": "获取A股/港股的实时行情、历史K线、基本面和资金流向数据",
      "path": "custom_tools/ak_market_tool.py",
      "enabled": true,
      "requires": ["akshare", "pandas"],
      "env_vars": ["AKSHARE_DATA_PATH"]
    },
    {
      "name": "web_quote_validator",
      "display_name": "Web行情验证器",
      "description": "通过东方财富/腾讯/新浪获取实时价格，验证AkShare数据准确性",
      "path": "custom_tools/web_quote_validator.py",
      "enabled": true,
      "requires": ["requests"],
      "env_vars": ["PROXY_URL"]
    }
  ],
  "env": {
    "AKSHARE_DATA_PATH": "${WORKSPACE}/data/akshare",
    "LOG_LEVEL": "INFO",
    "DEFAULT_TIMEOUT": "30",
    "PRICE_DIFF_THRESHOLD": "0.5"
  }
}
'''

    config_path = workspace / "openclaw.json.example"
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)
        print(f"  创建配置示例: {config_path}")
    except Exception as e:
        print(f"  警告: 创建配置示例失败: {e}")


def deploy(workspace: Path, source_dir: Path) -> bool:
    """执行部署"""
    print(f"开始部署 OpenClaw 投研分析系统...")
    print(f"  源目录: {source_dir}")
    print(f"  目标工作区: {workspace}")
    print()

    if not source_dir.exists():
        print(f"错误: 源目录不存在: {source_dir}")
        return False

    # 创建目标目录结构
    print("创建目录结构...")
    custom_tools_dir = workspace / "custom_tools"
    skills_dir = workspace / "skills" / "stock-research"

    ensure_dir(custom_tools_dir)
    ensure_dir(skills_dir)
    ensure_dir(workspace / "data")
    print()

    # 部署工具文件
    print("部署工具文件...")
    tools_source = source_dir / "src" / "openclaw_stock" / "tools"

    for tool_file in ["ak_market_tool.py", "web_quote_validator.py"]:
        src = tools_source / tool_file
        dst = custom_tools_dir / tool_file
        if src.exists():
            copy_file(src, dst)
        else:
            print(f"  警告: 源文件不存在: {src}")
    print()

    # 部署 SKILL.md
    print("部署技能定义...")
    skill_src = source_dir / "SKILL.md"
    skill_dst = skills_dir / "SKILL.md"
    if skill_src.exists():
        copy_file(skill_src, skill_dst)
    else:
        print(f"  警告: SKILL.md 不存在: {skill_src}")
    print()

    # 复制核心模块（用于独立运行）
    print("部署核心模块...")
    core_source = source_dir / "src" / "openclaw_stock"
    core_target = custom_tools_dir / "openclaw_stock"

    if core_source.exists():
        # 复制整个包，但排除 __pycache__ 和测试文件
        ignore_patterns = ["__pycache__", "*.pyc", "*.pyo", ".pytest_cache", "tests"]
        copy_dir(core_source, core_target, ignore_patterns)
    print()

    # 创建 OpenClaw 配置示例
    print("创建配置文件示例...")
    create_openclaw_config(workspace)
    print()

    # 显示部署摘要
    print("=" * 60)
    print("部署完成!")
    print("=" * 60)
    print()
    print("已部署的组件:")
    print(f"  - 工具: ak_market_tool, web_quote_validator")
    print(f"  - 技能: StockAnalystPro")
    print()
    print("目录结构:")
    print(f"  {workspace}/")
    print(f"  ├── custom_tools/          # 工具脚本")
    print(f"  │   ├── ak_market_tool.py")
    print(f"  │   ├── web_quote_validator.py")
    print(f"  │   └── openclaw_stock/    # 核心模块")
    print(f"  ├── skills/")
    print(f"  │   └── stock-research/")
    print(f"  │       └── SKILL.md       # 技能定义")
    print(f"  ├── data/                  # 数据缓存")
    print(f"  └── openclaw.json.example  # 配置示例")
    print()
    print("下一步:")
    print("  1. 配置环境变量: cp .env.example .env && vim .env")
    print("  2. 安装依赖: pip install -e .")
    print("  3. 配置 OpenClaw: cp openclaw.json.example ~/.openclaw/config.json")
    print("  4. 运行测试: pytest")
    print()

    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="OpenClaw 投研分析系统部署脚本"
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default=None,
        help="OpenClaw 工作区路径 (默认: ~/.openclaw/workspace)"
    )
    parser.add_argument(
        "--source",
        type=str,
        default=None,
        help="源代码目录 (默认: 脚本所在目录)"
    )

    args = parser.parse_args()

    # 确定工作区路径
    if args.workspace:
        workspace = Path(args.workspace).expanduser().resolve()
    else:
        workspace = get_default_workspace()

    # 确定源代码目录
    if args.source:
        source_dir = Path(args.source).expanduser().resolve()
    else:
        # 默认使用脚本所在目录的上级目录（假设脚本在项目根目录）
        source_dir = Path(__file__).parent.resolve()

    # 执行部署
    try:
        success = deploy(workspace, source_dir)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n部署已取消")
        sys.exit(130)
    except Exception as e:
        print(f"\n部署失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
