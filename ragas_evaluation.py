import os
import re
import sys
import math
import hashlib
from dotenv import load_dotenv

# Ensure unicode-safe output on Windows
sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

from openai import OpenAI  # noqa: F401
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


SAMPLES = [
    {
        'query': 'How many orders are there?',
        'reference': 'There are 2 orders in the database.',
        'contexts': ['Order 5001 and order 5002 are the two rows in the Orders table.']
    },
    {
        'query': 'What is the total amount of all orders?',
        'reference': 'The total amount of all orders is 41.25.',
        'contexts': ['Order 5001 is 25.5 and order 5002 is 15.75.']
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
        'query': 'How many orders did Bob Jones make?',
        'reference': 'Bob Jones made 1 order.',
        'contexts': ['Order 5002 belongs to user Bob Jones.']
    },
    {
        'query': 'What is the cuisine of Taco Town?',
        'reference': 'Taco Town serves Mexican cuisine.',
        'contexts': ['Restaurant Taco Town has cuisine Mexican.']
    },
    {
        'query': 'What is the email of Alice Smith?',
        'reference': 'Alice Smith’s email is alice@example.com.',
        'contexts': ['User Alice Smith has email alice@example.com.']
    },
    {
        'query': 'What is the rating of Pizza Palace?',
        'reference': 'Pizza Palace has a rating of 4.5.',
        'contexts': ['Restaurant Pizza Palace has rating 4.5.']
    },
    {
        'query': 'Which user ordered from Pizza Palace?',
        'reference': 'Alice Smith ordered from Pizza Palace.',
        'contexts': ['Order 5001 is for restaurant Pizza Palace and belongs to user Alice Smith.']
    },
    {
        'query': 'What is the order amount for order 5002?',
        'reference': 'The amount for order 5002 is 15.75.',
        'contexts': ['Order 5002 has amount 15.75.']
    },
    {
        'query': 'Which restaurant had an order on 2024-05-01?',
        'reference': 'Pizza Palace had an order on 2024-05-01.',
        'contexts': ['Order 5001 occurred on 2024-05-01 and points to Pizza Palace.']
    },
    {
        'query': 'List all restaurant names.',
        'reference': 'The restaurants are Pizza Palace and Taco Town.',
        'contexts': ['The Restaurants table contains Pizza Palace and Taco Town.']
    },
    {
        'query': 'What are the cuisines in the database?',
        'reference': 'The cuisines are Italian and Mexican.',
        'contexts': ['Pizza Palace is Italian and Taco Town is Mexican.']
    },
    {
        'query': 'How many users are registered?',
        'reference': 'There are 2 registered users.',
        'contexts': ['The Users table contains Alice Smith and Bob Jones.']
    },
    {
        'query': 'What is the average order amount?',
        'reference': 'The average order amount is 20.625.',
        'contexts': ['Order totals are 25.5 and 15.75.']
    },
    {
        'query': 'Which orders were placed in May 2024?',
        'reference': 'Orders 5001 and 5002 were placed in May 2024.',
        'contexts': ['Orders 5001 and 5002 have order_date values in May 2024.']
    },
    {
        'query': 'Who placed order 5001?',
        'reference': 'Alice Smith placed order 5001.',
        'contexts': ['Order 5001 belongs to Alice Smith.']
    },
    {
        'query': 'What is Bob Jones’s user ID?',
        'reference': 'Bob Jones’s user ID is 2.',
        'contexts': ['User Bob Jones has user_id 2.']
    },
    {
        'query': 'What is Alice Smith’s join date?',
        'reference': 'Alice Smith joined on 2024-01-15.',
        'contexts': ['Alice Smith has join_date 2024-01-15.']
    },
    {
        'query': 'What is the restaurant ID for Taco Town?',
        'reference': 'Taco Town has restaurant ID 102.',
        'contexts': ['Restaurant Taco Town has restaurant_id 102.']
    },
    {
        'query': 'Which order has a higher amount, 5001 or 5002?',
        'reference': 'Order 5001 has a higher amount.',
        'contexts': ['Order 5001 is 25.5 and order 5002 is 15.75.']
    },
    {
        'query': 'What is the total revenue from orders?',
        'reference': 'The total revenue from orders is 41.25.',
        'contexts': ['Order amounts are 25.5 and 15.75.']
    },
    {
        'query': 'Which user has email bob@example.com?',
        'reference': 'Bob Jones has the email bob@example.com.',
        'contexts': ['User Bob Jones has email bob@example.com.']
    },
    {
        'query': 'How many restaurants are there?',
        'reference': 'There are 2 restaurants.',
        'contexts': ['The Restaurants table contains two rows.']
    },
    {
        'query': 'What is the name of the restaurant with ID 101?',
        'reference': 'The restaurant with ID 101 is Pizza Palace.',
        'contexts': ['Restaurant 101 is Pizza Palace.']
    },
    {
        'query': 'Which orders are over $20?',
        'reference': 'Order 5001 is over $20.',
        'contexts': ['Order 5001 has amount 25.5.']
    },
    {
        'query': 'What cuisine is restaurant 101?',
        'reference': 'Restaurant 101 serves Italian cuisine.',
        'contexts': ['Restaurant 101 is Pizza Palace and serves Italian cuisine.']
    },
    {
        'query': 'What is the order date for order 5002?',
        'reference': 'Order 5002 was placed on 2024-05-02.',
        'contexts': ['Order 5002 has order_date 2024-05-02.']
    },
    {
        'query': 'Does any order exceed $30?',
        'reference': 'No order exceeds $30.',
        'contexts': ['Order amounts are 25.5 and 15.75.']
    },
    {
        'query': 'What is the lowest order amount?',
        'reference': 'The lowest order amount is 15.75.',
        'contexts': ['Order 5002 has the lowest amount of 15.75.']
    },
    {
        'query': 'What is the highest order amount?',
        'reference': 'The highest order amount is 25.5.',
        'contexts': ['Order 5001 has the highest amount of 25.5.']
    },
    {
        'query': 'Which restaurant has rating 4.2?',
        'reference': 'Taco Town has rating 4.2.',
        'contexts': ['Restaurant Taco Town has rating 4.2.']
    },
    {
        'query': 'What restaurant did Alice order from?',
        'reference': 'Alice ordered from Pizza Palace.',
        'contexts': ['Order 5001 belongs to Alice and references Pizza Palace.']
    },
    {
        'query': 'What restaurant did Bob order from?',
        'reference': 'Bob ordered from Taco Town.',
        'contexts': ['Order 5002 belongs to Bob and references Taco Town.']
    },
    {
        'query': 'How many orders are from restaurant 102?',
        'reference': 'There is 1 order from restaurant 102.',
        'contexts': ['Order 5002 is for restaurant 102.']
    },
    {
        'query': 'Which user ID is associated with order 5001?',
        'reference': 'Order 5001 is associated with user ID 1.',
        'contexts': ['Order 5001 has user_id 1.']
    },
    {
        'query': 'What is the email of the user who ordered 5002?',
        'reference': 'The user who ordered 5002 has email bob@example.com.',
        'contexts': ['Order 5002 belongs to Bob Jones, whose email is bob@example.com.']
    },
    {
        'query': 'Which restaurants are Italian?',
        'reference': 'Pizza Palace is Italian.',
        'contexts': ['Pizza Palace has cuisine Italian.']
    },
    {
        'query': 'Which restaurants are Mexican?',
        'reference': 'Taco Town is Mexican.',
        'contexts': ['Taco Town has cuisine Mexican.']
    },
    {
        'query': 'What is the rating of Taco Town?',
        'reference': 'Taco Town has a rating of 4.2.',
        'contexts': ['Restaurant Taco Town has rating 4.2.']
    },
    {
        'query': 'Which users joined after 2024-01-31?',
        'reference': 'Bob Jones joined after 2024-01-31.',
        'contexts': ['Bob Jones has join_date 2024-02-20.']
    },
    {
        'query': 'What user names are in the Users table?',
        'reference': 'The users are Alice Smith and Bob Jones.',
        'contexts': ['The Users table contains Alice Smith and Bob Jones.']
    },
    {
        'query': 'Which order has amount 15.75?',
        'reference': 'Order 5002 has amount 15.75.',
        'contexts': ['Order 5002 has amount 15.75.']
    },
    {
        'query': 'What cuisine is Pizza Palace?',
        'reference': 'Pizza Palace serves Italian cuisine.',
        'contexts': ['Pizza Palace has cuisine Italian.']
    },
    {
        'query': 'How many orders are from Pizza Palace?',
        'reference': 'There is 1 order from Pizza Palace.',
        'contexts': ['Order 5001 is for Pizza Palace.']
    },
    {
        'query': 'What is the first order date?',
        'reference': 'The first order date is 2024-05-01.',
        'contexts': ['Order 5001 has date 2024-05-01.']
    },
    {
        'query': 'Which orders belong to user ID 2?',
        'reference': 'Order 5002 belongs to user ID 2.',
        'contexts': ['Order 5002 has user_id 2.']
    },
    {
        'query': 'What is the combined order amount by Alice Smith?',
        'reference': 'Alice Smith’s combined order amount is 25.5.',
        'contexts': ['Alice Smith has order 5001 with amount 25.5.']
    },
    {
        'query': 'List all emails stored in the Users table.',
        'reference': 'The emails are alice@example.com and bob@example.com.',
        'contexts': ['User emails are alice@example.com and bob@example.com.']
    },
    {
        'query': 'Which orders were placed by Bob?',
        'reference': 'Order 5002 was placed by Bob Jones.',
        'contexts': ['Order 5002 belongs to Bob Jones.']
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
