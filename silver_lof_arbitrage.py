import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import re

# 尝试导入requests库
requests_available = False
try:
    import requests
    requests_available = True
except ImportError:
    st.error("❌ 缺少requests库，无法获取实时数据")
    st.write("请运行 `pip install requests` 安装依赖库")

st.set_page_config(page_title="白银LOF套利分析", layout="wide")
st.title("⚪ 乡下秋草白银套利-稳稳的幸福")
st.markdown("---")
# --- 第一部分：关键概念解释 ---
with st.expander("📚 什么是白银LOF套利？", expanded=True):
    st.markdown("""
    **套利核心**：利用LOF基金**场内交易价格**与**基金净值**之间的价差进行交易。
    - **基金净值**：基金持有的白银期货合约的实际价值，随国际银价波动。
    - **场内价格**：在证券交易所像股票一样买卖的价格，受市场情绪和供求影响。
    - **溢价率**：`(场内价格 - 基金净值) / 基金净值 * 100%`，是衡量套利空间的关键指标。
    **基本操作**：当出现高溢价时，理论上可在场外按净值申购基金，然后在场内以更高价格卖出。
    **请注意**：此操作涉及T+2交割、手续费和市场波动风险，高溢价可能快速回落。
    """)
# --- 第二部分：基本操作流程---
with st.expander("📚 如何进行交易？", expanded=True):
 st.markdown("""
    **交易流程**：选择你的券商软件，例如，东方财富或光大证券。
    - 点击【交易】
    - 点击【场内基金lof】
    - 点击【申购】
    - 输入基金代码：161226-国投白银lof
    - 输入申购数量：XX（单位：份）
    - 点击【确认】  
    **请注意**：因套利交易火热，基金会对申购数额做限制，例如只能购买100份或500份。
    """)


