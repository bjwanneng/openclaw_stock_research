#!/usr/bin/env python3
"""
Simple debug script for Windows (no special characters)
"""

import sys
import os

# Add project source to path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Set default environment variables
os.environ.setdefault('AKSHARE_DATA_PATH', os.path.join(project_root, 'data', 'akshare_cache'))
os.environ.setdefault('LOG_LEVEL', 'INFO')

print("=" * 70)
print(" OpenClaw Stock Research - Simple Debug")
print("=" * 70)
print()

# Test 1: Import
print("[Test 1] Import test")
try:
    from openclaw_stock.tools.ak_market_tool import ak_market_tool
    from openclaw_stock.tools.web_quote_validator import web_quote_validator_tool
    print("  Result: Import successful")
except Exception as e:
    print(f"  Result: Import failed - {e}")
    sys.exit(1)

# Test 2: Web Quote Validator (usually works better)
print()
print("[Test 2] Web Quote Validator (Eastmoney)")
try:
    result = web_quote_validator_tool(
        symbol="000001",
        market="sz",
        source="eastmoney"
    )
    print(f"  Stock: {result.get('name')}")
    print(f"  Price: {result.get('price')}")
    print(f"  Change: {result.get('change_pct')}%")
    print("  Result: Success")
except Exception as e:
    print(f"  Result: Failed - {e}")

# Test 3: AkShare (may fail due to network issues)
print()
print("[Test 3] AkShare Market Tool (Realtime)")
print("  Note: This may fail due to network connectivity issues")
try:
    result = ak_market_tool(
        action="realtime",
        symbol="000001",
        market="sz"
    )
    print(f"  Stock: {result.get('name')}")
    print(f"  Price: {result.get('price')}")
    print("  Result: Success")
except Exception as e:
    print(f"  Result: Failed - {type(e).__name__}")
    print(f"  Error: {str(e)[:100]}")

print()
print("=" * 70)
print(" Debug completed")
print("=" * 70)
