import string, base64, re, time, random, hmac, binascii, os, urllib.request
from hashlib import sha1
from json import load
import log

def percentEncode(toEncode):
	toEncode = toEncode.encode("UTF-8")
	okay = string.ascii_letters + string.digits + "-._~"
	okay = okay.encode("UTF-8")
	out = ""
	for char in toEncode:
		if not char in okay:
			hexVal = hex(char)[2:].upper()
			while len(hexVal) < 2:
				hexVal = "0" + str(hexVal)
			out += "%" + str(hexVal)
		else:
			out += chr(char)
	return out

def createNonce():
     out = ""
     for x in range(32):
             out += chr(int(random.random() * 256))

     out = base64.urlsafe_b64encode(bytes(out, "UTF-8"))
     out = re.sub(b"[^0-9a-zA-Z]", b"", out)

     return out[:42].decode("UTF-8")

def createSignature(http_method, base_url, parameters, consumer_secret, token_secret):
	parameter_string = ""
	first = True
	for key, value in sorted(parameters.items()):
		if not first:
			parameter_string += "&"
		else:
			first = False
		parameter_string += percentEncode(key) + "=" + percentEncode(value)
	base_string = http_method.upper() + "&" + percentEncode(base_url) + "&" + percentEncode(parameter_string)
	signing_key = percentEncode(consumer_secret) + "&" + percentEncode(token_secret)
	hashed = hmac.new(bytes(signing_key, "UTF-8"), bytes(base_string, "UTF-8"), sha1)
	signature = binascii.b2a_base64(hashed.digest())[:-1]
	return signature.decode("UTF-8")

def createAuthString(parameters):
	auth_string = "OAuth "

	first = True
	for key, value in sorted(parameters.items()):
		if not first:
			auth_string += ", "
		else:
			first = False
		auth_string += percentEncode(key) + '="' + percentEncode(value) + '"'

	return auth_string

def postStatus(status, consumer_secret, consumer_key, token_secret, access_token, debug=False):
	http_method = "POST"
	base_url = "https://api.twitter.com/1.1/statuses/update.json"

	oauth_parameters = {
	"oauth_consumer_key" : consumer_key, 
	"oauth_nonce" : createNonce(),
	"oauth_signature_method" : "HMAC-SHA1", 
	"oauth_timestamp" : str(int(time.time())), 
	"oauth_token" : access_token, 
	"oauth_version": "1.0"
	}

	info_parameters = {
	"status" : status,
	"include_entities" : "true"}


	parameters = info_parameters.copy()
	parameters.update(oauth_parameters.items())

	oauth_parameters["oauth_signature"] = createSignature(http_method, base_url, parameters, consumer_secret, token_secret)

	auth_string = createAuthString(oauth_parameters)
	post_data = bytes("status=" + percentEncode(info_parameters["status"]), "UTF-8")
	if debug:
		log.log("info.log", "[twitter_status.py]  Status Posted: " + str(post_data))

	req = urllib.request.Request("https://api.twitter.com/1.1/statuses/update.json?include_entities=true", data=post_data, headers={"Authorization":auth_string})
	urllib.request.urlopen(req)