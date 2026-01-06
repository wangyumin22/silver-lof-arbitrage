# -*- coding: utf-8 -*-
"""
直接测试腾讯财经API是否正常工作
"""
import requests
import re

def test_tencent_api():
    print("=== 测试腾讯财经API ===")
    
    # 使用用户指定的URL
    url = "http://qt.gtimg.cn/q=sz161226"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://finance.sina.com.cn/',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }
    
    try:
        print("请求URL:", url)
        response = requests.get(url, headers=headers, timeout=10)
        print("响应状态码:", response.status_code)
        print("响应内容:", response.text)
        
        if response.status_code == 200:
            content = response.text
            if '~' in content and len(content) > 10:
                try:
                    # 提取等号后面的内容
                    data_part = content.split('=')[1].strip().strip(';').strip('"')
                    data_parts = data_part.split('~')
                    print("解析后数据:", data_parts[:10])
                    
                    if len(data_parts) > 3 and data_parts[3]:
                        current_price = float(data_parts[3])  # 当前价格
                        print("✅ 成功获取实时价格:", current_price)
                        return True
                    else:
                        print("❌ 无法从数据中提取价格")
                        return False
                except Exception as parse_e:
                    print("解析数据失败:", type(parse_e).__name__, "-", str(parse_e))
                    return False
            else:
                print("❌ 响应内容格式不正确")
                return False
        else:
            print("❌ API返回错误状态码")
            return False
    except Exception as e:
        print("请求失败:", type(e).__name__, "-", str(e))
        return False

if __name__ == "__main__":
    test_tencent_api()
