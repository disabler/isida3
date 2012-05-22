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

# -------------- affiliation -----------------

def global_ban(type, jid, nick, text):
	text = text.lower()
	hroom = getRoom(jid)
	hr = getFile(ignoreban,[])
	al = get_level(jid,nick)[0]
	if al == 9: af = 'owner'
	else: af = get_affiliation(jid,nick)
	if af != 'owner': msg = L('This command available only for conference owner!')
	elif text == 'show' and al == 9:
		if len(hr):
			msg = L('Global ban is off in:')
			for tmp in hr: msg += '\n'+tmp
		else: msg = L('Global ban enable without limits!')
	elif text == 'del' and af == 'owner':
		if hroom in hr: msg = L('Conference %s already deleted from global ban list!') % hroom
		else:
			hr.append(hroom)
			msg = L('Conference %s has been deleted from global ban list!') % hroom
			writefile(ignoreban,str(hr))
	elif text == 'add' and af == 'owner':
		if hroom in hr:
			hr.remove(hroom)
			msg = L('Conference %s has been added from global ban list!') % hroom
			writefile(ignoreban,str(hr))
		else: msg = L('Conference %s already exist in global ban list!') % hroom
	else:
		if al == 9:
			if hroom in hr: msg = L('Your conference will be ignored for global ban!')
			elif '@' not in text or '.' not in text: msg = L('I need jid!')
			else:
				reason = L('banned global by %s from %s') % (nick, jid)
				for tmp in [t[0] for t in cur_execute_fetchall('select room from conference;')]:
					if not (getRoom(tmp) in hr):
						i = xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':getRoom(tmp)}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'outcast', 'jid':unicode(text)},[xmpp.Node('reason',{},reason)])])])
						sender(i)
						time.sleep(0.1)
				msg = L('jid %s has been banned in %s conferences.') % (text, cur_execute_fetchall('select count(*) from conference;')[0]-len(hr))
		else: msg = L('Command temporary blocked!')
	send_msg(type, jid, nick, msg)

def muc_tempo_ban(type, jid, nick,text):
	if text[:4].lower() == 'show' and '\n' not in text:
		text = text[5:]
		if not len(text): text = '.'
		ubl = getFile(tban,[])
		msg = ''
		for ub in ubl:
			if ub[0] == jid and text.lower() in ub[1]:
				if ub[2]-int(time.time()) > 0: msg += '\n%s\t%s' % (ub[1],un_unix(ub[2]-int(time.time())))
				else: msg += '\n%s\t < %s' % (ub[1],un_unix(GT('schedule_time')))
		if len(msg): msg = L('Found: %s') % msg
		else: msg = L('Not found.')
		send_msg(type, jid, nick, msg)

	elif text[:3].lower() == 'del' and '\n' not in text:
		text = text[4:]
		if not len(text): text = '@@'
		ubl = getFile(tban,[])
		msg = ''
		for ub in ubl:
			if ub[0] == jid and ub[1] == text.lower():
				msg += ub[1]+'\t'+un_unix(ub[2]-int(time.time()))
				i = xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':ub[0]}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'none', 'jid':getRoom(unicode(ub[1]))},[])])])
				sender(i)
				ubl.remove(ub)
		if len(msg):
			msg = L('Removed: %s') % msg
			writefile(tban,str(ubl))
		else: msg = L('Not found.')
		send_msg(type, jid, nick, msg)
	else: muc_tempo_ban2(type, jid, nick,text)

def muc_tempo_ban2(type, jid, nick,text):
	skip = None
	if len(text):
		who = text.split('\n',2)[0]
		try:
			ttime = text.split('\n',2)[1]
			tttime = int(ttime[:-1])
			tmode = ttime[-1:].lower()
			tkpd = {'s':1, 'm':60, 'h':3600, 'd':86400}
			tttime = tttime*tkpd[tmode]
		except: tttime = 0
		if tttime:
			try: reason = text.split('\n',2)[2]
			except: reason = L('No reason!')
			reason = L('ban on %s since %s because: %s') % \
				(un_unix(tttime), timeadd(tuple(time.localtime())), reason)
			fnd = cur_execute_fetchall('select jid from age where room=%s and (nick=%s or jid=%s) group by jid',(jid,who,who))
			if len(fnd) == 1: msg, whojid = L('done'), getRoom(unicode(fnd[0][0]))
			elif len(fnd) > 1:
				whojid = getRoom(get_level(jid,who)[1])
				if whojid != 'None': msg = L('done')
				else: msg, skip = L('I seen some peoples with this nick. Get more info!'), True
			else:
				if '.' in who:
					msg = L('I don\'n know %s, and use as is!') % who
					whojid = who
				else: msg, skip = L('I don\'t know %s') % who , True
		else: msg, skip = L('Time format error!'), True
	else: msg, skip = L('What?'), True

	if skip: send_msg(type, jid, nick, msg)
	else:
		i = xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'outcast', 'jid':unicode(whojid)},[xmpp.Node('reason',{},reason)])])])
		sender(i)

		ubl = getFile(tban,[])
		for ub in ubl:
			if ub[0] == jid and ub[1] == whojid: ubl.remove(ub)
		ubl.append((jid,whojid,tttime+int(time.time())))
		writefile(tban,str(ubl))
		send_msg(type, jid, nick, msg)

def muc_ban(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'outcast',0)
def muc_banjid(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'outcast',1)
def muc_none(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'none',0)
def muc_nonejid(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'none',1)
def muc_member(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'member',0)
def muc_memberjid(type, jid, nick,text): muc_affiliation(type, jid, nick, text, 'member',1)

