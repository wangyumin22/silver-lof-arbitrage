import requests
import re
import json

# 测试天天基金网API
fund_code = "161226"
url = f"http://fund.eastmoney.com/pingzhongdata/{fund_code}.js"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'http://fund.eastmoney.com/',
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"状态码: {response.status_code}")
    print(f"响应长度: {len(response.text)} 字符")
    
    if response.status_code == 200:
        content = response.text
        
        # 先保存完整响应内容到文件
        with open("fund_api_response.txt", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("\n=== 响应内容前1000字符 ===")
        print(content[:1000])
        print("\n=== 响应内容后1000字符 ===")
        print(content[-1000:])
        
        # 尝试提取基金名称
        print("\n=== 尝试提取基金名称 ===")
        name_match = re.search(r'fund_name="([^"]+)"', content)
        if name_match:
            print(f"基金名称: {name_match.group(1)}")
        else:
            print("❌ 无法提取基金名称")
        
        # 尝试提取净值趋势数据
        print("\n=== 尝试提取净值趋势数据 ===")
        trend_pattern = r'var Data_netWorthTrend\s*=\s*(\[[^\]]+\])'  # 包含完整数组
        trend_match = re.search(trend_pattern, content)
        if trend_match:
            trend_str = trend_match.group(1)
            print(f"趋势数据长度: {len(trend_str)} 字符")
            print(f"趋势数据前500字符: {trend_str[:500]}...")
            
            # 尝试解析为JSON
            try:
                trend_data = json.loads(trend_str)
                if trend_data:
                    last_point = trend_data[-1]
                    print(f"最后一个数据点: {last_point}")
                    print(f"净值: {last_point.get('y')}")
                    print(f"时间戳: {last_point.get('x')}")
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
        else:
            print("❌ 无法提取净值趋势数据")
            
        # 查找所有可能的净值相关变量
        print("\n=== 查找净值相关变量 ===")
        nav_patterns = [
            r'var\s+(\w+)\s*=\s*([\d.]+);',
            r'var\s+(\w+)\s*=\s*"([\d.]+)";'
        ]
        
        for pattern in nav_patterns:
            matches = re.findall(pattern, content)
            if matches:
                print(f"找到 {len(matches)} 个数值变量")
                for var_name, value in matches[:10]:  # 只显示前10个
                    if 'nav' in var_name.lower() or 'value' in var_name.lower() or 'price' in var_name.lower():
                        print(f"  {var_name}: {value}")

except Exception as e:
    print(f"❌ 请求失败: {e}")
