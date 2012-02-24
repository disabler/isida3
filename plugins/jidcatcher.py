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

def info_search(type, jid, nick, text):
	msg = L('What I must find?')
	if text:
		cur_execute('delete from jid where server ilike %s',('<temporary>%',))
		ttext = '%%%s%%' % text
		tma = cur_execute_fetchmany('select * from jid where login ilike %s or server ilike %s or resourse ilike %s order by login',(ttext,ttext,ttext),10)
		if tma: msg = '%s\n%s' % (L('Found:'),'\n'.join(['%s. %s@%s/%s' % tuple([tma.index(tt)+1]+list(tt)) for tt in tma]))
		else: msg = L('\'%s\' not found!') % text
	send_msg(type, jid, nick, msg)

def info_res(type, jid, nick, text):
	cur_execute('delete from jid where server ilike %s',('<temporary>%',))
	if text.lower() == 'count':
		tlen = cur_execute_fetchall('select count(*) from (select resourse,count(*) from jid group by resourse) tmp;')[0][0]
		text,jidbase = '',''
	else:
		text1 = '%%%s%%' % text
		tlen = cur_execute_fetchall('select count(*) from (select resourse,count(*) from jid where resourse ilike %s group by resourse) tmp;',(text1,))[0][0]
		jidbase = cur_execute_fetchmany('select resourse,count(*) from jid where resourse ilike %s group by resourse order by -count(*),resourse',(text1,),10)
	if not tlen: msg = L('\'%s\' not found!') % text
	else:
		if text: msg = L('Found resources: %s') % tlen
		else: msg = L('Total resources: %s') % tlen
		if jidbase: msg += '\n%s' % '\n'.join(['%s. %s\t%s' % tuple([jidbase.index(jj)+1]+list(jj)) for jj in jidbase])
	send_msg(type, jid, nick, msg)

def info_serv(type, jid, nick, text):
	cur_execute('delete from jid where server ilike %s',('<temporary>%',))
	if text == 'count':
		tlen = cur_execute_fetchall('select count(*) from (select server,count(*) from jid group by server) tmp;')[0][0]
		text,jidbase = '',''
	else:
		text1 = '%%%s%%' % text
		tlen = cur_execute_fetchall('select count(*) from (select server,count(*) from jid where server ilike %s group by server) tmp;',(text1,))[0][0]
		jidbase = cur_execute_fetchall('select server,count(*) from jid where server ilike %s group by server order by -count(*),server',(text1,))
	if not tlen: msg = L('\'%s\' not found!') % text
	else:
		if text: msg = L('Found servers: %s') % tlen
		else: msg = L('Total servers: %s') % tlen
		if jidbase: msg = '%s\n%s' %(msg,' | '.join(['%s:%s' % jj for jj in jidbase]))
	send_msg(type, jid, nick, msg)

#room number date

def info_top(type, jid, nick, text):
	tp = getFile(top_base,[])
	if text: room = text
	else: room = getRoom(jid)
	ttop = None
	for tmp in tp:
		if tmp[0] == room:
			ttop = tmp
			break
	if ttop: msg = L('Max count of members: %s %s') % (ttop[1], '(%s)' % disp_time(ttop[2]))
	else: msg = L('Statistic not found!')
	send_msg(type, jid, nick, msg)

def jidcatcher_presence(room,jid,nick,type,text):
	if jid != 'None' and not jid.startswith('<temporary>'):
		tmp = (getName(jid),getServer(jid),getResourse(jid))
		try:
			tmpp = cur_execute_fetchone('select login from jid where login=%s and server=%s and resourse=%s',tmp)
			if not tmpp: cur_execute('insert into jid values (%s,%s,%s)', tmp)
		except: pass
		tp = getFile(top_base,[])
		cnt = 0
		for tmp in megabase:
			if tmp[0] == room: cnt += 1
		ltop = None
		for tmp in tp:
			if tmp[0] == room:
				ltop = tmp
				break
		if ltop:
			if ltop[1] <= cnt:
				tp.remove(ltop)
				tp.append((room,cnt,int(time.time())))
				writefile(top_base,unicode(tp))
		else:
			tp.append((room,cnt,int(time.time())))
			writefile(top_base,unicode(tp))

global execute, presence_control

presence_control = [jidcatcher_presence]

execute = [(4, 'res', info_res, 2, L('Without parameters show top10 resources for all conferences, where bot is present.\nwith parameters - search in resources base\ncount - number of results.')),
		   (6, 'serv', info_serv, 2, L('Wihtout parameters show all servers freom where joined in rooms, where bot is present\nwith parameters - search on servers base\ncount - show number of results.')),
		   (9, 'search', info_search, 2, L('Search in internal jids base.')),
		   (2, 'top', info_top, 2, L('Conference\'s activity.'))]
