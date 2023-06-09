#!/usr/bin/env python3
import sys
import os
from urllib.request import urlopen, Request
import urllib
import json
import threading

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = 'h4sh5/pypi-auto-scanner'

headers = {"Accept":"application/vnd.github+json", "Authorization": f"Bearer {GITHUB_TOKEN}", "X-GitHub-Api-Version": "2022-11-28"}

# example https://api.github.com/search/issues?q=repo:h4sh5/pypi-auto-scanner+is:open+label:yara' 
issue_search_url = 'https://api.github.com/search/issues?per_page=100&q=repo:h4sh5/pypi-auto-scanner+is:open'

def search_issues(keyword):
    keyword = urllib.parse.quote(keyword)
    req = Request(issue_search_url+'+'+keyword, headers=headers)
    res = urlopen(req)
    r = json.loads(res.read().decode())
    return r

def close_issue(issue_url, title):
    data = json.dumps({'state':'closed'}).encode()
    req = Request(issue_url, headers=headers, method='PATCH', data=data)
    res = urlopen(req)
    issue_id = url.split('/')[-1]
    print(f'closing issue {issue_id}: {title}, resp code:', res.status)

#while True:
#keyword = input('keyword to search: ')

keyword = sys.argv[1]
r = search_issues(keyword)
issues = r['items']
print('found',len(issues),'issues')
# closing them all..
threads = []
for i in issues:
    url = i['url']
    issue_id = url.split('/')[-1]
    title = i['title']

    t = threading.Thread(target=close_issue, args=(url,title))
    threads.append(t)
    t.start()
print('waiting for threads..')
for t in threads:
    t.join()
print('done!')
#print(json.dumps(r,indent=2))

