import pandas as pd
import numpy as np 
import streamlit as st 
from datetime import date, time
from scripts.recommendation import get_trails


placeholder = st.empty()

with placeholder.container():
    zipcode = st.text_input('Please input your your zipcode.')
    radius = st.number_input('Please input how far you are willing to travel (in miles).')
    hour_of_day = st.time_input('What time would you like to go for a hike?', time(5, 45)).hour
    date = st.date_input("What day would you like to go for a hike?", date.today())
    btn = st.button('Find Recommended Trails')
if btn:
    placeholder.empty()
    trails = get_trails(zipcode,radius,hour_of_day)
    st.write(trails)
    st.map(trails)

