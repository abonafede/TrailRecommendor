# This script is NOT mine originally.
#It was made by Yoshio Hasegawa
# Various Edits added by Andrew Bonafede to accomadate for specific use case needs.
# wta-scraper/WTA_Hike_Scraper.py
#*************************************************************************************
# Programmer: Yoshio Hasegawa
# Class Name: None
# Super Class: None
#
# Revision     Date                        Release Comment
# --------  ----------  --------------------------------------------------------------
#   1.0     5/1/2019   Initial Release
#
# File Description
# ------------------------------------------------------------------------------------
# This is an ETL script that retrieves and organizes hike data from Washington Trails 
# Association's (WTA) web domain. The primary sub-domain this script explores is, 
# https://www.wta.org/go-outside/hikes. From this location, hike results page URLs 
# are retrieved. Then, each individual hike URL is parsed out and stored. Each 
# individual hike URL is used to gather information found on every hike page hosted 
# on WTA's website. Finally, this data is formatted into a DataFrame and, that 
# DataFrame is written to a CSV file. 
#
# This script was mostly created for exploratory research and personal interest in
# local hike data. Washington is full of beautiful places to explore! I simply 
# wanted to share this information with others :)
#
# Methods
# ------------------------------------------------------------------------------------
#       Name                                         Description
# ----------------------------------  ------------------------------------------------
# get_html_rows()                     Gets HTML code for a given website.
#
# get_hike_results_urls_list()        Returns a list of URLs for hike results found 
#                                     under this sub-domain:
#                                     'https://www.wta.org/go-outside/hikes'.
#
# get_individual_hike_urls()          Returns a list of individual hike URLs found on
#                                     hike results pages on WTA's website.
#
# get_individual_hike_data()          Returns formatted hike data hosted on WTA's
#                                     website.
#*************************************************************************************
# Imported Packages:
import pandas as pd
import requests
import urllib3
from bs4 import BeautifulSoup
import json
from datetime import datetime
from geopy.geocoders import Nominatim

# Initializing the current date for documentation purposes:
DATE = datetime.now().date()
# Initializing the project results folder path:
RESULTS_PATH = ''


#*************************************************************************************
# Method: main()
#
# Description
# ------------------------------------------------------------------------------------
# Method Main, responsible for proper execution of this script.
#
# First, all hike results page URLs are retrieved. With each hike results page URL,
# each individual hike URL is parsed out, retrieved and stored. Then, with each
# individual hike URL, data for each hike page hosted on WTA's website is extracted.
# This data is then formatted and stored in a DataFrame. Finally, this DataFrame
# containing all hike data from WTA's website is written to a CSV file.
#
#     RETurn
#      Type                                Description
# --------------  --------------------------------------------------------------------
# None
#
# ------------------------------- Arguments ------------------------------------------
#     Type               Name                         Description
# --------------  ------------------  ------------------------------------------------
# None
#*************************************************************************************
def main():
    """Method Main, responsible for proper execution of this script :)
    
    Instruction
    -----------
    Please edit the variable, RESULTS_PATH, which specifies the path for 
    the output of the final DataFrame.

    Arguments
    ---------
    None
    
    Raises
    ------
    None
    
    Returns
    -------
    None
    """

    print('\n>> Washington Trail Association Web Scraper <<\n')

    # Disabling insecure warnings to avoid printing multiple unnecessary warnings.
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print('\nGetting All URLs to Hike Results Pages...')
    # Retrieving a list of all hike results page URLs:
    all_hike_results_list_urls = list(set().union(
        get_hike_results_urls_list('https://www.wta.org/go-outside/hikes'),
                                  ['https://www.wta.org/go-outside/hikes']))
    print('  >> All URLs to Hike Results Pages Found: {0} Total URLs'.format(
        len(all_hike_results_list_urls)))

    # Retrieving all individual hike URLs with, 
    # the list of all hike results page URLs:
    all_individual_hike_urls = get_individual_hike_urls(all_hike_results_list_urls)

    # Retrieving and formatting all individual hike data with,
    # the list of all individual hike URLs:
    wta_hikes = get_individual_hike_data(all_individual_hike_urls)

    #Drop hikes without Lat/Long
    wta_hikes = wta_hikes.dropna(subset=['LATITUDE','LONGITUDE'])
    
    # Writing the formatted hike data to a CSV file:
    wta_hikes.to_csv('ResultsZip.csv')
    wta_hikes.to_json('ResultsZip.json')

    print('\n>> WTA Hike Data Scraping Complete <<\n')

