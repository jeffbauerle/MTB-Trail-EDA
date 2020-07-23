import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas import json_normalize
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import folium
# from folium import plugins
from folium.plugins import HeatMap
from PIL import Image


if __name__ == "__main__":

  # Denver
  denver_file = '../data/denver.json'

  with open(denver_file) as denver_file:
    denver = json.load(denver_file)

  # Park City
  park_city_file = '../data/parkcity.json'

  with open(park_city_file) as park_city_file:
    park_city = json.load(park_city_file)

  # Moab
  moab_file = '../data/moab.json'

  with open(moab_file) as moab_file:
    moab = json.load(moab_file)

  # Sedona
  sedona_file = '../data/sedona.json'

  with open(sedona_file) as sedona_file:
    sedona = json.load(sedona_file)

  # Marin County
  marin_county_file = '../data/marincounty.json'

  with open(marin_county_file) as marin_county_file:
    marin_county = json.load(marin_county_file)

  # Crested Butte
  crested_butte_file = '../data/crestedbutte.json'

  with open(crested_butte_file) as crested_butte_file:
    crested_butte = json.load(crested_butte_file)

  denver_trails = denver['trails']
  denver_df = json_normalize(denver_trails)
  denver_df["location"] = "denver"

  denver_df.head()

  print(round(denver_df['stars'].mean(),2))

  park_city_trails = park_city['trails']
  park_city_df = json_normalize(park_city_trails)
  park_city_df["location"] = "park_city"

  print(round(park_city_df['stars'].mean(),2))

  moab_trails = moab['trails']
  moab_df = json_normalize(moab_trails)
  moab_df["location"] = "moab"

  print(round(moab_df['stars'].mean(),2))

  sedona_trails = sedona['trails']
  sedona_df = json_normalize(sedona_trails)
  sedona_df["location"] = "sedona"

  print(round(sedona_df['stars'].mean(),2))

  marin_county_trails = marin_county['trails']
  marin_county_df = json_normalize(marin_county_trails)
  marin_county_df["location"] = "marin_county"

  print(round(marin_county_df['stars'].mean(),2))

  crested_butte_trails = crested_butte['trails']
  crested_butte_df = json_normalize(crested_butte_trails)
  crested_butte_df["location"] = "crested_butte"

  print(round(crested_butte_df['stars'].mean(),2))

  crested_butte_df.describe()

  # Columns
  crested_butte_df.columns

  crested_butte_df.info()

  cb_unique = crested_butte_df.copy()
  cb_unique = cb_unique.groupby("difficulty")

  cb_unique["difficulty"].unique()

  crested_butte_df[crested_butte_df["difficulty"] == "green"]["stars"].mean()
  crested_butte_df[crested_butte_df["difficulty"] == "greenBlue"]["stars"].mean()
  crested_butte_df[crested_butte_df["difficulty"] == "blue"]["stars"].mean()
  crested_butte_df[crested_butte_df["difficulty"] == "blueBlack"]["stars"].mean()
  crested_butte_df[crested_butte_df["difficulty"] == "black"]["stars"].mean()
  crested_butte_df[crested_butte_df["difficulty"] == "dblack"]["stars"].mean()

  crested_butte_df.groupby("difficulty")["stars"].mean()

  crested_butte_df.groupby("difficulty")["stars"].agg([min,max,sum])

  crested_butte_df.groupby("difficulty")["stars"].mean()

  crested_butte_df.pivot_table(values="stars",index="difficulty", aggfunc=[np.mean, np.median, np.min, np.max])

  crested_butte_df.set_index("difficulty")

  crested_butte_df.sort_index()

  crested_butte_df.corr(method ='pearson')

  text = " ".join(review for review in crested_butte_df.summary)
  print ("There are {} words in the combination of all review.".format(len(text)))

  crested_butte_df["summary"].head()

  stopwords = set(STOPWORDS)
  stopwords.update(["singletrack","trail","great","ride","climb","descent"])

  wordcloud = WordCloud(stopwords=stopwords).generate(text)

  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis("off")
  plt.show()

  # MTB_Trail_Data_EDA

  all_df = pd.concat([crested_butte_df, marin_county_df, denver_df, park_city_df, sedona_df, moab_df])

  print(all_df.tail())

  all_df.describe()

  text = " ".join(review for review in all_df.summary)
  print ("There are {} words in the combination of all review.".format(len(text)))

  stopwords = set(STOPWORDS)
  stopwords.update(["This,","An"])

  wordcloud = WordCloud(stopwords=stopwords).generate(text)

  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis("off")
  plt.show()

  bike_mask = np.array(Image.open("../images/wordcloud_bike.png"))
  bike_mask

  bike_mask[bike_mask == 0] = 255

  # Create a word cloud image
  wc = WordCloud(background_color="white", max_words=1000, mask=bike_mask,
                stopwords=stopwords, contour_width=3)

  # Generate a wordcloud
  wc.generate(text)

  # store to file
  # wc.to_file("../images/bike_wordcloud_after.png")

  # show
  plt.figure(figsize=[20,10])
  plt.imshow(wc, interpolation='bilinear')
  plt.axis("off")
  plt.show()

  # bike_mask2 = np.array(Image.open("../images/wordcloud_bike_big.png"))
  # bike_mask2

  # bike_mask2[bike_mask2 == 0] = 255

  # # Create a word cloud image
  # wc = WordCloud(background_color="white", max_words=1000, mask=bike_mask,
  #               stopwords=stopwords, contour_width=3)

  # # Generate a wordcloud
  # wc.generate(text)

  # # store to file
  # # wc.to_file("../images/bike_wordcloud_after.png")

  # # show
  # plt.figure(figsize=[30,15])
  # plt.imshow(wc, interpolation='bilinear')
  # plt.axis("off")
  # plt.show()

  all_df.corr(method ='pearson')

