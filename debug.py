#!/usr/bin/env python3
"""
OpenClaw 投研分析系统 - 本地调试脚本

此脚本用于在本地开发环境中快速测试工具功能，无需部署到 VPS。

使用方法:
    python debug.py [选项]

选项:
    --tool TOOL       指定要测试的工具 (ak_market_tool|web_quote_validator|all)
    --action ACTION   指定操作类型 (realtime|kline|fundamental|capital_flow)
    --symbol SYMBOL   股票代码 (默认: 000001)
    --market MARKET   市场类型 (默认: sz)
    --validate        启用价格验证

示例:
    # 测试 ak_market_tool 获取实时行情
    python debug.py --tool ak_market_tool --action realtime

    # 测试 web_quote_validator 并验证价格
    python debug.py --tool web_quote_validator --validate

    # 测试所有功能
    python debug.py --tool all
"""

import sys
import os
import argparse

# 添加项目源码到路径
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# 设置默认环境变量（如果 .env 文件不存在）
os.environ.setdefault('AKSHARE_DATA_PATH', os.path.join(project_root, 'data', 'akshare_cache'))
os.environ.setdefault('LOG_LEVEL', 'INFO')

def print_header(title):
    """打印标题"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def print_result(data, title="Result"):
    """格式化打印结果"""
    print(f"\n[ {title} ]")
    print("-" * 70)
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (int, float)):
                print(f"  {key:20s}: {value:>15.2f}")
            else:
                print(f"  {key:20s}: {value}")
    else:
        print(data)
    print("-" * 70)

def test_ak_market_tool_realtime(symbol="000001", market="sz"):
    """测试 ak_market_tool 获取实时行情"""
    from openclaw_stock.tools.ak_market_tool import ak_market_tool

    print_header("Testing ak_market_tool - Realtime Quote")
    print(f"Parameters: symbol={symbol}, market={market}")

    try:
        result = ak_market_tool(
            action="realtime",
            symbol=symbol,
            market=market
        )

        print_result(result, "Realtime Quote Data")

        # Verify key fields
        assert result["symbol"] == symbol
        assert result["market"] == market
        assert "name" in result
        assert "price" in result
        assert result["price"] > 0

        print("[ OK ] Test passed\n")
        return result

    except Exception as e:
        print(f"[ ERROR ] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_web_quote_validator(symbol="000001", market="sz", validate=False, reference_price=None):
    """测试 web_quote_validator"""
    from openclaw_stock.tools.web_quote_validator import web_quote_validator_tool

    print_header("Testing web_quote_validator")
    print(f"Parameters: symbol={symbol}, market={market}, validate={validate}")

    try:
        kwargs = {
            "symbol": symbol,
            "market": market,
            "source": "eastmoney"
        }

        if validate and reference_price:
            kwargs["reference_price"] = reference_price
            kwargs["threshold"] = 0.5

        result = web_quote_validator_tool(**kwargs)

        print_result(result, "Web Quote Data")

        assert result["symbol"] == symbol
        assert result["market"] == market
        assert result["source"] == "eastmoney"
        assert "price" in result
        assert result["price"] > 0

        if validate and reference_price:
            assert "validation" in result
            validation = result["validation"]
            print(f"\n[ Price Validation Result ]")
            print(f"  Web Price: {validation['web_price']}")
            print(f"  Reference Price: {validation['reference_price']}")
            print(f"  Difference: {validation['diff_pct']:.4f}%")
            print(f"  Valid: {'Yes' if validation['is_valid'] else 'No'}")

        print("[ OK ] Test passed\n")
        return result

    except Exception as e:
        print(f"[ ERROR ] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_all():
    """运行所有测试"""
    print("\n" + "=" * 70)
    print(" OpenClaw Stock Research - Full Test Suite")
    print("=" * 70)

    results = {
        "ak_market_realtime": None,
        "web_quote": None,
        "web_quote_validated": None
    }

    # 测试 ak_market_tool
    results["ak_market_realtime"] = test_ak_market_tool_realtime()

    # 测试 web_quote_validator（不带验证）
    results["web_quote"] = test_web_quote_validator(validate=False)

    # 如果 ak_market_tool 成功，用其价格验证 web_quote_validator
    if results["ak_market_realtime"]:
        ak_price = results["ak_market_realtime"].get("price")
        results["web_quote_validated"] = test_web_quote_validator(
            validate=True,
            reference_price=ak_price
        )

    # 打印测试总结
    print("\n" + "=" * 70)
    print(" Test Summary")
    print("=" * 70)

    passed = 0
    failed = 0
    for name, result in results.items():
        if result is not None:
            print(f" [ OK ] {name}")
            passed += 1
        else:
            print(f" [ FAIL ] {name}")
            failed += 1

    print(f"\n Total: {passed} passed, {failed} failed")
    print("=" * 70 + "\n")

    return failed == 0

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="OpenClaw Stock Research - Debug Script"
    )
    parser.add_argument(
        "--tool",
        choices=["ak_market_tool", "web_quote_validator", "all"],
        default="all",
        help="Specify tool to test"
    )
    parser.add_argument(
        "--action",
        choices=["realtime", "kline", "fundamental", "capital_flow"],
        default="realtime",
        help="Specify action type"
    )
    parser.add_argument(
        "--symbol",
        default="000001",
        help="Stock symbol (default: 000001)"
    )
    parser.add_argument(
        "--market",
        default="sz",
        help="Market type (default: sz)"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Enable price validation"
    )

    args = parser.parse_args()

    # Run tests based on arguments
    if args.tool == "all":
        success = test_all()
    elif args.tool == "ak_market_tool":
        if args.action == "realtime":
            success = test_ak_market_tool_realtime(args.symbol, args.market) is not None
        else:
            print(f"Action {args.action} not yet implemented in debug script")
            success = False
    elif args.tool == "web_quote_validator":
        result = test_web_quote_validator(args.symbol, args.market, args.validate)
        success = result is not None
    else:
        print(f"Unknown tool: {args.tool}")
        success = False

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
