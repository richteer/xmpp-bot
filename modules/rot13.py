
def rot13(string):
	return "".join([chr((((ord(c) - ord('a')) + 13 ) % 26) + ord('a')) for c in string])
	
def rot13_handler(string):
	if string == None:
		return None

	return rot13(string)


commands = {
	"!rot13":rot13_handler
}

help_text = {
	"!rot13":"\nUsage: !rot13 <string>\nReturns the string where each letter has been 'rotated' around the alphabet 13 places"
}
