import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

try:
    db = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=''
    )
    cursor = db.cursor()
    
    cursor.execute('CREATE DATABASE IF NOT EXISTS skin_cancer_db')
    cursor.execute('USE skin_cancer_db')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(150) NOT NULL,
        age INT NOT NULL,
        result VARCHAR(50) NOT NULL,
        probability FLOAT NOT NULL,
        image_path VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Add default admin if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
        print("Admin user created.")
    
    db.commit()
    print("Database initialized successfully.")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
