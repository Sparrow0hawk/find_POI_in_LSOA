## Basic count points of interest of specified type in LSOA

In my current project i'm compiling points of interest within specific lower super output areas.

Using the overpass API I built this script that takes inputs of a location (which is checked by Nominatim) and amenity type (point of interest type, https://wiki.openstreetmap.org/wiki/Key:amenity). It retrieves these and compares the lon/lat points to geojson polygons of LSOAs (in this case my pre-made West Yorkshire geojson file).

The principal used here might be helpful to others so here it is.
