import streamlit as st
import pandas as pd
from googletrans import Translator
import os
from importlib.machinery import SourceFileLoader
import pandasai as pai

# 动态导入Agent-templete.py
agent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../architecture/Agent-templete.py"))
AgentModule = SourceFileLoader("AgentTemplete", agent_path).load_module()

translator = Translator()

# 会话状态初始化
if "history" not in st.session_state:
    st.session_state.history = []
if "imported_files" not in st.session_state:
    st.session_state.imported_files = []
if "selected_file" not in st.session_state:
    st.session_state.selected_file = None

st.set_page_config(page_title="智能数据分析平台", layout="wide")

# 侧边栏：数据管理
with st.sidebar:
    st.title("📂 数据管理")
    uploaded_files = st.file_uploader("上传CSV/Excel（可多选）", type=["csv", "xlsx"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, sheet_name=0)
            st.session_state.imported_files.append((uploaded_file.name, df))
        st.success(f"已导入 {len(st.session_state.imported_files)} 个文件。")

    if st.session_state.imported_files:
        file_names = [f[0] for f in st.session_state.imported_files]
        st.session_state.selected_file = st.selectbox("选择要预览的文件", file_names)
        for fname, df in st.session_state.imported_files:
            if fname == st.session_state.selected_file:
                st.write(f"**{fname} 预览：**")
                st.dataframe(df.head(20))
                break
    st.markdown("---")
    if st.button("清空所有文件"):
        st.session_state.imported_files = []
        st.session_state.selected_file = None

# 主区：对话与AI分析
st.title("🤖 智能数据分析平台 (AI-EDI)")
st.caption("支持多文件上传、多轮对话、中文、可视化 | 类似 [weaviate-magic-chat](https://weaviate-magic-chat.streamlit.app/)")

st.markdown("### 对话历史")
for i, (q, a) in enumerate(st.session_state.history):
    with st.chat_message("user"):
        st.markdown(f"**Q{i+1}：{q}**")
    with st.chat_message("ai"):
        st.markdown(f"**A{i+1}：{a}**")

# 选择参与AI分析的文件
if st.session_state.imported_files:
    st.markdown("#### 选择参与AI分析的数据文件")
    file_names = [f[0] for f in st.session_state.imported_files]
    mode = st.radio("请选择分析模式", ["单一表", "多表"])
    if mode == "单一表":
        selected_file = st.selectbox("选择要分析的文件", file_names)
        selected_df = next(df for fname, df in st.session_state.imported_files if fname == selected_file)
    else:
        selected_files = st.multiselect("选择要分析的文件（可多选）", file_names, default=file_names)
        selected_dfs = [df for fname, df in st.session_state.imported_files if fname in selected_files]

# 对话输入
user_query = st.chat_input("请输入你的分析请求（支持中文）")
if user_query and st.session_state.imported_files:
    en_query = translator.translate(user_query, src="zh-cn", dest="en").text
    if mode == "单一表":
        ai_output = AgentModule.ai_chat_single(en_query, selected_df)
    else:
        ai_output = AgentModule.ai_chat_multi(en_query, selected_dfs)
    zh_output = translator.translate(str(ai_output), src="en", dest="zh-cn").text
    with st.chat_message("user"):
        st.markdown(user_query)
    with st.chat_message("ai"):
        st.markdown(zh_output)

# 页脚
st.markdown("---")
st.caption("© 2024 AIEDI | Powered by Streamlit & PandasAI")