# Text-to-SQL Interview - Quick Q&A Reference

## Quick Facts About the Project

| Aspect | Details |
|--------|---------|
| **Project Name** | Offline Text-to-SQL Application |
| **Purpose** | Convert natural language queries to SQL |
| **Domain** | Food Delivery Analytics |
| **Architecture** | Agent-based (Langchain) |
| **LLM** | Llama 3.2 (via Ollama - local) |
| **Frontend** | Streamlit |
| **Database** | SQLite (food_delivery.db) |
| **Language** | Python |
| **Key Libraries** | langchain, langchain-ollama, streamlit, pandas |

---

## 🎯 45-Second Elevator Pitch

"I built an offline text-to-SQL application using Langchain and Llama 3.2. The system converts natural language questions like 'Show Italian restaurants' into SQL queries, executes them against a local SQLite database, and returns formatted answers. Everything runs locally via Ollama—no API calls, no cloud dependency, fully private. The frontend is built with Streamlit for easy interaction."

---

## 📌 Most Important Concepts to Know

### 1. **SQL Agent Pattern** (40% of questions)
- What is it? AI that understands schema + generates SQL + executes queries
- How it works? LLM + database metadata + tools = SQL generation
- Why use it? Eliminates manual SQL writing

### 2. **Offline vs Cloud** (30% of questions)
- Offline = Ollama runs locally
- Advantages: Cost, privacy, no latency
- Trade-off: Requires local compute

### 3. **Database Design** (20% of questions)
- Schema: Users → Orders ← Restaurants
- Foreign keys for referential integrity
- Normalized (no redundancy)

### 4. **Tech Stack Integration** (10% of questions)
- Streamlit → Frontend
- Langchain → Orchestration
- Ollama → LLM runtime
- SQLite → Database

---

## 🔥 High-Probability Interview Questions

### Q1: "Walk me through what happens when a user asks a question"

**Answer Structure:**
1. User types query in Streamlit
2. Query sent to Langchain agent
3. Agent examines database schema
4. Llama 3.2 (via Ollama) generates SQL
5. SQL executed against SQLite
6. Results formatted and displayed

**Real Example:**
Input: "Average order value by cuisine?"
→ Agent generates: `SELECT cuisine, AVG(amount) FROM Orders JOIN Restaurants...`
→ Database returns: [{"cuisine": "Italian", "avg": 20.50}, ...]
→ Display: "Italian restaurants average $20.50"

---

### Q2: "What's the difference between your approach and just calling OpenAI API?"

**Answer:**
| Aspect | Your Approach (Ollama) | OpenAI API |
|--------|----------------------|-----------|
| Cost | Free (local) | $0.02+ per query |
| Speed | ~5-10s (local inference) | ~1-2s (cloud) |
| Privacy | 100% (local) | Data sent to OpenAI |
| Dependency | Ollama service | Internet + API key |
| Customization | Full control | Limited |
| Model Quality | Good (Llama 3.2) | Better (GPT-4) |

**Why you chose local:** Privacy, cost, no internet dependency.

---

### Q3: "How would you handle errors in SQL generation?"

**Answer:**
1. **Syntax Errors**: LLM receives error message, retries with corrected SQL
2. **Logic Errors**: Validation layer checks query safety
3. **Timeout**: Set max_iterations limit in agent
4. **Hallucinations**: Grounding with exact schema prevents most

```python
# In engine.py, you could add:
agent_executor = create_sql_agent(
    llm, 
    db=db,
    max_iterations=10,  # Prevent infinite loops
    verbose=True        # Debug visibility
)
```

---

### Q4: "Why is database.py separate from app.py?"

**Answer: Separation of Concerns**
- `app.py` = Frontend logic (Streamlit UI)
- `database.py` = Data access layer (SQL connection)
- `engine.py` = AI/Agent logic (LLM integration)

**Benefits:**
- Testable (mock database for unit tests)
- Maintainable (change DB without touching UI)
- Reusable (database.py can be imported elsewhere)

---

### Q5: "What's in auth.py? Why is it empty?"

**Answer:** 
Currently empty—this is where you'd add:
- User authentication (login/signup)
- Access control (user sees only their data)
- Session management
- Row-level security

**For production:** Implement with Flask-Login or similar.

---

### Q6: "How does Langchain's create_sql_agent work?"

**Answer:**
It creates an agent with:
- **LLM**: Decision-maker (Llama 3.2)
- **Tools**: Available actions (SQL execution, schema lookup)
- **Toolkit**: SQLDatabase toolkit with 3 tools:
  1. Query checker (validates syntax)
  2. SQL executor (runs query)
  3. Database schema inspector

**Agent Loop:**
```
Think → Choose Tool → Execute → Observe → Think → ... → Return Answer
```

Temperature=0 makes it deterministic.

---

### Q7: "What's the difference between embedding models and LLMs like Llama?"

**Answer:**
| Aspect | LLM (Llama) | Embedding Model |
|--------|------------|-----------------|
| Purpose | Generate text | Represent meaning |
| Output | Natural language | Vector (numbers) |
| Your use | SQL generation | Not used in project |
| Tokens | Many | 1 input = 1 vector |
| Speed | Slower | Very fast |

You use LLM to generate SQL, not embeddings.

---

