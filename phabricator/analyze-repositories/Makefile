INSTANCE = "devcentral.nasqueron.org"
TOKEN != ../read-token.py ${INSTANCE}

all: analyze

repositories.json:
	 curl https://${INSTANCE}/api/diffusion.repository.search -d api.token=${TOKEN} -d queryKey=all -d attachments[uris]=1 > repositories.json

analyze: repositories.json
	./coherence-check-repositories.py repositories.json
