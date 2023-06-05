# pypi auto scanner

A github action that fetches the latest pypi packages and scans them using semgrep rules in [h4sh-semgrep-rules](https://github.com/h4sh5/h4sh-semgrep-rules). Currently stores the JSON report in github action artifacts.

## Fetching the latest report

You will need a Github API token to do this. Export the token to `GH_TOKEN` by running `export GH_TOKEN=ghp...`

Then run `./fetch_latest_report.sh` and `unzip report.zip`

You can parse the JSON report for stuff using `parse-semgrep-json.py` as an example.


