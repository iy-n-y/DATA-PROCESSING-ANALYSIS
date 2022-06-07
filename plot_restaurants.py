import pandas as pd
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os
import seaborn
seaborn.set()

current_path = os.path.dirname(__file__)
data = current_path+'/osm/amenities-vancouver.json.gz'
restaurants_list = current_path+'/chain_restaurants.csv'
amenities = pd.read_json(data, lines=True)
vancouver = mpimg.imread(current_path+'/map.png')
chain_restaurants = pd.read_csv(restaurants_list, names=['name'])
chain_restaurants = chain_restaurants['name'].tolist()
def is_chain(name):
	return name in chain_restaurants

def convert_lon_lat(df):
	height = vancouver.shape[0]
	width = vancouver.shape[1]
	unit_lon = width / (-122 +123.5)
	unit_lat = height / 0.5
	x = (df['lon'].values + 123.5) * unit_lon
	y = (49.5 - df['lat'].values) * unit_lat 
	return x, y

def sep_restaurants(amenities):
	all_restaurants = amenities[(amenities['amenity'] == 'cafe') | 
				(amenities['amenity'] == 'restaurant') | 
				(amenities['amenity'] == 'fast_food')]
	chain = all_restaurants[all_restaurants['name'].apply(is_chain)]
	non_chain = all_restaurants[~all_restaurants['name'].apply(is_chain)]
	return chain, non_chain

if __name__ == "__main__":
	chain, non_chain = sep_restaurants(amenities)
	x_chain, y_chain = convert_lon_lat(chain)
	x_non_chain, y_non_chain = convert_lon_lat(non_chain)
	plt.imshow(vancouver)
	plt.title("Locations of chain/non-chain restaurants in Greater Vancouver")
	nc = plt.scatter(x_non_chain, y_non_chain, marker=".", color="red", s=15)
	c = plt.scatter(x_chain, y_chain, marker=".", color="black", s=15)
	plt.legend((nc, c), ('non-chain', 'chain'))
	plt.show()
