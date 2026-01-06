# -*- coding: utf-8 -*-
import requests
import json
from datetime import datetime

# 测试东方财富基金净值API
def test_eastmoney_api():
    print("=== 测试东方财富基金净值API ===")
    try:
        url = "https://fundgz.1234567.com.cn/js/161226.js"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://fund.eastmoney.com/'
        }
        
        print("请求URL: %s" % url)
        response = requests.get(url, headers=headers, timeout=10, verify=False)  # 添加verify=False绕过SSL验证
        print("响应状态码: %s" % response.status_code)
        print("响应内容: %s" % response.text)
        
        if response.status_code == 200:
            json_str = response.text.replace("jsonpgz(", "").replace(");", "")
            data = json.loads(json_str)
            print("解析结果: %s" % data)
            return True
        else:
            return False
    except Exception as e:
        print("错误: %s - %s" % (type(e).__name__, str(e)))
        return False

# 测试新浪财经API
def test_sina_api():
    print("\n=== 测试新浪财经API ===")
    try:
        url = "https://hq.sinajs.cn/list=sz161226"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        print("请求URL: %s" % url)
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        print("响应状态码: %s" % response.status_code)
        print("响应内容: %s" % response.text)
        
        if response.status_code == 200:
            content = response.text
            if len(content) > 20:
                data_str = content.split('"')[1]
                data_parts = data_str.split(',')
                print("解析结果: %s" % data_parts)
                return True
        return False
    except Exception as e:
        print("错误: %s - %s" % (type(e).__name__, str(e)))
        return False

# 测试腾讯财经API
def test_tencent_api():
    print("\n=== 测试腾讯财经API ===")
    try:
        url = "http://qt.gtimg.cn/q=s_161226"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        print("请求URL: %s" % url)
        response = requests.get(url, headers=headers, timeout=10)
        print("响应状态码: %s" % response.status_code)
        print("响应内容: %s" % response.text)
        
        if response.status_code == 200:
            content = response.text
            if '~' in content:
                data_parts = content.split('~')
                print("解析结果: %s" % data_parts)
                return True
        return False
    except Exception as e:
        print("错误: %s - %s" % (type(e).__name__, str(e)))
        return False

# 主函数
if __name__ == "__main__":
    print("API连接测试开始...")
    
    eastmoney_success = test_eastmoney_api()
    sina_success = test_sina_api()
    tencent_success = test_tencent_api()
    
    print("\n=== 测试结果汇总 ===")
    print("东方财富API: %s" % ("成功" if eastmoney_success else "失败"))
    print("新浪财经API: %s" % ("成功" if sina_success else "失败"))
    print("腾讯财经API: %s" % ("成功" if tencent_success else "失败"))
