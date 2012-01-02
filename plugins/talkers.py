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

def gtalkers(type, jid, nick, text):
	conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (base_name,base_user,base_host,base_pass));
	cur = conn.cursor()
	if text:
		ttext = '%%%s%%' % text
		cur.execute('select * from talkers where (jid like %s or nick like %s or room like %s) order by -words',(ttext,ttext,ttext))
		tma = cur.fetchmany(10)
	else:
		cur.execute('select * from talkers order by -words')
		tma = cur.fetchmany(10)
	cur.close()
	conn.close()
	if tma:
		msg = '%s\n' % L('Talkers:\nNick\t\tWords\tPhrases\tEffect\tConf.')
		msg += '\n'.join(['%s. %s\t\t%s\t%s\t%s\t%s' % (cnd + 1, tt[2], tt[3], tt[4], round(tt[3]/float(tt[4]), 2),'%s@%s.%s' % (getName(tt[0]),'.'.join([tmp[0] for tmp in tt[0].split('@')[1].split('.')[:-1]]),tt[0].split('.')[-1])) for cnd, tt in enumerate(tma)])
	else: msg = '%s %s' % (text, L('Not found!'))
	send_msg(type, jid, nick, msg)

def talkers(type, jid, nick, text):
	conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (base_name,base_user,base_host,base_pass));
	cur = conn.cursor()
	if text:
		ttext = '%%%s%%' % text
		cur.execute('select * from talkers where room=%s and (jid like %s or nick like %s) order by -words',(jid,ttext,ttext))
		tma = cur.fetchmany(10)
	else: 
		cur.execute('select * from talkers where room=%s order by -words',(jid,))
		tma = cur.fetchmany(10)
	cur.close()
	conn.close()
	if tma:
		msg = '%s\n' % L('Talkers:\nNick\t\tWords\tPhrases\tEffect')
		msg += '\n'.join(['%s. %s\t\t%s\t%s\t%s' % (cnd + 1, tt[2], tt[3], tt[4], round(tt[3]/float(tt[4]), 2)) for cnd, tt in enumerate(tma)])
	else: msg = '%s %s' % (text, L('Not found!'))
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'talkers', talkers, 2, L('Show local talkers')),
	   (4, 'gtalkers', gtalkers, 2, L('Show global talkers'))]