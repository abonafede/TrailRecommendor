# This is a script to get information of trail popularity from https://www.trailforks.com/

import requests
import json
import os
import numpy as np
import pandas as pd


class trailforksSearch:
    def __init__(self,url="https://www.trailforks.com"):
        self.url = url

    def fetchPopularityData(self): # still buggy
        '''
        Gets all the trails data from trailforks

        Inputs:
            None
            
        Returns:
            df(DataFrame): a dataframe containing information on trails that match the search query
        '''
        url = self.url + '/region/united-states/trails/?sort=t.popularity_score&order=desc&difficulty=2,3,4,11,9,5,6,8&activitytype=6'
        try:
            # Get response
            print("url", url)
            # Request the page and use BeautifulSoup to extract the contents
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Scrape data from specific tags
            data = soup.find_all('tr')

            # Find column names (the first row)
            columns_data = data[0].find_all('th')
            columns = [col.get_text() for col in columns_data]
            print("columns", columns)
            # Find all data in each row 
            all_data = []
            for raw_row in data[1:]: 
                row = [elem.get_text() for elem in raw_row.find_all('td')]
                all_data.append(row)

            # Finally create trail dataframe
            self.data = pd.DataFrame(all_data, columns = columns)
            return self.data
            
        except Exception as e:
            print('Error occurred')
            print(e)


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