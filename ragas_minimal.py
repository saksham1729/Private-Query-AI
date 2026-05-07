import os
import sys
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

from langchain_ollama import ChatOllama
from ragas.llms.base import LangchainLLMWrapper
from ragas import EvaluationDataset, SingleTurnSample, evaluate
from ragas.metrics._faithfulness import faithfulness
from ragas.metrics._answer_relevancy import answer_relevancy
from ragas.metrics._context_recall import context_recall
from database import get_db_engine
from engine import create_sql_executor

class HashEmbedding:
    def __init__(self, dim: int = 128):
        self.dim = dim

    def _vector(self, text: str):
        import re, math, hashlib
        tokens = re.findall(r"\w+", text.lower())
        vec = [0.0] * self.dim
        for token in tokens:
            idx = int(hashlib.sha256(token.encode('utf-8')).hexdigest()[:8], 16) % self.dim
            vec[idx] += 1.0
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    def embed_text(self, text: str, **kwargs):
        return self._vector(text)

    async def aembed_text(self, text: str, **kwargs):
        return self._vector(text)

    def embed_texts(self, texts, **kwargs):
        return [self._vector(text) for text in texts]

    async def aembed_texts(self, texts, **kwargs):
        return [self._vector(text) for text in texts]

    def embed_query(self, text: str):
        return self._vector(text)

    async def aembed_query(self, text: str):
        return self._vector(text)

    def embed_documents(self, texts, **kwargs):
        return [self._vector(text) for text in texts]

    async def aembed_documents(self, texts, **kwargs):
        return [self._vector(text) for text in texts]

# Single sample for testing
SAMPLES = [
    {
        'query': 'How many orders are there?',
        'reference': 'There are 10 orders in the database.',
        'contexts': ['The Orders table contains 10 rows.']
    }
]

def build_agent():
    db = get_db_engine()
    return create_sql_executor(db)

def build_evaluation_llm():
    llm = ChatOllama(model='llama3.2', temperature=0, timeout=60)  # Add timeout
    return LangchainLLMWrapper(llm)

def run_minimal_evaluation():
    agent = build_agent()
    llm = build_evaluation_llm()
    embeddings = HashEmbedding(dim=128)

    metrics = [faithfulness, answer_relevancy, context_recall]
    samples = []

    print("Generating response for single test query...")
    item = SAMPLES[0]
    try:
        response = agent.invoke({'input': item['query']})
        answer = response.get('output', '').strip()
        print(f"Agent response: {answer[:100]}...")
    except Exception as exc:
        print('Agent error:', exc)
        answer = 'Error generating response'

    samples.append(
        SingleTurnSample(
            user_input=item['query'],
            response=answer,
            reference=item['reference'],
            retrieved_contexts=item['contexts'],
        )
    )

    dataset = EvaluationDataset(samples)

    print("Running RAGAS evaluation with timeout...")
    try:
        result = evaluate(
            dataset,
            metrics=metrics,
            llm=llm,
            embeddings=embeddings,
            show_progress=True,
            timeout=120  # Add timeout parameter
        )
        print('\nRAGAS evaluation result:')
        print(result)
        return result
    except Exception as e:
        print(f"Evaluation failed: {e}")
        return None

if __name__ == '__main__':
    run_minimal_evaluation()