import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")
conn.execute('CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT, desc TEXT, rating INTEGER, image_url TEXT, price REAL)')
print("Table created successfully")
conn.close()