import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "barcelona_spain.osm"
post_code_re = re.compile(r'^\d{5}$', re.IGNORECASE)
post_codes = []

def audit_postcode(post_code):
    if not re.match(post_code_re, post_code):
        if post_code not in post_codes:
            post_codes.append(post_code)


def is_post_code(elem):
    return (elem.attrib["k"] == "addr:postcode")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_post_code(tag):
                    audit_postcode(tag.attrib["v"])

    return post_codes


def update_postcode(postcode):
    if re.match(r'^[0-9]{6}$', postcode):
        postcode = postcode[:-1]
    elif postcode == '08':
        postcode = '08000'
    elif re.match(r'^[0-9]{2}$', postcode):
        postcode = '080' + postcode
    elif re.match(r'^[0-9]{4}$', postcode): 
        postcode = '0' + postcode
    elif re.match(r'^[a-zA-z]$', postcode):
        postcode = '08000'
    elif re.match(r'^[0-9]{5}', postcode): 
        postcode = re.findall(r'^[0-9]{5}', postcode)[0]
    else:
        postcode = '08000'
    return postcode


def run():
    post_codes = audit(OSMFILE)
    print post_codes
    for po in post_codes:
        better_po = update_postcode(po)
        print po.encode("utf-8"), "=>", better_po.encode("utf-8")
            
if __name__ == "__main__":
    run()

