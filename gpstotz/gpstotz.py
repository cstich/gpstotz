'''
Author: Christoph Stich
Date: 2015-05-25
Finds for a lat, lon coordinate pair the appropriate timezone
'''

from rtree import index  # requires libspatialindex-c3.deb
from shapely.geometry import Polygon
from shapely.geometry import Point

import os
import fiona

''' Read the world timezone shapefile '''
tzshpFN = os.path.join(os.path.dirname(__file__),
                       'resources/world/tz_world.shp')

''' Build the geo-index '''
idx = index.Index()
with fiona.open(tzshpFN) as shapes:
    for i, shape in enumerate(shapes):
        assert shape['geometry']['type'] == 'Polygon'
        exterior = shape['geometry']['coordinates'][0]
        interior = shape['geometry']['coordinates'][1:]
        record = shape['properties']['TZID']
        poly = Polygon(exterior, interior)
        idx.insert(i, poly.bounds, obj=(i, record, poly))


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
    result = [q[1] for q in query
              if q[2].contains(queryPoint)]

    if len(result) > 0:
        return result[0]
    else:
        return None

if __name__ == "__main__":
    ''' Tests '''
    assert gpsToTimezone(0, 0) is None  # In the ocean somewhere
    assert gpsToTimezone(51.50, 0.12) == 'Europe/London'
