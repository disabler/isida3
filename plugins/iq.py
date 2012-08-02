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

# translate: FN,NICKNAME,N.FAMILY,N.GIVEN,N.MIDDLE,ADR.LOCALITY,ADR.REGION,ADR.PCODE,ADR.CTRY,ADR.STREET,TEL.NUMBER,EMAIL.USERID,EMAIL,JABBERID,ROLE,BDAY,URL,DESC,ROLE,ORG.ORGNAME,ORG.ORGUNIT,GEO.LAT,GEO.LON,TITLE,uptime,seconds,users/registered,users,users/online,contacts/online,contacts,contacts/total,messages/in,messages,messages/out,memory-usage,KB,users/all-hosts/total,users/all-hosts/online,users/total

VCARD_LIMIT_LONG = 256
VCARD_LIMIT_SHORT = 128
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
	elif len(msg) == msg.count(' ')+msg.count('\n'): msg = L('%s has empty caps!') % text
	send_msg(type, jid, nick, msg)

def iq_vcard(type, jid, nick, text):
	global iq_request
	if '\n' in text: text,args = text.split('\n',1)
	else: args = ''
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('vCard', {'xmlns': xmpp.NS_VCARD},[])])
	iq_request[iqid]=(time.time(),vcard_async,[type, jid, nick, text, args])
	sender(i)

def get_value_from_array2(a,v):
	for t in a:
		if t[0] == v: return t[1]
	return None
	
def get_array_from_array2(a1,a2):
	a_res = []
	for t in a1:
		if t[0] in a2: a_res.append(t)
	return a_res
	
def vcard_async(type, jid, nick, text, args, is_answ):
	try: vc,err = is_answ[1][1].getTag('vCard',namespace=xmpp.NS_VCARD),False
	except: vc,err = is_answ[1][0],True
	if not vc: msg = '%s %s' % (L('vCard:'),L('Empty!'))
	elif err: msg = '%s %s' % (L('vCard:'),vc[:VCARD_LIMIT_LONG])
	else:
		data = []
		for t in vc.getChildren():
			if t.getChildren():
				cm = []
				for r in t.getChildren():
					if r.getData(): cm.append(('%s.%s' % (t.getName(),r.getName()),unicode(r.getData())))
				data += cm
			elif t.getData(): data.append((t.getName(),t.getData()))
		try:
			photo_size = sys.getsizeof(get_value_from_array2(data,'PHOTO.BINVAL').decode('base64'))
			photo_type = get_value_from_array2(data,'PHOTO.TYPE')
			data_photo = L('type %s, %s byte(s)') % (photo_type,photo_size)
			data = (t for t in list(data) if t[0] not in ['PHOTO.BINVAL','PHOTO.TYPE'])
			data.append(('PHOTO',data_photo))
		except: pass
		args = args.lower()
		if not args:
			dd = get_array_from_array2(data,['NICKNAME','FN','BDAY','URL','PHOTO','DESC'])
			if dd: msg = '%s\n%s' % (L('vCard:'),'\n'.join(['%s: %s' % ([L(t[0]),t[0].capitalize()][L(t[0])==t[0]],[u'%s…' % t[1][:VCARD_LIMIT_LONG],t[1]][len(t[1])<VCARD_LIMIT_LONG]) for t in dd]))
			else: msg = '%s %s' % (L('vCard:'),L('Not found!'))
		elif args == 'all': msg = '%s\n%s' % (L('vCard:'),'\n'.join(['%s: %s' % ([L(t[0]),t[0].capitalize()][L(t[0])==t[0]],[u'%s…' % t[1][:VCARD_LIMIT_SHORT],t[1]][len(t[1])<VCARD_LIMIT_SHORT]) for t in data]))
		elif args == 'show':
			dd = []
			for t in data:
				if t[0] not in dd: dd.append(t[0])
			msg = '%s %s' % (L('vCard:'),', '.join([[t.capitalize(),'%s (%s)' % (t.capitalize(),L(t))][L(t)!=t] for t in dd]))
		else:
			args,dd = args.split('|'),[]
			for t in args:
				if ':' in t: val,loc = t.split(':',1)
				else: val,loc = t,t
				val = val.upper()
				dv = get_array_from_array2(data,(val))
				if dv: dd += dv
			if dd: msg = '%s\n%s' % (L('vCard:'),'\n'.join(['%s: %s' % ([L(t[0]),t[0].capitalize()][L(t[0])==t[0]],[u'%s…' % t[1][:VCARD_LIMIT_LONG],t[1]][len(t[1])<VCARD_LIMIT_LONG]) for t in dd]))
			else: msg = '%s %s' % (L('vCard:'),L('Not found!'))			
	send_msg(type, jid, nick, msg)

def iq_uptime(type, jid, nick, text):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_LAST},[])])
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
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('ping', {'xmlns': xmpp.NS_URN_PING},[])])
	iq_request[iqid]=(time.time(),ping_async,[type, jid, nick, text])
	sender(i)

