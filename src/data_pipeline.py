import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas import json_normalize
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import folium
from folium import plugins
from folium.plugins import HeatMap
from PIL import Image
import scipy.stats as stats

def make_ax_bar(loc_dict, col):
  fig, ax = plt.subplots()
  for df,loc in loc_dict.items():
    ax.bar(loc,all_df[all_df["location"]==df][col].mean())
  plt.xticks(rotation=45)
  return ax

def load_trail_df_from_file(filename, location_name):
  with open(filename) as data_file:
    data = json.load(data_file)
  data_trails = data['trails']
  data_df = json_normalize(data_trails)
  data_df["location"] = location_name
  return data_df

if __name__ == "__main__":

  # Denver
  denver_file = '../data/denver.json'
  denver_df = load_trail_df_from_file(denver_file, "denver")

  # Park City
  park_city_file = '../data/parkcity.json'
  park_city_df = load_trail_df_from_file(park_city_file, "park_city")

  # Moab
  moab_file = '../data/moab.json'
  moab_df = load_trail_df_from_file(moab_file, "moab")

  # Sedona
  sedona_file = '../data/sedona.json'
  sedona_df = load_trail_df_from_file(sedona_file, "sedona")

  # Marin County
  marin_county_file = '../data/marincounty.json'
  marin_county_df = load_trail_df_from_file(marin_county_file, "marin_county")

  # Crested Butte
  crested_butte_file = '../data/crestedbutte.json'
  crested_butte_df = load_trail_df_from_file(crested_butte_file, "crested_butte")

  loc_dict = {"denver":"Denver","crested_butte":"Crested Butte","marin_county":"Marin County","sedona":"Sedona","park_city":"Park City","moab":"Moab"}

  # MTB_Trail_Data_EDA

  all_df = pd.concat([crested_butte_df, marin_county_df, denver_df, park_city_df, sedona_df, moab_df])

  text = " ".join(review for review in all_df.summary)
  print ("There are {} words in the combination of all review.".format(len(text)))

  stopwords = set(STOPWORDS)
  stopwords.update(["This ,","An "])

  bike_mask = np.array(Image.open("../images/wordcloud_bike.png"))
  bike_mask

  bike_mask[bike_mask == 0] = 255

  # Create a word cloud image
  wc = WordCloud(background_color="white", max_words=1000, mask=bike_mask,
                stopwords=stopwords, contour_width=3)

  # Generate a wordcloud
  wc.generate(text)

  # show
  # plt.figure(figsize=[20,10])
  # plt.imshow(wc, interpolation='bilinear')
  # plt.axis("off")
  # plt.savefig("../images/wordcloud_bike_after.png")
  # plt.show()

  all_df.corr(method ='pearson')


  m = folium.Map(
      location=[38.8697, -106.9878],
      zoom_start=8,
      tiles='Stamen Terrain'
  )


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


  # convert to (n, 2) nd-array format for heatmap
  stationArr = crested_butte_df[['latitude', 'longitude']].to_numpy()

  # plot heatmap
  m.add_children(plugins.HeatMap(stationArr, radius=15))
  # m
  m.save("../images/crested_butte_locations2.html")
  # df_copy = crested_butte_df.copy()
  # df_copy['count'] = 1
  # HeatMap(data=df_copy[['latitude', 'longitude', 'count']].groupby(['latitude', 'longitude']).sum().reset_index().values.tolist(), radius=8, max_zoom=13).add_to(m)
  # m

  # all_df.groupby(["location","difficulty"])["stars"].agg([np.min,np.max,np.mean,np.median])
  all_df.groupby(["location","difficulty"])["stars"].mean()

  # all_df.to_csv("../data/all_data.csv")

# fig, ax = plt.subplots()

# Mean Ascent Per Trail
ax = make_ax_bar(loc_dict,"ascent")
ax.set_xlabel('Location')
ax.set_ylabel('Mean Ascent Per Trail')
ax.set_title('Mean Ascent Per Trail by Location')
plt.tight_layout()
plt.show()

