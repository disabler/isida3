#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2011 diSabler <dsy@dsy.name>                               #
#    Copyright (C) 2011 Vit@liy <vitaliy@root.ua>                             #
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

ANSW_PREV = {}
FLOOD_STATS = {}

if os.path.isfile(os.path.join(loc_folder, '%s.txt' % CURRENT_LOCALE)):
	chat_folder = 'plugins/chat/%s/' % CURRENT_LOCALE
else:
	chat_folder = 'plugins/chat/en/'

MIND_FILE = chat_folder + 'mind.txt'
EMPTY_FILE = chat_folder + 'empty.txt'
ANSWER_FILE = chat_folder + 'answer.txt'

list_of_mind = [m.strip() for m in readfile(MIND_FILE).split('\n') if m.strip()]
list_of_answers = readfile(ANSWER_FILE).split('\n')
list_of_empty = readfile(EMPTY_FILE).split('\n')

def flood_actions(type, room, nick, answ, msg):
	text = ''
	jid = getRoom(get_level(room,nick)[1])
	cof = getFile(conoff,[])
	tmppos = arr_semi_find(confbase, room)
	nowname = getResourse(confbase[tmppos])
	access_mode = get_level(room,nick)[0]
	if (room, answ[1:]) in cof: return
	if answ == '@ping':
		nicks = [d[1] for d in megabase if d[0]==room]
		tmp = [n for n in nicks if n.upper() in msg]
		if not tmp: text = 'ping'
		elif len(tmp) == 1: text = 'ping %s' % tmp[0]
		else: send_msg(type, room, nick, L('What?'))
	elif answ == '@anek': text = 'anek'
	elif answ == '@calend':
		if u'ЗАВТРА' in msg: text = time.strftime('calend %d.%m', time.localtime(time.time()+86400))
		else: text = 'calend'
	if text: com_parser(access_mode, nowname, type, room, nick, text, jid)

def addAnswerToBase(tx):
	if not len(tx) or tx.count(' ') == len(tx): return
	cur_execute('select ind from answer')
	lent = len(cur.fetchall())+1
	cur_execute('insert into answer values (%s,%s)', (lent,tx))
	conn.commit()

def getRandomAnswer(tx,room):
	if not tx.strip(): return None
	cur_execute('select ind from answer')
	lent = len(cur.fetchall())
	mrand = randint(1,lent)
	cur_execute('select body from answer where ind=%s', (mrand,))
	answ = to_censore(cur.fetchone()[0],room)
	return answ

def getSmartAnswer(type, room, nick, text):
	if '?' in text: answ = random.choice(list_of_answers).strip()
	else: answ = random.choice(list_of_empty).strip()
	score,sc, var = 1.0,0,[answ]
	text = ' %s ' % text.upper()
	for answer in list_of_mind:
		s = answer.split('||')
		sc = rating(s[0], text, room)
		if sc > score: score,var = sc,s[1].split('|')
		elif sc == score: var += s[1].split('|')
	answ = random.choice(var).decode('utf-8')
	if answ[0] != '@': return answ
	else:
		flood_actions(type, room, nick, answ, text)
		return ''

def rating(s, text, room):
	r,s = 0.0,s.decode('utf-8').split('|')
	for _ in s:
		if _ in text: r += 1
		if _ in ANSW_PREV.get(room, ''): r += 0.5
	return r

def getAnswer(type, room, nick, text):
	text = text.strip()
	if get_config(getRoom(room),'flood') in ['random',True]: answ = getRandomAnswer(text,room)
	else:
		answ = getSmartAnswer(type, room, nick, text)
		ANSW_PREV[room] = text.upper()
	if type == 'groupchat' and text == to_censore(text,room): addAnswerToBase(text)
	return answ
	
def flood_action(room,jid,nick,type,text):
	if get_config(room,'autoflood'):
		jjid = getRoom(jid)
		tm = time.time()
		prefix = get_local_prefix(room)
		first_word = text.split(' ', 1)[0]
		if nick in [get_xnick(room), ''] or jjid in ignorebase or ddos_ignore.has_key(jjid): return
		if first_word in [prefix + i[1] for i in comms] + [i[1] for i in aliases if i[0] == room] or first_word[:-1] in [d[1] for d in megabase if d[0]==room]:
			if FLOOD_STATS.has_key(room) and FLOOD_STATS[room][0] != jjid:
				FLOOD_STATS[room] = ['', 0, 0]
			return
		if not FLOOD_STATS.has_key(room) or FLOOD_STATS[room][0] != jjid:
			FLOOD_STATS[room] = [jjid, tm, 1]
		else:
			FLOOD_STATS[room][2] += 1

		if FLOOD_STATS.has_key(room) and FLOOD_STATS[room][2] >= get_config_int(room,'floodcount') and tm - FLOOD_STATS[room][1] > get_config_int(room,'floodtime'):
			msg = getAnswer(type, room, nick, text)
			send_msg(type, room, nick, msg)
			return True
	return False

global execute, message_act_control

message_act_control = [flood_action]
execute = []