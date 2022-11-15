# This is a script to get information of trail ratings for different date and time from https://www.alltrails.com

import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import numpy as np

class AllTrailsScrapper:
    def __init__(self, url="https://www.alltrails.com"):
        self.url = url
    
    def fetchAllTrailsByRegion(self, region):
        '''
        Scrapes trails data from trailforks

        Inputs:
            region: name of region such as washington, north-carolina
        Returns:
            Dataframe containing trail data for a given region
        '''

        # Specify headers, url and params
        search_url = self.url + '/us/' + region
        print("search_url:", search_url)
        try:
            # Request the page and use BeautifulSoup to extract the contents
            page = requests.get(search_url)
            soup = BeautifulSoup(page.content, 'html5lib')
            print(soup)
            table = soup.find_all('div')
            self.data = pd.read_html(str(table))[0]
        except Exception as e:
            print('Error occurred')
            print(e)

        return self.data

# testing
if __name__ == '__main__':
    region = 'north-carolina'
    s = AllTrailsScrapper()
    popularity_df = s.fetchAllTrailsByRegion(region)
    print(popularity_df)