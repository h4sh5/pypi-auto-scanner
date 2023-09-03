# pypi auto scanner

A github action that periodically fetches the latest pypi packages and scans them using a variety of methods:
- Datadog's guarddog tool (which uses `semgrep` rules to run static analysis on source code)
- custom yara rules
- running `file` and detection binary executables
- Sysdig+tcpdump dynamic analysis during install time

Note that the above techniques work well for NPM as well! A NPM equivalent of this repo will be available soon in the future.

Currently stores the JSON report in github action artifacts, `*.txt` files with a bunch of potentially malicious package names, and raises [issues](https://github.com/h4sh5/pypi-auto-scanner/issues) when suspicious packages are found.

