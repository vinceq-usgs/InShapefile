# shape2poly

Package to read a shapefile, determine the coordinate reference
system, turn it into a multipolygon, and determine if a point is 
inside it.

Uses pyproj, shapely, fiona.
Need to install GDAL, PROJ.4

INSTALLATION

NOTE: Remember to use mypy virtualenv

Install Proj.4 from, e.g., http://download.osgeo.org/proj/proj-4.9.2.tar.gz
(may be necessary to fix LD_LIBRARY_PATH)

Install GDAL
Install GEOS

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

