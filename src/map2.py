import gmplot
from pymongo import MongoClient

client = MongoClient(host='150.164.2.168')
db = client['kunkka-nyc']

latitudes = []
longitudes = []

result = db['venues'].find({}, {'uid': 1, 'point': 1})
venues = {}
for item in result:
    venues[item['uid']] = item['point']
result.close()

skip = 0
limit = 50000
result = db['checkins'].find({}, {'venue': 1})#.skip(skip).limit(limit)
for item in result:
    vid = item['venue']
    point = venues[vid]
    latitudes.append(point[1])
    longitudes.append(point[0])

result.close()

print(len(latitudes))
gmap = gmplot.GoogleMapPlotter(40.7128, -74.0059, 10)
# gmap.scatter(latitudes, longitudes, 'cornflowerblue', size=40, marker=False)
# gmap.scatter(latitudes, longitudes, 'cornflowerblue', size=40, marker=False)

# gmap = gmplot.from_geocode("Belo Horizonte")
# gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=40)
gmap.scatter(latitudes, longitudes, '#3B0B39', size=80, marker=False)
# gmap.scatter(latitudes, longitudes, 'g', size=40, marker=False)
# gmap.scatter(rel_lat, rel_lon, 'r', marker=True)
# gmap.scatter(point_lat, point_lon, 'b', marker=True)
# gmap.heatmap(latitudes, longitudes)

gmap.draw("checkins-venues.html")
