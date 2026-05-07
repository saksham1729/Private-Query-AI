# Text-to-SQL Project - Interview Preparation Guide

## 📋 Project Overview

### What is this project?
This is an **Offline Text-to-SQL Application** that converts natural language queries into SQL queries and executes them against a local SQLite database. The project uses:
- **Langchain** for orchestration
- **Ollama** for running local LLMs
- **Llama 3.2** as the AI model
- **Streamlit** as the web UI
- **SQLite** as the database

### Real-world Use Case
A **Food Delivery Analytics System** where users can ask questions in plain English (e.g., "Which restaurant has the highest rating?") and get SQL-generated answers without calling external APIs.

---

## 🎯 Architecture & Components

### 1. **Streamlit Frontend** (`app.py`)
#### What is Streamlit?
- A Python library for building data web apps quickly without frontend expertise
- Perfect for ML/AI demos, analytics dashboards, and prototypes
- Hot-reloading: changes auto-refresh in the browser

#### How does it work in this project?
```python
st.set_page_config(page_title="Offline Text-2-SQL", page_icon="🍔")
st.title("Local Food Delivery Analytics")
```
- Sets up the page title and icon
- Creates the UI title

#### Key Features Used:
1. **`st.text_input()`** - Accepts user queries
2. **`st.spinner()`** - Shows a loading indicator
3. **`st.subheader()` & `st.write()`** - Display results
4. **`st.error()`** - Error messages
5. **`st.sidebar`** - Side panel for system status
6. **`st.success()` & `st.info()`** - Status indicators

### 2. **Database Layer** (`database.py`)
#### SQLDatabase from Langchain
```python
from langchain_community.utilities import SQLDatabase
return SQLDatabase.from_uri("sqlite:///food_delivery.db")
```

**What does this do?**
- Creates a wrapper around SQLite database for Langchain integration
- Allows the agent to understand and interact with the database schema
- `SQLDatabase` is a **bridge** between Langchain and SQL databases

#### Why not use raw sqlite3?
- Langchain's `SQLDatabase` provides:
  - Schema introspection (agent understands tables/columns)
  - Safe execution context
  - Integration with the agent toolkit

### 3. **Database Initialization** (`init_db.py`)
#### Schema Design (Star Schema)
```
Users (1) ──┐
            ├──> Orders (Many)
Restaurants (1) ──┘
```

**Tables:**
1. **Users** - Customer information (user_id, name, email, join_date)
2. **Restaurants** - Restaurant details (restaurant_id, name, cuisine, rating)
3. **Orders** - Order records (order_id, user_id, restaurant_id, amount, order_date)
   - Contains **foreign keys** to maintain referential integrity

#### SQL Concept - FOREIGN KEYS
Foreign keys ensure data consistency. If you delete a user, orders linked to that user should be handled appropriately.

### 4. **SQL Agent Engine** (`engine.py`)
#### What is a SQL Agent?
A SQL agent is an AI component that:
1. **Understands natural language** (via LLM)
2. **Understands database schema** (via SQLDatabase)
3. **Generates correct SQL** based on the question
4. **Executes SQL** and interprets results
5. **Returns human-readable answers**

#### How does it work?
```python
llm = ChatOllama(model="llama3.2", temperature=0)
agent_executor = create_sql_agent(
    llm, 
    db=db, 
    agent_type="tool-calling",
    verbose=True
)
```

**Agent Execution Flow:**
1. User asks: "Which restaurants have rating > 4?"
2. Agent examines database schema
3. Agent generates: `SELECT * FROM Restaurants WHERE rating > 4.0`
4. Agent executes the query
5. Agent formats the result: "Pizza Palace (Rating: 4.5)"

---

## 🤖 Technologies Deep Dive

### **1. Langchain Framework**
#### What is Langchain?
A framework for developing applications powered by language models. It provides:
- **Agents** - AI systems that can use tools
- **Chains** - Sequences of operations
- **Tools** - Functions the LLM can call (like SQL execution)
- **Memory** - Context management
- **Integrations** - Connectors to various LLMs and databases

#### Why use Langchain instead of calling LLM directly?
- **Direct approach**: Ask LLM → Get text → Parse text → Execute SQL (error-prone)
- **Langchain approach**: Framework handles error handling, retries, tool use, validation

#### Key Concepts in Our Project:
1. **SQLDatabase** - Database abstraction layer
2. **create_sql_agent** - Factory function that creates an agent configured for SQL
3. **Tool-calling agent type** - Agent that decides which tools to use based on the query

### **2. Ollama - Local LLM Runtime**
#### What is Ollama?
A tool that lets you run large language models **locally** without cloud/API calls.

