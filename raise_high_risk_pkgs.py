#!/usr/bin/env python3
import json
import os
import sys
from urllib.request import urlopen,Request

'''
script to parse output of static / other scanners and raise github issues
'''

def create_github_issue(body):
    url = 'https://api.github.com/repos/h4sh5/pypi-auto-scanner/issues'
    request = Request(url, data=json.dumps(body).encode('utf-8'), headers={"Accept":"application/vnd.github+json", "Authorization":f"Bearer {os.getenv('GITHUB_TOKEN')}", "X-GitHub-Api-Version":"2022-11-28"})
    r = urlopen(request)
    data = r.read()
    if r.status not in[200,201]:
        print('ERROR create_github_issue', r.status, data)

def get_project_link(name):
    return 'https://pypi.org/project/'+name

def get_inspector_link(name):
    return 'https://inspector.pypi.io/project/'+name

# currently guarddog
file = 'report.json'

if len(sys.argv) > 1:
    file = sys.argv[1]

results = json.load(open(file, 'r'))

# detections
pkg_detections = {}

for i in results:
    name_ver = i['dependency'] + ' ' + i['version']
    if i['result']['issues'] > 0:
        pkg_detections[name_ver] = i

for name_ver in pkg_detections:
    name = name_ver.split()[0]
    issue_data = {"title":f"{name_ver} has {pkg_detections[name_ver]['result']['issues']} GuardDog issues", "body":f'{get_project_link(name)}\n{get_inspector_link(name)}\n```'+json.dumps(pkg_detections[name_ver],indent=2)+'```', "labels":["suspicious","guarddog"]}
    try:
        create_github_issue(issue_data)
    except:
        pass


# parse sus file extensions output
sus_files = {}
with open('new_sus_files.txt','r') as f:
    for line in f:
        line = line.strip()
        pkg_name = line.split('/')[1]
        filepath = line.split(':')[0]
        file_magic = line.split(': ')[1]
        if pkg_name not in sus_files:
            sus_files[pkg_name] = []
        sus_files[pkg_name].append(line)

for name in sus_files:
    issue_data = {"title":f"{name} has {len(sus_files[name])} suspicious file formats", "body":f'{get_project_link(name)}\n{get_inspector_link(name)}\n```'+json.dumps(sus_files[name],indent=2)+'```', "labels":["sus-file-formats"]}
    try:
        create_github_issue(issue_data)
    except:
        pass


# parse yara scan output WIP
yara_results = {}
with open('new_yara_results.txt','r') as f:
    for line in f:
        line = line.strip()
        if len(line) <= 1: #skip empty lines
            continue
        pkg_name = line.split(' ')[1].split('/')[1]
        if pkg_name not in yara_results:
            yara_results[pkg_name] = []
        yara_results[pkg_name].append(line)

for name in yara_results:
    issue_data = {"title":f"{name} has {len(yara_results[name])} yara scan results", "body":f'{get_project_link(name)}\n{get_inspector_link(name)}\n```'+json.dumps(yara_results[name],indent=2)+'```', "labels":["yara"]}
    try:
        create_github_issue(issue_data)
    except:
        pass


#import code
#code.interact(local=locals())
