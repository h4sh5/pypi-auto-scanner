echo 'make sure your GH_TOKEN is set! public repo access is enough to download the artifact.'
URLS=$(curl https://api.github.com/repos/h4sh5/pypi-auto-scanner/actions/artifacts | grep archive_download_url| cut -d '"' -f 4)

for DL_URL in $URLS
do
	echo Downloading from $DL_URL
	ARTIFACT_ID=$(echo $DL_URL|cut -d / -f9)
	curl -L -H "Accept: application/vnd.github+json" -H "Authorization: Bearer $GH_TOKEN" -H "X-GitHub-Api-Version: 2022-11-28"  -o report_${ARTIFACT_ID}.zip "$DL_URL" 
done
