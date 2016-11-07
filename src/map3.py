import sys
import gmplot
import itertools
import random
from math import pi, cos, sin, sqrt, asin
from pymongo import MongoClient

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))

def random_location(lat, lng, radius):
    # Convert radius from meters to degrees
    # 6371.0
    radius_in_degree = radius / 111000.0
    rand1 = random.random()
    rand2 = random.random()
    
    w = radius_in_degree * sqrt(rand1)
    t = 2 * pi * rand2
    
    long_off = w * cos(t)
    lat_off = w * sin(t)

    # Adjust the x-coordinate for the shrinking of the east-west distances
    # long_off = long_off / cos(lat)

    latitude = lat_off + lat
    longitude = long_off + lng

    return latitude, longitude

if len(sys.argv) < 4:
    print("Illegal number of parameters")
    print("map3.py <radius> <num checkins> <all|checked>")
    exit(1)

radius = eval(sys.argv[1])
num_samples = eval(sys.argv[2])
venues_arg = sys.argv[3].lower()
venues_db = 'venues-all' if (venues_arg == 'all') else 'venues'
filename = "radius-%s-%s-%s.html" % (str(radius), str(num_samples), venues_arg)

print('Radius: %d' % radius)
print('Samples: %d' % num_samples)
print('Collection: %s' % venues_db)
print('Output: %s' % filename)

client = MongoClient(host='150.164.2.168')
db = client['kunkka-nyc']
db.authenticate('jordan', '058414', source='admin')

#start, destination, candidates
colors = [['#EF9A9A', '#B71C1C', '#D50000'],
          ['#CE93D8', '#4A148C', '#AA00FF'],
          ['#9FA8DA', '#1A237E', '#304FFE'],
          ['#FFAB91', '#BF360C', '#DD2C00'],
          ['#81D4FA', '#01579B', '#0091EA'],
          ['#FFE082', '#FF6F00', '#FFAB00'],
          ['#C5E1A5', '#33691E', '#64DD17'],
          ['#80CBC4', '#004D40', '#00BFA5']
          ]
colors = itertools.cycle(colors)

# BH
# gmap = gmplot.GoogleMapPlotter(-19.9196016, -43.9484139, 10)

# NYC
gmap = gmplot.GoogleMapPlotter(40.7128, -74.0059, 10)

result = db['checkins'].find().limit(num_samples)
for item in result:
    point_lat = []
    point_lon = []
    rel_lat = []
    rel_lon = []
    latitudes = []
    longitudes = []


    venue = db['venues-all'].find_one({'uid': item['venue']})
    v_lat = venue['point'][1]
    v_lon = venue['point'][0]
    rel_lat.append(v_lat)
    rel_lon.append(v_lon)

    p_lat, p_lon = random_location(v_lat, v_lon, radius)
    point_lat.append(p_lat)
    point_lon.append(p_lon)
    item['point'] = [p_lon, p_lat]
    
    cand = item['venue']
    geo = {'type': 'Point', 'coordinates': item['point']}
    result2 = db[venues_db].find({'point': {'$near': 
                                    {'$geometry': geo,
                                     '$maxDistance': radius}},
                                     'uid': {'$ne': cand}},
                                    {'uid': 1, 'point': 1, '_id': 0},
                                    no_cursor_timeout=True)
    print(result2.count())
    for item2 in result2:
        latitudes.append(item2['point'][1])
        longitudes.append(item2['point'][0])

    result2.close()

    color = next(colors)
    gmap.scatter(point_lat, point_lon, color=color[0], size=radius, marker=False)
    gmap.scatter(point_lat, point_lon, color=color[1], marker=True)
    gmap.scatter(rel_lat, rel_lon, color=color[2], marker=True)
    gmap.scatter(latitudes, longitudes, color[2], marker=False)

result.close()

gmap.draw(filename)




