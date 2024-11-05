import sqlite3

connection = sqlite3.connect('not_telegrams.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Names(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER
)
''')

cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Names (email)')

# for i in range(1, 11):
#     cursor.execute('INSERT INTO Names (username, email, age, balance) VALUES (?, ?, ?, ?)',
#                    (f'User{i}', f'example{i}@gmail.com', i*10, 1000))
cursor.execute('UPDATE Names SET balance = ? WHERE username = ?', (500, 'User1'))
cursor.execute('UPDATE Names SET balance = ? WHERE username = ?', (500, 'User3'))
cursor.execute('UPDATE Names SET balance = ? WHERE username = ?', (500, 'User5'))
cursor.execute('UPDATE Names SET balance = ? WHERE username = ?', (500, 'User7'))
cursor.execute('UPDATE Names SET balance = ? WHERE username = ?', (500, 'User9'))

#cursor.execute('DELETE FROM User WHERE username = ?', ('User0'))
cursor.execute('DELETE FROM Names WHERE username = ?', ('User1',))
cursor.execute('DELETE FROM Names WHERE username = ?', ('User4',))
cursor.execute('DELETE FROM Names WHERE username = ?', ('User7',))

cursor.execute('SELECT username, email, age, balance FROM Names WHERE age != ?', (60,))
users = cursor.fetchall()
for user in users:
    print(f'Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}')

cursor.execute('DELETE FROM Names WHERE id = ?', (6,))
cursor.execute('SELECT COUNT(*) FROM Names')
print(cursor.fetchone()[0])
cursor.execute('SELECT SUM(balance) FROM Names')
print(cursor.fetchone()[0])
cursor.execute('SELECT AVG(balance) FROM Names')
print(cursor.fetchone()[0])

connection.commit()
connection.close()