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

def wtfsearch(type, jid, nick, text):
	msg = L('What need to find?')
	if len(text):
		text = '%%%s%%' % text
		cur_execute('select * from wtf where (room=%s or room=%s or room=%s) and (room like %s or jid like %s or nick like %s or wtfword like %s or wtftext like %s or time like %s)',(jid,'global','import',text,text,text,text,text,text))
		ww = cur.fetchall()
		msg = ''
		for www in ww: msg += www[4]+', '
		if len(msg): msg = L('Some matches in definitions: %s') % msg[:-2]
		else: msg = L('No matches.')
	send_msg(type, jid, nick, msg)

def wtfrand(type, jid, nick):
	cur_execute('select * from wtf where room=%s or room=%s or room=%s',(jid,'global','import'))
	ww = cur.fetchall()
	tlen = len(ww)
	ww = ww[randint(0,tlen-1)]
	msg = L('I know that %s is %s') % (ww[4],ww[5])
	send_msg(type, jid, nick, msg)

def wtfnames(type, jid, nick, text):
	if text == 'all': cur_execute('select * from wtf where room=%s or room=%s or room=%s',(jid,'global','import'))
	elif text == 'global': cur_execute('select * from wtf where room=%s',('global',))
	elif text == 'import': cur_execute('select * from wtf where room=%s',('import',))
	else: cur_execute('select * from wtf where room=%s',(jid,))
	tmp = cur.fetchall()
	msg = ''
	for ww in tmp: msg += ww[4]+', '
	if len(msg): msg = L('All I know is: %s') % msg[:-2]
	else: msg = L('No matches.')
	send_msg(type, jid, nick, msg)

def wtfcount(type, jid, nick):
	cur_execute('select * from wtf where 1=1')
	tlen = len(cur.fetchall())
	cur_execute('select * from wtf where room=%s',(jid,))
	cnt = len(cur.fetchall())
	cur_execute('select * from wtf where room=%s',('global',))
	glb = len(cur.fetchall())
	cur_execute('select * from wtf where room=%s',('import',))
	imp = len(cur.fetchall())
	msg = L('Locale definition: %s\nGlobal: %s\nImported: %s\nTotal: %s') % (cnt,glb,imp,tlen)
	send_msg(type, jid, nick, msg)

def wtf(type, jid, nick, text):
	wtf_get(0,type, jid, nick, text)

def wtff(type, jid, nick, text):
	wtf_get(1,type, jid, nick, text)

def wwtf(type, jid, nick, text):
	wtf_get(2,type, jid, nick, text)

def wtfp(type, jid, nick, text):
	if '\n' in text:
		text = text.split('\n')
		tnick = text[1]
		ttext = text[0]
		is_found = 0
		for mmb in megabase:
			if mmb[0]==jid and mmb[1]==tnick:
				is_found = 1
				break
		if is_found:
			wtf_get(0,'chat', jid, tnick, ttext)
			send_msg(type, jid, nick, L('Send to private %s') % tnick)
		else: send_msg(type, jid, nick, L('Nick %s not found!') % tnick)
	else: wtf_get(0,'chat', jid, nick, text)

def wtf_get(ff,type, jid, nick, text):
	if len(text):
		cur_execute('select * from wtf where (room=%s or room=%s or room=%s) and wtfword=%s',(jid,'global','import',text))
		ww = cur.fetchone()
		if ww:
			msg = L('I know that %s is %s') % (text,ww[4])
			if ff == 1: msg += L('\nfrom: %s %s') % (ww[2],'['+ww[5]+']')
			elif ff == 2: msg = L('I know that %s was defined by %s %s %s') % (text,ww[2],'('+ww[1]+')','['+ww[5]+']')
		else: msg = L('I don\'t know!')
	else: msg = L('What search?')
	send_msg(type, jid, nick, msg)

