from langchain_community.utilities import SQLDatabase
import sqlite3

def get_db_engine():
    # Points to a local file named 'food_delivery.db'
    return SQLDatabase.from_uri("sqlite:///food_delivery.db")

def init_mock_data():
    """Initializes the offline database with sample food delivery tables."""
    conn = sqlite3.connect('food_delivery.db')
    cursor = conn.cursor()
    # Create tables: Users, Restaurants, Orders
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (id INT, name TEXT, email TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Restaurants (id INT, name TEXT, cuisine TEXT)''')
    cursor.execute('''INSERT INTO Restaurants VALUES (1, 'Pizza Hut', 'Italian'), (2, 'Taco Bell', 'Mexican')''')
    conn.commit()
    conn.close()