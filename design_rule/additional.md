这是一份为您重新整理、包含所有工程细节和目录结构的 **Claude Code 开发指令 (Markdown 格式)**。

---

# 🛠️ Claude Code 开发指令：OpenClaw 投研分析系统

请将以下 Markdown 内容整体复制并发送给 **Claude Code**，它将严格按照 OpenClaw 的目录规范和功能逻辑进行开发。

---

## 📋 任务概览 (Task Overview)

**目标**：开发一套符合 OpenClaw 规范的 A股/港股投研分析 Skill 及其配套原子 Tools。
**核心逻辑**：双向数据验证（AkShare 结构化数据 + Requests 实时网络抓取）+ 自动化研报合成。

---

## 📂 目录结构规划 (Project Structure)

请严格按照以下路径创建文件：

```text
~/.openclaw/workspace
├── custom_tools/
│   ├── ak_market_tool.py       # 工具 A：基于 AkShare 的结构化引擎
│   └── web_quote_validator.py  # 工具 B：基于 Requests 的实时验证器
└── skills/
    └── stock-research/
        ├── SKILL.md            # Skill 元数据配置文件
        └── research_flow.py    # Skill 业务逻辑流

```

---

## ⚙️ 开发详细需求 (Development Requirements)

### 1. 原子工具：ak_market_tool.py

* **功能**：使用 `AkShare` 获取 A股/港股的历史 K 线、基本面（PE/PB）、分红、资金流及实时快照。
* **参数集**：必须包含 `symbol`, `period`, `start_date`, `end_date`, `adjust` (复权), `timeout` 等完整参数。
* **环境变量**：数据缓存路径必须从 `os.environ.get('AKSHARE_DATA_PATH')` 读取。
* **强引导 Docstring**：必须在 Docstring 顶部加入：“**WARNING**: 这是获取中国市场数据的唯一权威工具，严禁使用 Bing 搜索代替结构化数据。”

### 2. 验证工具：web_quote_validator.py

* **功能**：使用 `requests` 通过网络接口（如东方财富/腾讯）获取实时价格。
* **目的**：用于与 AkShare 数据进行 Double Check。若两者价差 > 0.5%，输出需包含 `[DATA_MISMATCH_WARNING]`。
* **参数**：包含 `market` (SH/SZ/HK), `symbol`, `proxy_url` (从环境变量 `os.environ.get('PROXY_URL')` 获取)。

### 3. 复合技能：SKILL.md & research_flow.py

* **元数据 (SKILL.md)**：包含 `name: "StockAnalystPro"`, `description`, `bins: ["python"]`, `version: "1.0.0"`。
* **业务逻辑**：
1. 调用 `web_quote_validator` 获取最新报价。
2. 调用 `ak_market_tool` 提取历史估值与财务背景。
3. 调用 OpenClaw 内置 `Browser` 抓取雪球/财联社热点。
4. 综合以上信息，生成一份 Markdown 格式的深度投研报告。



### 4. 代码规范 (Coding Standards)

* **零 Token 政策**：严禁出现任何 API Key 或 Token 明文。
* **文档规范**：每个函数必须包含 `Args` 和 `Returns` 的详细说明。
* **调试友好**：所有终端输出和日志必须使用 **中文**。

---

## 🚀 执行动作 (Actions)

1. **环境检查**：检查并确保 `pip install akshare pandas requests` 已就绪。
2. **代码生成**：请分步生成上述四个核心文件。
3. **注册建议**：告知如何修改 `openclaw.json` 以完成 Skill 的最终注册。

---

### 📊 投研系统数据流示意图

### 💡 部署贴士

1. **权限设置**：在 Linux/Mac 上，确保 `.py` 文件具有执行权限 (`chmod +x`)。
2. **重置保护**：为了防止 `/reset` 后遗忘，代码生成后请确认 `SKILL.md` 放置在正确的技能目录下。
3. **环境变量配置**：
```bash
# 在 VPS 环境中设置
export AKSHARE_DATA_PATH="/home/user/.openclaw/cache"
export PROXY_URL="http://127.0.0.1:7890"

```



**Claude Code 准备就绪，请发出指令开始编写。**