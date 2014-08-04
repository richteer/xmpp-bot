import requests


def ducksearch(string):
	if string == None:
		return "It is kind of hard to search for nothing..."
	r = requests.get("http://api.duckduckgo.com/?q={}&format=json&no_html=1".format(string))
	response = r.json["Abstract"]	
	if response == '':
		return "No result found :("
	else:
		return response


commands = {
	"!ddg":ducksearch
}
