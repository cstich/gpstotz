# gpstotz 0.2
Given a lat, lon coordinate pair returns the appropriate timezone. 
Basically a Python wrapper for Eric Muller's map of timezones (http://efele.net/maps/tz/world/).

## Usage
```
from gpstotz import gpstotz
lat = 51.50
lon = 0.12
timezone = gpstotz.gpsToTimezone(lat, lon)
```

## Timezone boundaries
The library follows the shapely convention that boundaries are not part of the object. Thus, a measurement on the
boundary of a timezone polygon is not part of the timezone.

## To-Do
- Add UTC-Offset
