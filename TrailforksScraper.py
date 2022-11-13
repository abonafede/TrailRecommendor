# This is a script to get information of trail popularity from https://www.trailforks.com/

import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import numpy as np


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
    
    def cleanUpCheckins(self,checkins, period):
        checkins = checkins[checkins.index(period)-2:checkins.rindex(']')+1]
        df = pd.read_csv(StringIO(checkins))
        checkins = pd.DataFrame({'Period':df.iloc[:,0],'Check-Ins':df.iloc[:,1]})
        return checkins
        
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
            checkins = soup.find_all('div',class_='col-6')
            
            # Extract checkins per year
            checkins_per_hour = self.cleanUpCheckins(str(checkins[1]),'Year')
            
            # Extract checkins per hour
            checkins_per_year = self.cleanUpCheckins(str(checkins[2]),'Hour')
            
            # Extract checkins per month
            checkins_per_month = self.cleanUpCheckins(str(checkins[3]),'Month')
            
            # Extract checkins per date
            checkins = soup.find_all('div',class_='block')
            for i in range(0,len(checkins)):
                if "data.addColumn('date', 'Date')" in str(checkins[i]):
                    checkins_per_date =  str(checkins[i])
                    break;
            checkins_per_date = checkins_per_date[checkins_per_date.index('new Date')-2:checkins_per_date.rindex(']')+1]
            df = pd.read_csv(StringIO(checkins_per_date))
            dates = np.add.reduce(df[df.iloc[:,:3].columns].astype(str), axis=1)
            checkins = df.iloc[:,3]
            checkins_per_date = pd.DataFrame({'Period':dates,'Check-Ins':checkins})
            checkins_per_date = checkins_per_date[checkins_per_date['Period'].str.contains('new Date')]
            checkins_per_date['Period'] = checkins_per_date['Period'].replace("new Date","",regex=True)
            checkins_per_date['Check-Ins'] = checkins_per_date['Check-Ins'].str.replace('\W', '')
            
            df = pd.concat([checkins_per_year,checkins_per_month,checkins_per_hour,checkins_per_date])
            df['Period'] = df['Period'].str.replace('\W', '')
            df = df.dropna()
            self.data = df
                
        except Exception as e:
            #print('Error occurred')
            #print(e)
            return

        return self.data
  


if __name__ == '__main__': # testing 
    s = trailforksScrapper()
    # popularity_df = s.fetchTrailPopularity()
    # print(popularity_df)
    # print("------------------------------------------------")
    search_url = 'https://www.trailforks.com/trails/rattlesnake-ledge-trail/stats/'
    page = requests.get(search_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = s.fetchTrailStats('rattlesnake-ledge-trail')
    print(result)
    result = result.fillna('')
    result = pd.DataFrame({'Period':np.add.reduce(result[['Hour','Month','Year','Date']].astype(str), axis=1),'Check-Ins':result['Check-Ins']})
    print(result)
    print(result['Date'].unique())