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

  park_city_trails = park_city['trails']
  park_city_df = json_normalize(park_city_trails)
  park_city_df["location"] = "park_city"

  moab_trails = moab['trails']
  moab_df = json_normalize(moab_trails)
  moab_df["location"] = "moab"

  sedona_trails = sedona['trails']
  sedona_df = json_normalize(sedona_trails)
  sedona_df["location"] = "sedona"

  marin_county_trails = marin_county['trails']
  marin_county_df = json_normalize(marin_county_trails)
  marin_county_df["location"] = "marin_county"

  crested_butte_trails = crested_butte['trails']
  crested_butte_df = json_normalize(crested_butte_trails)
  crested_butte_df["location"] = "crested_butte"


  proper_loc_list = ["Denver","Crested Butte","Marin County","Sedona","Park City","Moab"]
  df_loc_list = ["denver","crested_butte","marin_county","sedona","park_city","moab"]

  loc_dict = {"denver":"Denver","crested_butte":"Crested Butte","marin_county":"Marin County","sedona":"Sedona","park_city":"Park City","moab":"Moab"}

  # MTB_Trail_Data_EDA

  all_df = pd.concat([crested_butte_df, marin_county_df, denver_df, park_city_df, sedona_df, moab_df])

  print(all_df.tail())

  all_df.describe()

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

  # store to file
  # wc.to_file("../images/bike_wordcloud_after.png")

  # show
  # plt.figure(figsize=[20,10])
  # plt.imshow(wc, interpolation='bilinear')
  # plt.axis("off")
  # plt.savefig("../images/wordcloud_bike_after.png")
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

print(all_df[all_df["location"]=="crested_butte"]["ascent"].mean())

fig, ax = plt.subplots()

for df,loc in loc_dict.items():
  ax.bar(loc,all_df[all_df["location"]==df]["ascent"].mean())


# ax.bar("Crested Butte",all_df[all_df["location"]=="crested_butte"]["ascent"].mean())
# ax.bar("Marin County",all_df[all_df["location"]=="marin_county"]["ascent"].mean())
# ax.bar("Moab",all_df[all_df["location"]=="moab"]["ascent"].mean())
# ax.bar("Sedona",all_df[all_df["location"]=="sedona"]["ascent"].mean())
# ax.bar("Park City",all_df[all_df["location"]=="park_city"]["ascent"].mean())
# ax.bar("Denver",all_df[all_df["location"]=="denver"]["ascent"].mean())

ax.set_xlabel('Location')
ax.set_ylabel('Mean Ascent Per Trail')
ax.set_title('Mean Ascent Per Trail by Location')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


fig, ax = plt.subplots()

ax.bar("Crested Butte",all_df[all_df["location"]=="crested_butte"]["length"].mean())
ax.bar("Marin County",all_df[all_df["location"]=="marin_county"]["length"].mean())
ax.bar("Moab",all_df[all_df["location"]=="moab"]["length"].mean())
ax.bar("Sedona",all_df[all_df["location"]=="sedona"]["length"].mean())
ax.bar("Park City",all_df[all_df["location"]=="park_city"]["length"].mean())
ax.bar("Denver",all_df[all_df["location"]=="denver"]["length"].mean())

ax.set_xlabel('Location')
ax.set_ylabel('Mean Length Per Trail')
ax.set_title('Mean Length Per Trail by Location')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

all_df["ascent_per_trail"] = all_df["ascent"] / all_df["length"]
all_df["descent_per_trail"] = all_df["descent"] / all_df["length"]

# print(all_df["ascent_per_trail"].mean())
#Ascent

fig, ax = plt.subplots()

ax.bar("Crested Butte",all_df[all_df["location"]=="crested_butte"]["ascent_per_trail"].mean())
ax.bar("Marin County",all_df[all_df["location"]=="marin_county"]["ascent_per_trail"].mean())
ax.bar("Moab",all_df[all_df["location"]=="moab"]["ascent_per_trail"].mean())
ax.bar("Sedona",all_df[all_df["location"]=="sedona"]["ascent_per_trail"].mean())
ax.bar("Park City",all_df[all_df["location"]=="park_city"]["ascent_per_trail"].mean())
ax.bar("Denver",all_df[all_df["location"]=="denver"]["ascent_per_trail"].mean())

ax.set_xlabel('Location')
ax.set_ylabel('Mean Ascent Per Mile Per Trail')
ax.set_title('Mean Ascent Per Mile by Location')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Descent
fig, ax = plt.subplots()

ax.bar("Crested Butte",all_df[all_df["location"]=="crested_butte"]["descent_per_trail"].mean())
ax.bar("Marin County",all_df[all_df["location"]=="marin_county"]["descent_per_trail"].mean())
ax.bar("Moab",all_df[all_df["location"]=="moab"]["descent_per_trail"].mean())
ax.bar("Sedona",all_df[all_df["location"]=="sedona"]["descent_per_trail"].mean())
ax.bar("Park City",all_df[all_df["location"]=="park_city"]["descent_per_trail"].mean())
ax.bar("Denver",all_df[all_df["location"]=="denver"]["descent_per_trail"].mean())

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

# def get_norm_coef(df):
#   mean_df = df['ascent_per_trail'].mean()
#   sqrt_df = np.sqrt(len(df['ascent_per_trail']))
#   std = (df['ascent_per_trail'].std())/sqrt_df
#   return mean_df, std

# def normal_dist(mean, std):
#   return stats.norm(loc=mean, scale=std)

# fig, ax = plt.subplots()
# x = np.linspace(0,180,180)

# # mean_29, std_29 = get_norm_coef(df_29)
# mean_275, std_275 = get_norm_coef(df_275)
# # norm_29 = normal_dist(mean_29,std_29)
# norm_275 = normal_dist(mean_275,std_275)
# x1 = np.linspace(mean_275-6*std_275,mean_275+6*std_275,500)
# # x2 = np.linspace(mean_29-6*std_29,mean_29*std_29,500)
# # t_test = stats.ttest_ind(df_29['Price'],df_275['Price'],equal_var=False)
# # Distribution of means plots
# fig, ax = plt.subplots(figsize=(12,8))
# x = np.linspace(2600,3600,2000)
# ax.plot(x,norm_275.pdf(x),color='#C95948',label='27.5')
# ax.plot(x,norm_29.pdf(x),color= '#4586AC',label='29')


print(all_df[all_df["difficulty"]=="green"]["ascent_per_trail"].mean())

print(all_df.groupby("descent_per_trail")["stars"].agg([np.min,np.max,np.mean,np.median]))