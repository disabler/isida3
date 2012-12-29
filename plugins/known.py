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

def known(type, jid, nick, text):
	if not text.strip(): text = nick
	real_jid = cur_execute_fetchone('select jid from age where room=%s and (nick=%s or jid=%s) order by status,-time',(jid,text,text.lower()))
	if real_jid:
		nicks = ', '.join([t[0] for t in cur_execute_fetchall('select nick from age where room=%s and jid=%s',(jid,real_jid[0]))])
		if text == nick: msg = '%s %s' % (L('I know you as:','%s/%s'%(jid,nick)),nicks)
		else: msg = '%s %s' % (L('I know %s as:','%s/%s'%(jid,nick)) % text,nicks)
	else: msg = L('Not found!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'known', known, 2, L('Show user\'s nick changes.'))]
