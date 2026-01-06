# 完整测试应用功能的脚本，不依赖Streamlit服务器

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入数据获取函数
from silver_lof_arbitrage import get_fund_net_value_direct, get_realtime_price_direct

print("=== 完整测试白银LOF套利应用功能 ===")

# 测试基金净值获取
print("\n1. 测试基金净值获取")
nav, nav_date, fund_name = get_fund_net_value_direct("161226")
print(f"   结果: 基金名称={fund_name}, 净值={nav}, 净值日期={nav_date}")

# 测试实时价格获取
print("\n2. 测试实时价格获取")
realtime_price, update_time = get_realtime_price_direct("161226")
print(f"   结果: 实时价格={realtime_price}, 更新时间={update_time}")

# 计算溢价率
print("\n3. 计算溢价率")
if nav and realtime_price:
    try:
        nav_float = float(nav)
        price_float = float(realtime_price)
        premium_rate = (price_float - nav_float) / nav_float * 100
        print(f"   溢价率: {premium_rate:.2f}%")
        
        # 给出套利建议
        if premium_rate > 2.0:
            print("   套利建议: ⚠️ 溢价率较高，考虑卖出LOF份额并申购基金份额")
        elif premium_rate < -2.0:
            print("   套利建议: ⚠️ 折价率较高，考虑买入LOF份额并赎回基金份额")
        else:
            print("   套利建议: ✅ 溢价率在合理范围内，无明显套利机会")
    except ValueError as e:
        print(f"   计算失败: {e}")
else:
    print("   计算失败: 数据不完整")

print("\n=== 测试完成 ===")