def dfn(type, jid, nick, text):
	if len(text) and '=' in text:
		ta = get_level(jid,nick)
		realjid =ta[1]
		al = ta[0]
		ti = text.index('=')
		what = del_space_end(text[:ti])
		text = del_space_begin(text[ti+1:])
		cur_execute('select * from wtf where (room=%s or room=%s or room=%s) and wtfword=%s order by lim',(jid,'global','import',what))
		matches = cur.fetchone()
		if matches:
			if matches[7] > al:
				msg,text = L('Not enough rights!'),''
				try: msg += ' ' + unlevltxt[unlevlnum[matches[7]]] % unlevl[matches[7]]
				except: pass
			elif matches[1] == 'global': msg, text = L('This is global definition and not allowed to change!'), ''
			elif text == '':
				msg = L('Definition removed!')
				cur_execute('delete from wtf where wtfword=%s and room=%s',(what,jid))
			else:
				msg = L('Definition updated!')
				cur_execute('delete from wtf where wtfword=%s and room=%s',(what,jid))
		elif text == '': msg = L('Nothing to remove!')
		else: msg = L('Definition saved!')
		cur_execute('select * from wtf where 1=1')
		idx = len(cur.fetchall())
		if text != '': cur_execute('insert into wtf values (%s,%s,%s,%s,%s,%s,%s,%s)', (idx, jid, realjid, nick, what, text, timeadd(tuple(time.localtime())),al))
		conn.commit()
	else: msg = L('What need to remember?')
	send_msg(type, jid, nick, msg)

def gdfn(type, jid, nick, text):
	if len(text) and '=' in text:
		ta = get_level(jid,nick)
		realjid =ta[1]
		al = ta[0]
		ti = text.index('=')
		what = del_space_end(text[:ti])
		text = del_space_begin(text[ti+1:])
		cur_execute('select * from wtf where (room=%s or room=%s or room=%s) and wtfword=%s order by lim',(jid,'global','import',what))
		matches = cur.fetchone()
		if matches:
			if matches[7] > al:
				msg,text = L('Not enough rights!'),''
				try: msg += ' ' + unlevltxt[unlevlnum[matches[7]]] % unlevl[matches[7]]
				except: pass
			elif text == '':
				msg = L('Definition removed!')
				cur_execute('delete from wtf where wtfword=%s',(what,))
			else:
				msg = L('Definition updated!')
				cur_execute('delete from wtf where wtfword=%s',(what,))
		elif text == '': msg = L('Nothing to remove!')
		else: msg = L('Definition saved!')
		cur_execute('select * from wtf where 1=1')
		idx = len(cur.fetchall())
		if text != '': cur_execute('insert into wtf values (%s,%s,%s,%s,%s,%s,%s,%s)', (idx, 'global', realjid, nick, what, text, timeadd(tuple(time.localtime())),al))
		conn.commit()
	else: msg = L('What need to remember?')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'wtfrand', wtfrand, 1, L('Random definition from base.')),
	 (3, 'wtfnames', wtfnames, 2, L('List of definitions in conference.\nwtfnames [all|global|import]')),
	 (3, 'wtfcount', wtfcount, 1, L('Definitions count.')),
	 (3, 'wtfsearch', wtfsearch, 2, L('Search in definitions base.')),
	 (9, 'wwtf', wwtf, 2, L('Information about definition commiter.')),
	 (3, 'wtff', wtff, 2, L('Show definition with nick and date.')),
	 (3, 'wtfp', wtfp, 2, L('Show definition in private.\nwtfp word\n[nick]')),
	 (0, 'wtf', wtf, 2, L('Show definition.')),
	 (3, 'dfn', dfn, 2, L('Set definition.\ndfn word=definition - remember definition as word\ndfn word= - remove definition word')),
	 (3, 'gdfn', gdfn, 2, L('Set global definition.\ngdfn word=definition - remember definition as word\ngdfn word= - remove definition word'))]
