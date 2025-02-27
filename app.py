import streamlit as st
import sqlite3
import pandas as pd
from functions import register_user,log_workout

conn=sqlite3.connect("fitness_tracker.db",check_same_thread=False)
cursor=conn.cursor()

st.title("Personal Fitness Tracker 🏋️")

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
if st.button("Show Progress"):
    df=pd.read_sql_query(f"SELECT date,calories FROM workouts WHERE user_id={user_id}",conn)
    st.line_chart(df.set_index("date"))
    