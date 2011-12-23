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

def info_search(type, jid, nick, text):
	msg = L('What I must find?')
	if text != '':
		mdb = sqlite3.connect(jid_base,timeout=base_timeout)
		cu = mdb.cursor()
		cu.execute('delete from jid where server like ?',('<temporary>%',)).fetchall()
		ttext = '%'+text+'%'
		tma = cu.execute('select * from jid where login like ? or server like ? or resourse like ? order by login',(ttext,ttext,ttext)).fetchmany(10)
		if len(tma):
			msg = L('Found:')
			cnd = 1
			for tt in tma:
				msg += '\n'+str(cnd)+'. '+tt[0]+'@'+tt[1]+'/'+tt[2]
				cnd += 1
		else: msg = L('\'%s\' not found!') % text
	send_msg(type, jid, nick, msg)

def info_res(type, jid, nick, text):
	mdb = sqlite3.connect(jid_base,timeout=base_timeout)
	cu = mdb.cursor()
	cu.execute('delete from jid where server like ?',('<temporary>%',)).fetchall()
	if text == 'count':
		tlen = len(cu.execute('select resourse,count(*) from jid group by resourse order by -count(*)').fetchall())
		text,jidbase = '',''
	else:
		text1 = '%'+text+'%'
		tlen = len(cu.execute('select resourse,count(*) from jid where resourse like ? group by resourse order by -count(*)',(text1,)).fetchall())
		jidbase = cu.execute('select resourse,count(*) from jid where resourse like ? group by resourse order by -count(*)',(text1,)).fetchmany(10)
	if not tlen: msg = L('\'%s\' not found!') % text
	else:
		if text == '': msg = L('Total resources: %s') % str(tlen)
		else: msg = L('Found resources: %s') % str(tlen)
		if len(jidbase):
			msg += '\n'
			cnt = 1
			for jj in jidbase:
				msg += str(cnt)+'. '+jj[0]+'\t'+str(jj[1])+' \n'
				cnt += 1
			msg = msg[:-2]
	send_msg(type, jid, nick, msg)

def info_serv(type, jid, nick, text):
	mdb = sqlite3.connect(jid_base,timeout=base_timeout)
	cu = mdb.cursor()
	cu.execute('delete from jid where server like ?',('<temporary>%',)).fetchall()
	if text == 'count':
		tlen = len(cu.execute('select server,count(*) from jid group by server order by -count(*)').fetchall())
		text,jidbase = '',''
	else:
		text1 = '%'+text+'%'
		tlen = len(cu.execute('select server,count(*) from jid where server like ? group by server order by -count(*)',(text1,)).fetchall())
		jidbase = cu.execute('select server,count(*) from jid where server like ? group by server order by -count(*)',(text1,)).fetchall()
	if not tlen: msg = L('\'%s\' not found!') % text
	else:
		if text == '': msg = L('Total servers: %s') % str(tlen)
		else: msg = L('Found servers: %s') % str(tlen)
		msg += '\n'
		if len(jidbase):
			for jj in jidbase: msg += jj[0]+':'+str(jj[1])+' | '
			msg = msg[:-2]
	send_msg(type, jid, nick, msg)

#room number date

def info_top(type, jid, nick, text):
	tp = getFile(top_base,[])
	if len(text): room = text
	else: room = getRoom(jid)
	ttop = None
	for tmp in tp:
		if tmp[0] == room:
			ttop = tmp
			break
	if ttop: msg = L('Max count of members: %s %s') % (str(ttop[1]), '('+time.ctime(ttop[2])+')')
	else: msg = L('Statistic not found!')
	send_msg(type, jid, nick, msg)

def jidcatcher_presence(room,jid,nick,type,text):
	if jid != 'None' and jid[:11] != '<temporary>':
		aa1 = getName(jid)
		aa2 = getServer(jid)
		aa3 = getResourse(jid)
		try:
			mdb = sqlite3.connect(jid_base,timeout=base_timeout)
			cu = mdb.cursor()
			if not cu.execute('select login from jid where login=? and server=? and resourse=?',(aa1,aa2,aa3)).fetchone():
				cu.execute('insert into jid values (?,?,?)', (aa1,aa2,aa3))
				mdb.commit()
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
