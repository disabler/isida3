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

# id, room, jid, nick, level, tags, body, status, date, comment, accept_by, accept_date

issue_status = [L('new'),L('accepted'),L('rejected'),L('removed')]
issue_status_show = ['',L('Accepted by'),L('Rejected by'),L('Removed by')]
issue_accept_id = 1
issue_reject_id = 2
issue_remove_id = 3

def issue(type, room, nick, text):
	subc = reduce_spaces_all(text).split()
	acclvl,jid = get_level(room,nick)
	if not subc or subc[0] == 'show': msg = issue_show(subc,room)
	elif subc[0] in ['del','delete','rm','remove']: msg = issue_remove(subc,acclvl,room,jid,nick)
	elif subc[0] == 'accept': msg = issue_accept(subc,acclvl,room,jid,nick)
	elif subc[0] == 'reject': msg = issue_reject(subc,acclvl,room,jid,nick)
	else: msg = issue_new(subc,acclvl,room,jid,nick)
	send_msg(type, room, nick, msg)

def issue_new(s,acclvl,room,jid,nick):
	tags = []
	for t in s:
		if t[0] == '*' and len(t) > 1: tags.append(t[1:])
		else: break
	s = s[len(tags):]
	if not s: return L('No issue\'s body!')
	tags = ' '.join(tags)
	body = ' '.join(s)
	try: id = cur_execute_fetchone('select count(*) from issues where room=%s',(room,))[0] + 1
	except: id = 1
	tbody = cur_execute_fetchall('select id from issues where room=%s and body ilike %s',(room,'%%%s%%' % body))
	if tbody: return L('I know same issue(s): %s') % ', '.join('#%04d' % t for t in zip(*tbody)[0])
	err = cur_execute('insert into issues values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (id, room, getRoom(jid), nick, acclvl, tags, body, 0, int(time.time()),'','',0))
	if err: return err
	else: return L('Added issue #%04d') % id

def issue_show(s,room):
	if len(s) > 1: s = s[1]
	else: s = '%'
	s_original = s
	if s.isdigit() or s[0] == '#': iss = cur_execute_fetchall('select id,nick,tags,body,status,comment,accept_by,accept_date from issues where room=%s and id=%s order by id;',(room,int(s.replace('#',''))))
	elif s[0] == '*': iss = cur_execute_fetchall('select id,nick,tags,body,status,comment,accept_by,accept_date from issues where room=%s and tags ilike %s and status!=%s order by id;',(room,'%%%s%%' % s[1:],issue_remove_id))
	else:
		if s != '%': s = '%%%s%%' % s
		iss = cur_execute_fetchall('select id,nick,tags,body,status,comment,accept_by,accept_date from issues where room=%s and (tags ilike %s or body ilike %s or comment ilike %s or nick ilike %s) and status!=3 order by id;',(room,s,s,s,s))
	if iss:
		tm = []
		for t in iss:
			if t[2]: tmp = '#%04d (%s) *%s | %s\n%s' % (t[0],issue_status[t[4]],' *'.join(t[2].split()),L('Created by %s') % t[1],t[3])
			else: tmp = '#%04d (%s) %s\n%s' % (t[0],issue_status[t[4]],L('Created by %s') % t[1],t[3])
			if t[4]:
				tmp = '%s\n%s %s [%s]' % (tmp,issue_status_show[t[4]],t[6],disp_time(t[7]))
				if t[5]: tmp += L(', by reason: %s') % t[5]
			tm.append(tmp)
		return L('Issue(s) list:\n%s') % '\n\n'.join(tm)
	elif s_original == '%': return L('Issues not found!')
	else: return L('Issues with match \'%s\' not found!') % s_original
	
def issue_remove(s,acclvl,room,jid,nick):
	if len(s) > 1: id = s[1]
	else: return L('Which issue need remove?')
	if id.isdigit() or id[0] == '#':
		try: id = int(id.replace('#',''))
		except: return L('You must use numeric issue id.')
		iss = cur_execute_fetchall('select jid,level,status from issues where room=%s and id=%s;',(room,id))
	else: return L('You must use numeric issue id.')
	if iss:
		if iss[0][2] != issue_remove_id:
			if acclvl >= 7 or iss[0][0] == jid:
				if len(s) > 2: cmt = ' '.join(s[2:])
				else: cmt = ''
				cur_execute('update issues set status=%s,accept_by=%s,accept_date=%s,comment=%s where room=%s and id=%s', (issue_remove_id,nick,int(time.time()),cmt,room,id))
				return L('Issue #%04d removed!') % id
			else: return L('There is not Your issue or You have no rights to remove it.')
		else: return L('Issue #%04d was removed earlier!') % id
	else: return L('Issue #%04d not found!') % id

def issue_accept(s,acclvl,room,jid,nick):
	if len(s) > 1: id = s[1]
	else: return L('Which issue need accept?')
	if id.isdigit() or id[0] == '#':
		try: id = int(id.replace('#',''))
		except: return L('You must use numeric issue id.')
		iss = cur_execute_fetchall('select jid,level,status,tags from issues where room=%s and id=%s;',(room,id))
	else: return L('You must use numeric issue id.')
	if iss:
		if acclvl >= 7 or iss[0][0] == jid or iss[0][1] <= acclvl:
			if len(s) > 2:
				tags = iss[0][3].split()
				cnt = 2
				for t in s[2:]:
					if t[0] == '*' and len(t) > 1:
						if t[1:] not in tags: tags.append(t[1:])
						else: tags.remove(t[1:])
						cnt += 1
					else: break
				s = s[cnt:]
				tags = ' '.join(tags)
				cmt = ' '.join(s)
			else: cmt,tags = '',iss[0][3]
			cur_execute('update issues set status=%s,accept_by=%s,accept_date=%s,comment=%s,tags=%s where room=%s and id=%s', (issue_accept_id,nick,int(time.time()),cmt,tags,room,id))
			if iss[0][2] != issue_accept_id: return L('Issue #%04d accepted!') % id
			else: return L('Issue #%04d was accepted earlier!') % id
		else: return L('There is not Your issue or You have no rights to accept it.')
	else: return L('Issue #%04d not found!') % id

def issue_reject(s,acclvl,room,jid,nick):
	if len(s) > 1: id = s[1]
	else: return L('Which issue need reject?')
	if id.isdigit() or id[0] == '#':
		try: id = int(id.replace('#',''))
		except: return L('You must use numeric issue id.')
		iss = cur_execute_fetchall('select jid,level,status from issues where room=%s and id=%s;',(room,id))
	else: return L('You must use numeric issue id.')
	if iss:
		if iss[0][2] != issue_reject_id:
			if acclvl >= 7 or iss[0][0] == jid or iss[0][1] <= acclvl:
				if len(s) > 2: cmt = ' '.join(s[2:])
				else: cmt = ''
				cur_execute('update issues set status=%s,accept_by=%s,accept_date=%s,comment=%s where room=%s and id=%s', (issue_reject_id,nick,int(time.time()),cmt,room,id))
				return L('Issue #%04d rejected!') % id
			else: return L('There is not Your issue or You have no rights to reject it.')
		else: return L('Issue #%04d was rejected earlier!') % id
	else: return L('Issue #%04d not found!') % id

global execute

execute = [(3, 'issue', issue, 2, L('Issues\nissue [[[show|accept|reject|delete] id] reason] - actions with issue\nissue *tag1 *tag2 some text - add issue `some text` with tags tag1 and tag2'))]
