import sqlite3

connection = sqlite3.connect('main.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO genders (name) VALUES (?)",
    ('Male')
)
cur.execute("INSERT INTO genders (name) VALUES (?)",
    ('Female')
)
cur.execute("INSERT INTO entries (number, datetime, isExit, gender) VALUES (?, ?, ?, ?)",
    ('1', '2020-01-10T13:00:00', 0, 1)
)
cur.execute("INSERT INTO entries (number, datetime, isExit, gender) VALUES (?, ?, ?, ?)",
    ('2', '2020-01-10T13:05:00', 1, 1)
)

connection.commit()
connection.close()