#*************************************************************************************
# Method: get_html_rows(String)
#
# Description
# ------------------------------------------------------------------------------------
# Using Requests and BeautifulSoup, this method retrieves HTML code for a given URL. 
# The HTML code is split by line and, each line of code is entered as a value in a
# list. Finally, this list is returned value.
#
#     RETurn
#      Type                                Description
# --------------  --------------------------------------------------------------------
# List            Each value is a line of HTML code for the given URL.
#
# ------------------------------- Arguments ------------------------------------------
#     Type               Name                         Description
# --------------  ------------------  ------------------------------------------------
# String          url                 The URL for the desired HTML code.
#*************************************************************************************
def get_html_rows(url):
    """This method returns HTML code for a given URL as a list. Each value in the list
    corresponds to each line of the HTML code.

    Arguments
    ---------
    1. url {String} -- The URL for the desired HTML code.
    
    Raises
    ------
    None
    
    Returns
    -------
    List -- The HTML code for the given URL, split by lines.
    """

    # Getting a requests response from the given URL.
    resp = requests.get(url, verify=False)
    # Parsing the request response:
    soup = BeautifulSoup(resp.content, 'html5lib')
    # Formatting the parsed response:
    html = soup.prettify()
    # splitting the formatted HTML code into a list of lines:
    html_lines_list = html.splitlines()

    return html_lines_list


#*************************************************************************************
# Method: get_hike_results_urls_list(String, Boolean)
#
# Description
# ------------------------------------------------------------------------------------
# This method will extract all URLs to webpages containing lists of hikes and,
# will return all hike results page URLs as a list using recursion. Note, this method
# does not include 'https://www.wta.org/go-outside/hikes' in the returned list. So, 
# it may be best to append this URL to your final returned list.
#
#     RETurn
#      Type                                Description
# --------------  --------------------------------------------------------------------
# List            A list of all hike results page URLs.
#
# ------------------------------- Arguments ------------------------------------------
#     Type               Name                         Description
# --------------  ------------------  ------------------------------------------------
# String          url                 This URL should be
#                                     'https://www.wta.org/go-outside/hikes'
#
# Boolean         last_page           This argument is edited through recursive
#                                     techniques in order to exit the recursive loop.
#                                     Thus, initially, no value should be passed for 
#                                     this argument
#*************************************************************************************
def get_hike_results_urls_list(url, last_page = None):
    """This method retrieves and returns a list of URLs. 
    These URLs route to webpages under www.wta.org/ that contain lists of hikes.

    Arguments
    ---------
    1. url {string} -- This URL should be: 'https://www.wta.org/go-outside/hikes'
    2. last_page {boolean} -- This argument is handled through the recursive techniques.
    
    Raises
    ------
    None
    
    Returns
    -------
    list -- A list of all hike results page URLs.
    """

    # Retireve the HTML code for url as a list of lines.
    html_rows = get_html_rows(url)

    checker = False
    exiter = False
    active_page = 0
    index_start = 0
    index_end = 0

    itr = -1
    # Iterate over the list of HTML lines.
    for row in html_rows:
        itr += 1

        # '"active"' will indicate the starting index point for where the URLs
        # for hike pages are located in the HTML code. It also allows for the
        # variable storing the URL for the active page or current page to
        # be initialized.
        if '"active"' in row:
            index_start = html_rows.index(row)
            active_page = int(html_rows[itr + 2].lstrip())

        # '"last"' will indicate the ending index point for where the URLs
        # for hike pages are located in the HTML code. It also allows for the
        # variable storing the URL for the last page to be initialized.
        # Additionally, if we locate '"last"', we have successfully retrieved
        # all of the hike results page URLs and we can break from this loop.
        if '"last"' in row:
            index_end = html_rows.index(row)
            last_page = int(html_rows[itr + 2].lstrip())
            checker = True
            break
        # checker == False means "'last'" was not found.
        # If "'next'" is found we will retrieve the index range for the hike
        # page URLs found and break from this loop. This also initializes the variable
        # 'exiter' to True which will end our recursive loop.
        elif checker == False and '"next"' in row:
            index_end = html_rows.index(row)
            last_page = int(html_rows[itr - 3].lstrip())
            checker = True
            exiter = True
            break
        elif checker == False and active_page == last_page:
            return

    # Initializing the index range where hike results page URLs are found.
    rows_range = html_rows[index_start : index_end]
    # Initializing the URLs as a list.
    pages_found = [item[item.find('https') : item.find('">')] 
                    for item in rows_range if 'www.wta.org' in item]
    # Initializing the next page to parse through as the first URL in the 'pages_found' list.
    next_page = pages_found[0]

    print(' > URL Found: {0}'.format(pages_found[0]))
    # If 'exiter' == True, we will exit our recursive loop. 
    # Otherwise, keep running this recursive method.
    if exiter == True:
        return pages_found
    else:
        return list(set().union(pages_found,
                                get_hike_results_urls_list(next_page, last_page)))