def get_fund_net_value_direct(fund_code="161226"):
    """
    直接请求东方财富接口获取基金净值
    """
    if not requests_available:
        st.write("❌ requests库不可用，无法获取基金净值")
        return None, None, None
        
    try:
        # 使用天天基金网API替代东方财富
        url = f"http://fund.eastmoney.com/pingzhongdata/{fund_code}.js"
        # 添加更完整的浏览器头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'http://fund.eastmoney.com/',
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
        
        st.write(f"📡 请求天天基金网API: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        st.write(f"📥 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            st.write(f"📄 响应内容: {response.text[:100]}...")
            # 解析JavaScript变量
            content = response.text
            try:
                # 提取基金名称
                name_match = re.search(r'fund_name="([^"]+)"', content)
                if not name_match:
                    st.write("无法提取基金名称")
                    return None, None, None
                fund_name = name_match.group(1)
                
                # 提取单位净值和日期 - 从Data_netWorthTrend数组
                trend_pattern = r'var Data_netWorthTrend\s*=\s*\[([^\]]+)\]'
                trend_match = re.search(trend_pattern, content)
                if not trend_match:
                    st.write("无法提取净值趋势数据")
                    return None, None, fund_name
                
                # 从数组字符串中提取最后一个数据点
                trend_data = trend_match.group(1)
                # 查找最后一个},的位置
                last_data_point = trend_data.rsplit('},', 1)[-1].replace('}', '')
                
                # 提取x（时间戳）和y（净值）
                x_pattern = r'"x"\s*:\s*(\d+)'
                y_pattern = r'"y"\s*:\s*([\d.]+)'
                
                x_match = re.search(x_pattern, last_data_point)
                y_match = re.search(y_pattern, last_data_point)
                
                if not x_match or not y_match:
                    st.write("无法从趋势数据中提取净值和日期")
                    return None, None, fund_name
                
                # 转换时间戳为日期
                timestamp = int(x_match.group(1)) / 1000  # 毫秒转秒
                nav_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                latest_nav = float(y_match.group(1))
                
                st.write(f"✅ 成功获取基金数据: {fund_name}，净值: {latest_nav}，日期: {nav_date}")
                return latest_nav, nav_date, fund_name
            except Exception as parse_e:
                st.error(f"解析基金数据失败: {type(parse_e).__name__} - {str(parse_e)}")
                return None, None, None
        else:
            st.write(f"❌ 天天基金网API返回错误状态码: {response.status_code}")
            return None, None, None
    except Exception as e:
        st.error(f"获取基金净值失败: {type(e).__name__} - {str(e)}")
        return None, None, None

def get_realtime_price_direct(stock_code="161226"):
    """
    获取LOF基金实时行情（场内价格）
    注意：基金场内代码通常与基金代码相同，此处以新浪财经接口为例
    """
    if not requests_available:
        st.write("❌ requests库不可用，无法获取实时价格")
        return None, None
        
    try:
        # 方法1：尝试新浪财经接口（使用更完整的请求头）
        sina_url = f"https://hq.sinajs.cn/list=sz{stock_code}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://finance.sina.com.cn/',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
        
        st.write(f"📡 请求新浪财经实时行情API: {sina_url}")
        response = requests.get(sina_url, headers=headers, timeout=10)
        st.write(f"📥 新浪响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            st.write(f"📄 新浪响应内容: {response.text}")
            # 新浪返回的数据格式：var hq_str_sz161226="国投白银,2.377,2.376,...";
            content = response.text
            if len(content) > 20 and '=' in content and '"' in content:  # 检查是否有有效数据
                try:
                    data_str = content.split('"')[1]
                    data_parts = data_str.split(',')
                    st.write(f"🔍 解析后数据: {data_parts[:5]}")
                    if len(data_parts) > 1 and data_parts[1]:
                        current_price = float(data_parts[1])  # 当前价格
                        update_time = datetime.now().strftime('%H:%M:%S')
                        st.write(f"✅ 成功从新浪获取实时价格: {current_price}，时间: {update_time}")
                        return current_price, update_time
                except Exception as parse_e:
                        print(f"解析新浪数据失败: {type(parse_e).__name__} - {str(parse_e)}")
                        st.write(f"解析新浪数据失败: {type(parse_e).__name__} - {str(parse_e)}")
        
        # 方法1失败，尝试方法2：腾讯财经接口（使用指定的URL）
        tencent_url = "http://qt.gtimg.cn/q=sz161226"  # 使用用户指定的完整URL
        st.write(f"📡 请求腾讯财经实时行情API: {tencent_url}")
        response = requests.get(tencent_url, headers=headers, timeout=10)
        st.write(f"📥 腾讯响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            st.write(f"📄 腾讯响应内容: {response.text}")
            # 腾讯格式：v_sz161226="51~国投白银~2.377~...~";
            content = response.text
            if '~' in content and len(content) > 10:
                try:
                    # 提取等号后面的内容
                    data_part = content.split('=')[1].strip().strip(';').strip('"')
                    data_parts = data_part.split('~')
                    st.write(f"🔍 解析后数据: {data_parts[:5]}")
                    if len(data_parts) > 3 and data_parts[3]:
                        current_price = float(data_parts[3])
                        update_time = datetime.now().strftime('%H:%M:%S')
                        st.write(f"✅ 成功从腾讯获取实时价格: {current_price}，时间: {update_time}")
                        return current_price, update_time
                except Exception as parse_e:
                        print(f"解析腾讯数据失败: {type(parse_e).__name__} - {str(parse_e)}")
                        st.write(f"解析腾讯数据失败: {type(parse_e).__name__} - {str(parse_e)}")
        
        st.write("❌ 所有实时价格API都失败了")
        return None, None
    except Exception as e:
        st.error(f"获取实时行情失败: {type(e).__name__} - {str(e)}")
        return None, None

st.header("📊 真实数据溢价分析（直接获取版）")

# 1. 获取数据（使用不依赖akshare的新函数）
print("\n=== 开始获取数据 ===")
nav, nav_date, fund_name = get_fund_net_value_direct("161226")
print(f"基金净值获取结果: nav={nav}, nav_date={nav_date}, fund_name={fund_name}")

realtime_price, update_time = get_realtime_price_direct("161226")
print(f"实时价格获取结果: realtime_price={realtime_price}, update_time={update_time}")

# 2. 检查数据
if nav and realtime_price and fund_name:
    print(f"✅ 成功获取所有数据: 基金={fund_name}, 净值={nav}, 实时价格={realtime_price}")
    st.success(f"基金: {fund_name}")
else:
    print(f"❌ 数据获取不完整: nav={nav}, realtime_price={realtime_price}, fund_name={fund_name}")


    
# 4. 展示关键指标（保持你原有的布局）
col1, col2, col3 = st.columns(3)
if nav and realtime_price:
    # 使用真实数据计算溢价率
    premium_rate = (realtime_price - nav) / nav * 100
    col1.metric("基金净值", f"{nav:.4f}", f"更新于 {nav_date}")
    col2.metric("场内价格", f"{realtime_price:.4f}", f"更新于 {update_time}")
    col3.metric("实时溢价率", f"{premium_rate:.2f}%", delta=f"{premium_rate:.2f}%")
else:
    # 数据获取失败时，使用默认值
    default_nav = 2.1298
    default_price = 2.3770
    premium_rate = (default_price - default_nav) / default_nav * 100
    col1.metric("基金净值", f"{default_nav:.4f}", "使用默认值")
    col2.metric("场内价格", f"{default_price:.4f}", "使用默认值")
    col3.metric("实时溢价率", f"{premium_rate:.2f}%", delta=f"{premium_rate:.2f}%")
    st.warning("⚠️ 数据获取失败，使用默认值进行计算")

# 溢价率水平提示
if premium_rate > 20:
    st.warning(f"⚠️ 溢价率较高（>{20}%）。基金公司已提示风险，高溢价可能不可持续[citation:4]。")
elif premium_rate > 10:
    st.info(f"ℹ️ 溢价率超过10%，存在套利空间，但需关注市场波动风险[citation:1]。")
else:
    st.success("当前溢价率处于相对较低水平。")

# --- 第三部分：模拟历史数据与图表 ---
st.subheader("📈 历史溢价率走势（模拟）")
# 生成模拟历史数据（在实际项目中应替换为真实API数据）
date_range = pd.date_range(end=datetime.today(), periods=30, freq='D')
sim_dates = date_range.strftime('%Y-%m-%d').tolist()
# 模拟净值：围绕一个基准值轻微波动
# 使用获取到的净值或默认值作为基准
base_nav = nav if nav else 2.1298
sim_nav = [round(base_nav * (1 + (i % 7 - 3) * 0.01), 4) for i in range(30)]
# 模拟价格：在净值基础上增加一个波动的溢价
sim_price = [round(sim_nav[i] * (1 + 0.3 * (1 + 0.05 * (i % 5 - 2))), 4) for i in range(30)]
sim_premium = [round((sim_price[i] - sim_nav[i]) / sim_nav[i] * 100, 2) for i in range(30)]

sim_df = pd.DataFrame({
    '日期': sim_dates,
    '模拟净值': sim_nav,
    '模拟价格': sim_price,
    '模拟溢价率%': sim_premium
})

# 绘制双Y轴图表展示价格与溢价率
fig = go.Figure()
fig.add_trace(go.Scatter(x=sim_dates, y=sim_nav, mode='lines+markers', name='基金净值', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=sim_dates, y=sim_price, mode='lines+markers', name='场内价格', line=dict(color='red')))
fig.update_layout(title='基金净值与场内价格模拟走势', xaxis_title='日期', yaxis_title='价格（元）')
st.plotly_chart(fig, use_container_width=True)

# 绘制溢价率单独图表
fig2 = px.bar(sim_df, x='日期', y='模拟溢价率%', title='模拟历史溢价率变化')
fig2.update_layout(xaxis_title='日期', yaxis_title='溢价率 (%)')
st.plotly_chart(fig2, use_container_width=True)

# --- 第四部分：套利模拟计算器 ---
st.header("🧮 套利模拟计算器")
st.caption("注：此为简化模拟，未计入所有摩擦成本，实际结果可能不同。")

calc_col1, calc_col2 = st.columns(2)
with calc_col1:
    investment = st.number_input("投入本金（元）", min_value=100.0, value=10000.0, step=100.0)
    fee_rate = st.slider("估算手续费率 (%)", min_value=0.0, max_value=2.0, value=0.15, step=0.05) / 100

with calc_col2:
    # 假设T+2后溢价率可能的变化
    future_premium_change = st.slider("预估T+2后溢价率变化（百分点）", min_value=-30.0, max_value=10.0, value=-10.0, step=1.0)
    future_premium_rate = premium_rate + future_premium_change

# 进行套利收益计算
# 使用获取到的净值或默认值
calc_nav = nav if nav else 2.1298
shares_purchased = investment / calc_nav
cost = investment * (1 + fee_rate)
future_price = calc_nav * (1 + future_premium_rate / 100)
future_value = shares_purchased * future_price * (1 - fee_rate)
profit = future_value - investment

col_result1, col_result2, col_result3 = st.columns(3)
col_result1.metric("申购份额", f"{shares_purchased:.2f}")
col_result2.metric("未来预估卖出价", f"{future_price:.4f}")
col_result3.metric("**预估盈亏**", f"{profit:.2f} 元", delta=f"{(profit/investment*100):.2f}%")

# --- 第五部分：风险提示 ---
st.header("⚠️ 重要风险提示")
st.markdown("""
根据市场公开信息，投资白银LOF套利需特别注意以下风险[citation:1][citation:4][citation:5]：
1.  **溢价收敛风险**：高溢价是套利的前提，但也可能快速、剧烈地收窄甚至转为折价，导致亏损[citation:1]。
2.  **价格波动风险**：白银期货本身波动剧烈，基金净值会随之波动，可能吞噬价差收益[citation:5]。
3.  **流动性风险**：场内份额交易量可能有限，在快速下跌时难以卖出[citation:1]。
4.  **交易与时间成本**：套利涉及**T+2**的交割过程，期间市场可能已发生重大变化[citation:9]。同时需考虑申购费、赎回费、交易佣金等成本。
5.  **政策与限额风险**：基金管理人可能为控制溢价而**限制申购额度**（例如单日限购100元）[citation:4]，使大规模套利难以实现。
**结论**：套利并非无风险收益，尤其是对于溢价率已处于历史高位的品种，更应保持警惕[citation:5]。
""")

# 脚注
st.markdown("---")
st.caption("数据说明：本页面展示的基金净值与价格数据为模拟和示例，仅用于演示分析逻辑。实际投资请通过券商、基金公司官网或权威金融数据终端查询实时、准确的信息。")