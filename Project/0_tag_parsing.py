#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Prints out what tags are there and also how many, to get the
feeling on how much of which data you can expect to have in the map.
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    tags = {}
    osm_file = open(filename, 'r')
    for event, element in ET.iterparse(osm_file):
        try: 
            tags[element.tag] += 1
        except KeyError:
            tags[element.tag] = 1
    return tags

def run():

    tags = count_tags('barcelona_spain.osm')
    pprint.pprint(tags)

if __name__ == "__main__":
    run()