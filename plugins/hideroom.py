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

def hide_room(type, jid, nick, text):
	if type == 'groupchat': msg = L('This command available only in private!')
	else:
		hmode = text.split(' ')[0]
		try: hroom = text.split(' ')[1]
		except: hroom = jid
		hr = getFile(hide_conf,[])
		if hmode == 'show':
			if len(hr):
				msg = L('Hidden conferences:')
				for tmp in hr: msg += '\n'+tmp
			else: msg = L('No hidden conferences.')
		elif hmode == 'add':
			if not cur_execute_fetchall('select * from conference where room ilike %s;', ('%s/%%'%getRoom(hroom),)): msg = L('I am not in the %s') % hroom
			elif hroom in hr: msg = L('I\'m already hide a %s') % hroom
			else:
				hr.append(hroom)
				msg = L('%s has been hidden') % hroom
				writefile(hide_conf,str(hr))
		elif hmode == 'del':
			if hroom in hr:
				hr.remove(hroom)
				msg = L('%s will be shown') % hroom
				writefile(hide_conf,str(hr))
			else: msg = L('I\'m not hide room %s') % hroom
		else: msg = L('What?')
	send_msg(type, jid, nick, msg)

global execute

execute = [(9, 'hide', hide_room, 2, L('Hide conference.\nhide [add|del|show] [room@conference.server.tld]'))]
