#!/usr/bin/env python3
import json
import sys

'''
script to parse semgrep json output
'''

file = 'report.json'

if len(sys.argv) > 1:
    file = sys.argv[1]

d = json.load(open(file, 'r'))

results = d['results']

# detections
pkg_detections = {}
sev_map = {}

for i in results:
    pkg_name = i['path'].split('packages')[1].split('/')[1]
    if not pkg_name in pkg_detections:
        pkg_detections[pkg_name] = 0
    pkg_detections[pkg_name] += 1

    if not i['extra']['severity'] in sev_map:
        sev_map[i['extra']['severity']] = 0
    sev_map[i['extra']['severity']] += 1

#print(sev_map)
for name in sorted(pkg_detections, key=pkg_detections.get, reverse=True):
    print(name, pkg_detections[name])

#import code
#code.interact(local=locals())
