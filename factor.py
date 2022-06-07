import pandas as pd
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import os
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from plot_restaurants import sep_restaurants


current_path = os.path.dirname(__file__)
data = current_path+'/osm/amenities-vancouver.json.gz'
chain_file = current_path+'/chain_restaurants.csv'
park=pd.read_json(current_path+'/clean_park.json.gz',lines=True)
amenities = pd.read_json(data, lines=True)
deg_lat_permile = 1/69
deg_lon_permile = 1/55

park['lat_lon'] = park[['lat', 'lon']].values.tolist()
amenities['lat_lon'] = amenities[['lat', 'lon']].values.tolist()

def cal_num(lat_lon, chain):
	lat = lat_lon[0]
	lon = lat_lon[1]
	lat_max = lat + deg_lat_permile
	lat_min = lat - deg_lat_permile
	lon_max = lon + deg_lon_permile
	lon_min = lon - deg_lon_permile
	df_chain = chain[(chain['lat'] <= lat_max) & 
					(chain['lat'] >= lat_min) & 
					(chain['lon'] <= lon_max) & 
					(chain['lon'] >= lon_min) ]
	return df_chain.count()[0]

def f_num(facility_name, chain):
	facility = park[park['facilities'] == facility_name]
	facility['num_chain'] = facility['lat_lon'].apply(cal_num, args=(chain,))
	return facility[['facilities', 'num_chain']]


if __name__ == "__main__":
	chain, non_chain = sep_restaurants(amenities)
	

	satisfied_facility = park.groupby('facilities').count().reset_index()
	satisfied_facility = satisfied_facility[satisfied_facility['lat']>8]
	f_names = satisfied_facility['facilities'].values

	f_chain = pd.DataFrame(columns=['facilities', 'num_chain'])
	for names in f_names:
		df = f_num(names, chain)
		f_chain = pd.concat([f_chain, df])

	posthoc = pairwise_tukeyhsd(
	    f_chain['num_chain'].astype('float'), f_chain['facilities'],
	    alpha=0.05)
	

	df_posthoc = pd.DataFrame(data=posthoc._results_table.data[1:], columns=posthoc._results_table.data[0])
	
	results_1 = df_posthoc.groupby(['group1', 'reject']).count().reset_index()
	results_1 = results_1.pivot(index='group1', columns='reject', values='group2')

	results_2 = df_posthoc.groupby(['group2', 'reject']).count().reset_index()
	results_2 = results_2.pivot(index='group2', columns='reject', values='group1')

	results = results_1.join(results_2, lsuffix='_left').fillna(0)
	results.rename_axis("facilities", axis='index', inplace=True)
	results['False'] = results['False_left'] + results['False']
	results['True'] = results['True_left'] + results['True']
	results = results.iloc[:, [2, 3]]
	results['true_percentage'] = results.iloc[:, 1] / (results.iloc[:, 0] + results.iloc[:, 1])
	results = results.sort_values(by='true_percentage', ascending=False)
	results.to_csv(current_path+'/posthoc.csv')
	print(posthoc)
	fig = posthoc.plot_simultaneous()
	print(results)
	plt.show()
