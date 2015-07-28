#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # Temporal vars
        created = {} #dictionary for created object
        pos = [] #position list
        node_refs = [] #node references list
        # Starting document construction
        node["id"] = element.attrib["id"]
        node["type"] = element.tag
        #try if visible exists in tag. If so, assign it to "visible" key in node
        try:
            node["visible"] = element.attrib["visible"]
        except KeyError:
            node["visible"] = "false"
        #try if lat & lon exists in tag. If so, assign it to "visible" key in node
        try:
            pos.append(float(element.attrib["lat"]))
            pos.append(float(element.attrib["lon"]))
            node["pos"] = pos
        except KeyError:
            pass
        for createdKey in CREATED: #for each element in CREATED create a key in created with respective value 
            created[createdKey] = element.attrib[createdKey]
        node["created"] = created
        tags = element.findall("tag")
        nds = element.findall("nd")
        if len(tags) > 0: #there are tags labelled "tag" inside the node
            for tag in tags:
                tagKey = tag.attrib["k"]
                tagValue = tag.attrib["v"]
                tagKeySplit = re.split('\:', tagKey) #split all the words into tagKeySplit List
                if not problemchars.search(tagKey): # search for Problematic Chars
                    node = parse_key(node, tagKeySplit, tagValue)
            # Change the key name "addr" to "address"
            try: 
                node["address"] = node.pop("addr")
            except KeyError:
                pass
        if len(nds) > 0: #there are tags labelled "tag" inside the node
            for nd in nds: #for each node ref
                node_refs.append(nd.attrib["ref"]) #append to the nodes refs list
            node["node_refs"] = node_refs
        return node
    else:
        return None

def parse_key(keyDict, keyList, keyValue):     
    if len(keyList) == 1:
        keyDict[keyList[0]] = keyValue
    else:
        if keyList[0] not in keyDict:
            keyDict[keyList[0]] = {}
        if isinstance(keyDict[keyList[0]], dict):
            parse_key(keyDict[keyList[0]], keyList[1:], keyValue)
        else:
            keyDict[create_newKey(keyList)] = keyValue
    return keyDict

# Create new key name for keys 
def create_newKey(keyList):
    newKey = ""
    for key in keyList:
        newKey += key + "_"
    newKey = newKey[:-1] #remove last "_"
    return newKey

def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w", "utf-8") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def dbInsert(data):
   
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.map
    [db.barcelona.insert(line) for line in data]
    print db.barcelona.find_one()

def run():
    data = process_map('barcelona_spain.osm', True)
    dbInsert(data)

if __name__ == "__main__":
    run()
