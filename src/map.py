import sys
import gmplot
import itertools
from pymongo import MongoClient


if len(sys.argv) < 4:
    print("Illegal number of parameters")
    print("map.py <city> <num checkins> <all|checked>")
    exit(1)

db_arg = sys.argv[1].lower()
db_name = 'kunkka'
if db_arg == 'bh':
    db_name = 'kunkka'
    city_coord = [-19.9196016, -43.9484139]
elif db_arg == 'nyc':
    db_name = 'kunkka-nyc'
    city_coord = [40.7128, -74.0059]
else:
    print("Invalid database!")
    exit(1)

num_samples = eval(sys.argv[2])
venues_arg = sys.argv[3].lower()
venues_db = 'venues-all' if (venues_arg == 'all') else 'venues'
venues_attr = 'cand_all' if (venues_arg == 'all') else 'cand_checked'
filename = "%s-%s-%s.html" % (db_arg, str(num_samples), venues_arg)

client = MongoClient(host='150.164.2.168')
db = client[db_name]
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

gmap = gmplot.GoogleMapPlotter(city_coord[0], city_coord[1], 10)

result = db['checkins'].find().skip(10).limit(num_samples)

for item in result:
    point_lat = []
    point_lon = []
    rel_lat = []
    rel_lon = []
    latitudes = []
    longitudes = []

    point_lat.append(item['point'][1])
    point_lon.append(item['point'][0])

    venue = db['venues'].find_one({'uid': item['venue']})
    rel_lat.append(venue['point'][1])
    rel_lon.append(venue['point'][0])

    max_dist = 5000
    limit = 499
    cand = item['venue']

    result2 = db[venues_db].find({'uid': {'$in': item[venues_attr]}})
    for item2 in result2:
        if (item2['uid'] == item['venue']):
            continue
        latitudes.append(item2['point'][1])
        longitudes.append(item2['point'][0])

    result2.close()

    color = next(colors)
    gmap.scatter(point_lat, point_lon, color=color[0], size=500, marker=False)
    gmap.marker(lat=point_lat[0], lng=point_lon[0], color=color[1], title=item['id'])
    gmap.marker(lat=rel_lat[0], lng=rel_lon[0], color=color[2], title=item['id'])
    gmap.scatter(latitudes, longitudes, color[2], size=80, marker=False)
result.close()

# gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)
# Belo Horizonte
# gmap = gmplot.GoogleMapPlotter(-19.9196016, -43.9484139, 12)

# gmap = gmplot.from_geocode("Belo Horizonte")



# gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
# gmap.scatter(latitudes, longitudes, '#3B0B39', size=80, marker=False)
# gmap.scatter(latitudes, longitudes, 'g', size=40, marker=False)
# gmap.scatter(rel_lat, rel_lon, 'r', marker=True)
# gmap.scatter(point_lat, point_lon, 'b', marker=True)
# gmap.heatmap(latitudes, longitudes)

gmap.draw(filename)
