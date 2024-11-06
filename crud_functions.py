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

cursor.execute('CREATE INDEX IF NOT EXISTS idx_title ON Products (title)')

# for i in range(1, 5):
#     cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
#                    (f'Продукт {i}', f'Описание {i}', i*100))

def get_all_products():
    cursor.execute('SELECT * FROM Products')
    all_products = cursor.fetchall()
    return all_products

#def print_products():
products = get_all_products()
for product in products:
    # Выводим каждую строку в формате: id, title, description, price
    print(f'id: {product[0]}, title: {product[1]}, description: {product[2]}, price: {product[3]}')

#print_products()

connection.commit()
#connection.close()
