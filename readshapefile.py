#! /bin/env python3

import sys
#import shapefile
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import argparse
import json

import fiona
import pyproj

DEFAULT_SHAPEFILE='lib/ia/iowa_border.shp'

def loadShapefile(infile):
    with fiona.open(infile) as source:
        bounds=source.bounds
        crs=source.crs
        records=list(source)

    props={
            'bounds':bounds,
            'crs':crs
            }

    geojson={'type':'FeatureCollection','features':records,'properties':props}
    return geojson


def transformCoords(lat,lon,shapeproj):
    print('Using',shapeproj)

    proj0=pyproj.Proj(init='epsg:4326')  # Mercator lat/lon
    proj1=pyproj.Proj(init=shapeproj) # IA UTM

    (x,y)=pyproj.transform(proj0,proj1,lon,lat)
    return Point(x,y)


def inShape(point,jsonshape):
    isin=False

    for feature in jsonshape['features']: 
        featuretype=feature['geometry']['type']

        if featuretype=='Polygon':
            polygons=feature['geometry']['coordinates']
            for polypts in polygons:
                polygon=Polygon(polypts)
                if polygon.intersects(point):
                    return True

    return False

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

    jsonshape=loadShapefile(args.shapefile)
    shapeproj=jsonshape['properties']['crs']['init']
    point=transformCoords(args.lat,args.lon,shapeproj)

    print('%s,%s is now %s %s.' % (args.lat,args.lon,point.x,point.y))

    if inShape(point,jsonshape):
        print('Yes! in shape.')
    else:
        print('Nope, outside shape.')


