#!/usr/bin/env python3
import json
import os
import sys
from urllib.request import urlopen,Request

'''
script to parse semgrep json output
'''

def create_github_issue(body):
    url = 'https://api.github.com/repos/h4sh5/pypi-auto-scanner/issues'
    request = Request(url, data=json.dumps(body).encode('utf-8'), headers={"Accept":"application/vnd.github+json", "Authorization":f"Bearer {os.getenv('GITHUB_TOKEN')}", "X-GitHub-Api-Version":"2022-11-28"})
    r = urlopen(request)
    data = r.read()
    if r.status != 200:
        print('ERROR create_github_issue', r.status, data)

    

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
    if error_exists or len(pkg_detections[name]) > 3:
        print("High risk pkg:", name)
        with open('high_risk_pkgs.csv','a+') as f:
            f.write(f'{name},{len(pkg_detections[name])}\n')
        issue_data = {"title":f"{name} has {len(pkg_detections[name])} detections", "body":json.dumps(pkg_detections[name],indent=2), "labels":["suspicious"]}
        create_github_issue(issue_data)

#import code
#code.interact(local=locals())
