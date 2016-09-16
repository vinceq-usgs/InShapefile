#! /bin/env python3

import shapefile
import math
from osgeo import ogr, osr, gdal

import sys
oldpath=sys.path
sys.path=['/usr/local/lib/pkgconfig']
sys.path.extend(oldpath)

gdal.UseExceptions()
inSpatialRef=None
outSpatialRef=osr.SpatialReference()
outSpatialRef.ImportFromEPSG(4326)
print(outSpatialRef)

def loadFile2(file):
    dataset = ogr.Open(file)
    layer = dataset.GetLayerByIndex(0)
    layer.ResetReading()
    return layer


def getSpatialRef(infile):
    driver=ogr.GetDriverByName('ESRI Shapefile')
    dataSource=driver.Open(infile,0) # 0 means read-only. 1 means writeable.

    # Check to see if shapefile is found.
    if dataSource is None:
        print('Could not open %s' % (infile))
    else:
        layer = dataSource.GetLayer()
        inSpatialRef=layer.GetSpatialRef()
        print(inSpatialRef)


def loadFile(infile):
    data=shapefile.Reader(infile)
    shapes=data.shapes()
    print('Got',len(shapes),'shapes, only loading the first.')
    return shapes[0]


def processPoint(lat,lon):
    #Location for New Orleans: 29.98 N, -90.25 E
    print("lat=",lat,"lon=",lon)
    point = ogr.CreateGeometryFromWkt("POINT(%s %s)" % (lon,lat))

    # Transform the point into the specified coordinate system from WGS84
    spatialRef1 = osr.SpatialReference()
    spatialRef1.ImportFromEPSG(4326)
    spatialRef2 = osr.SpatialReference()
    spatialRef2.ImportFromEPSG(26915)
    coordTransform = osr.CoordinateTransformation(spatialRef1,spatialRef2)

    print("Transforming...")
    point.Transform(coordTransform)
    print(point)
    return point


def getPolygon(layer):
    polygon=ogr.Geometry(ogr.wkbLinearRing)
    lastx=None
    lasty=None
    npts=0
    nadded=0

    for pt in layer.points:
        npts+=1
        x=math.floor(pt[0])
        y=math.floor(pt[1])

        if x==lastx or y==lasty:
            continue

        polygon.AddPoint(x,y)
        lastx=x
        lasty=y
        nadded+=1

    print('Added',nadded,'/',npts,'points to polygon.')
    return polygon
 
def inPolygon(point,polygon):
    isin=False
    print('Testing Contains.')
    isin=polygon.Contains(point)
    
    return isin

def gdal_error_handler(err_class, err_num, err_msg):
    errtype = {
        gdal.CE_None:'None',
        gdal.CE_Debug:'Debug',
        gdal.CE_Warning:'Warning',
        gdal.CE_Failure:'Failure',
        gdal.CE_Fatal:'Fatal'
        }

    err_msg = err_msg.replace('\n',' ')
    err_class = errtype.get(err_class, 'None')
    print('Error Number: %s' % (err_num))
    print('Error Type: %s' % (err_class))
    print('Error Message: %s' % (err_msg))


if __name__=='__main__':

    # install error handler
    gdal.PushErrorHandler(gdal_error_handler)
           
    import argparse
    parser=argparse.ArgumentParser(
              description='See if a point is inside a shapefile.'
              )
    parser.add_argument('lat',type=float,default=20,help='Latitude')
    parser.add_argument('lon',type=float,default=20,help='Longitude')
    parser.add_argument('--shapefile',type=str,default='./lib/ia/iowa_border.shp',
            help='Shapefile')
    args=parser.parse_args()

    print("Loading input spatial ref.")
    getSpatialRef(args.shapefile)

    print("Loading layer.")
    layer=loadFile(args.shapefile)

    polygon=getPolygon(layer)

    print("Transforming point.")
    point=processPoint(args.lat,args.lon)

    print("Running inPolygon.")

    isin = inPolygon(point,polygon)
    if isin:
        print('Yes, inside polygon.')
    else:
        print('No, outside polygon.')

