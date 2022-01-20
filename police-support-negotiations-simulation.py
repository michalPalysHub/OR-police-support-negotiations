import streamlit as st
import pandas as pd
import numpy as np


st.title("Police support negotiations simulation")
st.write("""
_**Important:**_ In order to run the simulation, please fill in all the necessary initial data.
All the detailed information what is needed you may find in the attached project documentation.
""")


st.write("""
***
### Simulation initial data
""")
col1, col2 = st.columns(2)

# Simulation Start Hour
with col1:
    hour = st.slider('Choose the time of a day when the simulation should start', min_value=0, max_value=24, value=12, step=1)
    st.write('**Start Hour**: ', "{hour}:00".format(hour = hour))
st.write("")

# Simulation Start Day 
with col2:
    date = st.date_input("Choose the day of the month in which the simulation should be inited - day of the week and eg. holiday seasons are taken into consideration")

# Simulation Duration in hours
duration = st.slider('Choose the duration of the simulation in hours (min. 1h, max. 168h - one week)', min_value=1, max_value=168, value=12, step=1)
st.write('**Duration**: ', "{hrs} hours = {days} days".format(hrs = duration, days = duration/24))

# Initial number of Police Patrols
col1, col2 = st.columns(2)
with col1:
    nr_of_police_partols = st.number_input("Initial number of Police Patrols", 1, 100, 50)

# Initial number of Antiterrorist Squads
with col2:
    nr_of_at_squads = st.number_input("Initial number of Antiterrorist Squads", 1, 20, 5)

# Start the simulation
simulation_run = st.button("Start the simulation")


if simulation_run == True:
    st.write("""
    ***
    ### Simulation results 
    The map below presents all the shooting occurances with all the information regarding number of Police Patrols and Antiterrorist Squads involved, 
    """)
    df = pd.DataFrame(
        np.random.randn(50, 2) / [100, 50] + [50.07, 19.95],
        columns=['lat', 'lon'])
    st.map(df)


