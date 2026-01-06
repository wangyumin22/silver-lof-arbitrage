# 详细测试基金净值API

import requests
import re

print("=== 详细测试基金净值API ===")

# 测试天天基金网API
fund_code = "161226"
url = f"http://fund.eastmoney.com/pingzhongdata/{fund_code}.js"
print(f"\n1. 测试天天基金网API: {url}")

try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    
    print(f"   状态码: {response.status_code}")
    print(f"   响应内容长度: {len(response.text)} 字符")
    
    if response.status_code == 200:
        # 显示更多内容
        content = response.text
        print(f"   响应内容前500字符: {content[:500]}...")
        
        # 查找与净值相关的变量
        print("\n   查找与净值相关的变量:")
        lines = content.split(';')
        for line in lines[:50]:  # 查看前50行
            if 'netWorth' in line or 'Date' in line:
                print(f"   - {line.strip()}")
        
        # 尝试不同的正则表达式模式
        print("\n   尝试不同的正则表达式:")
        
        # 尝试1: 搜索所有var定义
        var_pattern = r'var\s+(\w+)\s*=\s*"?([^"]+)"?'
        matches = re.findall(var_pattern, content[:2000])
        print("   前2000字符中的变量:")
        for name, value in matches[:20]:
            print(f"   - {name}: {value}")
            
        # 尝试2: 专门查找净值相关数据
        nav_patterns = [
            r'var\s+fS_netWorth\s*=\s*"?([^"]+)"?',
            r'var\s+lastNetWorth\s*=\s*"?([^"]+)"?',
            r'var\s+netWorth\s*=\s*"?([^"]+)"?',
            r'var\s+fS_date\s*=\s*"?([^"]+)"?',
            r'var\s+lastDate\s*=\s*"?([^"]+)"?',
            r'var\s+endDate\s*=\s*"?([^"]+)"?',
        ]
        
        print("\n   尝试不同的净值数据模式:")
        for pattern in nav_patterns:
            match = re.search(pattern, content)
            if match:
                print(f"   - {pattern}: {match.group(1)}")
    else:
        print(f"   错误: {response.status_code}")
        print(f"   响应内容: {response.text}")
        
except Exception as e:
    print(f"   请求失败: {type(e).__name__} - {str(e)}")

print("\n=== 测试完成 ===")
