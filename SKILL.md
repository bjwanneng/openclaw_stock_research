---
name: stock-analyst-pro
description: Professional A-share/Hong Kong stock research and analysis skill. Combines AkShare structured data with real-time web validation to provide in-depth research report synthesis. Use when analyzing Chinese stocks, getting stock quotes, or generating investment research reports.
allowed-tools: Read, Grep, Glob, Bash, Task
---

# Stock Analyst Pro

Professional A-share/Hong Kong stock research and analysis skill that combines AkShare structured data with real-time web validation to provide in-depth research report synthesis.

## Definitions

### Name
StockAnalystPro

### Description
专业A股/港股投研分析技能，结合AkShare结构化数据与Web实时验证，提供深度研报合成能力。适用于股票分析、获取实时行情、生成投研报告。

### Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| symbol | string | Yes | - | Stock code (e.g., "000001") |
| market | string | No | sh | Market type: sh-Shanghai, sz-Shenzhen, hk-Hong Kong |
| period | string | No | daily | K-line period: daily, weekly, monthly |
| start_date | string | No | - | Historical data start date (YYYYMMDD) |
| end_date | string | No | - | Historical data end date (YYYYMMDD) |
| adjust | string | No | qfq | Adjustment method: qfq-forward, hfq-backward, none |
| include_fundamental | bool | No | true | Include fundamental data |
| include_capital_flow | bool | No | true | Include capital flow data |
| include_news | bool | No | true | Include related news |

### Output Format

#### Success Response
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
      "data": [...]
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
  "news": [...],
  "analysis": {
    "summary": "...",
    "technical_signals": [...],
    "risk_warnings": [],
    "investment_suggestion": "..."
  },
  "report": "# Markdown report..."
}
```

#### Validation Failed Response
```json
{
  "status": "warning",
  "symbol": "000001",
  "market": "sz",
  "data": {
    "realtime": {...},
    "validation": {
      "is_valid": false,
      "web_price": 10.25,
      "reference_price": 10.35,
      "diff_pct": 0.9662,
      "warning": "[DATA_MISMATCH_WARNING] 价格偏差超过0.5%！"
    }
  }
}
```

## Execution Flow

```mermaid
graph TD
    A[Start Analysis] --> B[Call web_quote_validator for real-time price]
    B --> C{Success?}
    C -->|No| D[Return error]
    C -->|Yes| E[Call ak_market_tool for historical data]
    E --> F{Success?}
    F -->|No| G[Return real-time data only]
    F -->|Yes| H[Perform price validation]
    H --> I{Diff < 0.5%?}
    I -->|No| J[Add [DATA_MISMATCH_WARNING] tag]
    I -->|Yes| K[Data validation passed]
    J --> L[Call Browser to fetch news from Xueqiu/Cailianshe]
    K --> L
    L --> M[Generate Markdown research report]
    M --> N[Return complete analysis report]
    G --> N
    D --> O[End]
    N --> O
```

## Error Handling

| Error Code | Description | Solution |
|------------|-------------|----------|
| DATA_SOURCE_ERROR | Data source access failed | Check network connection or proxy settings |
| VALIDATION_ERROR | Data validation failed | Check if stock code is correct |
| NETWORK_ERROR | Network request failed | Check network connection or proxy settings |
| SYMBOL_NOT_FOUND | Stock code does not exist | Confirm code and market type |
| PRICE_MISMATCH_ERROR | Price deviation too large | Manual review required |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| AKSHARE_DATA_PATH | Yes | - | AkShare data cache path |
| PROXY_URL | No | - | Proxy server address |
| LOG_LEVEL | No | INFO | Log level |

## Usage Examples

### Example 1: Complete Research Report

```python
# Analyze Ping An Bank comprehensive data
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

### Example 2: Hong Kong Stock Analysis

```python
# Analyze Tencent Holdings
stock_research_pro(
    symbol="00700",
    market="hk",
    period="daily",
    include_fundamental=True,
    include_capital_flow=False  # Hong Kong stocks don't support capital flow
)
```

### Example 3: Quick Real-time Quote

```python
# Get real-time quote only (no historical data)
stock_research_pro(
    symbol="600519",
    market="sh",
    start_date=None,  # No date specified = no historical data
    end_date=None
)
```

## Notes

1. **Data Delay**: Real-time quotes may have 15-minute delay (exchange regulations)
2. **Hong Kong Stock Limitations**: Some features (e.g., northbound capital flow) only apply to A-shares
3. **Rate Limiting**: Control call frequency to avoid stressing data sources
4. **Proxy Configuration**: Set PROXY_URL environment variable if access is restricted
5. **Price Validation**: Manual review required when price deviation exceeds 0.5%
