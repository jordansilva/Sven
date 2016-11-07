import sys
import gmplot
from pymongo import MongoClient

if len(sys.argv) < 2:
    print("Illegal number of parameters")
    print("map2.py <city>")
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

filename = "%s-checkins-heatmap.html" % (db_arg)

client = MongoClient(host='150.164.2.168')
db = client[db_name]
db.authenticate('jordan', '058414', source='admin')

latitudes = []
longitudes = []

# result = db['venues'].find({}, {'uid': 1, 'point': 1})
# venues = {}
# for item in result:
#     venues[item['uid']] = item['point']
# result.close()

gmap = gmplot.GoogleMapPlotter(city_coord[0], city_coord[1], 10)
result = db['checkins'].find({}, {'point': 1})#.skip(skip).limit(limit)
for item in result:
    # vid = item['venue']
    # point = venues[vid]
    point = item['point']
    latitudes.append(point[1])
    longitudes.append(point[0])

result.close()


# gmap.scatter(latitudes, longitudes, 'cornflowerblue', size=40, marker=False)
# gmap.scatter(latitudes, longitudes, 'cornflowerblue', size=40, marker=False)

# gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=40)
# gmap.scatter(latitudes, longitudes, '#3B0B39', size=80, marker=False)
# gmap.scatter(latitudes, longitudes, 'g', size=40, marker=False)
# gmap.scatter(rel_lat, rel_lon, 'r', marker=True)
# gmap.scatter(point_lat, point_lon, 'b', marker=True)
gmap.heatmap(latitudes, longitudes)

gmap.draw(filename)
