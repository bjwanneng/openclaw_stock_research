# OpenClaw 投研分析系统

基于 OpenClaw 框架的 A股/港股投研分析工具集，提供结构化数据获取、实时价格验证和深度研报合成能力。

## 项目概述

本项目包含以下核心组件：

- **ak_market_tool**: 基于 AkShare 的结构化数据引擎，获取 A股/港股的实时行情、历史K线、基本面和资金流向数据
- **web_quote_validator**: 基于 Requests 的实时验证器，通过东方财富/腾讯/新浪等数据源验证价格准确性
- **StockAnalystPro Skill**: 复合技能，整合上述工具生成深度投研报告

## 目录结构

```
openclaw_stock_research/
├── src/openclaw_stock/           # 源代码目录
│   ├── tools/                    # 工具脚本
│   │   ├── ak_market_tool.py     # AkShare数据引擎
│   │   └── web_quote_validator.py # Web验证器
│   ├── core/                     # 核心模块
│   │   ├── config.py             # 配置管理
│   │   ├── exceptions.py         # 自定义异常
│   │   └── models.py             # 数据模型
│   ├── adapters/                 # 数据源适配器
│   │   └── akshare_adapter.py    # AkShare适配器
│   └── utils/                    # 工具函数
│       ├── decorators.py         # 装饰器
│       └── logger.py             # 日志配置
├── SKILL.md                      # OpenClaw技能定义
├── pyproject.toml                # 项目配置
├── README.md                     # 本文件
└── .env.example                  # 环境变量示例
```

## 安装说明

### 方式一：VPS 一键部署（推荐）

如果您在 VPS 上部署 OpenClaw，可以使用我们提供的一键部署脚本：

```bash
# 1. 下载部署脚本
wget https://raw.githubusercontent.com/bjwanneng/openclaw-stock-research/main/deploy_vps.sh
chmod +x deploy_vps.sh

# 2. 执行部署
./deploy_vps.sh

# 或者指定自定义工作区路径
./deploy_vps.sh /path/to/your/workspace
```

部署脚本会自动完成以下操作：
- 检查系统依赖（Python 3.9+、Git）
- 创建 OpenClaw 工作区目录结构
- 克隆项目仓库
- 创建 Python 虚拟环境并安装依赖
- 配置环境变量（从 .env.example 复制）
- 创建 OpenClaw 符号链接
- 验证部署是否成功

部署完成后，请记得：
1. 编辑 `.env` 文件配置必要的环境变量（特别是 `AKSHARE_DATA_PATH`）
2. 测试工具是否能正常运行

### 方式二：手动部署

```bash
git clone https://github.com/bjwanneng/openclaw-stock-research.git
cd openclaw-stock-research
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -e .
# 或安装开发依赖
pip install -e ".[dev]"
```

## 环境变量配置

复制 `.env.example` 到 `.env` 并根据实际情况配置：

```bash
cp .env.example .env
```

关键环境变量：

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| AKSHARE_DATA_PATH | 是 | - | AkShare数据缓存路径 |
| PROXY_URL | 否 | - | 代理服务器地址 |
| LOG_LEVEL | 否 | INFO | 日志级别 |
| DEFAULT_TIMEOUT | 否 | 30 | 默认请求超时(秒) |

## 使用说明

### 1. 使用 ak_market_tool

```python
from openclaw_stock.tools.ak_market_tool import ak_market_tool

# 获取实时行情
result = ak_market_tool(
    action="realtime",
    symbol="000001",
    market="sz"
)

# 获取历史K线
result = ak_market_tool(
    action="kline",
    symbol="000001",
    market="sz",
    period="daily",
    start_date="20240101",
    end_date="20240131",
    adjust="qfq"
)
```

## 虚拟环境自动激活（可选）

### 方案一：工具脚本自动激活（推荐）

工具脚本已经集成了自动检测和激活虚拟环境的功能。当工具被调用时，会自动查找并激活正确的虚拟环境。

如果需要手动控制虚拟环境激活，可以使用 `venv_helper`：

```python
from openclaw_stock.utils.venv_helper import auto_activate

# 在脚本开头调用，自动查找并激活虚拟环境
auto_activate()

# 后续代码将在正确的虚拟环境中运行
from openclaw_stock.tools.ak_market_tool import ak_market_tool
# ...
```

### 方案二：OpenClaw 启动时自动激活

在 OpenClaw 的配置中，可以通过 `python_path` 指定虚拟环境的 Python 解释器路径。

编辑 OpenClaw 配置文件（通常是 `~/.openclaw/config.json`）：

