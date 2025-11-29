# 🎓 ScholarLens: Intelligent Research Assistant

ScholarLens is an AI-powered tool designed to help researchers quickly understand academic papers. It uses **LlamaParse** for high-fidelity PDF extraction and **DeepSeek-V3** for intelligent summarization and Q&A.

## 🚀 Features

- **Deep Parsing**: Extracts text from complex PDFs using LlamaParse (SOTA).
- **AI Q&A**: Chat with your paper using DeepSeek LLM.
- **Clean UI**: Built with Streamlit for a smooth user experience.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **PDF Engine**: LlamaIndex / LlamaParse
- **LLM**: DeepSeek API (OpenAI Compatible)
- **Language**: Python 3.10+

## 📦 How to Run

1. **Clone the repo**
   ```bash
   git clone [https://github.com/你的用户名/ScholarLens.git](https://github.com/你的用户名/ScholarLens.git)
   cd ScholarLens

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API Keys** Create a .env file in the root directory:
   ```
   LLAMA_API_KEY=your_llama_api_key
   DEEPSEEK_API_KEY=your_deepseek_api_key
   DEEPSEEK_BASE_URL=[https://api.deepseek.com](https://api.deepseek.com)
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

