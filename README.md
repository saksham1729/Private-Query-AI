# PrivateQuery AI: Offline Text-to-SQL Agent

An agentic AI system built with **LangChain** and **Llama 3.2** to translate natural language into optimized SQL queries. This project operates **100% offline** to ensure data privacy and zero API costs.

## 🚀 Key Features
*   **Agentic Reasoning:** Uses a self-correction loop to validate and fix SQL syntax.
*   **Local Inference:** Powered by Ollama (Llama 3.2) for privacy-first execution.
*   **Interactive UI:** Built with Streamlit for seamless data exploration.

## 🛠️ Tech Stack
*   **LLM:** Llama 3.2 (via Ollama)
*   **Orchestration:** LangChain & LangGraph
*   **Database:** SQLite
*   **Frontend:** Streamlit

## 📦 Setup
1. Clone the repo: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize the DB: `python init_db.py`
4. Run the app: `streamlit run app.py`
