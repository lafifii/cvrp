import util.gmaps as gmaps

import json
import pandas as pd


def load_data(file_dr, file_loc):
  
  def create_df(dic):
    c_names = [key for key in dic[0].keys()]
    df = pd.DataFrame(columns = c_names)
    i = 0

    for elem in dic:
      vals = []

      for c in c_names:
        vals.append(elem[c])
      
      df.loc[i] = vals
      i+= 1
    
    return df

  f = open(file_dr,)
  json_drivers = json.load(f)

  f = open(file_loc,)
  json_locations = json.load(f)


  df_drivers = create_df(json_drivers)
  df_locations = create_df(json_locations)

  return df_drivers, df_locations


def create_model(df_drivers, df_locations):

  ## multidepot

  n_drivers = df_drivers.shape[0]
  
  lng_combined = df_drivers.lng.to_list()  + df_locations.lng.to_list()
  lat_combined = df_drivers.lat.to_list() + df_locations.lat.to_list()

  data = {}
  data['latitudes'] = [ float(lat) for lat in lat_combined ]
  data['longitudes'] = [ float(lng) for lng in lng_combined ]
  data['distance_matrix'] = gmaps.create_distance_matrix(lat_combined, lng_combined)
  data['demands'] = [0]*n_drivers + df_locations.demand.to_list()
  data['vehicle_capacities'] = df_drivers.capacity.to_list()
  data['num_vehicles'] = n_drivers
  data['depot'] = 0


  data['starts'] = []
  data['ends'] = []
  for i in range(n_drivers):
    data['starts'].append(i)
    data['ends'].append(i)

  return data