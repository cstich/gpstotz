from rtree import index  # requires libspatialindex-c3.deb
from shapely.geometry import Polygon
from shapely.geometry import Point

import shapefile

''' Read the world timezone shapefile '''
tzshp = open("resources/world/tz_world.shp", "rb")
tzdbf = open("resources/world/tz_world.dbf", "rb")
tzshx = open("resources/world/tz_world.shx", "rb")
tzworld = shapefile.Reader(shp=tzshp, dbf=tzdbf, shx=tzshx)
shapes = tzworld.shapes()

''' Build the geo-index '''
idx = index.Index()
for i, shape in enumerate(shapes):
        idx.insert(i, shape.bbox, obj=(i, Polygon(shape.points)))


def gpsToTimezone(lat, lon):
    '''
    For a pair of lat, lon coordiantes returns the appropriate timezone info.
    If a point is on a timezone boundary, then this point is not within the
    timezone as it is on the boundary. Does not deal with maritime points.
    For a discussion of those see here:
    http://efele.net/maps/tz/world/
    @lat: latitude
    @lon: longitude
    @return: Timezone info string
    '''
    query = [n.object for n in idx.intersection((lon, lat, lon, lat),
                                                objects=True)]
    queryPoint = Point(lon, lat)
    result = [tzworld.records()[q[0]][0] for q in query
              if q[1].contains(queryPoint)]
    if len(result) > 0:
        return result[0]
    else:
        return None

if __name__ == "__main__":
    ''' Tests '''
    assert gpsToTimezone(0, 0) is None  # In the ocean somewhere
    assert gpsToTimezone(51.50, 0.12) == 'Europe/London'
