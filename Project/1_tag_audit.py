#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Audit "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
as well as see if there are any other potential problems.
"""


lower = re.compile(r'^([a-z]|_)*$')
upper = re.compile(r'^([A-Z]|_)*$')
mixed = re.compile(r'^([a-zA-Z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
double_lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')
triple_lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*:([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
colon = ["One level Colon", "Two levels Colon", "Three Levels Colon", "Four Levels Colon"]
other = []
problems = []

def key_type(element, keys):
    if element.tag == "tag":
        key = element.attrib['k']
        keyStatus = None
        if len(check_colon(key)) == 1:
            keyStatus = status(key)
        else:
            keyStatus = status_colon(key)

        process_status(keyStatus, keys)
    return keys

def status(key):
    if problemchars.search(key):
        problems.append(key)
        return "Problemchars"
    elif lower.search(key):
        return "Lowercase"
    elif upper.search(key):
        return "Uppercase"
    elif mixed.search(key):
        return "Mixed"
    else:
        other.append(key)
        return "Other"

def status_colon(key):
    keySplit = check_colon(key)
    keyLenght = len(keySplit)
    return colon[keyLenght-1]


def process_status(status, keys):
    if status in keys:
        keys[status] += 1
    else:
        keys[status] = 1
    return keys

def check_colon(key):
    return re.split('\:', key)

def process_map(filename):
    keys = {}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

def test():
    keys = process_map('barcelona_spain.osm')
    pprint.pprint(keys)
    print other, problems



if __name__ == "__main__":
    test()