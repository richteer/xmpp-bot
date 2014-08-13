
def rot13(string):
	result = ""
	
	for v in string:
		c = ord(v) - ord('a')
		c = (c + 13) % 26
		result += chr(c + ord('a'))
	return result

def rot13_handler(string):
	if string == None:
		return None

	return rot13(string)


commands = {
	"!rot13":rot13_handler
}
