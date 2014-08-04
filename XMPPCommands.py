import os
import imp

# TODO: Replace all calls to print() with appropriate logging statements

class Commander():
	commands = {}

	def __init__(self):
		self.update_commands()
		# TODO: Load this dynamically?
		self.admins = []

	def set_admins(self, ls):
		self.admins = ls

	def update_commands(self):
		mods = []
		self.commands = {}
		self.admincommands = {}
		for f in os.listdir("./modules"):
			if f[-2:] != "py":
				continue
			file,pathname,description = imp.find_module("./modules/" + f[:-3])
			mods.append(imp.load_module(f[:-3],file,pathname,description))


		for m in mods:
			try:
				for c in m.commands.keys():
					self.register(c, m.commands[c])
				if hasattr(m, "admincommands"):
					for c in m.admincommands:
						self.adminregister(c, m.admincommands[c])
				if hasattr(m, "init"):
					m.init()
			except Exception as e:
				print("Error loading commands from " + m.__name__)
				print(e)

		return "Registered commands: " + ",".join(self.commands.keys())
	
	def register(self, command, handler):
		if command in self.commands.keys():
			print("Command '{}' already registered!".format(command))
			return
		self.commands[command] = handler

	def adminregister(self, command, handler):
		if command in self.admincommands.keys():
			print("Command '{}' already registered!".format(command))
			return
		self.admincommands[command] = handler

	def handle_command(self, message, jid=None):
		temp = message.split(' ',1)
		args = temp[1] if len(temp) == 2 else None
		command = temp[0]

		if command == "!reloadmodules":
			if jid in self.admins:
				return self.update_commands()
			else:
				return "You are not authorized to run this command!"
		
		if command in self.commands.keys():
			return self.commands[command](args)
		if command in self.admincommands.keys():
			if jid in self.admins:
				return self.admincommands[command](args)
			else:
				return "You are not authorized to run this command!"

