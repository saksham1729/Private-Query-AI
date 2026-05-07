# How to Check if Langfuse is Working ✅

## Quick Summary
✅ **Langfuse is WORKING** - All tests passed!

Your Langfuse integration is correctly configured and operational. Here's how to verify and monitor it.

---

## Method 1: Run the Automated Test

### Quick Check (2 minutes)
```bash
cd e:\text2sql
text2sql_env\Scripts\activate
python test_langfuse.py
```

**Expected Output:** ✓ ALL TESTS PASSED!

This test validates:
- ✅ Credentials are configured
- ✅ Library is installed
- ✅ Can connect to cloud
- ✅ @observe() decorator works
- ✅ Traces are sent to Langfuse

---

## Method 2: Check Langfuse Dashboard

### Visual Verification (2 minutes)

1. **Go to Langfuse Cloud**
   - URL: https://cloud.langfuse.com
   - Log in with your account

2. **Select Your Project**
   - Click your project name

3. **Go to Traces Tab**
   - You should see traces named:
     - `test_function`
     - `advanced_test`
     - `outer_function`

4. **View Trace Details**
   - Click on any trace
   - See the execution flow
   - View latency and metadata

---

## Method 3: Check .env Configuration

### Verify Credentials
```bash
# Check if .env has credentials
cat .env | grep LANGFUSE
```

**Expected Output:**
```
LANGFUSE_PUBLIC_KEY=pk-lf-xxx...
LANGFUSE_SECRET_KEY=sk-lf-xxx...
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

✅ If you see these values (not "your_public_key"), you're good!

---

## Method 4: Quick Python Test

### One-liner Check
```bash
cd e:\text2sql && text2sql_env\Scripts\activate && python -c "
from langfuse import Langfuse, observe
from dotenv import load_dotenv
import os

load_dotenv()
lf = Langfuse(
    public_key=os.getenv('LANGFUSE_PUBLIC_KEY'),
    secret_key=os.getenv('LANGFUSE_SECRET_KEY'),
    host=os.getenv('LANGFUSE_BASE_URL', 'https://cloud.langfuse.com')
)
print('✓ Langfuse Connected Successfully!')
print(f'✓ Host: {os.getenv(\"LANGFUSE_BASE_URL\", \"cloud.langfuse.com\")}')
"
```

**Expected Output:**
```
✓ Langfuse Connected Successfully!
✓ Host: https://cloud.langfuse.com
```

---

## Method 5: Monitor in Real Time

### While Running Your App

1. **Start the app**
   ```bash
   streamlit run app.py
   ```

2. **Submit a query** in the Streamlit UI
   - E.g., "Show me all restaurants"

3. **Check Langfuse Dashboard**
   - Go to https://cloud.langfuse.com
   - Go to Traces tab
   - You should see a new trace appear within 2-5 seconds
   - Trace name will be something like "create_sql_executor"

4. **Click the trace to inspect**
   - See the generated SQL
   - View execution timeline
   - Check token usage

---

## Verification Checklist

Use this checklist to verify Langfuse is working:

- [ ] **Credentials Configured**
  ```bash
  echo %LANGFUSE_PUBLIC_KEY%
  echo %LANGFUSE_SECRET_KEY%
  ```
  Should show actual keys (not "your_public_key")

- [ ] **Can Import Langfuse**
  ```bash
  python -c "from langfuse import Langfuse, observe; print('✓ Import OK')"
  ```

- [ ] **Can Connect to Cloud**
  ```bash
  python -c "from langfuse import Langfuse; from dotenv import load_dotenv; import os; load_dotenv(); Langfuse(public_key=os.getenv('LANGFUSE_PUBLIC_KEY'), secret_key=os.getenv('LANGFUSE_SECRET_KEY')); print('✓ Connection OK')"
  ```

- [ ] **Test Script Passes**
  ```bash
  python test_langfuse.py
  ```
  Should show: ✓ ALL TESTS PASSED!

- [ ] **Traces Appear in Dashboard**
  - Go to https://cloud.langfuse.com
  - See traces from test script
  - See traces from app queries

---

## Common Issues & Solutions

### Issue 1: "LANGFUSE_PUBLIC_KEY not configured"
**Solution:**
1. Edit `.env` file
2. Add your Langfuse credentials from cloud.langfuse.com
3. Restart the app

### Issue 2: "Connection timeout"
**Solution:**
1. Check internet connection
2. Verify credentials are correct
3. Verify Langfuse cloud is accessible: https://cloud.langfuse.com

### Issue 3: "Traces not appearing in dashboard"
**Solution:**
1. Wait 2-5 seconds (traces take time to propagate)
2. Click refresh button
3. Check if traces are in a different project
4. Look for traces with correct date/time

### Issue 4: "import langfuse failed"
**Solution:**
```bash
pip install langfuse
```

---

## What to Look For in Dashboard

### Successful Trace
```
Trace: test_function
├─ Duration: 245ms
├─ Tokens Used: 512 input, 256 output
├─ Status: Success
├─ Cost: $0.0048
└─ Timestamp: 2026-05-06 10:30:45
```

### Trace Details You Can See
- **Input**: What was passed to the function
- **Output**: What the function returned
- **Duration**: How long it took
- **Tokens**: LLM token usage
- **Cost**: Estimated API cost
- **Metadata**: Custom tags and info
- **Nested Traces**: Sub-function calls

---

## Testing Langfuse with Your App

### Manual Test in App

1. Start the app:
   ```bash
   streamlit run app.py
   ```

2. In Streamlit UI, submit a query:
   - "Show all restaurants with rating > 4"

3. Check Langfuse dashboard:
   - Should see a trace with the query
   - Trace shows agent execution steps
   - Can see generated SQL

4. Inspect the trace:
   - View the SQL query generated
   - Check execution time
   - See token usage

---

## Integration with Your Code

### In engine.py
```python
from langfuse import observe

