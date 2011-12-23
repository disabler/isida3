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

def true_age_stat(type, jid, nick):
	try: llim = GT('age_default_limit')
	except: llim = 10
	mdb = sqlite3.connect(agestatbase, timeout=base_timeout)
	cu = mdb.cursor()
	t_age = cu.execute('select nick,sum(age) from age where room=? group by jid order by -sum(age),-time,-status',(jid,)).fetchmany(llim)
	mdb.close()
	msg = L('Age statistic:\n%s') % '\n'.join(['%s\t%s' % (t[0],un_unix(t[1])) for t in t_age])
	send_msg(type, jid, nick, msg)

def true_age_split(type, jid, nick, text):
	true_age_raw(type, jid, nick, text, True)

def true_age(type, jid, nick, text):
	true_age_raw(type, jid, nick, text, None)
	
def true_age_raw(type, jid, nick, text, xtype):
	text = text.rstrip().split('\n')
	llim = 10
	if len(text) > 1:
		try: llim = int(text[1])
		except: llim = GT('age_default_limit')
	text = text[0]
	if not text: text = nick
	if llim > GT('age_max_limit'): llim = GT('age_max_limit')
	mdb = sqlite3.connect(agestatbase, timeout=base_timeout)
	cu = mdb.cursor()
	real_jid = cu.execute('select jid from age where room=? and (nick=? or jid=?) order by -time,-status',(jid,text,text.lower())).fetchone()
	if not real_jid:
		text = '%' + text.lower() + '%'
		real_jid = cu.execute('select jid from age where room=? and (nick like ? or jid like ?) order by -time,-status',(jid,text,text)).fetchone()
	try:
		if xtype: sbody = cu.execute('select * from age where room=? and jid=? order by -time,-status',(jid,real_jid[0])).fetchmany(llim)
		else:
			t_age = cu.execute('select sum(age) from age where room=? and jid=? order by -time,-status',(jid,real_jid[0])).fetchone()
			sbody = cu.execute('select * from age where room=? and jid=? order by -time,-status',(jid,real_jid[0])).fetchone()
			sbody = [sbody[:4] + t_age + sbody[5:]]
	except: sbody = None
	mdb.close()
	if sbody:
		msg = L('I see:')
		for cnt, tmp in enumerate(sbody):
			if tmp[5]: r_age = tmp[4]
			else: r_age = int(time.time()) - tmp[3] + tmp[4]
			if xtype: msg += '\n%s. %s' % (cnt + 1, tmp[1])
			else: msg += ' %s' % tmp[1]
			msg += '\t%s, ' % un_unix(r_age)
			if tmp[5]:
				if tmp[6]: msg += L('%s %s ago') % (tmp[6], un_unix(int(time.time() - tmp[3])))
				else: msg += L('Leave %s ago') % un_unix(int(time.time() - tmp[3]))
				t7sp = tmp[7].split('\r')[0]
				if t7sp.count('\n') > 3:
					stat = t7sp.split('\n', 4)[4]
					if stat: msg += ' (%s)' % stat
				elif t7sp: msg += ' (%s)' % t7sp
				if '\r' in tmp[7]: msg += ', %s %s' % (L('Client:'),' // '.join(tmp[7].split('\r')[-1].split(' // ')[:-1]))
			else: msg += L('Is here: %s') % un_unix(int(time.time() - tmp[3]))
			if not xtype: msg = msg.replace('\t', ' - ')
	else: msg = L('Not found!')
	send_msg(type, jid, nick, msg)

def seen(type, jid, nick, text):
	seen_raw(type, jid, nick, text, None)

def seen_split(type, jid, nick, text):
	seen_raw(type, jid, nick, text, True)

