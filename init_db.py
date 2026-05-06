import sqlite3

def initialize_database():
    # Connect to (or create) the local database file
    conn = sqlite3.connect('food_delivery.db')
    cursor = conn.cursor()

    # 1. Create Tables
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            join_date DATE
        );

        CREATE TABLE IF NOT EXISTS Restaurants (
            restaurant_id INTEGER PRIMARY KEY,
            name TEXT,
            cuisine TEXT,
            rating REAL
        );

        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            restaurant_id INTEGER,
            amount REAL,
            order_date DATE,
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
        );
    ''')

    # 2. Insert Mock Data
    cursor.execute("INSERT OR IGNORE INTO Users VALUES (1, 'Alice Smith', 'alice@example.com', '2024-01-15')")
    cursor.execute("INSERT OR IGNORE INTO Users VALUES (2, 'Bob Jones', 'bob@example.com', '2024-02-20')")
    
    cursor.execute("INSERT OR IGNORE INTO Restaurants VALUES (101, 'Pizza Palace', 'Italian', 4.5)")
    cursor.execute("INSERT OR IGNORE INTO Restaurants VALUES (102, 'Taco Town', 'Mexican', 4.2)")

    cursor.execute("INSERT OR IGNORE INTO Orders VALUES (5001, 1, 101, 25.50, '2024-05-01')")
    cursor.execute("INSERT OR IGNORE INTO Orders VALUES (5002, 2, 102, 15.75, '2024-05-02')")

    conn.commit()
    conn.close()
    print("Offline database 'food_delivery.db' initialized successfully.")

if __name__ == "__main__":
    initialize_database()