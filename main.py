#!/usr/bin/env python3
import logging
import XMPPCommands
import time
import json
import getpass

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

admins = []

def loadConfig():
	global admins
	with open("config.json","r") as f:
		data = json.loads(f.read())

	admins = data["admins"] if "admins" in data.keys() else []	
	pwd = getpass.getpass()
	jid = data["jid"] if "jid" in data.keys() else None # TODO: Make this an error
	rooms = []
	if "muc" in data.keys():
		for r in data["muc"]:
			rooms.append((r["room"],r["nick"]))
	return (jid,pwd,rooms)



class Bot(ClientXMPP):

	def __init__(self, jid, password, rooms):
		ClientXMPP.__init__(self,jid,password)
		
		self.rooms = rooms
		self.comm = XMPPCommands.Commander(self)
		self.comm.set_admins(admins)
		self.lastcmd = time.time() 

		self.add_event_handler("session_start", self.session_start)
		self.add_event_handler("message", self.message)
		self.add_event_handler("groupchat_message", self.groupmsg)

	def session_start(self, event):
		self.send_presence()
		for r in self.rooms:
			self.plugin['xep_0045'].joinMUC(r[0], r[1], wait=True)
		
		# self.get_roster()

	def message(self, msg):
		temp = time.time()
		if temp - self.lastcmd <= 1:
			self.lastcmd = temp
			return

		if msg['type'] in ('chat', 'normal') and msg['body'][0] == "!":
			self.lastcmd = temp
			response = self.comm.handle_command(msg['body'], jid=msg['from'].bare)

			if response != None:
				self.send_message(mto=msg['from'].bare, mbody=response, mtype=msg['type'])
	
	
	def groupmsg(self, msg):
		temp = time.time()
		if temp - self.lastcmd <= 1:
			self.lastcmd = temp
			return

		self.lastcmd = temp
		# TODO: Check nick for specific muc
		if msg['mucnick'] not in [n[1] for n in self.rooms] and msg['body'][0] == '!':
			response = self.comm.handle_command(msg['body'])
			
			if response != None:
				self.send_message(mto=msg['from'].bare, mbody=response, mtype='groupchat')


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
	
	jid,pwd,rooms = loadConfig()

	xmpp = Bot(jid, pwd, rooms)
	xmpp.register_plugin('xep_0045')
	xmpp.connect()
	xmpp.process(block=True)
