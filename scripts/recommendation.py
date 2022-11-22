# This script creates predictions using knn clustering on our 
# combined dataset for all the washington trails

import pandas as pd
import numpy as np
import pgeocode # pip3 install pgeocode
import geopy.distance # pip3 install geopy
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def getDistFromLatLong(coord1, corrd2):
    '''
    Input: 
        coord1 : (lat, long) tuple
        coord2 : (lat, long) tuple
    
    Output:
        distance : int (in miles)
    '''
    return geopy.distance.geodesic(coord1, corrd2).miles

def convertToAMPM(hour):
    '''
    Inputs:
        hour : int (0-23)

    Outputs:    
        hourOfDay : string (AM/PM format time)
    '''
    if hour == 0: return "12am"
    elif hour < 12: return str(hour)+"am"
    elif hour == 12: return "12pm"
    else: return str(hour-12)+"pm"

def convertDist(dist):
    '''
    Inputs:
        dist : string

    Outputs:
        dist_numeric : int (unit:ft)
    '''
    if dist[-4:] == "mile": return 5280 # 1 mile is 5280 ft
    elif dist[-5:] == "miles": return int(dist[:-6])*5280
    else: return int(dist[:-3].replace(',', ''))

def get_trails(zipcode, radius, hour_of_day):
    df_raw = pd.read_csv('data files/combined-trails-w-weather.csv.zip', compression='zip')
    feature_kept = ['TITLE', 'REGION', 'LATITUDE', 'LONGITUDE', 'URL', 'riding area', \
                'distance', 'descent', 'climb', 'popularity_score', 'GAIN', 'HIGHEST', \
                    'RATING', 'RATING_COUNT', 'Period', 'Check-Ins', 'weather']
    df = df_raw[feature_kept]
    df = df.dropna()

    k = int(df[['REGION']].nunique())
    kmeans = KMeans(n_clusters=k, init ='k-means++')
    kmeans.fit(df[['LATITUDE', 'LONGITUDE']]) # Compute k-means clustering.
    df['coord_label'] = kmeans.fit_predict(df[['LATITUDE', 'LONGITUDE']])
    centers = kmeans.cluster_centers_ # Coordinates of cluster centers.
    labels = kmeans.predict(df[['LATITUDE', 'LONGITUDE']]) # Labels of each point

    nomi = pgeocode.Nominatim('US')
    coord = nomi.query_postal_code(str(zipcode))["latitude"], nomi.query_postal_code(str(zipcode))["longitude"]
    nearestCenterLabel, nearestDist = None, float('inf')
    for label, center in enumerate(centers):
        currDist = getDistFromLatLong(center, coord)
        if currDist < nearestDist:
            nearestDist = currDist
            nearestCenterLabel = label
    
    df_satisfy = df.loc[df['coord_label'] == nearestCenterLabel]
    df_satisfy = df_satisfy.loc[df_satisfy['weather'] == "Clear"]
    df_satisfy = df_satisfy[df_satisfy.apply(lambda x: x['Period'] == convertToAMPM(hour_of_day), axis=1)]
    df_satisfy = df_satisfy[df_satisfy.apply(lambda x: getDistFromLatLong((x['LATITUDE'], x['LONGITUDE']), coord) <= radius, axis=1)]
    df_satisfy = df_satisfy.drop_duplicates(keep="first")
    df_final = df_satisfy
    df_final['distance_ft'] = df_final['distance'].apply(lambda x: convertDist(x))

    kmeans = KMeans(n_clusters=3, init ='k-means++')
    kmeans.fit(df_final[['distance_ft', 'popularity_score', 'GAIN', 'RATING']]) # Compute k-means clustering.
    df_final['final_label'] = kmeans.fit_predict(df_final[['distance_ft', 'popularity_score', 'GAIN', 'RATING']])
    centers = kmeans.cluster_centers_ # Coordinates of cluster centers.
    labels = kmeans.predict(df_final[['distance_ft', 'popularity_score', 'GAIN', 'RATING']]) # Labels of each 

    highestRatingCenterLabel = np.argmax(centers, axis=0)[-1] # rating is at the last column
    df_final = df_final.loc[df_final['final_label'] == highestRatingCenterLabel]   
    df_final = df_final.sort_values(by=['RATING'], ascending=False) 
    df_final = df_final.rename(columns={"LATITUDE": "latitude", "LONGITUDE": "longitude"})
    df_final = df_final.drop_duplicates(subset=['TITLE'])
    return df_final.head(3)