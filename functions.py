import sqlite3
def register_user(name,age,weight,height):
    conn=sqlite3.connect("fitness_tracker.db")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO users(name,age,weight,height) VALUES (?,?,?,?)",(name,age,weight,height))
    conn.commit()
    conn.close()
    return "User Registered Successfully!"
def log_workout(user_id,exercise,duration,calories):
    conn=sqlite3.connect("fitness_tracker.db")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO workouts (user_id,exercise,duration,calories,date) VALUES (?,?,?,?,DATE('now'))",(user_id,exercise,duration,calories))
    conn.commit()
    conn.close()
    return " Workout Logged!"
def calculate_bmi(weight,height):
    bmi=weight/(height**2)
    return round(bmi,2)
