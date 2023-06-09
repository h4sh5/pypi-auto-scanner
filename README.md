# pypi auto scanner

A github action that periodically fetches the latest pypi packages and scans them using a variety of methods:
- Datadog's guarddog tool (which uses `semgrep` rules to run static analysis on source code)
- custom yara rules
- running `file` and detection binary executables
- Sysdig+tcpdump dynamic analysis during install time

Note that the above techniques work well for NPM as well! A NPM equivalent of this repo will be available soon in the future.

Currently stores the JSON report in github action artifacts, `*.txt` files with a bunch of potentially malicious package names, and raises [issues](https://github.com/h4sh5/pypi-auto-scanner/issues) when suspicious packages are found.


## Why?

If you search "pip malicious packages feed", you will not find anything other than a bunch of vendor blogs that say "researcher from our company found another 10,000 malicious pip packages..", some package names and screenshots.

If you want to identify these malicious packages across your environment and roll incident response, there is currently **no open data** to do so **accessible via an API**.

This repo is hopefully, eventually going to be low-noise enough to be used as a high-fidelity feed for malicious pip packages; you can even use the txt output files we provide and grab the github issues via Github API yourself, and match it against things in your environment and bypass the false positives from a list of known good packages you use. 

Since this repository is open source, all you need to access this data is a single HTTP request (for the txt files) and use a Github API key with permission to access public repos (for searching through issues and scan artifacts).

If you are a researcher / malware analyst / threat hunter, this dataset is also for you. In the github actions artifacts, you will find potential IoCs, PCAP files and so on; in the main repo, the yara scan results give you filenames and formats you can reverse engineer. You can use this dataset for security research academic projects.

**The supply chain security space is too important to be a closed ecosystem of vendors disclosing their findings in blogs.** 

Let's rip it open.


