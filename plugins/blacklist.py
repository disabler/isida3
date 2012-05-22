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

def leave_room(rjid, reason):
	msg = ''
	cnf = cur_execute_fetchone('select room from conference where room ilike %s',('%%%s'%rjid,))
	if cnf:
		cur_execute('delete from conference where room ilike %s;', ('%s/%%'%rjid,))
		leave(rjid, reason)
		msg = L('Leave conference %s\n') % rjid
	return msg

def blacklist(type, jid, nick, text):
	text, msg = unicode(text.lower()), ''
	templist = getFile(blacklist_base, [])
	reason = L('Conference was added in blacklist')
	try:
		text = text.split(' ')
		if '@' not in text[1]: text[1] += '@%s' % lastserver
		if text[0] == 'add':
			if text[1] in templist: msg = L('This conference already exist in blacklist.')
			elif cur_execute_fetchone('select count(*) from conference;')[0]==1 and getRoom(cur_execute_fetchone('select room from conference;')[0]) == text[1]:
				msg =L('You can\'t add last conference in blacklist.')
			else:
				msg = leave_room(text[1], reason)
				templist.append(text[1])
				msg += L('Add to blacklist: %s') % text[1]
		elif text[0] == 'del':
			if text[1] in templist: msg = L('Removed from blacklist: %s') % templist.pop(templist.index(text[1]))
			else: msg = L('Address not in blacklist.')
		else: msg = L('Error in parameters. Read the help about command.')
	except:
		if text[0] == 'show':
			if len(templist) == 0: msg = L('List is empty.')
			else: msg = '%s%s' % (L('List of conferences:\n'),'\n'.join(['%s. %s' % t for t in enumerate(templist)]))
		elif text[0] == 'clear': msg, templist = L('Cleared.'), []
		else: msg = L('Error in parameters. Read the help about command.')
	writefile(blacklist_base, str(templist))
	send_msg(type, jid, nick, msg)

global execute

execute = [(9, 'blacklist', blacklist, 2, L('Manage of conferences blacklist.\nblacklist add|del|show|clear\nblacklist add|del room@conference.server.tld - add|remove address from blacklist\nblacklist show - show blacklist\nblacklist clear - clear blacklist'))]