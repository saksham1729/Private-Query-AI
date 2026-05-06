import streamlit as st
from database import get_db_engine
from engine import create_sql_executor

st.set_page_config(page_title="Offline Text-2-SQL", page_icon="🍔")

st.title("Local Food Delivery Analytics")
st.markdown("---")

# Initialize DB and Agent
db = get_db_engine()
agent = create_sql_executor(db)

# UI Layout
user_query = st.text_input("What would you like to know about the delivery data?")

if user_query:
    with st.spinner("Llama 3.2 is thinking..."):
        try:
            # Running the agent
            response = agent.invoke({"input": user_query})
            
            st.subheader("Result")
            st.write(response["output"])
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Sidebar for metadata
with st.sidebar:
    st.header("System Status")
    st.success("Database: Connected (Offline)")
    st.info("Model: Llama 3.2 via Ollama")