#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2012 diSabler <dsy@dsy.name>                               #
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
# --------------------------------------------------------------------------- #

def bot_shutdown(type, jid, nick, text, reason, xtype):
	global game_over,bot_exit_type
	StatusMessage = L('%s by command from %s') % (reason, nick)
	if text != '': StatusMessage += ', ' + L('reason: %s') % text
	send_presence_all(StatusMessage)
	bot_exit_type, game_over = xtype, True

def bot_exit(type, jid, nick, text):
	bot_shutdown(type, jid, nick, text, L('Shutdown'), 'exit')

def bot_restart(type, jid, nick, text):
	bot_shutdown(type, jid, nick, text, L('Restart'), 'restart')

def bot_update(type, jid, nick, text):
	bot_shutdown(type, jid, nick, text, L('Update'), 'update')

def bot_soft_update(type, jid, nick, text):
	global plugins_reload
	caps_and_send(xmpp.Presence(show='dnd', status=L('Soft update activated!'), priority=Settings['priority']))
	plugins_reload = True
	while not game_over:
		if not plugins_reload:
			send_msg(type, jid, nick, L('Soft update finished! Plugins loaded: %s. Commands: %s') % (len(plugins)+1,len(comms)))
			break
		else: time.sleep(1)
	pprint('*** Send new hash in rooms')
	for tocon in confbase:
		tocon = tocon.strip()
		if '\n' in tocon: pprint('->- %s | pass: %s' % tuple(tocon.split('\n',1)),'green')
		else: pprint('->- %s' % tocon,'green')
		baseArg = unicode(tocon)
		if '/' not in baseArg: baseArg += '/%s' % unicode(Settings['nickname'])
		if '\n' in baseArg: baseArg,passwd = baseArg.split('\n',2)
		else: passwd = ''
		zz = join(baseArg, passwd)
	if Settings['status'] == 'online': caps_and_send(xmpp.Presence(status=Settings['message'], priority=Settings['priority']))
	else: caps_and_send(xmpp.Presence(show=Settings['status'], status=Settings['message'], priority=Settings['priority']))
	
global execute

execute = [(9, 'quit', bot_exit, 2, L('Shutting down the bot. You can set reason.')),
	 (9, 'restart', bot_restart, 2, L('Restart the bot. You can set reason.')),
	 (9, 'update', bot_update, 2, L('Update from VCS. You can set reason.')),
	 (9, 'soft_update', bot_soft_update, 2, L('Soft update from VCS.'))]
