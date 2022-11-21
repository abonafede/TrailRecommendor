import json
from datetime import datetime

import pandas as pd
from urllib import request, error

visited = dict()
storage = dict()


def query(latitude, longitude, report_date):
    try:
        value = datetime.fromisoformat(report_date)
    except Exception:
        print(f'{str(report_date)} is invalid')
        return None
    serialized = serialize(latitude, longitude, report_date)
    if serialized in visited:
        print('visited')
        return visited[serialized]
    try:
        ResultBytes = request.urlopen(
            "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" +
            f"{latitude}%2C{longitude}/{report_date}/{report_date}?unitGroup=metric&key=KG4U6KJ7GSZYV59V8KA3CW7LQ&" +
            "contentType=json")
        # Parse the results as JSON
        json_data = json.loads(ResultBytes.read())
        visited[serialized] = json_data['days'][0]['conditions']
        storage[serialized] = json_data

        return visited[serialized]
    except error.HTTPError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        return None
    except error.URLError as e:
        ErrorInfo = e.reason
        print('Error reason: ', ErrorInfo)
        return None


def serialize(latitude, longitude, report_date):
    return f'{latitude}#{longitude}#{report_date}'


if __name__ == '__main__':
    df = pd.read_csv('combined-trails.csv.zip', compression={'method': 'zip'})
    df.apply(lambda row: query(row['LATITUDE'], row['LONGITUDE'], row['REPORT_DATE']), axis=1)
    print(len(visited))
    df['weather'] = df.apply(lambda row: query(row['LATITUDE'], row['LONGITUDE'], row['REPORT_DATE']), axis=1)
    assert 'weather' in df.columns
    df.to_csv('combined-trails-w-weather.csv.zip', compression={'method': 'zip'})
    with open('storage.json', 'a') as f:
        json.dump(storage, f)