# Mean Length Per Trail Plot
ax = make_ax_bar(loc_dict,"length")
ax.set_xlabel('Location')
ax.set_ylabel('Mean Length Per Trail')
ax.set_title('Mean Length Per Trail by Location')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

all_df["ascent_per_trail"] = all_df["ascent"] / all_df["length"]
all_df["descent_per_trail"] = all_df["descent"] / all_df["length"]

# print(all_df["ascent_per_trail"].mean())

#Ascent Per Trail
ax = make_ax_bar(loc_dict,"ascent_per_trail")
ax.set_ylabel('Mean Ascent Per Mile Per Trail')
ax.set_title('Mean Ascent Per Mile by Location')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Descent
ax = make_ax_bar(loc_dict,"descent_per_trail")
ax.set_xlabel('Location')
ax.set_ylabel('Mean Descent Per Mile Per Trail')
ax.set_title('Mean Descent Per Mile by Location')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# difficulty
#Ascent
fig, ax = plt.subplots()

ax.bar("Green",all_df[all_df["difficulty"]=="green"]["ascent_per_trail"].mean(), color="green")
ax.bar("Green Blue",all_df[all_df["difficulty"]=="greenBlue"]["ascent_per_trail"].mean(), color="#0d98ba")
ax.bar("Blue",all_df[all_df["difficulty"]=="blue"]["ascent_per_trail"].mean(), color="blue")
ax.bar("Blue Black",all_df[all_df["difficulty"]=="blueBlack"]["ascent_per_trail"].mean(), color="#003366")
ax.bar("Black",all_df[all_df["difficulty"]=="black"]["ascent_per_trail"].mean(), color="black")
ax.bar("Double Black",all_df[all_df["difficulty"]=="dblack"]["ascent_per_trail"].mean(), color="white", hatch='*', edgecolor="black")

ax.set_xlabel('Difficulty')
ax.set_ylabel('Mean Ascent Per Mile Per Trail')
ax.set_title('Mean Ascent Per Mile by Difficulty')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Descent
fig, ax = plt.subplots()

ax.bar("Green",all_df[all_df["difficulty"]=="green"]["descent_per_trail"].mean(), color="green")
ax.bar("Green Blue",all_df[all_df["difficulty"]=="greenBlue"]["descent_per_trail"].mean(), color="#0d98ba")
ax.bar("Blue",all_df[all_df["difficulty"]=="blue"]["descent_per_trail"].mean(), color="blue")
ax.bar("Blue Black",all_df[all_df["difficulty"]=="blueBlack"]["descent_per_trail"].mean(), color="#003366")
ax.bar("Black",all_df[all_df["difficulty"]=="black"]["descent_per_trail"].mean(), color="black")
ax.bar("Double Black",all_df[all_df["difficulty"]=="dblack"]["descent_per_trail"].mean(), color="white", hatch='*', edgecolor="black")

ax.set_xlabel('Difficulty')
ax.set_ylabel('Mean Descent Per Mile Per Trail')
ax.set_title('Mean Descent Per Mile by Difficulty')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Stars
fig, ax = plt.subplots()

ax.bar("Green",all_df[all_df["difficulty"]=="green"]["stars"].mean(), color="green")
ax.bar("Green Blue",all_df[all_df["difficulty"]=="greenBlue"]["stars"].mean(), color="#0d98ba")
ax.bar("Blue",all_df[all_df["difficulty"]=="blue"]["stars"].mean(), color="blue")
ax.bar("Blue Black",all_df[all_df["difficulty"]=="blueBlack"]["stars"].mean(), color="#003366")
ax.bar("Black",all_df[all_df["difficulty"]=="black"]["stars"].mean(), color="black")
ax.bar("Double Black",all_df[all_df["difficulty"]=="dblack"]["stars"].mean(), color="white", hatch='*', edgecolor="black")

ax.set_xlabel('Difficulty')
ax.set_ylabel('Mean Stars')
ax.set_title('Difficulty')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

