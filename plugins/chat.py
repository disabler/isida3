#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2012 diSabler <dsy@dsy.name>                               #
#    Copyright (C) 2012 Vit@liy <vitaliy@root.ua>                             #
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

autophrases_time = {}

if os.path.isfile(os.path.join(loc_folder, '%s.txt' % CURRENT_LOCALE)):
	chat_folder = data_folder % 'chat/%s/' % CURRENT_LOCALE
else:
	chat_folder = data_folder % 'chat/en/'

MIND_FILE = chat_folder + 'mind.txt'
EMPTY_FILE = chat_folder + 'empty.txt'
ANSWER_FILE = chat_folder + 'answer.txt'
PHRASES_FILE = chat_folder + 'phrases.txt'

list_of_answers = readfile(ANSWER_FILE).split('\n')
list_of_empty = readfile(EMPTY_FILE).split('\n')
list_of_phrases_with_highlight = []
list_of_phrases_no_highlight = []
for phrase in readfile(PHRASES_FILE).split('\n'):
	if 'NICK' in phrase:
		list_of_phrases_with_highlight.append(phrase)
	else:
		list_of_phrases_no_highlight.append(phrase)

dict_of_mind = {}
for p in readfile(MIND_FILE).split('\n'):
	if '||' in p:
		tmp1, tmp2 = p.strip().split('||')
		dict_of_mind[tmp1] = tmp2.split('|')

def flood_actions(type, room, nick, answ, msg):
	text = ''
	jid = getRoom(get_level(room,nick)[1])
	nowname = getResourse(cur_execute_fetchone('select room from conference where room ilike %s',('%s/%%'%room,))[0])
	access_mode = get_level(room,nick)[0]
	if cur_execute_fetchone('select * from commonoff where room=%s and cmd=%s',(room,answ[1:])): return
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
	lent = len(cur_execute_fetchall('select ind from answer'))+1
	cur_execute('insert into answer values (%s,%s)', (lent,tx))
	conn.commit()

def getRandomAnswer(tx,room):
	if not tx.strip(): return None
	lent = len(cur_execute_fetchall('select ind from answer'))
	mrand = random.randint(1,lent)
	answ = to_censore(cur_execute_fetchone('select body from answer where ind=%s', (mrand,))[0],room)
	return answ

def getSmartAnswer(type, room, nick, text):
	if '?' in text: answ = random.choice(list_of_answers).strip()
	else: answ = random.choice(list_of_empty).strip()
	score,sc, var = 1.0,0,[answ]
	text = ' %s ' % text.upper()
	for answer in dict_of_mind:
		sc = rating(answer, text, room)
		if sc > score: score,var = sc,dict_of_mind[answer]
		elif sc == score: var += dict_of_mind[answer]
		
	answ = random.choice(var).decode('utf-8')
	if answ[0] != '@': return answ
	else:
		flood_actions(type, room, nick, answ, text)
		return ''

def rating(s, text, room):
	r,s = 0.0,s.decode('utf-8').split('|')
	for k in s:
		if k in text: r += 1
		if k in ANSW_PREV.get(room, ''): r += 0.5
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
		cur_alias = cur_execute_fetchall('select match from alias where room=%s',(room,))
		if cur_alias: cur_alias = [t[0] for t in cur_alias]
		else: cur_alias = []
		if nick in [get_xnick(room), ''] or cur_execute_fetchone('select pattern from bot_ignore where %s ilike pattern',(jjid,)) or ddos_ignore.has_key(jjid): return
		if first_word in [prefix + i[1] for i in comms] + cur_alias or first_word[:-1] in [d[1] for d in megabase if d[0]==room]:
			if FLOOD_STATS.has_key(room) and FLOOD_STATS[room][0] != jjid: FLOOD_STATS[room] = ['', 0, 0]
			return
		if not FLOOD_STATS.has_key(room) or FLOOD_STATS[room][0] != jjid: FLOOD_STATS[room] = [jjid, tm, 1]
		else: FLOOD_STATS[room][2] += 1
		if FLOOD_STATS.has_key(room) and FLOOD_STATS[room][2] >= get_config_int(room,'floodcount') and tm - FLOOD_STATS[room][1] > get_config_int(room,'floodtime'):
			pprint('Send msg human: %s/%s [%s] <<< %s' % (room,nick,type,text),'dark_gray')
			try:
				msg = getAnswer(type, room, nick, text)
				if text: send_msg_human(type, room, nick, msg, 'msg_human_auto')
				else: return False
			except: return False
			return True
	return False

def phrases_timer():
	for room in list(set([i[0] for i in megabase])):
		if get_config(room,'autophrases') != 'off':
			if not room in autophrases_time:
				autophrases_time[room] = time.time() + random.normalvariate(int(get_config(room,'autophrasestime')), 2) / 2
			if time.time() > autophrases_time[room]:
				if get_config(room,'autophrases') == 'without highlight':
					msg = random.choice(list_of_phrases_no_highlight).decode('utf-8')
				else:
					msg = random.choice(list_of_phrases_with_highlight + list_of_phrases_no_highlight).decode('utf-8')
				if 'NICK' in msg:
					rand_nicks = [d[1] for d in megabase if d[0]==room if cur_execute_fetchone('select pattern from bot_ignore where %s ilike pattern',(getRoom(d[4]),)) and d[1] not in [get_xnick(room), '']]
					msg = msg.replace('NICK', random.choice(rand_nicks))
				send_msg('groupchat', room, '', msg)
				autophrases_time[room] = time.time() + random.normalvariate(int(get_config(room,'autophrasestime')), 2)

global execute, message_act_control, timer

message_act_control = [flood_action]
timer = [phrases_timer] 
execute = []
