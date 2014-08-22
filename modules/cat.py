import requests
import re

def init():
	regex = re.compile(re.escape('<img src="(.*)">'))

def cat(string):
	if string in [None, "gif", "jpg", "png"]:
		picformat = string

	r = requests.get("http://thecatapi.com/api/images/get?format=html{}".format("&type="+picformat if picformat else ""))
	m = regex.search(r.text)

	if m:
		return m.group(1)
	else:
		return None

def catfacts(string):
	return requests.get("http://catfacts-api.appspot.com/api/facts").json["facts"]

commands = {
	"!cat":cat,
	"!catfact":catfacts
}
