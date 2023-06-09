#!/usr/bin/env python3

'''
a script to pull new pypi packages and print out all their names
'''

import xml.etree.ElementTree as ET
from urllib.request import urlopen
import os.path

# xml is crap, pypi please change to json at some point
url = 'https://pypi.org/rss/updates.xml'

response = urlopen(url)
body = response.read()
if response.status != 200:
    print("ERROR: response:", response.status, body)

# read already scanned list
already_scanned = []
if os.path.isfile('new.txt'):
    already_scanned = set(open('new.txt','r').read().split('\n'))

root = ET.fromstring(body)

for chan in root[0]:
    for e in chan:
        if e.tag == 'link':
            link = e.text
            name = link.split('/')[4]
            version = link.split('/')[5]
            name_ver = name + '==' + version
            if name_ver not in already_scanned:
                print(name_ver)

# debugging
#import code
#code.interact(local=locals())


