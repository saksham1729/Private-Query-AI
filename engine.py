import os
from langchain_ollama import ChatOllama
from langchain_community.agent_toolkits import create_sql_agent
from langfuse import observe
from dotenv import load_dotenv

load_dotenv()

# Initialize Langfuse client globally for @observe() decorator
from langfuse import Langfuse

_langfuse_client = None
if os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"):
    try:
        _langfuse_client = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_BASE_URL") or os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
        )
        print("✓ Langfuse client initialized for observability")
    except Exception as e:
        print(f"⚠ Langfuse initialization failed: {e}")
        _langfuse_client = None

@observe()
def create_sql_executor(db):
    """
    Creates a SQL agent with Langfuse observability integrated.
    
    The agent will:
    1. Look at the SQLite schema
    2. Write a SQL query
    3. Execute it locally
    4. Summarize the answer
    
    All interactions are logged to Langfuse for monitoring and debugging.
    """
    # Using Llama 3.2 for local, offline SQL generation
    llm = ChatOllama(model="llama3.2", temperature=0)
    
    # Create SQL agent
    agent_executor = create_sql_agent(
        llm, 
        db=db, 
        agent_type="tool-calling",
        verbose=True
    )
    return agent_executor