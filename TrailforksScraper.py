# This is a script to get information of trail popularity from https://www.trailforks.com/

import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


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
        search_url = self.url + 'region/united-states/?activitytype=6&z=10.4&lat=48.30699&lon=-120.42421&trailstyle=popularity'
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
    
    def fetchTrailsByRegionAndPages(self,region,pages):
        '''
        Scrapes trails data from trailforks

        Inputs:
            region: name of region such as washington, north-carolina
        Returns:
            Dataframe containing trail data for a given region
        '''

        # Specify headers, url and params
        try:
            self.data = pd.DataFrame()
            for page in range(0,pages):
                search_url = self.url + '/region/' + region + '/trails/?activitytype=6&page=' + str(page) + '&sort=t.popularity_score&order=asc'
                # Request the page and use BeautifulSoup to extract the contents
                page = requests.get(search_url)
                soup = BeautifulSoup(page.content, 'html.parser')
                table = soup.find_all('table')
                self.data = pd.concat([self.data,pd.read_html(str(table))[0]])
        except Exception as e:
            print('Error occurred')
            print(e)

        return self.data
    
    def fetchTrailStats(self,trail):
        '''
        Scrapes trails data from trailforks

        Inputs:
            trail: name of trail such as rattlesnake-ledge-trail
        Returns:
            Dataframe containing trail stats 
        '''

        # Specify headers, url and params
        try:
            self.data = pd.DataFrame()
            search_url = self.url + '/trails/'+ trail+ '/stats/'
            # Request the page and use BeautifulSoup to extract the contents
            page = requests.get(search_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            checkins = soup.find_all('div',class_='col-6 last')
            
            # Extract checkins per year
            checkins_per_year = str(checkins[0])
            checkins_per_year = checkins_per_year[checkins_per_year.index('Year')-2:checkins_per_year.rindex(']')+1]
            df = pd.read_csv(StringIO(checkins_per_year))
            checkins_per_year = df.iloc[:,:2]
            
            # Extract checkins per month
            checkins_per_month = str(checkins[1])
            checkins_per_month = checkins_per_month[checkins_per_month.index('Month')-2:checkins_per_month.rindex(']')+1]
            df = pd.read_csv(StringIO(checkins_per_month))
            checkins_per_month = df.iloc[:,:2]
            
            self.data = pd.concat([checkins_per_year,checkins_per_month])
                
        except Exception as e:
            print('Error occurred')
            print(e)

        return self.data
    
s = trailforksScrapper()
search_url = 'https://www.trailforks.com/trails/rattlesnake-ledge-trail/stats/'
page = requests.get(search_url)
soup = BeautifulSoup(page.content, 'html.parser')

#print(s.fetchTrailStats('rattlesnake-ledge-trail'))