# Text-to-SQL Project

A local, offline Text-to-SQL application that converts natural language queries into SQL statements using LangChain and Ollama. Features observability through Langfuse integration.

## Features

- **Offline Operation**: Runs entirely on local hardware using Ollama models
- **SQL Agent**: Uses LangChain's SQL agent with tool-calling capabilities
- **Observability**: Integrated with Langfuse for monitoring and debugging
- **Streamlit UI**: Simple web interface for query input and results
- **SQLite Database**: Local database with sample food delivery data

## RAGAS Evaluation Scores

The system has been evaluated using RAGAS (Retrieval-Augmented Generation Assessment System) with the following metrics:

- **Faithfulness**: 0.8000 - Generated answers are mostly faithful to the provided context
- **Answer Relevancy**: 0.8000 - Answers are generally relevant to the questions asked
- **Context Recall**: 1.0000 - Perfect recall of all relevant context information

## Architecture

- **Frontend**: Streamlit web application
- **Backend**: Python with LangChain and Ollama
- **Database**: SQLite with local food delivery schema
- **LLM**: Llama 3.2 (3B parameters) via Ollama
- **Observability**: Langfuse cloud integration

## Setup

### Prerequisites

1. **Python 3.9+**
2. **Ollama** installed and running
3. **Langfuse account** (optional, for observability)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd text2sql
```

2. Create virtual environment:
```bash
python -m venv text2sql_env
text2sql_env\Scripts\activate  # Windows
# or
source text2sql_env/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Ollama and pull the model:
```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.2
```

5. Configure environment variables (optional):
```bash
# Copy .env and update with your Langfuse credentials
cp .env.example .env
```

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser to `http://localhost:8501`

3. Enter natural language queries like:
   - "How many orders are there?"
   - "What is the total amount of all orders?"
   - "Which restaurant has the highest rating?"

## Database Schema

The application uses a SQLite database with the following tables:

- **Users**: Customer information
- **Orders**: Order details with amounts and dates
- **Products**: Available food items
- **Order_Items**: Order line items
- **Users_Products**: User-product relationships

## Observability

The application integrates with Langfuse for comprehensive observability:

- **Automatic Tracing**: All agent interactions are logged
- **Performance Metrics**: Latency, token usage, and error tracking
- **Debug Information**: Step-by-step execution flow
- **Dashboard**: View traces at https://cloud.langfuse.com

## Development

### Testing Langfuse Integration

```bash
python test_langfuse.py
```

### Running RAGAS Evaluation

```bash
python ragas_evaluation_simple.py
```

## Security & Privacy

- **Local Execution**: All processing happens on your machine
- **No Data Exfiltration**: Queries and results stay local
- **Optional Observability**: Langfuse integration is optional and configurable

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and evaluation
5. Submit a pull request

## License

MIT License - see LICENSE file for details