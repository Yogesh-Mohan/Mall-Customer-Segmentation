import sqlite3
import os

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create Customers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            gender TEXT,
            annual_income INTEGER,
            spending_score INTEGER,
            cluster INTEGER,
            customer_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Admin Users table just in case
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    
    # Insert default admin if not exists
    cursor.execute("SELECT * FROM Admins WHERE username='admin'")
    if not cursor.fetchone():
        # In a real app we would hash passwords, but for this mock we keep it simple
        cursor.execute("INSERT INTO Admins (username, password) VALUES ('admin', 'admin123')")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database and tables initialized successfully.")