def seen_raw(type, jid, nick, text, xtype):
	text = text.rstrip().split('\n')
	llim = GT('age_default_limit')
	if len(text)>1:
		try: llim = int(text[1])
		except: llim = GT('age_default_limit')
	text = text[0]
	if not text: text = nick
	if llim > GT('age_max_limit'): llim = GT('age_max_limit')
	mdb = sqlite3.connect(agestatbase,timeout=base_timeout)
	cu = mdb.cursor()
	real_jid = cu.execute('select jid from age where room=? and (nick=? or jid=?) order by status,-time',(jid,text,text.lower())).fetchone()
	if not real_jid:
		textt = '%' + text.lower() + '%'
		real_jid = cu.execute('select jid from age where room=? and (nick like ? or jid like ?) order by status,-time',(jid,textt,textt)).fetchone()
	if real_jid:
		if xtype: sbody = cu.execute('select * from age where room=? and jid=? order by status,-time',(jid,real_jid[0])).fetchmany(llim)
		else: sbody = [cu.execute('select * from age where room=? and jid=? order by status,-time',(jid,real_jid[0])).fetchone()]
	else: sbody = None
	mdb.close()
	if sbody:
		msg = L('I see:')
		for cnt, tmp in enumerate(sbody):
			if xtype: msg += '\n%s. ' % (cnt+1)
			else: msg += ' '
			if text != tmp[1]: msg += L('%s (with nick: %s)') % (text,tmp[1])
			else: msg += tmp[1]
			if tmp[5]:
				if tmp[6]: msg += ' - ' + L('%s %s ago') % (tmp[6], un_unix(int(time.time() - tmp[3])))
				else: msg += ' - ' + L('Leave %s ago') % un_unix(int(time.time() - tmp[3]))
				t7sp = tmp[7].split('\r')[0]
				if t7sp.count('\n') > 3:
					stat = t7sp.split('\n',4)[4]
					if stat: msg += ' (%s)' % stat
				elif t7sp: msg += ' (%s)' % t7sp
				if '\r' in tmp[7]: msg += ', %s %s' % (L('Client:'),' // '.join(tmp[7].split('\r')[-1].split(' // ')[:-1]))
			else: msg += ' - '+ L('Is here: %s') % un_unix(int(time.time()-tmp[3]))
	else: msg = L('Not found!')
	send_msg(type, jid, nick, msg)

def seenjid(type, jid, nick, text):
	seenjid_raw(type, jid, nick, text, None)

def seenjid_split(type, jid, nick, text):
	seenjid_raw(type, jid, nick, text, True)

def seenjid_raw(type, jid, nick, text, xtype):
	text = text.rstrip().split('\n')
	llim = GT('age_default_limit')
	if len(text)>1:
		try: llim = int(text[1])
		except: llim = GT('age_default_limit')
	text = text[0]
	ztype = None
	if not text: text = nick
	if llim > GT('age_max_limit'): llim = GT('age_max_limit')
	mdb = sqlite3.connect(agestatbase,timeout=base_timeout)
	cu = mdb.cursor()
	real_jid = cu.execute('select jid from age where room=? and (nick like ? or jid like ?) group by jid order by status,-time',(jid,text,text.lower())).fetchall()
	if not real_jid:
		txt = '%' + text.lower() + '%'
		real_jid = cu.execute('select jid from age where room=? and (nick like ? or jid like ?) group by jid order by status,-time',(jid,txt,txt)).fetchall()
	sbody = []
	if real_jid:
		for rj in real_jid:			
			if xtype: tmpbody = cu.execute('select * from age where room=? and jid=? order by status, jid',(jid,rj[0])).fetchmany(llim)
			else: tmpbody = cu.execute('select room, nick, jid, time, sum(age), status, type, message from age where room=? and jid=? group by jid order by status, jid',(jid,rj[0])).fetchmany(llim)
			if tmpbody:
				for t in tmpbody: sbody.append(t)
	mdb.close()
	if sbody:
		ztype = True
		msg = L('I saw %s:') % text
		for cnt, tmp in enumerate(sbody):
			msg += '\n%s. %s (%s)' % (cnt + 1, tmp[1], tmp[2])
			if tmp[5]:
				if tmp[6]: msg += '\t' + L('%s %s ago') % (tmp[6], un_unix(int(time.time() - tmp[3])))
				else: msg += '\t' + L('Leave %s ago') % un_unix(int(time.time() - tmp[3]))
				t7sp = tmp[7].split('\r')[0]
				if t7sp.count('\n') > 3:
					stat = t7sp.split('\n', 4)[4]
					if stat: msg += ' (%s)' % stat
				elif t7sp: msg += ' (%s)' % t7sp
				if '\r' in tmp[7]: msg += ', %s %s' % (L('Client:'), tmp[7].split('\r')[-1])
			else: msg += '\t' + L('Is here: %s') % un_unix(int(time.time() - tmp[3]))
			if not xtype: msg = msg.replace('\t', ' - ')
	else: msg = L('Not found!')
	if type == 'groupchat' and ztype:
		send_msg(type, jid, nick, L('Send for you in private'))
		send_msg('chat', jid, nick, msg)
	else: send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'age', true_age, 2, L('Show age of jid in conference.')),
	 (3, 'age_split', true_age_split, 2, L('Show age of jid in conference splitted by nicks.')),
	 (3, 'seen', seen, 2, L('Show time of join/leave.')),
	 (3, 'seen_split', seen_split, 2, L('Show time of join/leave splitted by nicks.')),
	 (3, 'agestat', true_age_stat, 1, L('Show age statistic for conference.')),
	 (7, 'seenjid', seenjid, 2, L('Show time of join/leave + jid.')),
	 (7, 'seenjid_split', seenjid_split, 2, L('Show time of join/leave + jid splitted by nicks.'))]