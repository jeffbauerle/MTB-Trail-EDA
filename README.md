# Mountain Biking Trail EDA: 
## What attributes are associated with highly rated trails?

## Background

I like to mountain bike. I enjoy looking at the "Best of" section of MTB Project's website to see what the most highly rated trails are, see if there's any new ones on the list, and target them for trips. I thought it would be interesting to see if there are any features about trails that leads them to be "highly rated", which get them on my radar. 

If there were features about the trails that were associated with its star rating, I want to see if there are regional differences.

![alt text](https://raw.githubusercontent.com/jeffbauerle/MTB-Trail-EDA/master/images/top_rated.png)


## Data

![alt text](https://holimont.com/wp-content/uploads/2020/03/mtb_project.png)


"MTB Project provides an API for developers to access it's data. MTB Project provides a simple API with access to certain limited data. All of the data returned by the API is already available on publicly available pages on the MTB Project site. Returned data is json."

[MTB Project Data API](https://www.mtbproject.com/data)

Method: getTrails

<img src="https://raw.githubusercontent.com/jeffbauerle/MTB-Trail-EDA/master/images/raw_data_example.png">

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



Regions considered: Denver, Crested Butte, Moab, Park City, Marin County, Sedona

Selected locations from this list, plus local (Denver) and alleged birthplace of MTB: Marin County; contested with Crested Butte.

[The Top 10 Best Mountain Bike Destinations in the USA](https://www.singletracks.com/mtb-trails/the-top-10-best-mountain-bike-destinations-in-the-usa/)

### Data Pipeline
Loaded JSON files into my Python script, converted and normalized dataframe. Added columns: ascent/mile, and descent/mile, recoded location and then concatenated the dataframes.


## Exploratory Data Analysis

<figure>
<img src="https://raw.githubusercontent.com/jeffbauerle/MTB-Trail-EDA/master/images/wordcloud_bike_after.png"
    width="1000" height="500"/>
    <figcaption>Wordcloud generated from 81198 words in the combination of all summaries.</figcaption>
</figure>



I started out by looking at the correlation of stars to all other features included, but no highly correlated features of interest were found:

<img src="https://raw.githubusercontent.com/jeffbauerle/MTB-Trail-EDA/master/images/stars_correlation.png">

The only category of interest not included in this was difficulty, since it is a categorical value, however I found that all of the star ratings were uniformly distributed: 

<img src="https://raw.githubusercontent.com/jeffbauerle/MTB-Trail-EDA/master/images/stars_by_difficulty.png">

I pivoted and started to look at regional differences in length and amount of ascent or descent on the trail. 



<img src="https://raw.githubusercontent.com/jeffbauerle/MTB-Trail-EDA/master/images/length_per_trail.png">

Notice that in ascent Denver is near the top of the list:

<img src="https://raw.githubusercontent.com/jeffbauerle/MTB-Trail-EDA/master/images/ascent_per_trail.png">

<img src="https://raw.githubusercontent.com/jeffbauerle/MTB-Trail-EDA/master/images/descent_per_trail.png">

Do Crested Butte and Denver have a steeper pitch or are they just longer? To explore this I added the descent per mile and ascent per mile columns to normalize the data.


<img src="https://raw.githubusercontent.com/jeffbauerle/MTB-Trail-EDA/master/images/descent_per_mile.png">

I also thought it would be interesting to also group the ascent per mile and descent per mile by difficulty.

With ascent per mile each difficulty level falls in line with the exception of the blue trails:

<img src="https://raw.githubusercontent.com/jeffbauerle/MTB-Trail-EDA/master/images/apm_by_difficulty.png">

Descent Per Mile by Difficulty is where I found the most interesting relationship. As the difficulty increases, the mean descent per mile is increasingly more negative.

<img src="https://raw.githubusercontent.com/jeffbauerle/MTB-Trail-EDA/master/images/dpm_by_difficulty.png">


## Conclusions

There weren't any features in my dataset highly associociated with star rating. People like most trails, rating them on average around 4 stars, regardless of difficulty type.

Noticeable relationship between decent per mile and difficulty.


## Further Work

Look at regional differences in the relationship of decent per mile and difficulty, and perform a t-test.
Subset word frequency / wordcloud for higher ranked trails and lower ranked trails.

Look into clustering of trails by difficulty.
[Link to interactive map](https://jeff-den18-capstones.s3-us-west-2.amazonaws.com/crested_butte_locations2.html)