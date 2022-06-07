import pandas as pd
import os
pd.set_option('display.max_columns', None)

current_path = os.path.dirname(__file__)
def get_park_name(row):
    park_name = row['fields']['name']
    return park_name

def get_park_lat(row):
    park_gps = row['fields']['googlemapdest']
    return park_gps[0]

def get_park_lon(row):
    park_gps = row['fields']['googlemapdest']
    return park_gps[1]

def get_park_strname(row):
    park_street = row['fields']['streetname']
    return park_street

def make_tag(row):
    tags = {}
    tags['addr:street'] = row['fields']['streetname']
    return tags

def get_id(row):
    park_id=row['fields']['parkid']
    return park_id

def get_type(row):
    facilities_type=row['fields']['facilitytype']
    return facilities_type

def get_type2(row):
    facilities_type=row['fields']['facilities']
    return facilities_type

van_park_dataset = pd.read_json(current_path+'/parks.json',orient = 'records')
f_data = pd.read_json(current_path+'/parks-facilities.json',orient = 'records')
van_park_dataset['name'] = (van_park_dataset.apply(get_park_name,axis=1))
van_park_dataset['lat'] = (van_park_dataset.apply(get_park_lat,axis=1))
van_park_dataset['lon'] = (van_park_dataset.apply(get_park_lon,axis=1))
van_park_dataset['tags'] = (van_park_dataset.apply(make_tag,axis=1))
van_park_dataset['parkid']=(van_park_dataset.apply(get_id,axis=1))
van_park_dataset['facilities'] = (van_park_dataset.apply(get_type2,axis=1))
f_data['name'] = (f_data.apply(get_park_name,axis=1))
f_data['facilities'] = (f_data.apply(get_type,axis=1))
f_data['parkid']=(f_data.apply(get_id,axis=1))
facilities_dataset = f_data[['name', 'facilities','parkid']]
clean_van_park_dataset = van_park_dataset[['name', 'lat','lon','tags','parkid','facilities']]
facilities_dataset=facilities_dataset.sort_values(by='parkid',ascending=False)
clean_van_park_dataset=clean_van_park_dataset.sort_values(by='parkid',ascending=False)
for i in range(len(clean_van_park_dataset['name'])):
    for j in range(len(facilities_dataset['name'])):
        if(clean_van_park_dataset.iloc[i]['parkid']==facilities_dataset.iloc[j]['parkid']):
            clean_van_park_dataset.iloc[i,clean_van_park_dataset.columns=='facilities']=facilities_dataset.iloc[j,facilities_dataset.columns=='facilities']

clean_van_park_dataset = clean_van_park_dataset.assign(amenity='park') 
park_output_path = current_path+'/clean_park.json.gz'
clean_van_park_dataset.to_json(park_output_path, orient = 'records',lines=True,compression = 'gzip') 
