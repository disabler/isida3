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

def wtfall(type, jid, nick, text):
	if text:
		ww = cur_execute_fetchall('select * from wtf where (room=%s or room=%s or room=%s) and wtfword=%s order by -time',(jid,'global','import',text))
		if ww: msg = L('I know that %s is %s') % (text,'\n%s' % '\n\n'.join([L('from %s: %s') % (t[3],t[5]) for t in ww]))
		else: msg = L('I don\'t know!')
	else: msg = L('What search?')
	send_msg(type, jid, nick, msg)

def wtfsearch(type, jid, nick, text):
	if text:
		text = '%%%s%%' % text
		ww = cur_execute_fetchall('select wtfword from wtf where (room=%s or room=%s or room=%s) and (room ilike %s or jid ilike %s or nick ilike %s or wtfword ilike %s or wtftext ilike %s or time ilike %s)',(jid,'global','import',text,text,text,text,text,text))
		if ww: msg = L('Some matches in definitions: %s') % ', '.join(zip(*ww)[0])
		else: msg = L('No matches.')
	else: msg = L('What need to find?')
	send_msg(type, jid, nick, msg)

def wtfrand(type, jid, nick):
	ww = cur_execute_fetchall('select * from wtf where room=%s or room=%s or room=%s',(jid,'global','import'))
	tlen = len(ww)
	ww = ww[randint(0,tlen-1)]
	msg = L('I know that %s is %s') % (ww[4],ww[5])
	send_msg(type, jid, nick, msg)

def wtfnames(type, jid, nick, text):
	text = text.strip().lower()
	if text == 'all': tmp = cur_execute_fetchall('select wtfword from wtf where room=%s or room=%s or room=%s',(jid,'global','import'))
	elif text == 'global': tmp = cur_execute_fetchall('select wtfword from wtf where room=%s',('global',))
	elif text == 'import': tmp = cur_execute_fetchall('select wtfword from wtf where room=%s',('import',))
	else: tmp = cur_execute_fetchall('select wtfword from wtf where room=%s',(jid,))
	if tmp: msg = L('All I know is: %s') % ', '.join(zip(*tmp)[0])
	else: msg = L('No matches.')
	send_msg(type, jid, nick, msg)

def wtfcount(type, jid, nick):
	tlen = cur_execute_fetchall('select count(*) from wtf')[0][0]
	cnt = cur_execute_fetchall('select count(*) from wtf where room=%s',(jid,))[0][0]
	glb = cur_execute_fetchall('select count(*) from wtf where room=%s',('global',))[0][0]
	imp = cur_execute_fetchall('select count(*) from wtf where room=%s',('import',))[0][0]
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
	if text:
		ww = cur_execute_fetchone('select * from wtf where (room=%s or room=%s or room=%s) and wtfword=%s order by -time',(jid,'global','import',text))
		if ww:
			msg = L('I know that %s is %s') % (text,ww[5])
			if ff == 1: msg += L('\nfrom: %s %s') % (ww[3],'[%s]' % disp_time(ww[6]))
			elif ff == 2: msg = L('I know that %s was defined by %s %s %s') % (text,ww[3],'(%s)' % ww[2],'[%s]' % disp_time(ww[6]))
		else: msg = L('I don\'t know!')
	else: msg = L('What search?')
	send_msg(type, jid, nick, msg)

def dfn(type, jid, nick, text):
	if text and '=' in text:
		ta = get_level(jid,nick)
		realjid =ta[1]
		al = ta[0]
		ti = text.index('=')
		what = del_space_end(text[:ti])
		text = del_space_begin(text[ti+1:])
		matches = cur_execute_fetchall('select * from wtf where (room=%s or room=%s or room=%s) and wtfword=%s order by lim,-time',(jid,'global','import',what))
		if matches:
			max = -1
			for t in matches:
				if t[7] >= max: max,match=t[7],t
			if match[7] > al:
				msg,text = L('Not enough rights!'),''
				try: msg += ' ' + unlevltxt[unlevlnum[match[7]]] % unlevl[match[7]]
				except: pass
			elif match[1] == 'global': msg, text = L('This is global definition and not allowed to change!'), ''
			elif text == '':
				msg = L('Definition removed!')
				cur_execute('delete from wtf where wtfword=%s and room=%s',(what,jid))
			else:
				msg = L('Definition updated!')
				if getRoom(realjid) == getRoom(match[2]): cur_execute('delete from wtf where wtfword=%s and room=%s and jid=%s',(what,jid,match[2]))
		elif text == '': msg = L('Nothing to remove!')
		else: msg = L('Definition saved!')
		idx = cur_execute_fetchall('select count(*) from wtf')[0][0]
		if text != '': cur_execute('insert into wtf values (%s,%s,%s,%s,%s,%s,%s,%s)', (idx, jid, realjid, nick, what, text, int(time.time()),al))
	else: msg = L('What need to remember?')
	send_msg(type, jid, nick, msg)

def gdfn(type, jid, nick, text):
	if text and '=' in text:
		ta = get_level(jid,nick)
		realjid =ta[1]
		al = ta[0]
		ti = text.index('=')
		what = del_space_end(text[:ti])
		text = del_space_begin(text[ti+1:])
		matches = cur_execute_fetchall('select * from wtf where (room=%s or room=%s or room=%s) and wtfword=%s order by lim,-time',(jid,'global','import',what))
		if matches:
			max = -1
			for t in matches:
				if t[7] >= max: max,match=t[7],t
			if match[7] > al:
				msg,text = L('Not enough rights!'),''
				try: msg += ' ' + unlevltxt[unlevlnum[match[7]]] % unlevl[match[7]]
				except: pass
			elif text == '':
				msg = L('Definition removed!')
				cur_execute('delete from wtf where wtfword=%s',(what,))
			else:
				msg = L('Definition updated!')
				if getRoom(realjid) == getRoom(match[2]): cur_execute('delete from wtf where wtfword=%s and jid=%s',(what,match[2]))
		elif text == '': msg = L('Nothing to remove!')
		else: msg = L('Definition saved!')
		idx = cur_execute_fetchall('select count(*) from wtf')[0][0]
		if text != '': cur_execute('insert into wtf values (%s,%s,%s,%s,%s,%s,%s,%s)', (idx, 'global', realjid, nick, what, text, int(time.time()),al))
	else: msg = L('What need to remember?')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'wtfrand', wtfrand, 1, L('Random definition from base.')),
	 (3, 'wtfnames', wtfnames, 2, L('List of definitions in conference.\nwtfnames [all|global|import]')),
	 (3, 'wtfcount', wtfcount, 1, L('Definitions count.')),
	 (3, 'wtfsearch', wtfsearch, 2, L('Search in definitions base.')),
	 (3, 'wtfall', wtfall, 2, L('All definitions of word.')),
	 (9, 'wwtf', wwtf, 2, L('Information about definition commiter.')),
	 (3, 'wtff', wtff, 2, L('Show definition with nick and date.')),
	 (3, 'wtfp', wtfp, 2, L('Show definition in private.\nwtfp word\n[nick]')),
	 (0, 'wtf', wtf, 2, L('Show definition.')),
	 (3, 'dfn', dfn, 2, L('Set definition.\ndfn word=definition - remember definition as word\ndfn word= - remove definition word')),
	 (3, 'gdfn', gdfn, 2, L('Set global definition.\ngdfn word=definition - remember definition as word\ngdfn word= - remove definition word'))]
