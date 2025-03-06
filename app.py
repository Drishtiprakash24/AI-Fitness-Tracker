import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from functions import register_user,log_workout,calculate_bmi

conn=sqlite3.connect("fitness_tracker.db",check_same_thread=False)
cursor=conn.cursor()

st.title("Personal Fitness Tracker 🏋️")
st.write("In this WebApp you will be able to observe your predicted calories burned in your body. Pass your parameters such as `Age`, `Gender`, `BMI`, etc., into this WebApp and then you will see the predicted value of kilocalories burned.")

st.header("Register User")
name=st.text_input("Name :")
age=st.number_input("Age :",min_value=10,max_value=100)
weight=st.number_input("Weight (kg) :",min_value=20.0,max_value=200.0)
height=st.number_input("Height (m) :",min_value=1.0,max_value=2.5)
if st.button("Register"):
    st.success(register_user(name,age,weight,height))

st.header("Log Workout")
user_id=st.number_input("User ID:",min_value=1)
exercise=st.text_input("Exercise:")
duration=st.number_input("Duration (min):",min_value=1)
calories=st.number_input("Calories Burned:",min_value=1)
if st.button("Save Workout"):
    st.success(log_workout(user_id,exercise,duration,calories))

st.header("View Progress")
if st.button("Calculate BMI"):
    st.write("Your BMI is:", calculate_bmi(weight, height))

if st.button("Show Progress"):
    
    df = pd.read_sql_query(f"SELECT date, calories FROM workouts WHERE user_id={user_id}", conn)
    conn.close()
    fig,ax=plt.subplots(figsize=(8,5))
    ax.plot(df['date'],df['calories'],marker="o",linestyle='-')
    ax.set_xlabel("Date")
    ax.set_ylabel("Calories Burned")
    ax.set_title("Workout Progress")
    ax.tick_params(axis='x',rotation=45)
    st.pyplot(fig)
    