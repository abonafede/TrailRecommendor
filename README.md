# Trail Recommendor

## Introduction
The trail recommendor aims to provide optimal recommendations for public trails in the region Washington for a particular user.

For example, 

*"I am an enthusiastic hiker but a busy porofessional in Seattle city who wants to explore nature on weekends but avoid the crowds"*. 

This recommendor will provide me the best trails available in the area according to my preferences. 

## Getting Live Recommendations
In order to get recommendations using this project, follow the guidelines below;

- Install `streamlit` on your machine
- Run `streamlit run demo.py`
- Once the window pops up, enter your *zipcode*, distance to *drive*, *date* and *time* of your visit.

## Data sources
The goal of this project was to collect historical weather, trails information, and hikers' foot traffic on the trails. 

We used the following to accomplish that;

| Source      | Description | Type | Key metrics |
| ----------- | ----------- |------|----|
| [Washington Trails Association](https://www.wta.org/)| Washington Trails Association is a non-profit organization that advocates protection of hiking trails and wilderness, conducts trail maintenance, and promotes hiking in Washington state.| Web scrapping | Elevation gain, Distance, Difficulty level, Location etc. |
| [Trailforks](https://www.trailforks.com/)   | Trailforks is a trail database, map & management system for users, builders and associations. A platform for trail associations to keep track of trail conditions, builders to log work & users to discover, plan and share their activities.| Web scrapping | User checkins for year, month, date, and hour of a day.|
| [Visual Crossing](https://www.visualcrossing.com/) | Visual Crossing is a leading provider of weather data and enterprise analysis tools to data scientists, business analysts, professionals, and academics. | API | For a particular day and hour; Sunny, Rainy etc.|


## Recommendation Model
The project uses knn clustering to arrange trails with similar *usage* and *popularity* and predicts the ones with lower popularity within hiker's given radius. 