# This is a script to get information of trail popularity from https://www.trailforks.com/

import requests
import pandas as pd
from bs4 import BeautifulSoup


class trailforksScrapper:
    def __init__(self,url="https://www.trailforks.com"):
        self.url = url

    def fetchTrailPopularity(self):
        '''
        Scrapes trails data from trailforks

        Inputs:
            
        Returns:
            df(DataFrame): a dataframe containing information on trails that match the search query
        '''

        # Specify headers, url and params
        search_url = self.url + '/region/united-states/trails/?sort=t.popularity_score&order=desc&difficulty=2,3,4,11,9,5,6,8&activitytype=6'
        try:
            # Get response
            response = requests.get(search_url)
            # Decode
            self.data = pd.DataFrame(response.json()['data'])
            
        except Exception as e:
            print('Error occurred')
            print(e)

        return self.data
    
    def fetchTrailPopularityByName(self,name):
        '''
        Scrapes trails data from trailforks

        Inputs:
            Name: name of the trail e.g. lanham-lake-trail-70813
        Returns:
            Raw text containing popularity score for a given trail
        '''

        # Specify headers, url and params
        search_url = self.url + '/trails/' + name
        try:
            # Request the page and use BeautifulSoup to extract the contents
            page = requests.get(search_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            # Decode
            self.data = soup.find(attrs={'id':'popularity_activity'}).text

            
        except Exception as e:
            print('Error occurred')
            print(e)

        return self.data
    
    def fetchAllTrailsByRegion(self,region):
        '''
        Scrapes trails data from trailforks

        Inputs:
            region: name of region such as washington, north-carolina
        Returns:
            Dataframe containing trail data for a given region
        '''

        # Specify headers, url and params
        search_url = self.url + '/region/' + region + '/trails/'
        try:
            # Request the page and use BeautifulSoup to extract the contents
            page = requests.get(search_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find_all('table')
            self.data = pd.read_html(str(table))[0]
        except Exception as e:
            print('Error occurred')
            print(e)

        return self.data
