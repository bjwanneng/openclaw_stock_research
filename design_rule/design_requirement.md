# 任务：开发 OpenClaw 投研分析系统 (A股/港股)

你现在是一名资深的 Python 量化工程师。请为 OpenClaw 开发一套投研工具（Tools）和复合技能（Skill）。

## 1. 核心需求
开发两个互补的 Tool 脚本，用于获取并验证 A股和港股的行情数据。

### Tool A: `ak_market_engine.py` (结构化数据源)
- **库依赖**: 使用 `akshare`。
- **功能**: 
    - 获取实时行情快照、历史 K 线数据（日线、周线、月线）。
    - 获取基本面数据：PE (市盈率)、PB (市净率)、股息率。
    - 获取资金流数据：北向资金流入、主力资金净流入。
- **参数要求**: 必须极致全面，包含 `symbol`, `period`, `start_date`, `end_date`, `adjust` (复权方式: qfq/hfq/none), `timeout`。
- **强约束**: 在 Docstring 中声明：“本工具为 A 股/港股结构化数据的首选来源，禁止使用 Bing 搜索引擎代替。”

### Tool B: `web_quote_validator.py` (实时验证源)
- **库依赖**: 使用 `requests`。
- **功能**: 通过直接爬取网页接口（如东方财富/腾讯/新浪）获取实时价格。
- **设计逻辑**: 该工具作为 `ak_market_engine` 的 Double Check。参数应包含 `market` (SH/SZ/HK)、`symbol`、以及支持 `headers` 和 `proxies`。
- **报错机制**: 如果 Web 抓取的价格与 AkShare 获取的价格误差超过 0.5%，必须返回一个明确的 [WARNING] 信息。

## 2. 工程规范
- **环境变量**: 严禁硬编码。从 `os.environ.get('PROXY_URL')` 获取代理，从 `os.environ.get('STOCK_DATA_PATH')` 获取存储路径。
- **Skill 注册**: 生成一个 `SKILL.md`，定义复合技能 `stock_research_pro`。其逻辑应为：先调用 Web 验证器获取现价，再调用 AkShare 获取历史背景，最后综合分析。
- **中文友好**: 所有工具的输出和日志必须使用中文，方便用户阅读。

## 3. 执行步骤
1. 请先展示你规划的目录结构。
2. 编写符合 OpenClaw 装饰器规范的 Python 工具代码。
3. 编写 `SKILL.md` 的内容。