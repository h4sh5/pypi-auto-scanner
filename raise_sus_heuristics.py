#!/usr/bin/env python3
import json
import os
import sys
from urllib.request import urlopen,Request


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

## bypass lists
# if the command starts with these, bypassed.
cmds_bypass_starts = ["runc init", "uname", "/usr/local/bin/pip", "/usr/local/bin/python", "/usr/bin/gcc", "/usr/lib/gcc/x86_64-linux-gnu/8/cc1", "git", "as "]
# tuples of IP:port to bypass
ip_port_bypass = [ ("168.63.129.16", "53"), ("0.0.0.0","0"), ("151.101.45.63", "443"), ("140.82.114.3","443"),("140.82.114.10","443"),("140.82.114.4","443"),("140.82.114.5","443"),("140.82.114.6","443"),("140.82.114.7","443"),("140.82.114.8","443"),("140.82.114.9","443")]

files = sys.argv[1:]

for file in files:
    try:
        d = json.load(open(file, 'r'))
    except Exception as e:
        print("error json loading",file,e)
        continue
    # keys: package, connections (protocol,address,port), dns, files, commands
    # (maybe fix src so that package is in source json file instead of filename?)
    name_ver = file.split('.iocs.json')[0]
    commands = d['commands']
    connections = d['connections']

    if commands == None:
        commands = []
    if connections == None:
        connections = []
    # TODO files and dns

    # detections
    detection_tags = set(["sysdig"])
    pkg_detections = {}
    num_detections = 0
    for c in commands:
        sus = True
        for word in cmds_bypass_starts:
            if c.startswith(word):
                sus = False
                break
        if sus == True and "commands" not in pkg_detections:
            pkg_detections["commands"] = []
            pkg_detections["commands"].append(c)
            num_detections += 1
            detection_tags.add("commands")
    for conn in connections:
        addr_port = (conn['address'], conn['port'])
        if addr_port not in ip_port_bypass:
            if "connections" not in pkg_detections:
                pkg_detections["connections"] = []
            pkg_detections["connections"].append(conn)
            num_detections += 1
            detection_tags.add("connections")
    if pkg_detections != {}:
        # create issues
        detection_tags = list(detection_tags)
        name = name_ver.split('==')[0]
        version = name_ver.split('==')[1]
        issue_data = {"title":f"{name_ver} has heuristics detections", "body":f'{get_project_link(name)}\n{get_inspector_link(name+"/"+version)}\n```'+json.dumps(pkg_detections,indent=2)+'```', "labels":detection_tags}
        create_github_issue(issue_data)
