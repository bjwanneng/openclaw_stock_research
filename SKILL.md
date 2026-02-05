# OpenClaw Skill: StockAnalystPro

## 元数据 (Metadata)

- **名称**: StockAnalystPro
- **版本**: 1.0.0
- **描述**: 专业A股/港股投研分析技能，结合AkShare结构化数据与Web实时验证，提供深度研报合成能力
- **运行时**: python
- **依赖工具**:
  - ak_market_tool
  - web_quote_validator
  - browser (OpenClaw内置)

## 执行流程 (Execution Flow)

```mermaid
graph TD
    A[开始分析] --> B[调用 web_quote_validator 获取实时价格]
    B --> C{获取成功?}
    C -->|否| D[返回错误信息]
    C -->|是| E[调用 ak_market_tool 获取历史数据]
    E --> F{获取成功?}
    F -->|否| G[仅返回实时数据]
    F -->|是| H[执行价格验证]
    H --> I{误差<0.5%?}
    I -->|否| J[添加 [DATA_MISMATCH_WARNING] 标记]
    I -->|是| K[数据验证通过]
    J --> L[调用 Browser 抓取雪球/财联社热点]
    K --> L
    L --> M[综合信息生成 Markdown 研报]
    M --> N[返回完整分析报告]
    G --> N
    D --> O[结束]
    N --> O
```

## 输入参数 (Input Parameters)

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| symbol | string | 是 | - | 股票代码（如"000001"） |
| market | string | 否 | sh | 市场类型: sh-上证, sz-深证, hk-港股 |
| period | string | 否 | daily | K线周期: daily-日线, weekly-周线, monthly-月线 |
| start_date | string | 否 | - | 历史数据开始日期(YYYYMMDD) |
| end_date | string | 否 | - | 历史数据结束日期(YYYYMMDD) |
| adjust | string | 否 | qfq | 复权方式: qfq-前复权, hfq-后复权, none-不复权 |
| include_fundamental | bool | 否 | true | 是否包含基本面数据 |
| include_capital_flow | bool | 否 | true | 是否包含资金流向数据 |
| include_news | bool | 否 | true | 是否抓取相关新闻热点 |

## 输出格式 (Output Format)

### 成功响应

```json
{
  "status": "success",
  "symbol": "000001",
  "market": "sz",
  "name": "平安银行",
  "timestamp": "2024-01-15T14:30:00+08:00",
  "data": {
    "realtime": {
      "price": 10.25,
      "change": 0.15,
      "change_pct": 1.48,
      "volume": 152345600,
      "amount": 1562345678.90
    },
    "validation": {
      "is_valid": true,
      "web_price": 10.25,
      "reference_price": 10.26,
      "diff_pct": 0.0975
    },
    "kline": {
      "period": "daily",
      "adjust": "qfq",
      "data_count": 100,
      "data": [
        {
          "date": "2024-01-15",
          "open": 10.10,
          "high": 10.30,
          "low": 10.05,
          "close": 10.25,
          "volume": 152345600
        }
      ]
    },
    "fundamental": {
      "pe_ttm": 4.52,
      "pb": 0.52,
      "dividend_yield": 2.15,
      "market_cap": 198523456789.12
    },
    "capital_flow": {
      "main_force_inflow": 1234567.89,
      "retail_inflow": -987654.32,
      "net_inflow": 246913.57
    }
  },
  "news": [
    {
      "title": "平安银行发布2024年业绩预告",
      "source": "财联社",
      "time": "2024-01-15 10:30",
      "url": "https://..."
    }
  ],
  "analysis": {
    "summary": "平安银行当前股价10.25元，涨1.48%。PE仅4.52倍，估值处于历史低位。主力资金净流入123万元，短期走势偏强。",
    "technical_signals": ["价格突破5日均线", "MACD金叉"],
    "risk_warnings": [],
    "investment_suggestion": "估值处于历史低位，可关注"
  },
  "report": "# 平安银行(000001)投研分析报告\n\n## 一、行情概览\n当前股价：10.25元\n涨跌幅：+1.48%\n成交额：15.62亿元\n\n## 二、估值分析\n市盈率TTM：4.52倍\n市净率：0.52倍\n股息率：2.15%\n\n## 三、资金流向\n主力资金净流入：123.46万元\n散户资金净流入：-98.77万元\n\n## 四、技术面\n- 价格突破5日均线\n- MACD金叉\n\n## 五、投资建议\n估值处于历史低位，可关注。"
}
```

### 验证失败响应（价格偏差>0.5%）

```json
{
  "status": "warning",
  "symbol": "000001",
  "market": "sz",
  "data": {
    "realtime": {
      "price": 10.25,
      "change": 0.15,
      "change_pct": 1.48
    },
    "validation": {
      "is_valid": false,
      "web_price": 10.25,
      "reference_price": 10.35,
      "diff_pct": 0.9662,
      "warning": "[DATA_MISMATCH_WARNING] 价格偏差超过0.5%！Web价格(10.25)与参考价格(10.35)差异为0.9662%"
    }
  }
}
```

## 错误处理

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| DATA_SOURCE_ERROR | 数据源访问失败 | 检查网络连接或代理设置 |
| VALIDATION_ERROR | 数据验证失败 | 检查股票代码是否正确 |
| NETWORK_ERROR | 网络请求失败 | 检查网络连接或代理设置 |
| SYMBOL_NOT_FOUND | 股票代码不存在 | 确认代码和市场类型 |
| PRICE_MISMATCH_ERROR | 价格偏差过大 | 进行人工复核 |

## 环境变量

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| AKSHARE_DATA_PATH | 是 | - | AkShare数据缓存路径 |
| PROXY_URL | 否 | - | 代理服务器地址 |
| LOG_LEVEL | 否 | INFO | 日志级别 |

## 使用示例

### 示例1: 完整研报分析

```python
# 分析平安银行的全面数据
stock_research_pro(
    symbol="000001",
    market="sz",
    period="daily",
    start_date="20231001",
    end_date="20240115",
    adjust="qfq",
    include_fundamental=True,
    include_capital_flow=True,
    include_news=True
)
```

### 示例2: 港股分析

```python
# 分析腾讯控股
stock_research_pro(
    symbol="00700",
    market="hk",
    period="daily",
    include_fundamental=True,
    include_capital_flow=False  # 港股暂不支持资金流向
)
```

### 示例3: 快速实时查询

```python
# 仅获取实时行情（不获取历史数据）
stock_research_pro(
    symbol="600519",
    market="sh",
    start_date=None,  # 不指定日期则不获取历史数据
    end_date=None
)
```

## 注意事项

1. **数据延迟**：实时行情数据可能有15分钟延迟（交易所规定）
2. **港股限制**：部分功能（如北向资金）仅适用于A股
3. **频率限制**：请合理控制调用频率，避免对数据源造成压力
4. **代理配置**：如访问受限，请设置PROXY_URL环境变量
5. **价格验证**：当价格偏差超过0.5%时，务必进行人工复核
