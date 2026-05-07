# Langfuse Integration Guide

## What is Langfuse?

Langfuse is an **open-source LLM observability platform** that helps you:
- 🔍 **Monitor** LLM interactions in real-time
- 🐛 **Debug** agent behavior and trace execution steps
- 📊 **Analyze** token usage, latency, and costs
- 📈 **Track** performance metrics over time
- 🔄 **Understand** how your LLM application behaves

## Why Add Langfuse to Your Project?

### Before Langfuse
- You can only see final results
- Hidden intermediate steps
- No visibility into SQL generation process
- Difficult to debug errors
- No performance metrics

### After Langfuse
- See complete execution traces
- Inspect generated SQL queries
- Monitor token usage and latency
- Debug agent decision-making
- Track query performance over time

## Setup Instructions

### Step 1: Sign Up for Langfuse Cloud

1. Go to https://cloud.langfuse.com
2. Create a free account
3. Create a new project
4. Copy your credentials:
   - **Public Key** (Project ID)
   - **Secret Key** (API Key)

### Step 2: Update .env File

Edit `e:\text2sql\.env` and add:

```env
LANGFUSE_PUBLIC_KEY=your_public_key_here
LANGFUSE_SECRET_KEY=your_secret_key_here
LANGFUSE_HOST=https://cloud.langfuse.com
```

**Example:**
```env
LANGFUSE_PUBLIC_KEY=pk_prod_abc123def456
LANGFUSE_SECRET_KEY=sk_prod_xyz789uvw123
LANGFUSE_HOST=https://cloud.langfuse.com
```

### Step 3: Install Dependencies

```bash
# Activate your virtual environment
text2sql_env\Scripts\activate

# Install Langfuse
pip install langfuse

# Or reinstall all requirements
pip install -r requirements.txt
```

### Step 4: Run Your App

```bash
streamlit run app.py
```

When you submit a query, Langfuse will automatically capture:
- User input
- Generated SQL
- Execution time
- Token usage
- Results and errors

## What Gets Tracked?

### 1. **Traces** - Complete Execution Flow
```
Trace: user_query
├── Input: "Which restaurants have rating > 4?"
├── Model: llama3.2
├── Steps:
│   ├── Step 1: Examine schema
│   ├── Step 2: Generate SQL
│   ├── Step 3: Execute query
│   └── Step 4: Format response
└── Output: "Pizza Palace (4.5), Taco Town (4.2)"
```

### 2. **Generations** - LLM Calls
- Model used
- Tokens used (input + output)
- Latency
- Temperature setting
- Cost estimation

### 3. **Observations** - Custom Events
- Agent decisions
- Tool calls
- Errors

## Langfuse Dashboard Features

### Traces View
- See all queries processed
- Click on trace to expand details
- View exact SQL generated
- Check execution timeline

### Metrics Dashboard
- Total traces processed
- Average latency
- Error rate
- Token usage
- Cost tracking

### Model Comparison
- Compare different LLM responses
- A/B test different agents

## Code Changes Made

### 1. **requirements.txt**
Added: `langfuse`

### 2. **engine.py**
```python
from langfuse.callback import CallbackHandler

langfuse_callback = CallbackHandler(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

agent_executor = create_sql_agent(
    llm, db=db,
    callbacks=[langfuse_callback]  # Enable tracing
)
```

### 3. **app.py**
```python
# Initialize Langfuse client
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY")
)

# Create trace for each query
trace = langfuse.trace(
    name="user_query",
    input={"query": user_query}
)

# Log response
trace.generation(
    name="agent_response",
    output=response["output"],
    model="llama3.2"
)
```

### 4. **.env**
Added Langfuse configuration:
```env
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

## Example: Viewing Traces in Langfuse

### Step 1: Submit a Query
In your Streamlit app, ask: "Show me all restaurants"

### Step 2: Check Langfuse Dashboard
Go to https://cloud.langfuse.com → Your Project → Traces

### Step 3: View Trace Details
Click on the trace to see:
```
┌─ Trace: user_query
│  ├─ Input: {"query": "Show me all restaurants"}
│  ├─ Session: default
│  ├─ User: streamlit_user
│  │
│  ├─ Generation 1: Schema Lookup
│  │  ├─ Model: llama3.2
│  │  ├─ Latency: 245ms
│  │  ├─ Input Tokens: 256
│  │  └─ Output Tokens: 128
│  │
│  ├─ Generation 2: SQL Execution
│  │  ├─ Query: SELECT * FROM Restaurants
│  │  ├─ Latency: 12ms
│  │  └─ Rows: 2
│  │
│  └─ Output: "Found 2 restaurants..."
```

## Advanced Features

### 1. Custom Session IDs
```python
trace = langfuse.trace(
    name="user_query",
    session_id="user_123",  # Track sessions
    user_id="alice@example.com"
)
```

### 2. Cost Tracking
Langfuse automatically calculates:
- Input tokens × model price
- Output tokens × model price
- Total cost per trace

### 3. Filtering & Search
- Filter by user
- Filter by session
- Search by query content
- Date range filtering

### 4. Alerts & Monitoring
- Alert on high latency
- Alert on errors
- Alert on unusual token usage

## Troubleshooting

### Issue: "Langfuse: Not configured"
**Solution:** Add credentials to .env
```env
LANGFUSE_PUBLIC_KEY=your_key
LANGFUSE_SECRET_KEY=your_secret
```

### Issue: Connection timeout
**Solution:** 
1. Check internet connection
2. Verify credentials are correct
3. Check LANGFUSE_HOST setting

### Issue: No traces appearing
**Solution:**
1. Verify .env credentials are loaded
2. Check Langfuse cloud account is active
3. Look for error messages in Streamlit logs

## Performance Impact

- **Minimal overhead**: Langfuse sends data asynchronously
- **Latency impact**: <50ms per query
- **Token impact**: None (Langfuse only observes, doesn't modify)

## Cost Analysis

### Free Tier
- 1,000 traces/month
- 7-day retention
- Basic dashboard
- Perfect for development

### Pro Tier
- Unlimited traces
- 12-month retention
- Advanced analytics
- Custom integrations

For local Ollama model, focus on tracing & debugging, not costs.

## Interview Talking Points

**Q: Why did you add Langfuse?**
A: "For observability and debugging. I can see:
- Exact SQL generated
- Agent decision process
- Performance metrics
- Error patterns"

**Q: How does it help with debugging?**
A: "If a query fails, I can see:
- What schema the agent saw
- What SQL it generated
- Where it failed
- Why it failed"

**Q: What's the overhead?**
A: "Minimal. Langfuse sends data asynchronously in the background. The query latency impact is <50ms."

## Next Steps

1. ✅ Sign up at cloud.langfuse.com
2. ✅ Add credentials to .env
3. ✅ Run `pip install langfuse`
4. ✅ Start your app: `streamlit run app.py`
5. ✅ Submit some queries
6. ✅ View traces in Langfuse dashboard

## Resources

- **Langfuse Docs**: https://langfuse.com/docs
- **Langfuse Python SDK**: https://github.com/langfuse/langfuse-python
- **Langchain Integration**: https://langfuse.com/docs/sdk/python/langchain
- **Cloud Dashboard**: https://cloud.langfuse.com

---

**Benefits Summary:**
- 🔍 Full visibility into LLM behavior
- 🐛 Easy debugging and troubleshooting
- 📊 Performance monitoring
- 💰 Cost tracking
- 🔄 Usage patterns analysis
- ✨ Production-ready observability

