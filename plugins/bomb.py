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

bomb_colors = [L('blue'),L('red'),L('magenta'),L('green'),L('cyan'),L('yellow'),L('white'),L('black')]
bomb_current = {}

bomb_random_list = {}
bomb_random_timer_check_period = 10
bomb_random_sleep = 600
bomb_deny_access = [-1,9]
bomb_last_activity = {}
bomb_access_level = {}

def bomb_idle(jid,nick):
	global idle_base
	for tmp in idle_base:
		if tmp[0] == jid and tmp[1] == nick:
			bid = get_config_int(getRoom(jid),'bomb_idle')
			if int(time.time())-tmp[3] >= bid: break
			else: return False
	return True

def boom_bomb(room,type,nick,bc,mode):
	global bomb_access_level
	b_fault = None
	if get_config(getRoom(room),'bomb_fault'):
		bfp = get_config_int(getRoom(room),'bomb_fault_persent')
		if bfp < 0 or bfp > 100: bfp = int(config_prefs['bomb_fault_persent'][3])
		b_fault = random.randint(0,100) < bfp
	if b_fault: send_msg(type, room, nick, L('It\'s a lucky day for you! Bomb is fault! Right wide is %s') % bc)
	else:
		if mode: send_msg(type, room, nick, L('You were wrong! Right wire is %s') % bc)
		try:
			if get_config(getRoom(room),'bomb_action') == 'kick' and bomb_access_level.pop(room+nick) >= get_config_int(getRoom(room),'bomb_action_level'): muc_role(type, room, nick, '%s\n%s' % (nick,get_config(getRoom(room),'bomb_reason')), 'none',0)
		except: pass

def get_next_random(room):
	btm = get_config_int(room,'bomb_random_timer')
	if btm < 0: btm = int(config_prefs['bomb_random_timer'][3])
	btmp = get_config_int(room,'bomb_random_timer_persent')
	if btmp <= 0 or btmp > 99: btmp = int(config_prefs['bomb_random_timer_persent'][3])
	btm_pers = int(btm/100*btmp)
	bskp = get_config_int(room,'bomb_random_timer_skip_persent')
	if bskp <= 0 or bskp > 99: bskp = int(config_prefs['bomb_random_timer_skip_persent'][3])
	if random.randint(0,100) > bskp: btm *= 2
	return time.time() + btm + random.randint(-btm_pers,btm_pers)

def bomb_joke(type, jid, nick, text):
	global bomb_current,bomb_random_list,bomb_access_level
	if type == 'chat':
		send_msg(type, jid, nick, L('Not allowed in private!'))
		return
	if len(text) == 0 or len(text) == text.count(' ')+text.count('\n'):
		rlist,tconf = [],getRoom(jid)
		for tm in megabase:
			if tm[0] == tconf and not bomb_idle(jid,text) and not (get_level(tconf,tm[1])[0] in bomb_deny_access) and not (getRoom(get_level(tconf,tm[1])[1]) in ['None',getRoom(selfjid)]): rlist.append(tm[1])
		if len(rlist): text = rlist[random.randrange(len(rlist))]
		else:
			if not (nick == text == ''): send_msg(type, jid, nick, L('Here is no candidate to take a bomb!'))
			return
	bmb = False
	if not get_config(getRoom(jid),'bomb'): msg = L('In this room not allowed take a bomb!')
	elif jid in bomb_current.keys(): msg = L('This room alredy boombed!')
	elif bomb_idle(jid,text) or get_level(jid,text)[0] in bomb_deny_access or getRoom(get_level(jid,text)[1]) in ['None',getRoom(selfjid)]: msg = L('I can\'t take a bomb to %s') % text
	else:
		bomb_access_level[jid+text] = get_level(jid,nick)[0]
		b_timer = get_config_int(getRoom(jid),'bomb_timer')
		if b_timer < 0: b_timer = (config_prefs['bomb_timer'][3])
		b_wire = get_config_int(getRoom(jid),'bomb_wire')
		if b_wire < 3 or b_wire > len(bomb_colors): b_wire = int(config_prefs['bomb_wire'][3])
		b_clrs = []
		while len(b_clrs) < b_wire:
			bc = bomb_colors[random.randrange(len(bomb_colors))]
			if bc not in b_clrs: b_clrs.append(bc)
		bomb_current[getRoom(jid)] = [text,b_clrs,b_clrs[random.randrange(len(b_clrs))]]
		msg,bmb = L('/me take a bomb to %s with wires %s. Time to deactivate is %s sec.') % (text,', '.join(b_clrs),b_timer),True
	send_msg(type, jid, '', msg)
	if bmb:
		while b_timer > 0 and not game_over:
			time.sleep(1)
			b_timer -= 1
			if jid not in bomb_current.keys(): break
		if b_timer <= 0 and not game_over:
			if bomb_current.has_key(getRoom(jid)): bc = bomb_current.pop(getRoom(jid))
			else: bc = L('unknown')
			b_fault = None
			if get_config(getRoom(jid),'bomb_fault'):
				bfp = get_config_int(getRoom(jid),'bomb_fault_persent')
				if bfp < 0 or bfp > 100: bfp = int(config_prefs['bomb_fault_persent'][3])
				b_fault = random.randint(0,100) < bfp
			if b_fault: send_msg(type, jid, text, L('It\'s a lucky day for you! Bomb is fault! Right wide is %s') % bc[2])
			else:
				send_msg(type, jid, '', L('/me explode %s') % text)
				if get_config(getRoom(jid),'bomb_action') == 'kick' and bomb_access_level.pop(jid+text) >= get_config_int(getRoom(jid),'bomb_action_level'): muc_role(type, jid, nick, '%s\n%s' % (text,get_config(getRoom(jid),'bomb_reason')), 'none',0)
			bomb_random_list[getRoom(jid)] = get_next_random(getRoom(jid))

