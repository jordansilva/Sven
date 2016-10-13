import gmplot
import itertools
from pymongo import MongoClient

client = MongoClient(host='150.164.2.168')
db = client['kunkka-nyc']

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

gmap = gmplot.GoogleMapPlotter(40.7128, -74.0059, 10)

result = db['checkins'].find().skip(50000).limit(6)
for item in result:
    point_lat = []
    point_lon = []
    rel_lat = []
    rel_lon = []
    latitudes = []
    longitudes = []

    point_lat.append(item['point'][1])
    point_lon.append(item['point'][0])

    venue = db['venues-all'].find_one({'uid': item['venue']})
    rel_lat.append(venue['point'][1])
    rel_lon.append(venue['point'][0])

    max_dist = 5000
    limit = 499
    cand = item['venue']
    
    result2 = db['venues'].find({'uid': {'$in': item['cand_checked']}})
    for item2 in result2:
        latitudes.append(item2['point'][1])
        longitudes.append(item2['point'][0])

    result2.close()

    color = next(colors)
    gmap.scatter(point_lat, point_lon, color=color[0], size=5000, marker=False)
    gmap.scatter(point_lat, point_lon, color=color[1], marker=True)
    gmap.scatter(rel_lat, rel_lon, color=color[2], marker=True)
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

gmap.draw("mymap-checked.html")
