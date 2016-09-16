#! /bin/env python3

import sys
#import shapefile
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
import argparse
import json

import fiona
import pyproj

DEFAULT_SHAPEFILE='lib/ia/iowa_border.shp'

nativeProj=None

def loadShapefile(infile):

    with fiona.open(infile) as source:
        bounds=source.bounds
        crs=source.crs
        records=list(source)

    props={
            'bounds':bounds,
            'crs':crs
            }

    global nativeProj
    nativeProj=crs['init']

    polygons=[]
    for feature in records:
        featuretype=feature['geometry']['type']
        if featuretype=='Polygon':
            coordinates=feature['geometry']['coordinates']
            for ring in coordinates:
                polygons.append(Polygon(ring))

    return MultiPolygon(polygons)


def transformCoords(lat,lon):

    assert nativeProj, print("transformCoords: No nativeProj, run loadShapefile first!")

    proj0=pyproj.Proj(init='epsg:4326')  # Mercator lat/lon
    proj1=pyproj.Proj(init=nativeProj) # IA UTM

    (x,y)=pyproj.transform(proj0,proj1,lon,lat)
    return Point(x,y)


if __name__=='__main__':

    import argparse
    parser=argparse.ArgumentParser(
            description='Read a shapefile.'
            )

    parser.add_argument('lat',type=float,
            help='Latitude')
    parser.add_argument('lon',type=float,
            help='Longitude')
    parser.add_argument('--shapefile',type=str,default=DEFAULT_SHAPEFILE,
            help='path to shapefile.shp')

    args=parser.parse_args()

    polyshape=loadShapefile(args.shapefile)

    point=transformCoords(args.lat,args.lon)
#    print('%s,%s is now %s %s.' % (args.lat,args.lon,point.x,point.y))

    if polyshape.intersects(point):
        print('Yes! in shape.')
    else:
        print('Nope, outside shape.')


