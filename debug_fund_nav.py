# 调试基金净值API获取

import requests
import re
from datetime import datetime

print("=== 调试基金净值API ===")

fund_code = "161226"
url = f"http://fund.eastmoney.com/pingzhongdata/{fund_code}.js"
print(f"URL: {url}")

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    
    print(f"状态码: {response.status_code}")
    print(f"响应长度: {len(response.text)} 字符")
    
    if response.status_code == 200:
        content = response.text
        
        # 检查特定部分
        print("\n--- 查找基金名称 ---")
        name_pattern = r'var fS_name = "([^"]+)"'
        name_match = re.search(name_pattern, content)
        if name_match:
            fund_name = name_match.group(1)
            print(f"找到基金名称: {fund_name}")
        else:
            print("未找到基金名称")
            # 显示更多内容来调试
            print("前500字符:")
            print(content[:500])
        
        print("\n--- 查找净值趋势数据 ---")
        # 先查找Data_netWorthTrend的开始位置
        trend_start = content.find('Data_netWorthTrend')
        if trend_start != -1:
            print(f"找到Data_netWorthTrend在位置: {trend_start}")
            # 显示该位置附近的内容
            snippet = content[trend_start:trend_start+200]
            print(f"附近内容: {snippet}")
            
            # 使用正则表达式提取
            trend_pattern = r'var Data_netWorthTrend\s*=\s*\[([^\]]+)\]'
            trend_match = re.search(trend_pattern, content)
            if trend_match:
                trend_data = trend_match.group(1)
                print(f"提取到趋势数据，长度: {len(trend_data)} 字符")
                
                # 查找最后一个数据点
                print("\n--- 查找最后一个数据点 ---")
                data_points = trend_data.split('},{')
                print(f"总共找到 {len(data_points)} 个数据点")
                
                if data_points:
                    last_point = data_points[-1]
                    # 确保格式正确
                    if not last_point.startswith('{'):
                        last_point = '{' + last_point
                    if not last_point.endswith('}'):
                        last_point = last_point + '}'
                    
                    print(f"最后一个数据点: {last_point}")
                    
                    # 提取x和y
                    x_pattern = r'"x"\s*:\s*(\d+)'
                    y_pattern = r'"y"\s*:\s*([\d.]+)'
                    
                    x_match = re.search(x_pattern, last_point)
                    y_match = re.search(y_pattern, last_point)
                    
                    if x_match and y_match:
                        x = int(x_match.group(1))
                        y = float(y_match.group(1))
                        
                        # 转换时间
                        timestamp = x / 1000
                        nav_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                        
                        print(f"提取到: x={x}, y={y}")
                        print(f"转换为: 净值={y}, 日期={nav_date}")
                    else:
                        print("无法从最后一个数据点提取x和y")
                else:
                    print("没有找到数据点")
            else:
                print("正则表达式未匹配到趋势数据")
        else:
            print("未找到Data_netWorthTrend")
    else:
        print(f"请求失败: {response.status_code}")
        print(f"响应内容: {response.text}")
        
except Exception as e:
    print(f"请求异常: {type(e).__name__} - {str(e)}")
    import traceback
    traceback.print_exc()

print("\n=== 调试完成 ===")
