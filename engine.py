from langchain_ollama import ChatOllama
from langchain_community.agent_toolkits import create_sql_agent

def create_sql_executor(db):
    # Using Llama 3.2 which you've used for structured tasks previously
    llm = ChatOllama(model="llama3.2", temperature=0)
    

    # The agent will: 
    # 1. Look at the SQLite schema 
    # 2. Write a SQL query 
    # 3. Execute it locally 
    # 4. Summarize the answer
    agent_executor = create_sql_agent(
        llm, 
        db=db, 
        agent_type="tool-calling", # Standard for local models supporting tools
        verbose=True
    )
    return agent_executor