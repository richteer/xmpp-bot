#!/usr/bin/env python3
import logging
import XMPPCommands
import time
import sys

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout


class Bot(ClientXMPP):

	def __init__(self, jid, password, room, nick):
		ClientXMPP.__init__(self,jid,password)
		
		self.room = room
		self.nick = nick
		self.comm = XMPPCommands.Commander()
		self.lastcmd = time.time() 

		self.add_event_handler("session_start", self.session_start)
		self.add_event_handler("message", self.message)
		self.add_event_handler("groupchat_message", self.groupmsg)

	def session_start(self, event):
		self.send_presence()
		self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)
		
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
		if msg['mucnick'] != self.nick and msg['body'][0] == '!':
			response = self.comm.handle_command(msg['body'], msg.getMucnick())
			
			if response != None:
				self.send_message(mto=msg['from'].bare, mbody=response, mtype='groupchat')


if __name__ == '__main__':
	if len(sys.argv) != 5:
		print("Usage: {} <jid> <pass> <room> <mucnick>".format(sys.argv[0]))
		exit(1)
	# TODO: Use argparse here
	logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
	xmpp = Bot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	xmpp.register_plugin('xep_0045')
	xmpp.connect()
	xmpp.process(block=True)