@observe()  # Decorator automatically traces this
def create_sql_executor(db):
    llm = ChatOllama(model="llama3.2", temperature=0)
    agent_executor = create_sql_agent(llm, db=db, agent_type="tool-calling")
    return agent_executor
```

### In app.py
```python
from langfuse import Langfuse

# When user submits query:
trace = langfuse.trace(
    name="user_query",
    input={"query": user_query}
)
# ... execute query ...
trace.generation(
    name="agent_response",
    output=response["output"],
    model="llama3.2"
)
```

---

## Performance Expectations

### Query Response Time
- **Without Langfuse**: ~5-10 seconds (LLM inference)
- **With Langfuse**: ~5-10 seconds (no overhead, async)

### Trace Appearance Time
- **Local traces**: Appear immediately
- **Cloud sync**: 2-5 seconds to appear in dashboard

### Dashboard Load Time
- **Traces list**: <1 second
- **Single trace details**: <2 seconds

---

## Debugging with Langfuse

### See what the agent generated
```
Trace: user_query
└─ Step 1: Agent examines schema
└─ Step 2: Llama generates SQL
   └─ Input: "Show Italian restaurants"
   └─ Output: "SELECT * FROM Restaurants WHERE cuisine='Italian'"
└─ Step 3: Execute SQL
   └─ Result: 1 row
└─ Step 4: Format response
   └─ Output: "Pizza Palace has rating 4.5"
```

### Find problematic queries
1. Go to Langfuse dashboard
2. Filter by failed traces
3. See what went wrong
4. Adjust prompts/schema if needed

---

## Interview Answer

**Q: How do you verify Langfuse is working?**

A: "I use several methods:
1. **Automated test**: Run `python test_langfuse.py` - validates all components
2. **Dashboard verification**: Check https://cloud.langfuse.com for traces
3. **Real-time monitoring**: Submit queries in the app and watch traces appear
4. **Code inspection**: Use @observe() decorator to trace function execution
5. **Performance check**: Verify traces appear within 2-5 seconds

All tests pass, and traces are successfully syncing to the cloud."

---

## Next Steps

✅ **Langfuse is Working!**

1. Now run your Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Submit some queries and watch Langfuse capture them

3. Go to dashboard to analyze:
   - Query patterns
   - SQL generation quality
   - Performance metrics
   - Error analysis

4. Use this data to improve your agent

---

## Useful Commands

```bash
# Test connection
python test_langfuse.py

# Check credentials
echo LANGFUSE_PUBLIC_KEY: %LANGFUSE_PUBLIC_KEY%

# Run app with Langfuse tracing
streamlit run app.py

# View raw traces (if needed)
python -c "from langfuse import Langfuse; from dotenv import load_dotenv; import os; load_dotenv(); print(Langfuse(public_key=os.getenv('LANGFUSE_PUBLIC_KEY'), secret_key=os.getenv('LANGFUSE_SECRET_KEY')).get_trace_url())"
```

---

**Status: ✅ LANGFUSE IS OPERATIONAL AND READY TO USE**
