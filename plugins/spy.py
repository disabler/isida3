#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) diSabler <dsy@dsy.name>                                    #
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

spy_stat_time = int(time.time())	# время последнего сканирования

#conf hrs usrs msgs action
def spy_add(text):
	if text == '': return L('what do you want to add?')
	text = text.lower()
	sconf = text.split(' ')[0]
	try: saction = text.split(' ',1)[1]
	except: return L('not given tracking')
	for tmp in saction.split(' '):
		if tmp[0] != 'u' and tmp[0] != 'm':
			return L('is not specified criterion tracking')
		try: int(tmp[1:])
		except: return L('incorrect digital parameter')
	if sconf not in [t[0] for t in cur_execute_fetchone('select room from conference;')]: return L('I am not in the %s ') % sconf
	if cur_execute_fetchone('select room from spy where room=%s;',(sconf,)):
		msg = L('Updated: %s') % text
		cur_execute('delete from spy where room=%s;',(sconf,))
	else: msg = L('Append: %s') % text
	cnt = len(['' for t in megabase if t[0]==tmp[0]])
	cur_execute('insert into spy values (%s,%s,%s,%s,%s)',(sconf,int(time.time()),cnt,0,saction))
	return msg

def spy_del(text):
	if text == '': return L('what do you want remove?')
	text = text.lower().split(' ')[0]
	if cur_execute_fetchone('select room from spy where room=%s;',(text,)):
		cur_execute('delete from spy where room=%s;',(text,))
		return L('Removed: %s') % text
	else: return L('Not found: %s') % text

def spy_show():
	sb = cur_execute_fetchall('select * from spy;')
	if not sb: return L('List is empty.')
	msg = L('Monitoring conferences:')
	msg += '\n%s' % '\n'.join(['%s %s (%s|u%s|m%s)' % (tmp[0],tmp[4],un_unix(int(time.time()-tmp[1])),tmp[2],tmp[3]) for tmp in sb])
	msg += L('\nNext scanning across %s') % un_unix(int(GT('scan_time')-(time.time()-spy_stat_time)))
	return msg

def conf_spy(type, jid, nick,text):
	text = text.strip().lower()
	msg = None
	if text.startswith('add '): msg = spy_add(text[4:])
	elif text.startswith('del '): msg = spy_del(text[4:])
	elif text == 'show': msg = spy_show()
	if not msg: msg = L('Smoke help about command!','%s/%s'%(jid,nick))
	send_msg(type, jid, nick, msg)

def spy_message(room,jid,nick,type,text):
	sb = cur_execute_fetchone('select message from spy where room=%s;',(room,))
	if sb: cur_execute('update spy set message=message+1 where room=%s',(room,))

def get_spy_stat():
	global spy_stat_time
	if time.time()-spy_stat_time < GT('scan_time'): return None
	spy_stat_time = time.time()
	sb = cur_execute_fetchone('select room from spy;')
	if sb:
		for tmp in sb:
			cnt = len(['' for t in megabase if t[0]==tmp[0]])
			cur_execute('update spy set participant=(participant+%s)/2 where room=%s',(cnt,tmp[0]))

def spy_action():
	try:
		if cur_execute_fetchone('select count(*) from conference;')[0] == 1: raise
	except: return None # Last conference
	sb = cur_execute_fetchall('select * from spy where %s-time>%s;',(int(time.time()),GT('spy_action_time')))
	for tmp in sb:
		act = tmp[4].split(' ')
		mist = None
		for tmp2 in act:
			if tmp2[0] == 'u' and int(tmp2[1:]) > tmp[2]: mist = tmp2
			elif tmp2[0] == 'm' and int(tmp2[1:]) > tmp[3]: mist = tmp2
			cur_execute('delete from spy where room=%s',(tmp[0],))
			if mist:
				if cur_execute_fetchall('select * from conference where room ilike %s;', ('%s/%%'%getRoom(tmp[0]),)):
					cur_execute('delete from conference where room ilike %s;', ('%s/%%'%getRoom(tmp[0]),))
					leave(tmp[0], L('I leave your conference because low activity'))
					pprint('*** Leave room: %s by spy activity!' % tmp[0],'red')
					own = cur_execute_fetchall('select * from bot_owner;')
					if own:
						for tmpo in own: send_msg('chat', tmpo[0], '', L('I leave conference %s by condition spy plugin: %s') % (tmp[0], mist))
			else: cur_execute('insert into spy values (%s,%s,%s,%s,%s)',(tmp[0],int(time.time()),tmp[2], 0,tmp[4]))

global execute, timer, message_control

timer = [get_spy_stat, spy_action]

message_control = [spy_message]

execute = [(9, 'spy', conf_spy, 2, 'Check conference activity\nspy add <conference>[ u<number>][ m<number>] - add conference to list. u - count users, m - count message per night. At default At least one condition - the bot will leave the conference\nspy del <conference> - remove conference from list\nspy show - show active monitoring.')]
