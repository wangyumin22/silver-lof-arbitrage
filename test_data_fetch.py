# -*- coding: utf-8 -*-
"""
测试数据获取功能是否正常工作
"""
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from silver_lof_arbitrage import get_fund_net_value_direct, get_realtime_price_direct

def test_data_fetching():
    print("=== 测试数据获取功能 ===")
    
    # 测试获取基金净值
    print("\n1. 测试获取基金净值:")
    fund_net_value = get_fund_net_value_direct()
    if fund_net_value is not None:
        print("   ✅ 成功获取基金净值:", fund_net_value)
    else:
        print("   ❌ 无法获取基金净值")
    
    # 测试获取实时价格
    print("\n2. 测试获取实时价格:")
    realtime_price = get_realtime_price_direct()
    if realtime_price is not None:
        print("   ✅ 成功获取实时价格:", realtime_price)
    else:
        print("   ❌ 无法获取实时价格")
    
    # 测试溢价计算
    print("\n3. 测试溢价计算:")
    if fund_net_value is not None and realtime_price is not None:
        premium_rate = ((realtime_price - fund_net_value) / fund_net_value) * 100
        print("   ✅ 成功计算溢价率:", "{:.2f}%", premium_rate)
    else:
        print("   ❌ 无法计算溢价率(缺少数据)")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_data_fetching()
