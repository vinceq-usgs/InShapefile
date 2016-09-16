#! /bin/env python3

import shape2poly as s2p

shape=s2p.loadShapefile('lib/ia/iowa_border.shp')
point=s2p.transformCoords(43,-93)

if shape.intersects(point):
    print("Yes!")

else:
    print("No!")

    
