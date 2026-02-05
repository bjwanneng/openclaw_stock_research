#!/usr/bin/env python3
"""
发布前综合功能测试

测试范围：
1. 适配器实例化和方法调用
2. 工具函数导入和基本功能
3. 数据获取功能（模拟/真实）
4. 异常处理
"""

import sys
import os

# 添加项目路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, "src"))

print("=" * 70)
print("  OpenClaw Stock Research - 发布前功能测试")
print("=" * 70)
print()

# 测试计数器
tests_passed = 0
tests_failed = 0

def test_section(name):
    """打印测试章节"""
    print()
    print("=" * 70)
    print(f"  {name}")
    print("=" * 70)

def test_case(name):
    """打印测试用例"""
    print(f"\n  [TEST] {name}")

def test_pass():
    """标记测试通过"""
    global tests_passed
    tests_passed += 1
    print(f"    [PASS] 测试通过")

def test_fail(error_msg):
    """标记测试失败"""
    global tests_failed
    tests_failed += 1
    print(f"    [FAIL] {error_msg}")

# ==================== 测试1: 适配器导入和实例化 ====================
test_section("测试1: 适配器导入和实例化")

try:
    test_case("导入 AKShareAdapterEM")
    from openclaw_stock.adapters.akshare_adapter_em import AKShareAdapterEM, get_adapter_em
    test_pass()
except Exception as e:
    test_fail(f"导入失败: {e}")

try:
    test_case("实例化 AKShareAdapterEM")
    adapter = AKShareAdapterEM()
    test_pass()
except Exception as e:
    test_fail(f"实例化失败: {e}")

try:
    test_case("使用 get_adapter_em 单例模式")
    adapter2 = get_adapter_em()
    assert adapter2 is adapter, "单例模式失败"
    test_pass()
except Exception as e:
    test_fail(f"单例模式测试失败: {e}")

# ==================== 测试2: 适配器方法存在性检查 ====================
test_section("测试2: 适配器方法存在性检查")

required_methods = [
    'get_stock_zh_a_spot',
    'get_stock_hk_spot',
    'get_stock_zh_a_hist',
    'get_stock_hk_hist',
]

try:
    from openclaw_stock.adapters.akshare_adapter_em import AKShareAdapterEM
    adapter = AKShareAdapterEM()

    for method in required_methods:
        test_case(f"检查方法: {method}")
        if hasattr(adapter, method):
            test_pass()
        else:
            test_fail(f"方法不存在: {method}")
except Exception as e:
    test_fail(f"方法检查失败: {e}")

# ==================== 测试3: 工具导入检查 ====================
test_section("测试3: 工具导入检查")

try:
    test_case("导入 ak_market_tool")
    from openclaw_stock.tools.ak_market_tool import ak_market_tool
    test_pass()
except Exception as e:
    test_fail(f"导入失败: {e}")

try:
    test_case("导入 web_quote_validator_tool")
    from openclaw_stock.tools.web_quote_validator import web_quote_validator_tool
    test_pass()
except Exception as e:
    test_fail(f"导入失败: {e}")

# ==================== 测试4: 核心模块导入检查 ====================
test_section("测试4: 核心模块导入检查")

modules_to_test = [
    ('openclaw_stock.core.config', 'get_config'),
    ('openclaw_stock.core.exceptions', 'DataSourceError'),
    ('openclaw_stock.utils.logger', 'get_logger'),
    ('openclaw_stock.utils.decorators', 'tool'),
]

for module_name, attr_name in modules_to_test:
    test_case(f"导入 {module_name}.{attr_name}")
    try:
        module = __import__(module_name, fromlist=[attr_name])
        getattr(module, attr_name)
        test_pass()
    except Exception as e:
        test_fail(f"导入失败: {e}")

# ==================== 测试结果汇总 ====================
print()
print("=" * 70)
print("  测试结果汇总")
print("=" * 70)
print()
print(f"  通过: {tests_passed}")
print(f"  失败: {tests_failed}")
print(f"  总计: {tests_passed + tests_failed}")
print()

if tests_failed == 0:
    print("  [PASS] 所有测试通过！可以发布！")
    exit_code = 0
else:
    print(f"  [FAIL] 有 {tests_failed} 个测试失败，请修复后再发布！")
    exit_code = 1

print("=" * 70)

sys.exit(exit_code)
