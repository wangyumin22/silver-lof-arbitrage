import streamlit as st
# markdown
st.markdown('LOF基金套利')

# 设置网页标题
st.title('白银lof基金')

# 展示一级标题
st.header('1. 买入')

st.text('买入场内LOF基金份额')
code1 = '''场内基金LOF-申购-输入基金代码-161226'''
st.code(code1, language='bash')


# 展示一级标题
st.header('2. 卖出')


# 纯文本
st.text('卖出溢价的场外交易白银')

# 展示代码，有高亮效果
code2 = '''T+2日后选择卖出'''
st.code(code2, language='python')

text = st.text_input("查询你想套利的基金")

st.write(text)


col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")