#*************************************************************************************
# Method: get_individual_hike_urls(list)
#
# Description
# ------------------------------------------------------------------------------------
# Using a list of URLs to webpages containing lists of hikes, this method will
# find all URLs routing to webpages hosting information on individual hikes found on 
# each of the URLs in the list passed to this method.
#
#     RETurn
#      Type                                Description
# --------------  --------------------------------------------------------------------
# list            A list of URLs that route to individual hike pages.
#
# ------------------------------- Arguments ------------------------------------------
#     Type               Name                         Description
# --------------  ------------------  ------------------------------------------------
# list            hike_page_urls      This list should be a list of URLs that route to 
#                                     webpages containing lists of hikes.
#*************************************************************************************
def get_individual_hike_urls(hike_page_urls):
    """This method retrieves and returns a list of URLs to webpages. 
    These webpages are the individual hikes hosted on www.wta.org/.

    Arguments
    ---------
    1. hike_page_urls {list} -- A list of URLs that route to webpages containing lists of hikes.
    
    Raises
    ------
    None
    
    Returns
    -------
    list -- A list of URLs that route to individual hike pages.
    """

    print('\nGetting All URLs to Individual Hikes...')

    hike_urls_list = []

    # Parse through all URLs...
    for url in hike_page_urls:
        html_rows = get_html_rows(url)

        #Parse through HTML code for each URL...
        for row in html_rows:

            # Append the individual hike URL to a list...
            if "listitem-title" in row:
                hike_link = row[row.find('https') : row.find('" title=')]
                hike_urls_list.append(hike_link)
        
        print(' > Total Hike URLs: {0}'.format(len(hike_urls_list)))

    print('  >> All Individual Hike URLs Extracted: {0} Total URLs'.format(len(hike_urls_list)))
    # Return the list containing all individual hike URLs.
    return hike_urls_list


