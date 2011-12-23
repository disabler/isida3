#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2011 diSabler <dsy@dsy.name>                               #
#    Copyright (C) 2011 dr.Schmurge <dr.schmurge@isida-bot.com>               #
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

def adminmail(type, jid, nick, text):
	if len(text):
		if len(text) > GT('amsg_limit_size'): text = text[:GT('amsg_limit_size')]+u'[…]'
		timesent = getFile(time_limit_base, {})
		ga = get_level(jid, nick)
		fjid = getRoom(ga[1])
		tmp_lim = GT('amsg_limit')[ga[0]]
		if timesent.has_key(fjid):
			wt = int(timesent[fjid]-time.time())
			if wt >= 0:
				send_msg(type, jid, nick, L('Time limit exceeded. Wait: %s') % un_unix(wt))
				return None
			else: del timesent[fjid]
		timesent[fjid] = int(time.time())+tmp_lim
		writefile(time_limit_base, str(timesent))
		msg = L('User %s (%s) from %s at %s send massage to you: %s') % (nick,fjid,jid,str(time.strftime("%H:%M %d.%m.%y", time.localtime (time.time()))),text)
		for ajid in ownerbase: send_msg('chat', getRoom(ajid), '', msg)
		send_msg(type, jid, nick, L('Sent'))
	else: send_msg(type, jid, nick, L('What?'))

global execute

execute = [(4, 'msgtoadmin', adminmail, 2, L('Send message to bot\'s owner\nmsgtoadmin text'))]
