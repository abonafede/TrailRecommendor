import argparse
import json
import sys
from urllib import request, error


def query(latitude, longitude, start_date, end_date):
    try:
        ResultBytes = request.urlopen(
            "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" +
            f"{latitude},{longitude}/{start_date}/{end_date}?unitGroup=metric&key=KG4U6KJ7GSZYV59V8KA3CW7LQ&" +
            "contentType=json")
        # Parse the results as JSON
        print(type(ResultBytes))
        json_data = json.loads(ResultBytes.read())

        return json_data
    except error.HTTPError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except error.URLError as e:
        ErrorInfo = e.reason
        print('Error reason: ', ErrorInfo)
        sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query weather data within the given date range')
    parser.add_argument('latitude', type=float, help='a valid US latitude, where the weather data would be queried')
    parser.add_argument('longitude', type=float, help='a valid US longitude, where the weather data would be queried')
    parser.add_argument('start_date', type=str, help='the start of the date range, must be in format yyyy-mm-dd')
    parser.add_argument('end_date', type=str, help='the end of the date range, must be in format yyyy-mm-dd')

    args = parser.parse_args()
    print(query(str(args.latitude), str(args.longitude), args.start_date, args.end_date))