# All scatter matrix
  # sns.pairplot(all_df)
  # plt.show()

  all_df.groupby("location")["length"].agg([np.min,np.max,np.mean,np.median])

  all_df.groupby(["location"])["length"].median()

  all_df.groupby(["location"])["ascent"].median()

  all_df[all_df["length"] == 294.3]

  all_df.info()

  m = folium.Map(
      location=[38.8697, -106.9878],
      zoom_start=8,
      tiles='Stamen Terrain'
  )

  tooltip = 'Click me!'

  folium.Marker([38.4965, -106.3254], popup='<i>Mt. Hood Meadows</i>', tooltip=tooltip).add_to(m)
  folium.Marker([45.3311, -121.7113], popup='<b>Timberline Lodge</b>', tooltip=tooltip).add_to(m)

  m


  for index, row in crested_butte_df.iterrows():
      if row['difficulty'] == 'black': 
          folium.CircleMarker([row['latitude'], row['longitude']],
                              radius=15,
                              popup=row['name'],
                              fill_color="#000000", # divvy color
                            ).add_to(m)
      elif row['difficulty'] == 'blue': 
          folium.CircleMarker([row['latitude'], row['longitude']],
                              radius=15,
                              popup=row['name'],
                              fill_color="#0000FF", # divvy color
                            ).add_to(m)
      elif row['difficulty'] == 'green': 
          folium.CircleMarker([row['latitude'], row['longitude']],
                              radius=15,
                              popup=row['name'],
                              fill_color="#008000", # divvy color
                            ).add_to(m)
      elif row['difficulty'] == 'blueBlack': 
          folium.CircleMarker([row['latitude'], row['longitude']],
                              radius=15,
                              popup=row['name'],
                              fill_color="#003366", # divvy color
                            ).add_to(m)
      elif row['difficulty'] == 'greenBlue': 
          folium.CircleMarker([row['latitude'], row['longitude']],
                              radius=15,
                              popup=row['name'],
                              fill_color="#00DDDD", # divvy color
                            ).add_to(m)
      elif row['difficulty'] == 'dblack': 
          folium.CircleMarker([row['latitude'], row['longitude']],
                              radius=15,
                              popup=row['name'],
                              fill_color="#000000", # divvy color
                            ).add_to(m)

  m

  # convert to (n, 2) nd-array format for heatmap
  # stationArr = crested_butte_df[['latitude', 'longitude']].to_numpy()

  # # plot heatmap
  # m.add_children(plugins.HeatMap(stationArr, radius=15))
  # m

  # df_copy = crested_butte_df.copy()
  # df_copy['count'] = 1
  # HeatMap(data=df_copy[['latitude', 'longitude', 'count']].groupby(['latitude', 'longitude']).sum().reset_index().values.tolist(), radius=8, max_zoom=13).add_to(m)
  # m

  # all_df.groupby(["location","difficulty"])["stars"].agg([np.min,np.max,np.mean,np.median])
  all_df.groupby(["location","difficulty"])["stars"].mean()
