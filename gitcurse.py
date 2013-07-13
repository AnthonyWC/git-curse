import urllib.request, urllib.error, json, re
import twitter_status

regexPattern = "(fuck|bitch|shit|asshole|damn|wtf)"
oauth = json.load(open("keys.json"))
mostRecent = 0
headers = [("User-Agent", "GitCurse Bot")]
c = 0
while True:
	opener = urllib.request.build_opener()
	opener.addheaders = headers

	try:
		req = opener.open("https://api.github.com/events?client_id=7263b8ecab24f4b9aa2d&client_secret=eb9ac06e62d4538417a1d3b9b7b56a775584b95b")
		headers = [("If-Modified-Since", req.info()["Last-Modified"]), ("User-Agent", "GitCurse Bot")]
		out = json.loads(req.read().decode("UTF-8"))

		for event in reversed(out):
			if int(event['id']) > mostRecent and event['type'] == "PushEvent" and event['payload']['commits']:
				mostRecent = int(event['id'])
				for commit in event['payload']['commits']:
					if(re.search(regexPattern, commit['message'], re.IGNORECASE)):
						url = commit['url'].replace("api.", "").replace("/repos", "").replace("commits", "commit")
						twitter_status.postStatus(commit['message'] + '\n' +  url, oauth["consumer_secret"], oauth["consumer_key"], oauth["token_secret"], oauth["access_token"])

	except urllib.error.HTTPError as e:
		continue