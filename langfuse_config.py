"""
Langfuse Configuration Module
Centralizes all Langfuse setup and initialization for the Text-to-SQL project.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LangfuseConfig:
    """Configuration for Langfuse observability platform."""
    
    # Credentials from .env
    PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
    SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
    HOST = os.getenv("LANGFUSE_BASE_URL") or os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    
    # Feature flags
    ENABLED = PUBLIC_KEY is not None and SECRET_KEY is not None
    
    # Trace settings
    TRACE_NAME = "text2sql_query"
    USER_ID = "streamlit_user"
    SESSION_ID = "default_session"
    
    # Sampling (for high-volume scenarios)
    # Set to 1.0 to trace everything, 0.5 to trace 50%, etc.
    SAMPLE_RATE = 1.0
    
    # Tags for organizing traces
    DEFAULT_TAGS = ["text2sql", "ollama", "sqlite"]
    
    # Model information
    MODEL_NAME = "llama3.2"
    MODEL_PROVIDER = "ollama"
    
    # Custom metadata
    APPLICATION_NAME = "Offline Text-to-SQL"
    VERSION = "1.0.0"
    
    @classmethod
    def validate(cls) -> bool:
        """Check if Langfuse is properly configured."""
        if not cls.ENABLED:
            return False
        
        if not cls.PUBLIC_KEY or not cls.SECRET_KEY:
            return False
        
        return True
    
    @classmethod
    def get_client_config(cls) -> dict:
        """Get configuration dict for Langfuse client."""
        return {
            "public_key": cls.PUBLIC_KEY,
            "secret_key": cls.SECRET_KEY,
            "host": cls.HOST,
        }
    
    @classmethod
    def get_trace_config(cls, query: str = None, session_id: str = None) -> dict:
        """Get configuration dict for creating traces."""
        return {
            "name": cls.TRACE_NAME,
            "user_id": cls.USER_ID,
            "session_id": session_id or cls.SESSION_ID,
            "tags": cls.DEFAULT_TAGS,
            "metadata": {
                "application": cls.APPLICATION_NAME,
                "version": cls.VERSION,
                "model": cls.MODEL_NAME,
                "provider": cls.MODEL_PROVIDER,
            }
        }


def get_langfuse_client():
    """
    Factory function to create and return Langfuse client.
    
    Returns:
        Langfuse client if configured, None otherwise
    """
    if not LangfuseConfig.ENABLED:
        return None
    
    try:
        from langfuse import Langfuse
        
        return Langfuse(**LangfuseConfig.get_client_config())
    except ImportError:
        print("Langfuse library not installed. Install with: pip install langfuse")
        return None
    except Exception as e:
        print(f"Failed to initialize Langfuse: {e}")
        return None


# Example usage in your code:
"""
from langfuse_config import LangfuseConfig, get_langfuse_client
from langfuse import observe

# Use @observe() decorator on functions you want to trace
@observe()
def my_function():
    pass

# Get client if needed
if LangfuseConfig.ENABLED:
    langfuse = get_langfuse_client()
    trace = langfuse.trace(**LangfuseConfig.get_trace_config())
"""