#*************************************************************************************
# Method: get_individual_hike_data(list)
#
# Description
# ------------------------------------------------------------------------------------
# Using a list of URLs that route to webpages containing information on individual 
# hikes, this method will return specific information for each hike in the format of a
# DataFrame.
#
#     RETurn
#      Type                                Description
# --------------  --------------------------------------------------------------------
# DataFrame       A DataFrame consisting of organized hike data.
#
# ------------------------------- Arguments ------------------------------------------
#     Type               Name                         Description
# --------------  ------------------  ------------------------------------------------
# list            hike_urls           This list should be a list of URLs that route to
#                                     webpages containing information on individual
#                                     hikes
#*************************************************************************************
def get_individual_hike_data(hike_urls):
    """Using a list of URLs that route to webpages containing information on 
    individual hikes, this method will retrieve and organize hike data. Then, it will
    return hike data in the format of a DataFrame.

    Arguments
    ---------
    1. hike_urls {list} -- A list of URLs routing to individual hikes.
    
    Raises
    ------
    None
    
    Returns
    -------
    DataFrame -- Clean, organized and actionable hike data :)
    """
    
    print('\nGetting Individual Hike Data...')

    titles = []
    regions = []
    distances = []
    dist_types = []
    gains = []
    highests = []
    ratings = []
    rating_counts = []
    latitudes = []
    longitudes = []
    report_counts = []
    report_dates = []
    hike_urls2 = []

    rownum = 1
    # Parse through all individual hike URLs...
    for url in hike_urls:
        # Get HTML code as a list of lines.
        hike_html_rows = get_html_rows(url)

        itr1 = -1
        # Parse through HTML code...
        for row in hike_html_rows:
            itr1 += 1

            # Messy/Hacky initialization of data fields based on
            # HTML code...

            # Retrieving the hike title...
            if '"documentFirstHeading"' in row:
                hike_title = hike_html_rows[itr1 + 1].lstrip()
                titles.append(hike_title)

            # Retrieving the hike region...
            if '"hike-region"' in row:
                hike_region = hike_html_rows[itr1 + 3].lstrip()
                regions.append(hike_region)

            # Retrieving the hike distance and distance type...
            if '"distance"' in row:
                hike_distance_string = hike_html_rows[itr1 + 2].lstrip()
                hike_distance = float(hike_distance_string[ : hike_distance_string.find(' mile')])
                if ',' in hike_distance_string:
                    hike_distance_type = hike_distance_string[hike_distance_string.find(', ') + 2 : ]
                elif 'of trails' in hike_distance_string:
                    hike_distance_type = hike_distance_string[hike_distance_string.find('of trails') + 3 : ]
                else:
                    hike_distance = 'ERROR'
                distances.append(hike_distance)
                dist_types.append(hike_distance_type)

            # Retrieving the hike gain...
            if 'Gain:' in row:
                hike_gain = float(hike_html_rows[itr1 + 2].lstrip())
                gains.append(hike_gain)

            # Retrieving the hike highest point...
            if 'Highest Point:' in row:
                hike_highest = float(hike_html_rows[itr1 + 2].lstrip())
                highests.append(hike_highest)

            # Retrieving the hike rating...
            if '"current-rating"' in row:
                rating_string = hike_html_rows[itr1 + 1].lstrip()
                hike_rating = float(rating_string[ : rating_string.find(' out of')])
                ratings.append(hike_rating)

            # Retrieving the hike rating count...
            if '"rating-count"' in row:
                rating_count_string = hike_html_rows[itr1 + 1].lstrip()
                rating_count = int(rating_count_string[rating_count_string.find('(') + 1 : rating_count_string.find(' vote')])
                rating_counts.append(rating_count)

            # Retrieving the hike geographic location...
            if '<script type="application/ld+json">' in row:
                json_string = hike_html_rows[itr1 + 1].lstrip()
                try:
                    hike_json = json.loads(json_string)
                    latitude = hike_json['geo']['latitude']
                    longitude = hike_json['geo']['longitude']
                    latitudes.append(latitude)
                    longitudes.append(longitude)
                except:
                    pass


        # If any of the above data fields were not found,
        # append a None value to the corresponding list in order to
        # keep all lists of data fields in line with each other.
        if len(titles) != rownum:
            titles.append(None)

        if len(regions) != rownum:
            regions.append(None)

        if len(distances) != rownum:
            distances.append(None)

        if len(dist_types) != rownum:
            dist_types.append(None)

        if len(gains) != rownum:
            gains.append(None)

        if len(highests) != rownum:
            highests.append(None)

        if len(ratings) != rownum:
            ratings.append(None)

        if len(rating_counts) != rownum:
            rating_counts.append(None)
        
        if len(latitudes) != rownum:
            latitudes.append(None)

        if len(longitudes) != rownum:
            longitudes.append(None)


        # Retrieve the URL for the corresponding trip report and,
        # get the HTML code for that URL.
        report_url = url + '/@@related_tripreport_listing'
        report_html_rows = get_html_rows(report_url)
        report_date_list = []

        itr2 = -1
        # Parse through the HTML code for the hike's trip report URL...
        for row in report_html_rows:
            itr2 += 1

            # More Messy/Hacky initialization of data fields based on
            # HTML code...

            # Retrieving the hike trip report counts...
            if '"count-data"' in row:
                report_count = int(report_html_rows[itr2 + 1].lstrip())
                report_counts.append(report_count)

            # Retrieving the hike trip report date...
            if '"elapsed-time"' in row:
                report_date = datetime.strptime(row[row.find('title="') + 7 : row.find('">')], '%b %d, %Y')
                report_date_list.append(report_date)

        # If any of the above data fields were not found,
        # append a None value to the corresponding list in order to
        # keep all lists of data fields in line with each other.
        if len(report_counts) != rownum:
            report_counts.append(None)

        # Special Case: If the trip report date list is not empty,
        # append the first date to the final report_dates list
        # that will be used for creating the final DataFrame.
        # We only want the most recent trip report date.
        if len(report_date_list) != 0:
            report_dates.append(report_date_list[0])
        # Else, append None value... to keep things in line.
        elif len(report_dates) != rownum:
            report_dates.append(None)

        # We also want to include a column of the hike URLs :)
        hike_urls2.append(url)

        # Print performance...
        if rownum < 6:
            print(' > ' + str(rownum) + ' Hikes Loaded...')
        elif rownum < 50 and rownum % 5 == 0:
            print(' > ' + str(rownum) + ' Hikes Loaded...')
        else:
            if rownum % 50 == 0:
                print(' > ' + str(rownum) + ' Hikes Loaded...')
        rownum += 1

    # Print more performance stuff...
    print('\nAll Hikes Loaded!\n > ' + str(rownum - 1) + ' Hikes Successfully Loaded\n')
    print('----------------------------------')
    print('  - titles: ', len(titles), 'Entries')
    print('  - regions: ', len(regions), 'Entries')
    print('  - distances: ', len(distances), 'Entries')
    print('  - dist_types: ', len(dist_types), 'Entries')
    print('  - gains: ', len(gains), 'Entries')
    print('  - highests: ', len(highests), 'Entries')
    print('  - ratings: ', len(ratings), 'Entries')
    print('  - rating_counts: ', len(rating_counts), 'Entries')
    print('  - latitudes: ', len(latitudes), 'Entries')
    print('  - longitudes: ', len(longitudes), 'Entries')
    print('  - report_dates: ', len(report_dates), 'Entries')
    print('  - report_counts: ', len(report_counts), 'Entries')
    print('  - hike_links: ', len(hike_urls2), 'Entries')
    print('----------------------------------')

    # Initialize the final DataFrame that houses all hike data in an organize fashion!
    hike_data = pd.DataFrame({'TITLE': titles, 'REGION': regions, 'DISTANCE': distances,
                              'DIST_TYPE': dist_types, 'GAIN': gains, 'HIGHEST': highests,
                              'RATING': ratings, 'RATING_COUNT': rating_counts, 
                              'LATITUDE': latitudes, 'LONGITUDE': longitudes, 
                              'REPORT_DATE': report_dates, 'REPORT_COUNT': report_counts, 
                              'URL': hike_urls2})

    # Sort final DataFrame by hike title:
    hike_data.sort_values(by=['TITLE'], inplace=True)
    # Return final DataFrame:
    return hike_data




######################################################################################
#                         Method Main Execution If Statement                         #
######################################################################################
if __name__ == '__main__':
    main()