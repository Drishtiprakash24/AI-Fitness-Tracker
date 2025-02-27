import sqlite3
conn = sqlite3.connect("fitness_tracker.db")
cursor= conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT, age INTEGER , weight REAL , height REAL)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS workouts (
               id INTEGER PRIMARY KEY AUTOINCREMENT ,
               user_id INTEGER, exercise TEXT , duration INTEGER, calories INTEGER, date TEXT,
               FOREIGN KEY(user_id) REFERENCES users(id))''')
conn.commit()
conn.close()