def bomb_presence(room,jid,nick,type,mass):
	global bomb_current
	if not get_config(getRoom(room),'bomb'): return
	try: bc = bomb_current[getRoom(room)]
	except: return
	if nick != bc[0]: return
	if type == 'unavailable':
		if bomb_current.has_key(getRoom(room)): bc = bomb_current.pop(getRoom(room))
		else: bc = L('unknown')
		if mass[8]:
			time.sleep(1)
			boom_bomb(room,'groupchat',mass[8],bc[2],None)
			bomb_random_list[getRoom(room)] = get_next_random(getRoom(room))

def bomb_message(room,jid,nick,type,text):
	global bomb_current,bomb_random_list
	gr = getRoom(room)
	if not get_config(gr,'bomb'): return
	try: bc = bomb_current[gr]
	except: return
	if nick != bc[0]: return
	if text.lower() not in bc[1]: return
	if bomb_current.has_key(gr): bomb_current.pop(gr)
	type = 'groupchat'
	if text.lower() == bc[2]: send_msg(type, room, nick, L('Bomb is deactivated! Congratulations!'))
	else: boom_bomb(room,type,nick,bc[2],True)
	bomb_random_list[gr] = get_next_random(gr)

def bomb_random():
	global bomb_current,bomb_random_list
	bt = bomb_random_sleep
	while not game_over and bt > 0:
		time.sleep(1)
		bt -= 1
	while not game_over:
		ntime = time.time()
		cb = [t[0] for t in cur_execute_fetchone('select room from conference;')]
		for tmp in cb:
			tconf = getRoom(tmp)
			try: bla = get_config(tconf,'bomb_random_active') and (ntime - bomb_last_activity[tconf]) < get_config_int(tconf,'bomb_random_active_timer')
			except: bla = True
			if get_config(tconf,'bomb') and get_config(tconf,'bomb_random') and bla:
				try: bsets = bomb_random_list[tconf]
				except:
					bsets = ntime
					bomb_random_list[tconf] = bsets
				if bsets < ntime:
					bomb_joke('groupchat', tconf, '', '')
					bomb_random_list[tconf] = get_next_random(tconf)
		bt = bomb_random_timer_check_period
		while not game_over and bt > 0:
			time.sleep(1)
			bt -= 1

def bomb_message_active(room,jid,nick,type,mass):
	global bomb_last_activity
	if jid != 'None': bomb_last_activity[getRoom(room)] = int(time.time())

global execute, presence_control, message_control

presence_control = [bomb_presence]
message_act_control = [bomb_message,bomb_message_active]

execute = [(4, 'bomb', bomb_joke, 2, L('Take a bomb joke!'))]
