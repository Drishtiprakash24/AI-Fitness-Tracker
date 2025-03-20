import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from functions import register_user,log_workout,calculate_bmi,recommend_workout
import streamlit as st

import streamlit as st

# Custom CSS for full theme styling
def apply_custom_styles():
    st.markdown("""
        <style>
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: #e6f7ff !important; /* Light Blue */
                padding: 20px;
            }

            /* Main Background Color */
            [data-testid="stAppViewContainer"] {
                background-color: #f0f2f6 !important; /* Light Grey */
            }

            /* Text Styling */
            h1, h2, h3, h4, h5, h6 {
                color: #1E90FF !important; /* Dodger Blue */
                font-family: 'Arial', sans-serif;
            }

            /* Button Styling */
            div.stButton > button {
                background-color: #1E90FF !important; /* Dodger Blue */
                color: white !important;
                font-size: 16px !important;
                padding: 10px 20px !important;
                border-radius: 8px !important;
                border: none;
                transition: 0.3s;
            }
            
            div.stButton > button:hover {
                background-color: #104E8B !important; /* Darker Blue */
            }

            /* Input Box Styling */
            div[data-testid="stTextInput"] input {
                background-color: #ffffff !important; /* White */
                color: #000000 !important; /* Black */
                font-size: 14px !important;
                border-radius: 5px;
                padding: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

# Apply CSS styling
apply_custom_styles()

# Streamlit UI elements
st.sidebar.title("AI Fitness Tracker")
st.sidebar.write("Health is Wealth.")



# Connect to DB
conn=sqlite3.connect("fitness_tracker.db",check_same_thread=False)
cursor=conn.cursor()

st.title("Personal Fitness Tracker 🏋️")
st.write("In this WebApp you will be able to observe your predicted calories burned in your body. Pass your parameters such as `Age`, `Gender`, `BMI`, etc., into this WebApp and then you will see the predicted value of kilocalories burned.")

if "user_data" not in st.session_state:
    st.session_state.user_data=None

# Function to clear input fields
def clear_inputs():
    st.session_state["name"] = ""
    st.session_state["age"] = 10  # Set to min value
    st.session_state["weight"] = 20.0  # Set to min value
    st.session_state["height"] = 1.0  # Set to min value
    st.session_state["fitness_level"] = "Beginner"

# User Registration
st.header("Register User")
name=st.text_input("Name :")
age=st.number_input("Age :",min_value=10,max_value=100)
weight=st.number_input("Weight (kg) :",min_value=20.0,max_value=200.0)
height=st.number_input("Height (m) :",min_value=1.0,max_value=2.5)
fitness_level=st.selectbox("Select your fitness level",["Beginner","Intermediate","Advanced"])
fitness_map={"Beginner":1,"Intermediate":2,"Advanced":3}

if st.button("Register") :
    if name:
        st.session_state.user_data={
            "Name" : name,
            "Age": age,
            "Weight":weight,
            "Height": height,
            "Fitness Level":fitness_level
        }
        st.success(f"✔ {name}, you have been registered successfully !")
        clear_inputs()
        
if st.session_state.user_data:
    st.sidebar.title("User Profile")
    for key,value in st.session_state.user_data.items():
        st.sidebar.markdown(f"<b>{key}:</b> {value}",unsafe_allow_html=True)

# Log Workout 
st.header("Log Workout")
user_id=st.number_input("User ID:",min_value=1)
exercise=st.text_input("Exercise:")
duration=st.number_input("Duration (min):",min_value=1)
calories=st.number_input("Calories Burned:",min_value=1)
if st.button("Save Workout"):
    st.success(log_workout(user_id,exercise,duration,calories))

# View BMI
st.header("View Progress")
if st.button("Calculate BMI"):
    st.write("Your BMI is:", calculate_bmi(weight, height))

if st.button("Show Progress"):
    
    # Read workout progress data
    df = pd.read_sql_query(f"SELECT date, calories FROM workouts WHERE user_id={user_id}", conn)
    conn.close()

    # Create a Matplotlib figure
    fig,ax=plt.subplots(figsize=(8,5))
    ax.plot(df['date'],df['calories'],marker="o",linestyle='-')

    # Add labels and title
    ax.set_xlabel("Date")
    ax.set_ylabel("Calories Burned")
    ax.set_title("Workout Progress")
    ax.tick_params(axis='x',rotation=45)

    # Display graph in Streamlit
    st.pyplot(fig)
    
st.header("AI-Powered Workout Recommendation")
if st.button("Get Workout Plan"):
    workout,duration=recommend_workout(age,weight,height,fitness_map[fitness_level])
    
    # Store in database
    conn = sqlite3.connect("fitness_tracker.db")
    cursor=conn.cursor()
    cursor.execute("INSERT INTO recommendations(user_id,workout,duration,date) VALUES (?,?,?,DATE('now'))",(user_id,workout,duration))
    
    conn.commit()
    conn.close()
    st.success(f"Recommended Workout: {workout} 🏋️‍♂️ ({duration} min)")


