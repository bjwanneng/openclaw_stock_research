"""
Pydantic数据模型定义

定义投研分析系统中使用的所有数据模型
"""

from typing import Optional, List, Dict, Any, Literal
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field, validator, field_validator


class StockSymbol(BaseModel):
    """股票代码模型"""

    symbol: str = Field(..., description="股票代码（如 000001, 00700）")
    market: Literal["sh", "sz", "hk"] = Field(..., description="市场类型: sh-上证, sz-深证, hk-港股")
    name: Optional[str] = Field(None, description="股票名称")

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        """验证股票代码格式"""
        v = v.strip().upper()
        if not v.isalnum():
            raise ValueError("股票代码只能包含字母和数字")
        return v

    def __str__(self) -> str:
        return f"{self.market}:{self.symbol}"


class RealtimeQuote(BaseModel):
    """实时行情数据模型"""

    source: str = Field(..., description="数据来源")
    symbol: str = Field(..., description="股票代码")
    market: str = Field(..., description="市场类型")
    name: str = Field(..., description="股票名称")
    price: float = Field(..., description="当前价格")
    change: float = Field(..., description="涨跌额")
    change_pct: float = Field(..., description="涨跌幅(%)")
    volume: int = Field(..., description="成交量（手）")
    amount: float = Field(..., description="成交额（元）")
    open: float = Field(..., description="开盘价")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    pre_close: float = Field(..., description="昨收价")
    timestamp: datetime = Field(default_factory=datetime.now, description="数据时间戳")


class KlineData(BaseModel):
    """K线数据模型"""

    date: date = Field(..., description="日期")
    open: float = Field(..., description="开盘价")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    close: float = Field(..., description="收盘价")
    volume: int = Field(..., description="成交量")
    amount: float = Field(..., description="成交额")
    amplitude: Optional[float] = Field(None, description="振幅(%)")
    change_pct: Optional[float] = Field(None, description="涨跌幅(%)")
    change: Optional[float] = Field(None, description="涨跌额")
    turnover: Optional[float] = Field(None, description="换手率(%)")


class FundamentalData(BaseModel):
    """基本面数据模型"""

    symbol: str = Field(..., description="股票代码")
    pe_ttm: Optional[float] = Field(None, description="市盈率TTM")
    pe_lyr: Optional[float] = Field(None, description="市盈率LYR")
    pb: Optional[float] = Field(None, description="市净率")
    ps_ttm: Optional[float] = Field(None, description="市销率TTM")
    dividend_yield: Optional[float] = Field(None, description="股息率(%)")
    market_cap: Optional[float] = Field(None, description="总市值")
    float_market_cap: Optional[float] = Field(None, description="流通市值")
    eps: Optional[float] = Field(None, description="每股收益")
    bps: Optional[float] = Field(None, description="每股净资产")
    roe: Optional[float] = Field(None, description="净资产收益率(%)")
    debt_ratio: Optional[float] = Field(None, description="资产负债率(%)")


class CapitalFlowData(BaseModel):
    """资金流向数据模型"""

    symbol: str = Field(..., description="股票代码")
    north_bound_inflow: Optional[float] = Field(None, description="北向资金净流入（亿元）")
    main_force_inflow: Optional[float] = Field(None, description="主力资金净流入（亿元）")
    retail_inflow: Optional[float] = Field(None, description="散户资金净流入（亿元）")
    large_order_inflow: Optional[float] = Field(None, description="大单净流入（亿元）")
    medium_order_inflow: Optional[float] = Field(None, description="中单净流入（亿元）")
    small_order_inflow: Optional[float] = Field(None, description="小单净流入（亿元）")


class ValidationResult(BaseModel):
    """验证结果模型"""

    is_valid: bool = Field(..., description="验证是否通过")
    web_price: float = Field(..., description="Web抓取价格")
    reference_price: float = Field(..., description="参考价格")
    diff: float = Field(..., description="价格差异绝对值")
    diff_pct: float = Field(..., description="价格差异百分比(%)")
    threshold: float = Field(default=0.5, description="验证阈值(%)")
    warning: Optional[str] = Field(None, description="警告信息")


class StockResearchResult(BaseModel):
    """股票投研分析结果模型"""

    status: str = Field(..., description="状态: success/warning/error")
    symbol: str = Field(..., description="股票代码")
    market: str = Field(..., description="市场类型")
    timestamp: datetime = Field(default_factory=datetime.now, description="分析时间戳")

    # 数据部分
    realtime: Optional[RealtimeQuote] = Field(None, description="实时行情数据")
    validation: Optional[ValidationResult] = Field(None, description="验证结果")
    kline: Optional[Dict[str, Any]] = Field(None, description="K线数据")
    fundamental: Optional[FundamentalData] = Field(None, description="基本面数据")
    capital_flow: Optional[CapitalFlowData] = Field(None, description="资金流向数据")

    # 分析部分
    analysis: Optional[Dict[str, Any]] = Field(None, description="综合分析结果")
    warnings: Optional[List[str]] = Field(None, description="警告信息列表")
    errors: Optional[List[str]] = Field(None, description="错误信息列表")
