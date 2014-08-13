import os
from subprocess import check_output as px

def init():
	pass

def pull_handler(string):
	remote = "origin"
	branch = "master"

	if string:
		args = string.split(" ")
		if (len(string.split(" ")) == 2):
			remote = args[0]
			branch = args[1]

	try:
		out = px(["git","pull", remote, branch], universal_newlines=True);
	except:
		return "I have failed to pull, master!"
	return out.split("\n")[-2]

commands = {
}

admincommands = {
	"!gitpull":pull_handler
}