#### Why not use OpenAI/Cloud APIs?
✅ **Advantages of Ollama:**
- No API costs
- Data privacy (runs locally)
- No internet dependency
- Works offline
- Full control

❌ **Trade-offs:**
- Requires local compute power
- Slower inference (CPU-based usually)
- Model quality varies by model size

#### Llama 3.2 in this project
```python
llm = ChatOllama(model="llama3.2", temperature=0)
```

**Configuration:**
- **Model**: llama3.2 (8B parameters)
- **Temperature**: 0 (deterministic, no randomness)
  - 0 = Always same answer
  - 1.0 = Creative/random answers
  - For SQL tasks, we want 0 (consistent, predictable)

#### How to use Ollama:
1. Install Ollama from ollama.ai
2. Run: `ollama run llama3.2`
3. Ollama runs a local server (default: localhost:11434)

### **3. SQLite Database**
#### What is SQLite?
- Lightweight, file-based SQL database
- No server needed (unlike MySQL/PostgreSQL)
- Perfect for local development and embedded systems
- Stores everything in a single `.db` file

#### In this project:
- Database file: `food_delivery.db`
- Tables: Users, Restaurants, Orders
- No external database server needed

#### SQL Concepts Used:
1. **CREATE TABLE** - Define table structure
2. **PRIMARY KEY** - Unique identifier for each row
3. **FOREIGN KEY** - References to other tables
4. **INSERT** - Add data
5. **SELECT** (generated by agent) - Query data

### **4. Python-dotenv**
#### What is it?
Loads environment variables from `.env` file into Python.

#### Usage in this project:
```
# In .env file:
OPENAI_API_KEY="sk-proj-..."
DATABRICKS_TOKEN="..."
```

#### Why?
- Keep secrets out of code
- Easy configuration per environment (dev/prod)
- Avoid exposing API keys in version control

### **5. Pandas**
While imported in requirements.txt, used for:
- Data manipulation and analysis
- Converting SQL results to DataFrames
- Easy display in Streamlit

---

## 🔄 Complete Query Flow

### Example: "Show me all restaurants with Italian cuisine"

```
1. User Input (Streamlit)
   ↓
   "Show me all restaurants with Italian cuisine"
   
2. Agent Receives Query
   ↓
   Agent examines Restaurants schema
   
3. LLM Reasoning (Llama 3.2)
   ↓
   "The user wants restaurants with Italian cuisine
    I should SELECT * FROM Restaurants WHERE cuisine = 'Italian'"
   
4. SQL Generation
   ↓
   Generated SQL: SELECT * FROM Restaurants WHERE cuisine = 'Italian'
   
5. Execution (SQLDatabase)
   ↓
   Execute query against food_delivery.db
   
6. Result Processing
   ↓
   [
     {"restaurant_id": 101, "name": "Pizza Palace", "cuisine": "Italian", "rating": 4.5}
   ]
   
7. Response Formatting
   ↓
   "I found 1 Italian restaurant: Pizza Palace with rating 4.5"
   
8. Display (Streamlit)
   ↓
   Shows result in UI
```

---

## 📊 Database Schema

### Users Table
| Column | Type | Purpose |
|--------|------|---------|
| user_id | INTEGER PRIMARY KEY | Unique identifier |
| name | TEXT | Customer name |
| email | TEXT | Contact email |
| join_date | DATE | When they joined |

### Restaurants Table
| Column | Type | Purpose |
|--------|------|---------|
| restaurant_id | INTEGER PRIMARY KEY | Unique identifier |
| name | TEXT | Restaurant name |
| cuisine | TEXT | Type of cuisine |
| rating | REAL | 5-star rating |

### Orders Table
| Column | Type | Purpose |
|--------|------|---------|
| order_id | INTEGER PRIMARY KEY | Unique identifier |
| user_id | INTEGER FK | Links to Users |
| restaurant_id | INTEGER FK | Links to Restaurants |
| amount | REAL | Order total |
| order_date | DATE | When ordered |

### Sample Queries
```sql
-- Get all orders from Italian restaurants
SELECT o.order_id, u.name, r.name 
FROM Orders o
JOIN Users u ON o.user_id = u.user_id
JOIN Restaurants r ON o.restaurant_id = r.restaurant_id
WHERE r.cuisine = 'Italian'

-- Average order amount by cuisine
SELECT r.cuisine, AVG(o.amount) as avg_amount
FROM Orders o
JOIN Restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.cuisine
```

---

## 🚀 Execution Setup

### Prerequisites
1. **Python 3.9+** installed
2. **Ollama** installed and running
3. **Llama 3.2 model** downloaded in Ollama

### Installation
```bash
# Create virtual environment
python -m venv text2sql_env

# Activate it
text2sql_env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run the app
streamlit run app.py
```

