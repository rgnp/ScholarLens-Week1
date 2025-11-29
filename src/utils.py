import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
from openai import OpenAI
import nest_asyncio

# 1. 加载环境变量 (自动读取 .env)
load_dotenv()

# 解决 Jupyter/Streamlit 异步循环冲突的补丁
nest_asyncio.apply()

def get_api_key(key_name):
    """安全地获取 API Key"""
    key = os.getenv(key_name)
    if not key:
        raise ValueError(f"❌ 找不到 {key_name}，请检查 .env 文件！")
    return key

def parse_pdf(file_path):
    """
    【API 调用 1】使用 LlamaParse 解析 PDF
    """
    print(f"[Log] 正在调用 LlamaParse 解析: {file_path}...")
    
    parser = LlamaParse(
        api_key=get_api_key("LLAMA_CLOUD_API_KEY"),
        result_type="markdown", 
        verbose=True,
        language="en", 
    )
    
    # 获取文档列表 (这里可能包含多个 Document 对象，例如一页一个)
    documents = parser.load_data(file_path)
    
    if not documents:
        raise ValueError("LlamaParse 解析失败，返回了空结果。")
    
    # --- 🔥 核心修复开始 ---
    # 旧代码：return documents[0].text  <-- 只取了第一页
    
    # 新代码：使用列表推导式，把所有页面的 text 提取出来，用换行符拼在一起
    full_text = "\n\n".join([doc.text for doc in documents])
    # --- 核心修复结束 ---

    print(f"[Log] 解析成功，共提取了 {len(full_text)} 个字符。")
    return full_text

def chat_with_ai(context, question):
    """
    【API 调用 2】调用 DeepSeek 回答问题
    输入：文章内容(context), 用户问题(question)
    输出：AI 的回答字符串
    """
    client = OpenAI(
        api_key=get_api_key("DEEPSEEK_API_KEY"),
        base_url=os.getenv("DEEPSEEK_BASE_URL")
    )

    # 提示词工程 (Prompt Engineering)
    # 我们把从 PDF 解析出来的很长的文本，塞进 'system' 或者 'user' 的上下文中
    system_prompt = "你是一个专业的学术助手。请根据用户提供的论文内容回答问题。如果不知道，就说不知道。"
    
    user_prompt = f"""
    【论文内容开始】
    {context[:30000]} 
    【论文内容结束】
    
    (注意：为了防止超长，上面只截取了前30000字符。实际生产中需要用 RAG 切片，但在 Week1 我们先做简单的上下文填充)

    用户问题：{question}
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1 # 学术问题需要严谨，温度调低
    )
    
    return response.choices[0].message.content