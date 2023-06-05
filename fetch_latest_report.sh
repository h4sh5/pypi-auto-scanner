echo 'make sure your GH_TOKEN is set! public repo access is enough to download the artifact.'
DL_URL=$(curl https://api.github.com/repos/h4sh5/pypi-auto-scanner/actions/artifacts | grep archive_download_url| head -1 |cut -d '"' -f 4)
echo Downloading from $DL_URL
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -o report.zip \
  "$DL_URL" 
echo Saved to report.zip
