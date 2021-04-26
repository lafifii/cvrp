import requests 
import json 
import numpy as np

import googlemaps
import requests
import json

api_key = "AIzaSyBxI_rtVjyCashC_RtMxOuZnrRorwKc34M"

def reverse_geo(lat, lon):

  gmaps = googlemaps.Client(key=api_key)
  geocode = gmaps.reverse_geocode((lat,lon))

  loc = ""
  
  for x in geocode[0]['address_components']:
    loc+= x['long_name'] + " "

  return loc[:-1]


def get_route_points(lat1, lon1, lat2, lon2):
  endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
  
  origin = reverse_geo(lat1,lon1).replace(' ','+')
  destination = reverse_geo(lat2,lon2).replace(' ','+')
  
  nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
  request = endpoint + nav_request
  response = json.loads(requests.get(request).text)
  
  route = [[lat1,lon1]]

  if(len(response['routes']) > 0):

    for x in response['routes'][0]['legs'][0]['steps']:
      route.append( [ x['end_location']['lat'], x['end_location']['lng'] ])
  
  route.append([lat2, lon2])

  return route

def get_distance(lat1, lon1, lat2, lon2):
  endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
  
  origin = reverse_geo(lat1,lon1).replace(' ','+')
  destination = reverse_geo(lat2,lon2).replace(' ','+')
  
  nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
  request = endpoint + nav_request
  response = json.loads(requests.get(request).text)

  dist = 0
  
  if(len(response['routes']) == 0):
    return 0

  for x in response['routes'][0]['legs'][0]['steps']:
    dist+=x['distance']['value']

  return dist #metros

def create_distance_matrix(latList, lonList):

    n = len(latList)

    M = np.zeros(shape=(n,n))

    for i in range(n):
        for j in range(i + 1, n):
          
            dist = get_distance(latList[i],lonList[i],latList[j],lonList[j])
            
            M[i, j] = dist
            M[j, i] = dist

    return M
