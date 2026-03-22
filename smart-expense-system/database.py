print("File is running...")

import sqlite3

#function to create connection
def create_connection():
    conn=sqlite3.connect("expense_tracker.db")
    return conn

#function to create tables
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    #users table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                   user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   email TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL
                   )
                """)
    
    #expenses table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS expenses(
                   expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   amount REAL NOT NULL,
                   category TEXT NOT NULL,
                   date TEXT NOT NULL,
                   description TEXT,
                   FOREIGN KEY (user_id) REFERENCES users(user_id)
                   )
                   """)
    #budgets table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS budgets(
                   budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   category TEXT NOT NULL,
                   monthly_limit REAL NOT NULL,
                   FOREIGN KEY (user_id) REFERENCES users(user_id)
                   )
                   """)
    
def add_user(name,email,password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO users (name,email,password)
                   VALUES (?,?,?)
                   """,(name,email,password))
    conn.commit()
    conn.close()
    print("User added successfully!")

def add_expense(user_id,amount,category,date,description):
    category=category.lower()
    conn=create_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO expenses (user_id,amount,category,date,description)
                   VALUES (?,?,?,?,?)
                   """,(user_id,amount,category,date,description))
    
    conn.commit()
    conn.close()
    print("Expense added successfully!")

def get_expenses():
    conn=create_connection()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses=cursor.fetchall()

    conn.close()
    return expenses

def get_expenses_by_user(user_id):
    conn=create_connection()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE user_id= ?",(user_id,))
    expenses=cursor.fetchall()

    return expenses

def clear_data():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses")
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM budgets")

    conn.commit()
    conn.close()

    print("All data deleted!")

    
if __name__ == "__main__":
    clear_data()