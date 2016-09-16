# InShapefile
Package to read a shapefile and determine if a set of points is inside it


INSTALLATION

NOTE: Remember to use mypy virtualenv

pip install fiona
pip install pyproj
pip install shapely

USAGE

from readshapefile import loadShapefile,transformCoords

# Returns a shapely MultiPolygon
polyshape=loadShapefile('someshape.shp')

# Returns a shapely Point
point=transformCoords(lat,lon)

# obj.intersects() method from shapely
if polyshape.intersects(point):
	print('Yes, inside someshape!')

