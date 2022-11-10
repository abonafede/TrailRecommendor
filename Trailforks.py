# This is a script to get information of trail popularity from https://www.trailforks.com/

import requests
import json
import os
import numpy as np
import pandas as pd


class trailforksSearch:
    def __init__(self,url="https://www.trailforks.com"):
        self.url = url

    def fetchData(self):
        '''
        Gets all the trails data from trailforks

        Inputs:
            
        Returns:
            df(DataFrame): a dataframe containing information on trails that match the search query
        '''

        # Specify headers, url and params
        search_url = self.url + '/api/1/trails?api_key=docs'
        try:
            # Get response
            response = requests.get(search_url)
            # Decode
            self.data = pd.DataFrame(response.json()['data'])
            
        except Exception as e:
            print('Error occurred')
            print(e)

        return self.data
    
    def fetchDataByTrailType(self, trailtype):
        '''
        Gets all the trails data from trailforks by given trailtype

        Inputs:
            
        Returns:
            df(DataFrame): a dataframe containing information on trails that match the search query
        '''

        # Specify headers, url and params
        search_url = self.url + '/api/1/trails?api_key=docs&filter=trailtype%3D' + trailtype
        try:
            # Get response
            response = requests.get(search_url)
            # Decode
            self.data = pd.DataFrame(response.json()['data'])
            
        except Exception as e:
            print('Error occurred')
            print(e)

        return self.data