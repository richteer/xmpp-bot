from subprocess import check_output as px

cow_enabled = True

def init():
	global cow_enabled
	try:
		px(["cowsay", "test"])
	except:
		cow_enabled = False

def get_fortune():
	try:
		out = px("fortune",universal_newlines=True)
	except:
		return None

	return out

def handle_fortune(string):
	return get_fortune()

def handle_cowsay(string):
	if not cow_enabled:
		return "Cowsay not installed!"

	if string == None:
		return None

	if string == "!fortune":
		string = get_fortune()
		if string == None:
			return None

	try:
		out = px(["cowsay"] + string.split(" "),universal_newlines=True)
	except:
		return None

	return '\n' + out

commands = {
	"!cowsay":handle_cowsay,
	"!fortune":handle_fortune
}

help_text = {
	"!cowsay":'''
Usage: !cowsay [-bdgpstwy] [-h] [-e eyes] [-f cowfile] 
          [-l] [-n] [-T tongue] [-W wrapcolumn] <message>
''' + "\nYou can also enter '!cowsay !fortune' for a fortunate cow.",
	"!fortune":"\nUsage: !fortune\nReplies with a random fortune"
}
