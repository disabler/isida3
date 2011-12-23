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

iq_ping_minimal = 0

def get_who_iq(text,jid,nick):
	if text == '': who = '%s/%s' % (getRoom(jid),nick)
	else:
		who = text
		for mega1 in megabase:
			if mega1[0] == jid and mega1[1] == text:
				who = '%s/%s' % (getRoom(jid),text)
				break
	return who

def get_caps(room,nick):
	try:
		(id_node,id_ver,id_bmver) = capses['%s/%s' % (room,nick)].split('\n')
		if id_bmver: msg = '%s %s (%s)' % (id_node,id_ver,id_bmver)
		else: msg = '%s %s' % (id_node,id_ver)
	except: msg = None
	return msg

def noiq_caps(type, jid, nick, text):
	text = [text,nick][text == '']
	msg = get_caps(jid,text)
	if not msg: msg = L('I can\'t get caps of %s') % text
	send_msg(type, jid, nick, msg)

def iq_vcard(type, jid, nick, text):
	global iq_request
	if '\n' in text: text,args = text.split('\n',1)
	else: args = ''
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('vCard', {'xmlns': NS_VCARD},[])])
	iq_request[iqid]=(time.time(),vcard_async,[type, jid, nick, text, args])
	sender(i)

def vcard_async(type, jid, nick, text, args, is_answ):
	isa = is_answ[1][0]
	if isa == '<vCard xmlns="vcard-temp" />': msg = L('vCard:') + ' ' + L('Empty!')
	elif isa[:6] == '<vCard' and isa[-8:] == '</vCard>':
		while '<BINVAL>' in isa and '</BINVAL>' in isa: isa=isa[:isa.find('<BINVAL>')]+isa[isa.find('</BINVAL>')+9:]
		while '<PHOTO>' in isa and '</PHOTO>' in isa: isa=isa[:isa.find('<PHOTO>')]+isa[isa.find('</PHOTO>')+8:]
		msg = ''
		if args.lower() == 'show':
			msg_header = '%s ' % L('vCard tags:')
			for i in range(0,len(isa)):
				if isa[i] == '<':
					tag = isa[i+1:isa.find('>',i)]
					if '</%s>' % tag in isa[i:]: msg += '%s, ' % tag
			msg = msg[:-2]
		elif args != '':
			msg_header = '%s ' % L('vCard:')
			for tmp in args.split('|'):
				if ':' in tmp: tname,ttag = tmp.split(':')[1],tmp.split(':')[0]
				else: tname,ttag = tmp,tmp
				tt = get_tag(isa,ttag.upper())
				if tt != '': msg += '\n%s: %s' % (tname,rss_del_nn(remove_ltgt(tt.replace('><','> <').replace('>\n<','> <'))))
		else:
			msg_header = L('vCard:')
			for tmp in [(L('Nick'),'NICKNAME'),(L('Name'),'FN'),(L('About'),'DESC'),(L('URL'),'URL')]:
				tt = remove_ltgt(get_tag(isa,tmp[1]))
				if len(tt): msg += '\n%s: %s' % (tmp[0],tt)
		if len(msg): msg = msg_header + msg
		else: msg = msg_header + L('Empty!')
	else: msg = '%s %s' % (L('vCard:'),L('Not found!'))
	send_msg(type, jid, nick, msg)

def iq_uptime(type, jid, nick, text):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_LAST},[])])
	iq_request[iqid]=(time.time(),uptime_async,[type, jid, nick, text])
	sender(i)

def uptime_async(type, jid, nick, text, is_answ):
	isa = is_answ[1][0]
	try:
		msg = L('Uptime: %s') % un_unix(int(get_tag_item(isa,'query','seconds')))
		up_stat = esc_min(get_tag(isa,'query'))
		if len(up_stat): msg = '%s // %s' % (msg,up_stat)
	except: msg = L('I can\'t do it')
	send_msg(type, jid, nick, msg)

def urn_ping(type, jid, nick, text):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('ping', {'xmlns': NS_URN_PING},[])])
	iq_request[iqid]=(time.time(),ping_async,[type, jid, nick, text])
	sender(i)

def ping(type, jid, nick, text):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_VERSION},[])])
	iq_request[iqid]=(time.time(),ping_async,[type, jid, nick, text])
	sender(i)

def ping_async(type, jid, nick, text, is_answ):
	global iq_ping_minimal
	if '%s %s!' % (L('Error!'),L('Remote server not found')) == is_answ[1][0]: msg = is_answ[1][0]
	else:
		tpi_old = float(is_answ[0])-time_nolimit
		tpi = round(tpi_old - iq_ping_minimal,GT('ping_digits'))
		if tpi <= 0: tpi = round(iq_ping_minimal,GT('ping_digits'))
		if iq_ping_minimal == 0 or iq_ping_minimal > tpi_old: iq_ping_minimal = tpi_old
		if text == '': msg = L('Ping from you %s sec.') % tpi
		else: msg = L('Ping from %s %s sec.') % (text, tpi)
	send_msg(type, jid, nick, msg)

def iq_time(type, jid, nick, text):
	iq_time_get(type, jid, nick, text, None)

def iq_time_raw(type, jid, nick, text):
	iq_time_get(type, jid, nick, text, True)

def iq_time_get(type, jid, nick, text, mode):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_TIME},[])])
	iq_request[iqid]=(time.time(),time_async,[type, jid, nick, text, mode])
	sender(i)

