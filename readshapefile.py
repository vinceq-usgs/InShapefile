#! /bin/env python3

import sys
#import shapefile
import argparse
import json

import fiona
import pyproj

if __name__=='__main__':

    import argparse
    parser=argparse.ArgumentParser(
            description='Read a shapefile.'
            )

    parser.add_argument('infile',type=str,
            help='path to shapefile.shp')

    args=parser.parse_args()

    infile=args.infile
    print("Reading",infile)

    with fiona.open(infile) as source:
            records=list(source)
    geojson={'type':'FeatureCollection','features':records}

    proj0=pyproj.Proj(init='epsg:26915')
    proj1=pyproj.Proj(init='epsg:4326')

    for record in records:
        recordtype=record['geometry']['type']

        if recordtype=='Polygon':
            for pt in record['geometry']['coordinates'][0]:
                x,y=pt
                lon,lat=pyproj.transform(proj0,proj1,x,y)
                print('%i %i => %.4f,%.4f' % (x,y,lon,lat))

