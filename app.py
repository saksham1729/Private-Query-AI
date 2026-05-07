import streamlit as st
import os
from database import get_db_engine
from engine import create_sql_executor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Offline Text-2-SQL", page_icon="🍔")

st.title("Local Food Delivery Analytics")
st.markdown("---")

# Check if Langfuse is enabled
langfuse_enabled = os.getenv("LANGFUSE_PUBLIC_KEY") is not None and os.getenv("LANGFUSE_SECRET_KEY") is not None

# Initialize DB and Agent (this will initialize Langfuse if enabled)
db = get_db_engine()
agent = create_sql_executor(db)

# UI Layout
user_query = st.text_input("What would you like to know about the delivery data?")

if user_query:
    with st.spinner("Llama 3.2 is thinking..."):
        try:
            # Running the agent (automatically traced if Langfuse is enabled)
            response = agent.invoke({"input": user_query})
            
            st.subheader("Result")
            st.write(response["output"])
            
            # Show generated SQL if available
            if "intermediate_steps" in response:
                with st.expander("📋 View Generated SQL"):
                    for step in response["intermediate_steps"]:
                        st.code(step, language="sql")
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
            if langfuse_enabled:
                st.info("This error has been logged to Langfuse for debugging.")
                trace.generation(
                    name="error",
                    output=str(e),
                    model="llama3.2"
                )

# Sidebar for metadata and monitoring
with st.sidebar:
    st.header("System Status")
    st.success("Database: Connected (Offline)")
    st.info("Model: Llama 3.2 via Ollama")
    
    if langfuse_enabled:
        st.success("📊 Langfuse: Connected (Observability Enabled)")
        st.markdown("[View Traces](https://cloud.langfuse.com)")
    else:
        st.warning("📊 Langfuse: Not configured (set credentials in .env)")
    
    st.divider()
    st.subheader("About")
    st.caption("Text-to-SQL with Langfuse Observability")
    st.caption("All queries are logged for monitoring and debugging")