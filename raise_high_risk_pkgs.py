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
    if r.status not in[200,201]:
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
        issue_data = {"title":f"{name} has {len(pkg_detections[name])} detections", "body":json.dumps(pkg_detections[name],indent=2), "labels":["suspicious","semgrep"]}
        try:
            create_github_issue(issue_data)
        except:
            pass

# parse sus file extensions output
sus_files = {}
with open('sus_files.txt','r') as f:
    for line in f:
        line = line.strip()
        pkg_name = line.split('/')[1]
        filepath = line.split(':')[0]
        file_magic = line.split(': ')[1]
        if pkg_name not in sus_files:
            sus_files[pkg_name] = []
        sus_files[pkg_name].append(line)

for name in sus_files:
    issue_data = {"title":f"{name} has {len(sus_files[name])} suspicious file formats", "body":json.dumps(sus_files[name],indent=2), "labels":["sus-file-formats"]}
    try:
        create_github_issue(issue_data)
    except:
        pass


# parse yara scan output WIP
yara_results = {}
with open('sus_files.txt','r') as f:
    for line in f:
        line = line.strip()
        pkg_name = line.split(' ')[1].split('/')[1]
        if pkg_name not in yara_results:
            yara_results[pkg_name] = []
        yara_results[pkg_name].append(line)

for name in yara_results:
    issue_data = {"title":f"{name} has {len(yara_results[name])} yara scan results", "body":'```'+json.dumps(yara_results[name],indent=2)+'```', "labels":["yara"]}


#import code
#code.interact(local=locals())
