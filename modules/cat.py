import requests
import re

regex = None

def init():
	global regex
	regex = re.compile('<img src="(.*)">')

def cat(string):
	if string in [None, "gif", "jpg", "png"]:
		picformat = string

	r = requests.get("http://thecatapi.com/api/images/get?format=html{}".format("&type="+picformat if picformat else ""))
	m = regex.search(r.text)

	if m:
		return m.group(1)
	else:
		print("Error extracting the image url!")
		return None

def catfacts(string):
	return requests.get("http://catfacts-api.appspot.com/api/facts").json["facts"]

commands = {
	"!cat":cat,
	"!catfact":catfacts
}

help_text = {
	"!cat":"\nUsage: !cat [ gif | jpg | png ]\nReturns a link to a cat picture. You may optionally supply either jpg, png, or gif, to specify the image format.",
	"!catfact":"\nUsage: !catfact\nReplies with a random cat fact. Nothing more, nothing less."
}
