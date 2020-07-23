# Mountain Biking Trail EDA: 
## What attributes are associated with highly rated trails?

<img src="https://raw.githubusercontent.com/jeffbauerle/MTB-Trail-EDA/master/images/wordcloud_bike_after.png"
    width="1200" height="600"/>

## Background

I like to mountain bike. I enjoy looking at the "Best of" section of MTB Project's website to see what the most highly rated trails are, see if there's any new ones on the list, and target them for trips. I thought it would be interesting to see if there are any features about trails that leads them to be "highly rated", which get them on my radar. 

If there were features about the trails that were associated with its star rating, I want to see if there are regional differences.

![alt text](https://raw.githubusercontent.com/jeffbauerle/MTB-Trail-EDA/master/images/top_rated.png)


## Data

![alt text](https://holimont.com/wp-content/uploads/2020/03/mtb_project.png)


"MTB Project provides an API for developers to access it's data. MTB Project provides a simple API with access to certain limited data. All of the data returned by the API is already available on publicly available pages on the MTB Project site. Returned data is json."

[MTB Project Data API](https://www.mtbproject.com/data)

Method: getTrails

|#  | column   | Non-null count  | DType  |
|---|---|---|---|
| 0  | id  |  1200 non-null | int64  |
|  1 | name  | 1200 non-null  |  object |
|  2 | type  |  1200 non-null | object  |
|  3 | ***summary***  |  1200 non-null | object  |
|  4 | ***difficulty***  | 1200 non-null  | object  |
|  5 | ***stars***  | 1200 non-null  | float64  |
|   6| starVotes  |  1200 non-null | int64  |
|   7| location  | 1200 non-null  | object  |
|   8| url  | 1200 non-null  | object  |
|   9|  imgSqSmall | 1200 non-null  | object  |
|   10| imgSmall  | 1200 non-null  | object  |
|   11| imgSmallMed  | 1200 non-null  | object  |
|   12| imgMedium  | 1200 non-null  | object  |
|   13| ***length***  | 1200 non-null  | float64  |
|   14| ***ascent***  | 1200 non-null  | int64  |
|   15| descent  | 1200 non-null  | int64  |
|   16| high  | 1200 non-null  | int64  |
|   17| low  |  1200 non-null | int64  |
|   18| ***longitude***  | 1200 non-null  | float64  |
|   19| ***latitude***  | 1200 non-null  | float64  |
|   20| conditionStatus  | 1200 non-null  | object  |
|   21| conditionDetails  | 868 non-null  | object  |
|   22| conditionDate  | 1200 non-null  | object  |

Regions considered:

Selected locations from this list, plus local (Denver) and alleged birthplace of MTB (Marin County)

[The Top 10 Best Mountain Bike Destinations in the USA](https://www.singletracks.com/mtb-trails/the-top-10-best-mountain-bike-destinations-in-the-usa/)

### Data Pipeline



## Exploratory Data Analysis

### Subtitle

![](src/readme/imgs/2343.jpg)

## Conclusions



## Further Work