def muc_affiliation(type, jid, nick, text, aff, is_jid):
	nowname = get_xnick(jid)
	xtype = get_xtype(jid)
	if xtype == 'owner': send_msg(type, jid, nick, L('Command is locked!'))
	elif len(text):
		skip = None
		if '\n' in text: who, reason = text.split('\n',1)[0], text.split('\n',1)[1]
		else: who, reason = text, []
		if reason: reason = [xmpp.Node('reason',{},reason)]
		whojid = [unicode(get_level(jid,who)[1]),who][is_jid]
		if whojid != 'None': sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':aff, 'jid':whojid},reason)])]))
		else: send_msg(type, jid, nick, L('I don\'t know %s') % who)
	else: send_msg(type, jid, nick, L('What?'))

def muc_ban_past(type, jid, nick,text): muc_affiliation_past(type, jid, nick, text, 'outcast')
def muc_none_past(type, jid, nick,text): muc_affiliation_past(type, jid, nick, text, 'none')
def muc_member_past(type, jid, nick,text): muc_affiliation_past(type, jid, nick, text, 'member')

def muc_affiliation_past(type, jid, nick, text, aff):
	nowname = get_xnick(jid)
	xtype = get_xtype(jid)
	if xtype == 'owner': msg, text = L('Command is locked!'), ''
	else: msg = L('What?')
	if len(text):
		skip = None
		if '\n' in text: who, reason = text.split('\n',1)[0], text.split('\n',1)[1]
		else: who, reason = text, []
		if reason: reason = [xmpp.Node('reason',{},reason)]
		fnd = cur_execute_fetchall('select jid from age where room=%s and (nick=%s or jid=%s) group by jid',(jid,who,who))
		if len(fnd) == 1: msg, whojid = L('done'), getRoom(unicode(fnd[0][0]))
		elif len(fnd) > 1:
			whojid = getRoom(get_level(jid,who)[1])
			if whojid != 'None': msg = L('done')
			else: msg, skip = L('I seen some peoples with this nick. Get more info!'), True
		else:
			msg = L('I don\'n know %s, and use as is!') % who
			whojid = who
	else: skip = True
	if skip: send_msg(type, jid, nick, msg)
	else:
		i = xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':aff, 'jid':unicode(whojid)},reason)])])
		sender(i)
		send_msg(type, jid, nick, msg)

def muc_kick(type, jid, nick, text): muc_role(type, jid, nick, text, 'none',1)
def muc_participant(type, jid, nick, text): muc_role(type, jid, nick, text, 'participant',1)
def muc_visitor(type, jid, nick, text): muc_role(type, jid, nick, text, 'visitor',1)
def muc_moderator(type, jid, nick, text): muc_role(type, jid, nick, text, 'moderator',1)

def muc_role(type, jid, nick, text, role, unused):
	nowname = get_xnick(jid)
	xtype = get_xtype(jid)
	if xtype == 'owner': send_msg(type, jid, nick, L('Command is locked!'))
	elif len(text):
		skip = None
		if '\n' in text: who, reason = text.split('\n',1)[0], text.split('\n',1)[1]
		else: who, reason = text, []
		if reason: reason = [xmpp.Node('reason',{},reason)]
		whojid = unicode(get_level(jid,who)[1])
		if whojid != 'None': sender(xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'role':role, 'nick':who},reason)])]))
		else: send_msg(type, jid, nick, L('I don\'t know %s') % who)
	else: send_msg(type, jid, nick, L('What?'))

def check_unban():
	unban_log = getFile(tban,[])
	if unban_log != '[]':
		ubl = []
		for ub in unban_log:
			if ub[2] > int(time.time()): ubl.append(ub)
			else:
				i = xmpp.Node('iq', {'id': get_id(), 'type': 'set', 'to':ub[0]}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_MUC_ADMIN},[xmpp.Node('item',{'affiliation':'none', 'jid':getRoom(unicode(ub[1]))},[])])])
				sender(i)
		if unban_log != ubl: writefile(tban,str(ubl))

global execute, timer

#timer = [check_unban]

execute = [(7, 'ban_past', muc_ban_past, 2, L('Ban user.')),
	   (7, 'ban', muc_ban, 2, L('Ban user.')),
	   (7, 'banjid', muc_banjid, 2, L('Ban user by jid.')),
	   (7, 'unban', muc_none, 2, L('Unban user.')),
	   (7, 'unbanjid', muc_nonejid, 2, L('Unban user by jid.')),
	   (7, 'tban', muc_tempo_ban, 2, L('Temporary ban.\ntban show|del [jid] - show/del temporary bans\ntban nick\ntimeD|H|M|S\nreason - ban nick for time because reason.')),
	   (7, 'none_past', muc_none_past, 2, L('Remove user affiliation.')),
	   (7, 'none', muc_none, 2, L('Remove user affiliation.')),
	   (7, 'nonejid', muc_nonejid, 2, L('Remove user affiliation.')),
	   (7, 'member_past', muc_member_past, 2, L('Get member affiliation.')),
	   (7, 'member', muc_member, 2, L('Get member affiliation.')),
	   (7, 'memberjid', muc_memberjid, 2, L('Get member affiliation.')),
	   (7, 'kick', muc_kick, 2, L('Kick user.')),
	   (7, 'participant', muc_participant, 2, L('Change role to participant.')),
	   (7, 'visitor', muc_visitor, 2, L('Revoke voice.')),
	   (7, 'moderator', muc_moderator, 2, L('Grant moderator.')),
	   (8, 'global_ban', global_ban, 2, L('Global ban. Available only for confernce owner.\nglobal_ban del - remove conference from banlist,\nglobal_ban add - add conference into banlist,\nglobal_ban <jid> - ban jid in all rooms, where bot is admin.'))]
