import urllib.request, urllib.error, json, re, sys, time
import twitter_status, log

debug = False
if("-d" in sys.argv):
	debug = True

regexPattern = "(fuck|bitch|shit|asshole|damn|wtf|boob|vagina|penis|in the ass)"
oauth = json.load(open("keys.json"))
mostRecent = 0
headers = [("User-Agent", "GitCurse Bot")]
c = 0
while True:
	opener = urllib.request.build_opener()
	opener.addheaders = headers

	try:
		req = opener.open("https://api.github.com/events?client_id={}&client_secret={}".format(oauth['github_id'], oauth['github_secret']))
		headers = [("If-Modified-Since", req.info()["Last-Modified"]), ("User-Agent", "GitCurse Bot")]
		out = json.loads(req.read().decode("UTF-8"))

		for event in reversed(out):
			if int(event['id']) > mostRecent and event['type'] == "PushEvent" and event['payload']['commits']:
				mostRecent = int(event['id'])
				for commit in event['payload']['commits']:
					if(re.search(regexPattern, commit['message'], re.IGNORECASE)):
						url = commit['url'].replace("api.", "").replace("/repos", "").replace("commits", "commit")
						twitter_status.postStatus('"' + commit['message'] + '"' + '\n' +  url, oauth["consumer_secret"], oauth["consumer_key"], oauth["token_secret"], oauth["access_token"], debug)

	except urllib.error.HTTPError as e:
		if(e.code != 304 and debug):
			log.log("info.log", "[gitcurse.py] HTTPError: {}".format(e.code))
	except KeyboardInterrupt as e:
		log.log("info.log", "[gitcurse.py] Exit")
		sys.exit(0)
	except:
		log.log("info.log", "[gitcurse.py] Exception: {}".format(sys.exc_info()[1]))

	time.sleep(1)