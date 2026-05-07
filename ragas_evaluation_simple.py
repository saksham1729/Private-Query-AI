import os
import re
import sys
import math
import hashlib
from dotenv import load_dotenv

# Ensure unicode-safe output on Windows
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

from langchain_ollama import ChatOllama
from ragas.llms.base import LangchainLLMWrapper
from ragas import EvaluationDataset, SingleTurnSample, evaluate
from ragas.metrics._faithfulness import faithfulness
from ragas.metrics._answer_relevance import answer_relevancy
from ragas.metrics._context_recall import context_recall
from database import get_db_engine
from engine import create_sql_executor

class HashEmbedding:
    def __init__(self, dim: int = 128):
        self.dim = dim

    def _vector(self, text: str):
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


# Reduced sample set for faster testing
SAMPLES = [
    {
        'query': 'How many orders are there?',
        'reference': 'There are 10 orders in the database.',
        'contexts': ['The Orders table contains 10 rows.']
    },
    {
        'query': 'What is the total amount of all orders?',
        'reference': 'The total amount of all orders is 41.25.',
        'contexts': ['Order amounts are 25.5 and 15.75.']
    },
    {
        'query': 'Which restaurant has the highest order amount?',
        'reference': 'Pizza Palace has the highest order amount of 25.5.',
        'contexts': ['Order 5001 is from restaurant Pizza Palace with amount 25.5.']
    },
    {
        'query': 'How many orders did Alice Smith make?',
        'reference': 'Alice Smith made 1 order.',
        'contexts': ['Order 5001 belongs to user Alice Smith.']
    },
    {
        'query': 'What is the cuisine of Taco Town?',
        'reference': 'Taco Town serves Mexican cuisine.',
        'contexts': ['Restaurant Taco Town has cuisine Mexican.']
    },
]


def build_agent():
    db = get_db_engine()
    return create_sql_executor(db)


def build_evaluation_llm():
    llm = ChatOllama(model='llama3.2', temperature=0)
    return LangchainLLMWrapper(llm)


def run_evaluation():
    agent = build_agent()
    llm = build_evaluation_llm()
    embeddings = HashEmbedding(dim=128)

    metrics = [faithfulness, answer_relevancy, context_recall]
    samples = []

    for item in SAMPLES:
        print('Generating response for:', item['query'])
        try:
            response = agent.invoke({'input': item['query']})
            answer = response.get('output', '').strip()
        except Exception as exc:
            print('Agent error for query:', item['query'], exc)
            answer = ''

        samples.append(
            SingleTurnSample(
                user_input=item['query'],
                response=answer,
                reference=item['reference'],
                retrieved_contexts=item['contexts'],
            )
        )

    dataset = EvaluationDataset(samples)
    result = evaluate(
        dataset,
        metrics=metrics,
        llm=llm,
        embeddings=embeddings,
        show_progress=True,
    )

    print('\nRAGAS evaluation result:')
    print(result)
    return result


if __name__ == '__main__':
    run_evaluation()