def time_async(type, jid, nick, text, mode, is_answ):
	isa = is_answ[1]
	if len(isa) == 3:
		msg = isa[0]
		if mode: msg += ', Raw time: %s, TimeZone: %s' % (isa[1],isa[2])
	else: msg = ' '.join(isa)
	send_msg(type, jid, nick, msg)

def iq_utime(type, jid, nick, text):
	iq_utime_get(type, jid, nick, text, None)

def iq_utime_raw(type, jid, nick, text):
	iq_utime_get(type, jid, nick, text, True)

def iq_utime_get(type, jid, nick, text, mode):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('time', {'xmlns': NS_URN_TIME},[])])
	iq_request[iqid]=(time.time(),utime_async,[type, jid, nick, text, mode])
	sender(i)

def utime_async(type, jid, nick, text, mode, is_answ):
	isa,ert = is_answ[1],L('Error! %s')%''
	if isa[0][:len(ert)] == ert: msg = isa[0]
	else:
		try:
			ttup,tt = isa[0].replace('T','-').replace('Z','').replace(':','-').split('-')+['0','0',str(tuple(time.localtime())[8])],[]
			for tmp in ttup: tt.append(int(tmp.split('.',1)[0]))
			msg = nice_time(time.mktime(tuple(tt)) + (int(isa[1].split(':')[0])*60+int(isa[1].split(':')[1]))*60)[2]
			if mode: msg = '%s | %s %s' % (msg,isa[0],isa[1])
		except: msg = '%s %s' % (L('Unknown server answer!'),isa[0])
	send_msg(type, jid, nick, msg)

def iq_version(type, jid, nick, text): iq_version_raw(type, jid, nick, text, False)

def iq_version_caps(type, jid, nick, text): iq_version_raw(type, jid, nick, text, True)

def iq_version_raw(type, jid, nick, text, with_caps):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [Node('query', {'xmlns': NS_VERSION},[])])
	iq_request[iqid]=(time.time(),version_async,[type, jid, nick, text, with_caps])
	sender(i)

def version_async(type, jid, nick, text, with_caps, is_answ):
	isa = is_answ[1]
	if len(isa) == 3: msg = '%s %s // %s' % isa
	else: msg = ' '.join(isa)
	if with_caps:
		caps = get_caps(jid,[text,nick][text == ''])
		if caps: msg += ' || %s' % caps
	send_msg(type, jid, nick, msg)

def iq_stats_host(type, jid, nick, text): iq_stats_raw(type, jid, nick, text, True)

def iq_stats(type, jid, nick, text): iq_stats_raw(type, jid, nick, text, False)

def iq_stats_raw(type, jid, nick, text, flag):
	global iq_request
	if text == '':
			send_msg(type, jid, nick, u'Ась?')
			return
	iqid = get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':text}, payload = [Node('query', {'xmlns': NS_STATS},[Node('stat', {'name':'users/total'},[]),Node('stat', {'name':'users/online'},[]),Node('stat', {'name':'users/all-hosts/online'},[]),Node('stat', {'name':'users/all-hosts/total'},[])])])
	iq_request[iqid]=(time.time(),stats_async,[type, jid, nick, text, flag])
	sender(i)

def stats_async(type, jid, nick, text, flag, is_answ):
	isa,ert = is_answ[1],L('Error! %s')%''
	if isa[0][:len(ert)] == ert: msg = isa[0]
	else:
		isa = unicode(isa)
		if isa == 'None': ans = [0,0,0,0]
		else:
			stat_mas = {}
			while len(get_tag(isa,'query')):
				tmp_stat = get_tag_full(isa,'stat')
				stat_mas[get_tag_item(tmp_stat,'stat','name')] = get_tag_item(tmp_stat,'stat','value')
				isa = isa.replace(tmp_stat,'')
			ans = []
			for tmp in ['users/total','users/online','users/all-hosts/total','users/all-hosts/online']:
				try: t_ans = int(stat_mas[tmp])
				except: t_ans = 0
				ans.append(t_ans)
		msg = L('Server statistic: %s | Total/Online: %s/%s') % (text,ans[0],ans[1])
		if flag and ans[2:] != [0,0]: msg += ' | ' + L('Total/Online on all hosts: %s/%s') % (ans[2],ans[3])
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, u'ver', iq_version, 2, L('Client version.')),
		   (3, u'ver+', iq_version_caps, 2, L('Client version with caps.')),
		   (3, u'caps', noiq_caps, 2, L('Show caps node and version of client.')),
		   (3, u'ping_old', ping, 2, L('Ping - reply time. You can ping nick in room, jid, server or transport.')),
		   (3, u'ping', urn_ping, 2, L('Ping - reply time. You can ping nick in room, jid, server or transport.')),
		   (3, u'time_old', iq_time, 2, L('Client side time.')),
		   (3, u'time', iq_utime, 2, L('Client side time.')),
		   (3, u'time_old_raw', iq_time_raw, 2, L('Client side time + raw time format.')),
		   (3, u'time_raw', iq_utime_raw, 2, L('Client side time + raw time format.')),
		   (3, u'stats', iq_stats, 2, L('Users server statistic.')),
		   (3, u'stats+', iq_stats_host, 2, L('Users server statistic.')),
		   (3, u'vcard_raw', iq_vcard, 2, L('vCard query. Recomends make command base alias for query needs info.\nvcard_raw [nick] - query generic info\nvcard_raw nick\nshow - show available fields\nvcard_raw nick\n[field:name|field:name] - show requested fields from vcard.')),
		   (3, u'uptime', iq_uptime, 2, L('Server or jid uptime.'))]
