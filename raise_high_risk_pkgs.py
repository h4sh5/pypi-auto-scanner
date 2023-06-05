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
        pkg_detections[pkg_name] = []
    pkg_detections[pkg_name].append(i)


#print(sev_map)
for name in pkg_detections:
    #print(name, pkg_detections[name])
    error_exists = False
    for d in pkg_detections[name]:
        severity = d['extra']['severity']
        if severity == "ERROR":
            error_exists = True
            break
    if len(pkg_detections[name]) > 2 and error_exists:
        print("High risk pkg:", name)
        with open('high_risk_pkgs.txt','a+') as f:
            f.write(name+'\n')
#import code
#code.interact(local=locals())
