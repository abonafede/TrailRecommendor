# File to Load Data into Database
import pandas as pd 
import numpy as np 
import sqlite3 as db 

df_raw = pd.read_csv('data files/combined-trails-w-weather.csv.zip', compression='zip')
feature_kept = ['TITLE', 'REGION', 'LATITUDE', 'LONGITUDE', 'URL', 'riding area', \
            'distance', 'descent', 'climb', 'popularity_score', 'GAIN', 'HIGHEST', \
                'RATING', 'RATING_COUNT', 'Period', 'Check-Ins', 'weather']
df = df_raw[feature_kept]
df = df.dropna()
df = df.iloc[:50]
conn = db.connect('Trails.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS Trail_Data")
df.to_sql(name='Trail_Data',con=conn,index=False)
conn.commit()