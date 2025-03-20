import sqlite3
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# Sample training data (age, BMI) -> workout type
data=np.array([
    [20,22,1,"Running",30], # Beginner
    [25,18,2,"Yoga",45], # Intermediate
    [30,25,3,"Weight Training",60], # Advanced
    [35,30,4,"Cycling",20],
    [40,35,5,"Swimming",40],
    [45,40,6,"Walking",60]
])

# Convert workout types to numerical values for AI
workout_types={"Running":0,"Yoga":1,"Weight Training":2,"Cycling":3,"Swimming":4,"Walking":5}
reverse_workout_types={v:k for k,v in workout_types.items()}

# Prepare training data
X_train = data[:,:3].astype(float) # Age, BMI, Fitness Level
y_train=np.array([[workout_types[w],int(d)] for w,d in data[:,3:]]) # Workout and Duration

# Train KNN model
model=KNeighborsClassifier(n_neighbors=2)
model.fit(X_train,y_train)

# AI workout recommendation function
def recommend_workout(age,weight,height,fitness_level):
    bmi=weight/(height**2)
    prediction=model.predict([[age,bmi,fitness_level]])[0]
    workout,duration= reverse_workout_types[prediction[0]],prediction[1]
    return workout,duration

# Register user
def register_user(name,age,weight,height):
    conn=sqlite3.connect("fitness_tracker.db")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO users(name,age,weight,height) VALUES (?,?,?,?)",(name,age,weight,height))
    conn.commit()
    conn.close()
    return "User Registered Successfully!"

# Log Workout
def log_workout(user_id,exercise,duration,calories):
    conn=sqlite3.connect("fitness_tracker.db")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO workouts (user_id,exercise,duration,calories,date) VALUES (?,?,?,?,DATE('now'))",(user_id,exercise,duration,calories))
    conn.commit()
    conn.close()
    return " Workout Logged!"

# Calculate BMI
def calculate_bmi(weight,height):
    bmi=weight/(height**2)
    return round(bmi,2)
