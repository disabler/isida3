#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2011 diSabler <dsy@dsy.name>                               #
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
	text = text.strip()
	if text == '': text = nick
	conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (base_name,base_user,base_host,base_pass));
	cur = conn.cursor()
	cur.execute('select jid from age where room=%s and (nick=%s or jid=%s)',(jid,text,text.lower()))
	real_jid = cur.fetchone()
	if real_jid:
		cur.execute('select nick from age where room=%s and jid=%s',(jid,real_jid[0]))
		nicks = cur.fetchall()
		if text == nick: msg = L('I know you as:') + ' '
		else: msg = L('I know %s as:') % text + ' '
		for tmp in nicks:
			msg += tmp[0] + ', '
		msg = msg[:-2]
	else: msg = L('Not found!')
	cur.close()
	conn.close()
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'known', known, 2, L('Show user\'s nick changes.'))]