def ping(type, jid, nick, text):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_VERSION},[])])
	iq_request[iqid]=(time.time(),ping_async,[type, jid, nick, text])
	sender(i)

def ping_async(type, jid, nick, text, is_answ):
	global iq_ping_minimal
	if '%s %s!' % (L('Error!'),L('Remote server not found')) == is_answ[1][0]: msg = is_answ[1][0]
	else:
		tpi_old = float(is_answ[0])-time_nolimit
		p_digits = GT('ping_digits')
		tpi = round(tpi_old - iq_ping_minimal,p_digits)
		if tpi <= 0: tpi = round(iq_ping_minimal,p_digits)
		if iq_ping_minimal == 0 or iq_ping_minimal > tpi_old: iq_ping_minimal = tpi_old
		f = '%'+'.0%sf' % p_digits
		if text == '': msg = L('Ping from you %s sec.') % f % tpi
		else: msg = L('Ping from %s %s sec.') % (text, f % tpi)
	send_msg(type, jid, nick, msg)

def iq_time(type, jid, nick, text):
	iq_time_get(type, jid, nick, text, None)

def iq_time_raw(type, jid, nick, text):
	iq_time_get(type, jid, nick, text, True)

def iq_time_get(type, jid, nick, text, mode):
	global iq_request
	who,iqid = get_who_iq(text,jid,nick),get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_TIME},[])])
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
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('time', {'xmlns': xmpp.NS_URN_TIME},[])])
	iq_request[iqid]=(time.time(),utime_async,[type, jid, nick, text, mode])
	sender(i)

def utime_async(type, jid, nick, text, mode, is_answ):
	isa = is_answ[1]
	if isa[0].startswith(L('Error! %s')%''): msg = isa[0]
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
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':who}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_VERSION},[])])
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

def iq_stats(type, jid, nick, text):
	global iq_request
	if text == '':
		send_msg(type, jid, nick, L('What?'))
		return
	iqid = get_id()
	i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':text}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_STATS},[])])
	iq_request[iqid]=(time.time(),stats_async_features,[type, jid, nick, text])
	sender(i)

def stats_async_features(type, jid, nick, text, is_answ):
	isa = is_answ[1]
	if isa[0].startswith(L('Error! %s')%''): send_msg(type, jid, nick, isa[0])
	else:
		try: stats_list = [t.getAttr('name') for t in isa[1].getTag('query',namespace=xmpp.NS_STATS).getTags('stat')]
		except: stats_list = []
		if stats_list:
			iqid = get_id()
			i = xmpp.Node('iq', {'id': iqid, 'type': 'get', 'to':text}, payload = [xmpp.Node('query', {'xmlns': xmpp.NS_STATS},[xmpp.Node('stat', {'name':t},[]) for t in stats_list])])
			iq_request[iqid]=(time.time(),stats_async,[type, jid, nick, text])
			sender(i)		
		else: send_msg(type, jid, nick, L('Unavailable!'))

def stats_async(type, jid, nick, text, is_answ):
	isa = is_answ[1]
	if isa[0].startswith(L('Error! %s')%''): msg = isa[0]
	else:
		try: stats_list = [[L(t.getAttr('name')),L(t.getAttr('value')),L(t.getAttr('units'))] for t in isa[1].getTag('query',namespace=xmpp.NS_STATS).getTags('stat')]
		except: stats_list = []
		if stats_list:
			stats_list = ['%s: %s' % (t[0].capitalize(),t[1]) if t[2] in t[0] else '%s: %s %s' % (t[0].capitalize(),t[1],t[2]) for t in stats_list]
			msg = L('Server statistic: %s\n%s') % (text,'\n'.join(stats_list))
		else: msg = L('Unavailable!')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'ver', iq_version, 2, L('Client version.')),
		   (3, 'ver+', iq_version_caps, 2, L('Client version with caps.')),
		   (3, 'caps', noiq_caps, 2, L('Show caps node and version of client.')),
		   (3, 'ping_old', ping, 2, L('Ping - reply time. You can ping nick in room, jid, server or transport.')),
		   (3, 'ping', urn_ping, 2, L('Ping - reply time. You can ping nick in room, jid, server or transport.')),
		   (3, 'time_old', iq_time, 2, L('Client side time.')),
		   (3, 'time', iq_utime, 2, L('Client side time.')),
		   (3, 'time_old_raw', iq_time_raw, 2, L('Client side time + raw time format.')),
		   (3, 'time_raw', iq_utime_raw, 2, L('Client side time + raw time format.')),
		   (3, 'stats', iq_stats, 2, L('Users server statistic.')),
		   (3, 'vcard_raw', iq_vcard, 2, L('vCard query. Recomends make command base alias for query needs info.\nvcard_raw [nick] - query generic info\nvcard_raw nick\nshow - show available fields\nvcard_raw nick\n[field:name|field:name] - show requested fields from vcard.')),
		   (3, 'uptime', iq_uptime, 2, L('Server or jid uptime.'))]
