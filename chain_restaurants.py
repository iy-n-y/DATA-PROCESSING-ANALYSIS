import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

current_path = os.path.dirname(__file__)
chain_restaurants = []
restaurants = []

data = 'https://en.wikipedia.org/wiki/List_of_Canadian_restaurant_chains'
data2 = 'https://en.wikipedia.org/wiki/List_of_restaurant_chains'

result = requests.get(data)
bs = BeautifulSoup(result.text, 'html.parser')

for restaurant in bs.findAll("span", {"class": "mw-headline"}):
	restaurants.append(restaurant.get_text())

restaurants = restaurants[1:-3]
for restaurant in restaurants:
	name = restaurant.split(' (')
	chain_restaurants.append(name[0])

result = requests.get(data2)
bs = BeautifulSoup(result.text, 'html.parser')
contentTable = bs.find("table", {"class": "wikitable sortable"})
for restaurant in contentTable.findAll("tr"):
	name = restaurant.find('a', href=True, title=True)
	if name is not None:
		chain_restaurants.append(name.get_text()) 
 
chain_restaurants.sort()
chain_restaurants = list(dict.fromkeys(chain_restaurants))

chain = pd.DataFrame(chain_restaurants)
chain.to_csv(current_path+'/chain_restaurants.csv', index=False, header=False)