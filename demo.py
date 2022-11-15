import pandas as pd
import numpy as np 
import streamlit as st 
from datetime import date, time

zipcode = st.text_input('Please input your your zipcode.')
radius = st.number_input('Please input how far you are willing to travel (in miles).')
hour_of_day = st.time_input('What time would you like to go for a hike?', time(8, 45))
date = st.date_input("What day would you like to go for a hike?", date.today())

