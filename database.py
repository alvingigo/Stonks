import mysql.connector

class Database:
    def __init__(self):
        # Connect to database
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootroot"
        )
        self.cursor = self.connection.cursor()
        
        # Create database 
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS paper_trading")
        self.cursor.execute("USE paper_trading")
        self.connection.commit()
        
        # Create table users and transactions
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY,name VARCHAR(100),email VARCHAR(150),balance FLOAT(10, 2))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS transactions (id INT PRIMARY KEY AUTO_INCREMENT, user_id INT,symbol VARCHAR(10),action VARCHAR(4),quantity INT,price FLOAT(10, 2),date DATETIME DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS shares (name VARCHAR(100) PRIMARY KEY, total_count INT)")
        # Giving initial values for the user
        self.cursor.execute("select * from users")
        result  = self.cursor.fetchall()
        if result== []:
            self.cursor.execute("INSERT INTO users (id, name, email, balance) VALUES (1, 'John Jose', 'john@abcd.com', 10000.00)")
        self.connection.commit()
        
    def get_balance(self):
        # Get user's balance from database
        self.cursor.execute("SELECT balance FROM users WHERE id = 1")
        balance = self.cursor.fetchone()[0]
        return balance

    def update_balance(self, balance):
        # Update user's balance in database
        self.cursor.execute("UPDATE users SET balance = %s WHERE id = 1", (balance,))
        self.connection.commit()

    def view_shares(self):
        self.cursor.execute("SELECT * FROM shares")
        rows=self.cursor.fetchall()
        for row in rows:
            print(row)
            
    def update_shares_buy(self,symbol,quantity):
        self.cursor.execute("SELECT total_count FROM shares WHERE name = %s", (symbol,))
        existing_share=self.cursor.fetchone()
        if existing_share:
            total_count=existing_share[0]
            total_count+=quantity
            self.cursor.execute("UPDATE shares SET total_count = %s WHERE name = %s", (total_count,symbol))
        else:
            self.cursor.execute("INSERT INTO shares (name,total_count) VALUES (%s, %s)", (symbol,quantity))
            
    def update_shares_sell(self,symbol,quantity):
        self.cursor.execute("SELECT total_count FROM shares WHERE name = %s", (symbol,))
        existing_share=self.cursor.fetchone()
        if existing_share:
            total_count=existing_share[0]
            total_count-=quantity
            if total_count==0:
                self.cursor.execute("DELETE FROM shares WHERE name = %s", (symbol,))
            else:
                self.cursor.execute("UPDATE shares SET total_count = %s WHERE name = %s", (total_count,symbol))
    
    def get_quantity(self, symbol):
        # Get user's quantity of a stock from database
        self.cursor.execute("SELECT total_count FROM shares WHERE name = %s", (symbol,))
        quantity = self.cursor.fetchone()[0]
        return quantity if quantity else 0

    def update_transaction(self, symbol, action, quantity, price):
        # Insert a new transaction into database
        self.cursor.execute("INSERT INTO transactions (user_id, symbol, action, quantity, price) VALUES (1, %s, %s, %s, %s)", (symbol, action, quantity, price))
        self.connection.commit()

    def close_connection(self):
        # Close database connection
        self.connection.close()
