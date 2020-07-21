import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import seaborn as sns

file = '/Users/jeffbauerle/Documents/galvanize/capstones/capstone_1/data/response200.json'

with open(file) as trails_file:
  data = json.load(trails_file)

trails = data['trails']

# length = trails[trails['length']]

# print(trails.head())

# print(trails)

df = json_normalize(trails)

# df['stars'].hist(bins=10)

print(df['stars'].mean())

# fig, ax = plt.subplots(1,1)
# plt.scatter(df['length'])

# plt.show()

sns.pairplot(df)
plt.show()


# library & dataset
# df = sns.load_dataset('iris')
# import matplotlib.pyplot as plt
 
# Basic correlogram
# sns.pairplot(df)
# sns.plt.show()



            # "id": 7000620,
            # "difficulty": "black",
            # "length": 9.4,
            # "ascent": 1668,
            # "descent": -1667,
            # "high": 7309,
            # "low": 6164,
            # "stars": 4.4,
            # "starVotes": 176,
            # "longitude": -105.2097,
            # "latitude": 39.7162,


            # "name": "Apex Park Tour",
            # "type": "Recommended Route",
            # "summary": "This technical front range ride is only possible on even numbered days but it's worth the planning!",
            # "conditionStatus": "All Clear",
            # "conditionDetails": "Dry, Mostly Dry",
            # "conditionDate": "2020-07-12 17:08:29"
            # "location": "West Pleasant View, Colorado",
            # "url": "https:\/\/www.mtbproject.com\/trail\/7000620\/apex-park-tour",
            # "imgSqSmall": "https:\/\/cdn2.apstatic.com\/photos\/mtb\/7018020_sqsmall_1554917670.jpg",
            # "imgSmall": "https:\/\/cdn2.apstatic.com\/photos\/mtb\/7018020_small_1554917670.jpg",
            # "imgSmallMed": "https:\/\/cdn2.apstatic.com\/photos\/mtb\/7018020_smallMed_1554917670.jpg",
            # "imgMedium": "https:\/\/cdn2.apstatic.com\/photos\/mtb\/7018020_medium_1554917670.jpg",
