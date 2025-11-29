import streamlit as st
import tempfile
import os
from utils import parse_pdf, chat_with_ai # 导入我们刚才写的函数

# 页面配置
st.set_page_config(page_title="ScholarLens v1.0", layout="wide")
st.title("🎓 ScholarLens: 智能论文阅读器")
st.caption("Week 1 Project: Built with LlamaParse & DeepSeek")

# 初始化 Session State (用来存解析好的文本，防止每次刷新都重新解析)
if "parsed_content" not in st.session_state:
    st.session_state.parsed_content = ""

# --- 侧边栏：上传区 ---
with st.sidebar:
    st.header("📄 上传论文")
    uploaded_file = st.file_uploader("选择 PDF 文件", type=["pdf"])
    
    if uploaded_file and not st.session_state.parsed_content:
        if st.button("开始解析"):
            with st.spinner("正在请求 LlamaCloud 进行深度解析... (可能需要十几秒)"):
                # 1. 保存临时文件
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                # 2. 调用我们在 utils 里写的函数
                try:
                    text = parse_pdf(tmp_path)
                    st.session_state.parsed_content = text
                    st.success("解析成功！")
                except Exception as e:
                    st.error(f"解析失败: {e}")
                
                # 3. 清理垃圾
                os.remove(tmp_path)

# --- 主界面：展示与问答 ---
if st.session_state.parsed_content:
    # 创建两列布局
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 解析结果预览 (Markdown)")
        # 放入一个滚动框查看原文
        st.text_area("原文内容", st.session_state.parsed_content, height=600)
        
    with col2:
        st.subheader("💬 AI 问答")
        # 简单的聊天界面
        user_query = st.text_input("向论文提问 (例如：这篇论文的核心创新点是什么？)")
        
        if st.button("发送") and user_query:
            with st.spinner("AI 正在思考..."):
                answer = chat_with_ai(st.session_state.parsed_content, user_query)
                st.markdown("### 🤖 回答")
                st.write(answer)

else:
    st.info("👈 请先在左侧上传 PDF 并点击解析")