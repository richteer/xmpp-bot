import random
import os

quotes = []

def init():
	global quotes
	quotes = []
	with open("quotes.txt","r")as f:
		quotes = f.read().splitlines()

def quote_handler(string):
	if len(quotes) == 0:
		return "Error: quotes.txt wasn't initialized properly?"
	if string == None:
		return quotes[random.randint(0, len(quotes)-1)]
	temp = [q for q in quotes if string.lower() in q.lower()]
	if len(temp) == 0:
		return "No quotes match your string"
	return temp[random.randint(0, len(temp)-1)]

def quoteadd_handler(string):
	if string == None:
		return "No quote supplied!"
	if len(quotes) >= 50:
		return "Too many quotes in the buffer, sorry :("
	quotes.append(string)
	return "Added! :)"

def writequotes_handler(string):
	try:
		with open("quotes.txt","w") as f:
			f.write("\n".join(quotes))
	except:
		return "Could not write to 'quotes.txt', sorry..."
	return "Updated 'quotes.txt'!"


commands = {
	"!quote":quote_handler,
	"!quoteadd":quoteadd_handler
}

admincommands = {
	"!writequotes":writequotes_handler,
	"!reloadquotes":lambda x: init()
}

help_text = {
	"!quote":"\nUsage: !quote [substring]\nReplies with a random quote from 'quotes.txt'.\nIf an argument is supplied, return only quotes that contain that substring",
	"!quoteadd":"\nUsage: !quoteadd <quote>\nTemporarily add the quote into the pool of quotes.\nNOTE: Quotes added this way will NOT persist when the bot is shut down, or the module is reloaded."
}
