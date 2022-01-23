import streamlit as st

from simulation.main import Simulation


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
    hour = st.slider('Choose the time of a day when the simulation should start', min_value=0, max_value=23, value=12, step=1)
    st.write('**Start Hour**: ', "{hour}:00".format(hour = hour))
st.write("")

# Simulation Start Day 
with col2:
    date = st.date_input("Choose the day of the month in which the simulation should be inited - day of the week and eg. holiday seasons are taken into consideration")

# Simulation Duration in hours
col1, col2 = st.columns(2)
with col1:
    duration = st.slider('Duration of the simulation (min. 1h, max. 168h - one week)', min_value=1, max_value=168, value=24, step=1)
    st.write('**Duration**: ', "{hrs} hours = {days:.2f} day(s)".format(hrs = duration, days = duration/24))

# Simulation Time Step Duration in hours
with col2:
    time_step = st.slider('Time step duration for the simulation', min_value=0.1, max_value=2.0, value=1.0, step=0.1)
    st.write('**Time step duration**: ', "{hrs} hour(s)".format(hrs = duration))

# Initial number of Police Patrols
col1, col2 = st.columns(2)
with col1:
    nr_of_police_partols = st.number_input("Initial number of Police Patrols", 1, 200, 100)

# Initial number of Antiterrorist Squads
with col2:
    nr_of_at_squads = st.number_input("Initial number of Antiterrorist Squads", 1, 20, 5)

# Start the simulation
simulation_run = st.button("Start the simulation")
if simulation_run == True:
    simulation = Simulation(hour, date, duration, time_step, nr_of_police_partols, nr_of_at_squads)
    result = simulation.run()

    st.write("""
    ***
    ### Simulation results

    Detailed stats containing information about all the agent negotiations that took place during the simulation.
    """)
    st.write(result)

    st.write("""
    The map below presents all the shooting location that occured during the simulation.
    """)
    st.map(result)