---

## ❓ Common Interview Questions

### Architecture & Design
**Q: Why is this architecture called "offline"?**
A: Because everything runs locally without external API calls. The LLM (Llama) runs via Ollama locally, the database (SQLite) is local, and no cloud services are needed.

**Q: What would you change to make this production-ready?**
A: 
- Use PostgreSQL instead of SQLite for concurrency
- Add authentication (currently auth.py is empty)
- Add error handling and logging
- Implement rate limiting
- Use cloud LLM (OpenAI) for better accuracy
- Add query caching
- Implement audit logging for SQL queries

**Q: How does the SQL agent handle incorrect queries?**
A: 
1. If SQL is syntactically wrong, the execution fails
2. Agent catches the error and retries with corrected SQL
3. The LLM learns from the error message

**Q: Why temperature=0 for the LLM?**
A: SQL generation must be deterministic. Temperature=0 means the LLM always chooses the most likely token, producing consistent SQL.

### LLM & AI
**Q: What are hallucinations in LLMs and how do you prevent them?**
A: Hallucinations are when LLMs generate false information. Prevention:
- Provide schema information to ground the model
- Use temperature=0 for deterministic output
- Validate SQL before execution
- Use smaller, fine-tuned models

**Q: How does prompt engineering work in SQL agents?**
A: The system prompt tells Llama:
"You have access to a database with tables: Users, Restaurants, Orders. Convert natural language to SQL."

**Q: Why not use GPT-4 instead of Llama?**
A:
- Cost (OpenAI API calls add up)
- Privacy (data stays local)
- Speed (no network latency)
- Control (no vendor lock-in)

### Database
**Q: What are the risks of auto-generated SQL?**
A:
- SQL injection (though Langchain prevents this)
- Performance issues (N+1 queries)
- Missing indexes
- Incorrect business logic interpretation

**Q: How would you add security?**
A:
- Input validation
- Query whitelisting (only allow certain query patterns)
- Row-level security (users see only their own data)
- Audit logging

### Streamlit
**Q: Why Streamlit instead of Flask/Django?**
A:
- Rapid prototyping (less boilerplate)
- Perfect for ML/AI demos
- Built-in caching and interactivity
- Great for non-web developers

**Q: What are Streamlit's limitations?**
A:
- Reruns entire script on each interaction
- Not ideal for complex user interfaces
- Performance issues with large datasets
- Not suitable for multi-user real-time apps

---

## 🔧 Potential Improvements

### 1. **Multi-turn Conversation**
Currently, each query is independent. Add conversation history:
```python
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
```

### 2. **Query Validation**
Before execution:
```python
# Only allow SELECT queries
if not query.upper().strip().startswith("SELECT"):
    raise ValueError("Only SELECT queries allowed")
```

### 3. **Caching Results**
```python
@st.cache_data
def execute_query(sql_query):
    return agent.invoke({"input": sql_query})
```

### 4. **Enhanced Error Handling**
```python
try:
    response = agent.invoke({"input": user_query})
except ValueError as e:
    st.error(f"Schema Error: {e}")
except TimeoutError:
    st.error("Query timeout - try a simpler question")
```

### 5. **Query Explanation**
Show the generated SQL to the user for transparency.

### 6. **Analytics Dashboard**
Use Streamlit columns and metrics for visual analytics:
```python
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", 2)
col2.metric("Avg Rating", 4.35)
col3.metric("Revenue", "$41.25")
```

---

## 📝 Key Takeaways for Interview

1. **End-to-end understanding**: You understand the full pipeline from UI to database
2. **Modern tech stack**: LLMs, local inference, vector databases are industry trends
3. **Practical thinking**: Aware of production challenges and solutions
4. **System design**: Understand trade-offs (local vs cloud, SQLite vs PostgreSQL)
5. **Problem-solving**: Can explain how the system handles edge cases

---

## 🎓 Further Learning Resources

- **Langchain Docs**: https://docs.langchain.com/
- **Ollama**: https://ollama.ai
- **Streamlit Docs**: https://docs.streamlit.io
- **SQLite**: https://www.sqlite.org
- **LLM Fundamentals**: https://huggingface.co/course

---

## 💡 Discussion Points for Interview

1. "How would you scale this to handle 1 million queries/day?"
2. "What happens if Ollama is unavailable - fallback strategy?"
3. "How would you ensure data security and privacy?"
4. "How would you optimize slow queries?"
5. "How would you test an LLM-based system?"
6. "What's the difference between deterministic and probabilistic outputs?"

---

**Last Updated**: May 6, 2026
**Project**: Offline Text-to-SQL with Llama 3.2 & Langchain
