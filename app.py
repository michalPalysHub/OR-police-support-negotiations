import streamlit as st
import pandas as pd
import numpy as np

from simulation.agents import PolicePatrol, AntiTerroristSquad, ManagementCenter
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
    duration = st.slider('Duration of the simulation (min. 1h, max. 168h - one week)', min_value=1, max_value=168, value=12, step=1)
    st.write('**Duration**: ', "{hrs} hours = {days:.2f} day(s)".format(hrs = duration, days = duration/24))

# Simulation Time Step Duration in hours
with col2:
    time_step = st.slider('Time step duration for the simulation', min_value=0.1, max_value=2.0, value=1.0, step=0.1)
    st.write('**Time step duration**: ', "{hrs} hour(s)".format(hrs = duration))

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
    simulation = Simulation(hour, date, duration, time_step, nr_of_police_partols, nr_of_at_squads)
    result = simulation.run()
    st.write(result)




# TODO: zamiast pokazywania mapy pokazywać modal z podsumowaniem, albo printować póki co podsumowanie, potem ew. dorobić wyświetlanie tych statystyk na mapie
# if simulation_run == True:
#     st.write("""
#     ***
#     ### Simulation results 
#     The map below presents all the shooting occurances with all the information regarding number of Police Patrols and Antiterrorist Squads involved, 
#     """)
#     df = pd.DataFrame(
#         np.random.randn(50, 2) / [100, 50] + [50.07, 19.95],
#         columns=['lat', 'lon'])
#     st.map(df)

""" 
### Do zrobienia

W klasie Simulation:
 - generujemy określoną liczbę policjantów na terenie całego miasta (zamiast po współrzędnych i zaznaczania na mapie tych 
 miejsc strzelanin losujemy dzielnicę z listy wszystkich dzielnic które są w JSONie, które mają przyporządkowane stopnie bezpieczeństwa)
 - z określoną częstotliwością kroków czasowych z zadanym prawdopodobieństwem (te prawdopodobieństwa hard-coduje, potem ew podawanie ze strony) 
 dzieją się interwencje i dalej strzelaniny
 - w momencie wybuchu strzelaniny dokonujemy NEGOCJACJI - każda taka NEGOCJACJA jest logowana do osobnego pliczku .csv, poza tym generowany jest osobny 
 .csv z podsumowaniem (zamiast wyświetlania tego na mapie - EWENTUALNIE wyświetlać takie statystyki zbiorcze dla każdej dzielnicy na mapie)

Flow całej aplikacji
 1. app.py
 2. main.py (w klasie Simulation wykonujemy w pętli kolejne kroki czasowe, zapisujemy stan końcowy po zakończeniu symulacji) -> 
 3. MC komunikuje się z wewnętrznymi PP i AS i wewnątrz nimi dyryguje (tak jakby odpowiednik Board w ForestFire)
"""