```json
{
  "version": "1.0.0",
  "python_path": "/home/username/.openclaw/workspace/openclaw-stock-research/venv/bin/python",
  "skills": [
    {
      "name": "StockAnalystPro",
      "path": "skills/stock-research/SKILL.md",
      "enabled": true
    }
  ],
  "tools": [
    {
      "name": "ak_market_tool",
      "path": "custom_tools/ak_market_tool.py",
      "enabled": true
    },
    {
      "name": "web_quote_validator",
      "path": "custom_tools/web_quote_validator.py",
      "enabled": true
    }
  ]
}
```

通过设置 `python_path` 指向虚拟环境的 Python 解释器，OpenClaw 将始终在该虚拟环境中运行所有工具和技能。

### 方案三：使用激活脚本（兼容性好）

在 `~/.openclaw/workspace/custom_tools/` 目录下创建激活脚本 `activate_venv.sh`：

```bash
#!/bin/bash
# 激活虚拟环境脚本

VENV_PATH="${VENV_PATH:-$HOME/.openclaw/workspace/openclaw-stock-research/venv}"

if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
    echo "已激活虚拟环境: $VENV_PATH"
else
    echo "错误: 找不到虚拟环境: $VENV_PATH"
    exit 1
fi
```

然后在工具的 Python 文件开头添加：

```python
import os
import subprocess

# 尝试激活虚拟环境
venv_path = os.path.expanduser("~/.openclaw/workspace/openclaw-stock-research/venv")
if os.path.exists(f"{venv_path}/bin/activate"):
    # 检查当前是否已在虚拟环境中
    if not hasattr(__import__('sys'), 'real_prefix') and not (
        hasattr(__import__('sys'), 'base_prefix') and
        __import__('sys').base_prefix != __import__('sys').prefix
    ):
        # 重新执行当前脚本在虚拟环境中
        os.execl(f"{venv_path}/bin/python", f"{venv_path}/bin/python", *sys.argv)
```

### 2. 使用 web_quote_validator

```python
from openclaw_stock.tools.web_quote_validator import web_quote_validator_tool

# 仅获取Web价格
result = web_quote_validator_tool(
    symbol="000001",
    market="sz",
    source="eastmoney"
)

# 获取Web价格并与参考价格验证
result = web_quote_validator_tool(
    symbol="000001",
    market="sz",
    source="eastmoney",
    reference_price=10.26,
    threshold=0.5
)
```

### 3. 使用 StockAnalystPro Skill

Skill 的执行通过 OpenClaw 框架调用，配置方式如下：

1. 将 `SKILL.md` 放置在 OpenClaw 的 skills 目录下
2. 在 `openclaw.json` 中注册该 Skill
3. 通过 OpenClaw CLI 调用

示例配置 (`openclaw.json`):

```json
{
  "skills": [
    {
      "name": "StockAnalystPro",
      "path": "~/.openclaw/workspace/skills/stock-research/SKILL.md",
      "enabled": true
    }
  ],
  "tools": [
    {
      "name": "ak_market_tool",
      "path": "~/.openclaw/workspace/custom_tools/ak_market_tool.py",
      "enabled": true
    },
    {
      "name": "web_quote_validator",
      "path": "~/.openclaw/workspace/custom_tools/web_quote_validator.py",
      "enabled": true
    }
  ]
}
```

## 开发指南

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_ak_market_tool.py

# 带覆盖率报告
pytest --cov=openclaw_stock --cov-report=html
```

### 代码格式化

```bash
# 使用 black 格式化
black src tests

# 使用 isort 排序导入
isort src tests
```

### 类型检查

```bash
mypy src/openclaw_stock
```

## 部署指南

### 部署到 OpenClaw 工作区

1. 构建分发包:

```bash
python -m build
```

2. 安装到 OpenClaw 环境:

```bash
# 复制工具到 OpenClaw 工作区
cp -r src/openclaw_stock/tools/* ~/.openclaw/workspace/custom_tools/

# 复制 SKILL.md
mkdir -p ~/.openclaw/workspace/skills/stock-research
cp SKILL.md ~/.openclaw/workspace/skills/stock-research/
```

3. 更新 OpenClaw 配置:

编辑 `~/.openclaw/config.json`，添加工具和技能的注册信息。

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 致谢

- [AkShare](https://www.akshare.xyz/) - 强大的金融数据接口库
- [OpenClaw](https://github.com/openclaw) - 智能助手框架
- [东方财富](https://www.eastmoney.com/) - 数据来源
- [腾讯财经](https://finance.qq.com/) - 数据来源
- [新浪财经](https://finance.sina.com.cn/) - 数据来源

## 联系方式

- 项目主页: https://github.com/bjwanneng/openclaw-stock-research
- 问题反馈: https://github.com/bjwanneng/openclaw-stock-research/issues
- 邮箱: bjzhangwn@gmail.com

---

**免责声明**: 本工具仅供学习和研究使用，不构成任何投资建议。投资有风险，入市需谨慎。