### Q8: "What would you change for production?"

**Top Changes:**
1. **Database**: SQLite → PostgreSQL (concurrency, reliability)
2. **LLM**: Llama 3.2 → GPT-4 (accuracy)
3. **Auth**: Implement user login + row-level security
4. **Monitoring**: Add logging, error tracking (Sentry)
5. **Testing**: Unit tests, integration tests
6. **Caching**: Cache frequent queries
7. **Rate Limiting**: Prevent abuse
8. **Validation**: Whitelist allowed query patterns

---

### Q9: "How would you improve accuracy?"

**Strategies:**
1. **Few-shot prompting**: Show examples of Q→SQL pairs
2. **Fine-tuning**: Train Llama on your specific database
3. **Query validation**: Reject suspicious SQL patterns
4. **Feedback loop**: Log failed queries and improve prompts
5. **Better schema docs**: More detailed table descriptions

---

### Q10: "What's the role of 'temperature' in the LLM?"

**Answer:**
Temperature controls randomness in LLM output:
- **0**: Deterministic (always picks most likely word)
- **0.5**: Balanced
- **1.0**: Creative/random

**Your choice: 0**
- Why? SQL must be consistent and correct
- Never want random SQL generation
- E.g., "SELECT * FROM Users" not "SELECTS from users"

---

## 📊 Architecture Diagram

```
┌─────────────────────────┐
│   Streamlit Frontend    │
│  (Web UI, Input Box)    │
└──────────┬──────────────┘
           │ user_query
           ↓
┌──────────────────────────┐
│  Langchain Agent         │
│  (SQL Agent Executor)    │
└──────────┬───────────────┘
           │ question
           ├─────────────────┬──────────────┐
           │                 │              │
           ↓                 ↓              ↓
     ┌──────────┐   ┌──────────────┐  ┌────────────┐
     │Ollama    │   │Database      │  │SQL Database│
     │Llama 3.2 │   │Schema Lookup │  │Executor    │
     └────┬─────┘   └──────┬───────┘  └────┬───────┘
          │                │              │
          └────────────────┴──────────────┘
                    │
                    ↓ (SQL + Schema)
          ┌─────────────────────────┐
          │  SQLite Database        │
          │  (food_delivery.db)     │
          │  Tables: Users,         │
          │          Restaurants,   │
          │          Orders         │
          └──────────┬──────────────┘
                     │
                     ↓ (Results)
          ┌─────────────────────────┐
          │  Response Formatting    │
          │  (Natural Language)     │
          └──────────┬──────────────┘
                     │
                     ↓
          ┌─────────────────────────┐
          │  Streamlit Display      │
          │  (UI Result)            │
          └─────────────────────────┘
```

---

## 🧪 Sample Questions You Might Get Asked

### Technical Deep Dive
1. "Explain the difference between tool-calling agent type vs other types"
2. "How would you implement caching for repeated queries?"
3. "What SQL injection risks exist and how does Langchain prevent them?"
4. "How would you handle multi-table joins?"
5. "What's the worst-case performance for a query?"

### System Design
1. "Design a multi-tenant version of this system"
2. "How would you handle 1000 concurrent users?"
3. "How would you migrate from SQLite to PostgreSQL?"
4. "What monitoring would you add?"
5. "How would you handle LLM API failures?"

### Business/Product
1. "What's your go-to-market strategy?"
2. "What's your key differentiator vs existing BI tools?"
3. "How would you measure success?"
4. "What's the business model?"
5. "Who's your ideal customer?"

### Debugging/Troubleshooting
1. "The agent is generating wrong SQL—what would you check?"
2. "Queries are slow—how would you optimize?"
3. "Ollama is down—how should the system handle it?"
4. "User is confused by results—what could be wrong?"
5. "Database is growing—when should we archive?"

---

## 💻 Code Snippets to Memorize

### Agent Creation
```python
from langchain_ollama import ChatOllama
from langchain_community.agent_toolkits import create_sql_agent

llm = ChatOllama(model="llama3.2", temperature=0)
agent = create_sql_agent(llm, db=db, agent_type="tool-calling", verbose=True)
response = agent.invoke({"input": user_query})
```

### Database Connection
```python
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///food_delivery.db")
```

### Database Initialization
```python
import sqlite3

conn = sqlite3.connect('food_delivery.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
)''')
conn.commit()
```

---

## 🎯 Interview Strategy

### Before Interview
- [ ] Reread this guide 30 minutes before
- [ ] Practice your 45-second pitch
- [ ] Review sample questions
- [ ] Think of 1-2 questions to ask them

### During Interview
- [ ] Start with elevator pitch
- [ ] Use examples (Users, Restaurants, Orders tables)
- [ ] Draw diagrams if asked about architecture
- [ ] Ask clarifying questions before diving in
- [ ] Admit when you don't know something

### After Interview
- [ ] Send thank-you email within 24 hours
- [ ] Mention specific technical discussion points
- [ ] Reiterate interest in the role

---

## 📞 Questions to Ask Them

1. "What does a typical development cycle look like here?"
2. "What's your tech stack and why did you choose it?"
3. "What's the biggest technical challenge your team faces?"
4. "How do you handle production incidents?"
5. "What's the team structure and who would I work with?"

---

**Good luck with your interview! 🚀**
