import sqlite3

connection = sqlite3.connect('initiate.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER
)
''')

cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER NOT NULL,
balance INTEGER NOT NULL
)
''')

cursor.execute('CREATE INDEX IF NOT EXISTS idx_title ON Products (title)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users (email)')



def add_users(username, email, age, balance):
    cursor.execute('INSERT INTO Users (username, email, age, balance ) VALUES(?, ?, ?, ?)', (username, email, age, balance))
    connection.commit()

def is_included(username):
    check_user = cursor.execute('SELECT * FROM Users WHERE username=?', (username,))
    if check_user.fetchone():
        return True
    else:
        return False

def get_all_users():
    cursor.execute('SELECT * FROM Users')
    all_users = cursor.fetchall()
    return all_users


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    all_products = cursor.fetchall()
    return all_products



products = get_all_products()
for product in products:
    # Выводим каждую строку в формате: id, title, description, price
    print(f'id: {product[0]}, title: {product[1]}, description: {product[2]}, price: {product[3]}')



connection.commit()

