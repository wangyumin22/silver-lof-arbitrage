# -*- coding: utf-8 -*-
"""
直接测试API响应
"""
import requests
import json
from datetime import datetime

def test_eastmoney_api():
    print("=== 测试东方财富基金API ===")
    fund_code = "161226"
    url = "https://fundgz.1234567.com.cn/js/{}.js".format(fund_code)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://fund.eastmoney.com/'
    }
    
    try:
        print("请求URL:", url)
        response = requests.get(url, headers=headers, timeout=10)
        print("响应状态码:", response.status_code)
        print("响应内容:", response.text)
        
        if response.status_code == 200:
            # 移除函数包装，提取JSON字符串
            if response.text.startswith("jsonpgz(") and response.text.endswith(");"):
                json_str = response.text.replace("jsonpgz(", "").replace(");", "")
                data = json.loads(json_str)
                print("解析后的JSON:", data)
                return True
            else:
                print("响应格式不符合预期")
                return False
        else:
            print("API返回错误状态码")
            return False
    except Exception as e:
        print("错误:", type(e).__name__, "-", str(e))
        return False

def test_sina_api():
    print("\n=== 测试新浪财经API ===")
    stock_code = "161226"
    url = "https://hq.sinajs.cn/list=sz{}".format(stock_code)
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        print("请求URL:", url)
        response = requests.get(url, headers=headers, timeout=10)
        print("响应状态码:", response.status_code)
        print("响应内容:", response.text)
        
        if response.status_code == 200 and len(response.text) > 20:
            return True
        else:
            return False
    except Exception as e:
        print("错误:", type(e).__name__, "-", str(e))
        return False

def test_tencent_api():
    print("\n=== 测试腾讯财经API ===")
    stock_code = "161226"
    url = "http://qt.gtimg.cn/q=s_{}".format(stock_code)
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        print("请求URL:", url)
        response = requests.get(url, headers=headers, timeout=10)
        print("响应状态码:", response.status_code)
        print("响应内容:", response.text)
        
        if response.status_code == 200 and '~' in response.text:
            return True
        else:
            return False
    except Exception as e:
        print("错误:", type(e).__name__, "-", str(e))
        return False

if __name__ == "__main__":
    print("测试API可用性...\n")
    
    eastmoney_ok = test_eastmoney_api()
    sina_ok = test_sina_api()
    tencent_ok = test_tencent_api()
    
    print("\n=== 测试结果 ===")
    print("东方财富基金API:", "✅ 可用" if eastmoney_ok else "❌ 不可用")
    print("新浪财经API:", "✅ 可用" if sina_ok else "❌ 不可用")
    print("腾讯财经API:", "✅ 可用" if tencent_ok else "❌ 不可用")
