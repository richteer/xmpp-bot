import requests

def handle_xkcd(string):
	if string == None:
		return None

	if string == "today":
		r = requests.get("http://xkcd.com/info.0.json")
		if r.json:
			return 'xkcd {0} - "{1}": {2}'.format(string, r.json["title"], r.json["img"])
		else:
			return "Could not find that one, does it even exist?"


	try:
		int(string)
	except:
		return None

	r = requests.get("http://xkcd.com/{0}/info.0.json".format(string))
	if r.json:
		return 'xkcd {0} - "{1}": {2}'.format(string, r.json["title"], r.json["img"])
	else:
		return "Could not find that one, does it even exist?"

commands = {
	"!xkcd":handle_xkcd
}
