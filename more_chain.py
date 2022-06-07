import pandas as pd
import numpy as np
import sys
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from scipy import stats
import os
from plot_restaurants import sep_restaurants
from plot_restaurants import convert_lon_lat

import seaborn as sns


import seaborn
seaborn.set()
current_path = os.path.dirname(__file__)
data = current_path+'/osm/amenities-vancouver.json.gz'
chain_file = current_path+('/chain_restaurants.csv')
amenities = pd.read_json(data, lines=True)
vancouver = mpimg.imread(current_path+'/map.png')
chain_restaurants = pd.read_csv(chain_file, names=['name'])
chain_restaurants = chain_restaurants['name'].tolist()

deg_lat_permile = 1/69
deg_lon_permile = 1/55

def cal_near(chain,lat,lon):
	minimum1 = lat - deg_lat_permile
	maximum1 = lat + deg_lat_permile
	minimum2 = lon - deg_lon_permile
	maximum2 = lon + deg_lon_permile
	df_chain = chain[((chain['lat'] <= maximum1) & (chain['lat'] >= minimum1))&((chain['lon'] <= maximum2) & (chain['lon'] >= minimum2))]
	return df_chain.count()[0]

def cal_num(chain):
	chain['num_dim'] = chain.apply(lambda row: cal_near(chain,row['lat'], row['lon']), axis=1)
	return chain

if __name__ == "__main__":
	chain, non_chain = sep_restaurants(amenities)
	num_chain = cal_num(chain)

	sort_lat = num_chain.sort_values(by='lat')
	sort_lon = num_chain.sort_values(by='lon')
	model1 = stats.linregress(sort_lat['lat'].values, sort_lat['num_dim'].values)
	model2 = stats.linregress(sort_lon['lon'].values, sort_lon['num_dim'].values)
	print("pvalue of fit line for latitude: ", model1.pvalue)
	print("pvalue of fit line for longitude: ", model2.pvalue)
	sns.pairplot(chain,kind="reg",diag_kind="kde",vars=["num_dim","lat"])
	sns.pairplot(chain,kind="reg",diag_kind="kde",vars=["num_dim","lon"]) 
	plt.show()
