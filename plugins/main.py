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

# translate: random,smart,full,partial,on,off,kick,ban,replace,mute,visitor,truncate,paste,chat,online,away,xa,dnd,on start,on shutdown,by time

rlmas_min = ((u'&','&amp;'),(u'\"','&quot;'),(u'\'','&apos;'),(u'<','&lt;'),(u'>','&gt;'))

rlmas = rlmas_min + ((u'˜\'','&tilde;'),('\t','&nbsp;'*8))

lmass = (('\n','<br>'),('\n','<br />'),('\n','<br/>'),('\n','\n\r'),('','<![CDATA['),('',']]>'),
		(u'','&shy;'),(u'','&ensp;'),(u'','&emsp;'),(u'','&thinsp;'),(u'','&zwnj;'),(u'','&zwj;'))

rmass = ((u'&','&amp;'),(u'\"','&quot;'),(u'\'','&apos;'),(u'˜\'','&tilde;'),(u' ','&nbsp;'),
		(u'<','&lt;'),(u'>','&gt;'),(u'¡','&iexcl;'),(u'¢','&cent;'),(u'£','&pound;'),
		(u'¤','&curren;'),(u'¥','&yen;'),(u'¦','&brvbar;'),(u'§','&sect;'),(u'¨','&uml;'),(u'©','&copy;'),(u'ª','&ordf;'),
		(u'«','&laquo;'),(u'¬','&not;'),(u'®','&reg;'),(u'¯','&macr;'),(u'°','&deg;'),(u'±','&plusmn;'),
		(u'²','&sup2;'),(u'³','&sup3;'),(u'´','&acute;'),(u'µ','&micro;'),(u'¶','&para;'),(u'·','&middot;'),(u'¸','&cedil;'),
		(u'¹','&sup1;'),(u'º','&ordm;'),(u'»','&raquo;'),(u'¼','&frac14;'),(u'½','&frac12;'),(u'¾','&frac34;'),(u'¿','&iquest;'),
		(u'×','&times;'),(u'÷','&divide;'),(u'À','&Agrave;'),(u'Á','&Aacute;'),(u'Â','&Acirc;'),(u'Ã','&Atilde;'),(u'Ä','&Auml;'),
		(u'Å','&Aring;'),(u'Æ','&AElig;'),(u'Ç','&Ccedil;'),(u'È','&Egrave;'),(u'É','&Eacute;'),(u'Ê','&Ecirc;'),(u'Ë','&Euml;'),
		(u'Ì','&Igrave;'),(u'Í','&Iacute;'),(u'Î','&Icirc;'),(u'Ï','&Iuml;'),(u'Ð','&ETH;'),(u'Ñ','&Ntilde;'),(u'Ò','&Ograve;'),
		(u'Ó','&Oacute;'),(u'Ô','&Ocirc;'),(u'Õ','&Otilde;'),(u'Ö','&Ouml;'),(u'Ø','&Oslash;'),(u'Ù','&Ugrave;'),(u'Ú','&Uacute;'),
		(u'Û','&Ucirc;'),(u'Ü','&Uuml;'),(u'Ý','&Yacute;'),(u'Þ','&THORN;'),(u'ß','&szlig;'),(u'à','&agrave;'),(u'á','&aacute;'),
		(u'â','&acirc;'),(u'ã','&atilde;'),(u'ä','&auml;'),(u'å','&aring;'),(u'æ','&aelig;'),(u'ç','&ccedil;'),(u'è','&egrave;'),
		(u'é','&eacute;'),(u'ê','&ecirc;'),(u'ë','&euml;'),(u'ì','&igrave;'),(u'í','&iacute;'),(u'î','&icirc;'),(u'ï','&iuml;'),
		(u'ð','&eth;'),(u'ñ','&ntilde;'),(u'ò','&ograve;'),(u'ó','&oacute;'),(u'ô','&ocirc;'),(u'õ','&otilde;'),(u'ö','&ouml;'),
		(u'ø','&oslash;'),(u'ù','&ugrave;'),(u'ú','&uacute;'),(u'û','&ucirc;'),(u'ü','&uuml;'),(u'ý','&yacute;'),(u'þ','&thorn;'),
		(u'ÿ','&yuml;'),(u'∀','&forall;'),(u'∂','&part;'),(u'∃','&exists;'),(u'∅','&empty;'),(u'∇','&nabla;'),(u'∈','&isin;'),
		(u'∉','&notin;'),(u'∋','&ni;'),(u'∏','&prod;'),(u'∑','&sum;'),(u'−','&minus;'),(u'∗','&lowast;'),(u'√','&radic;'),
		(u'∝','&prop;'),(u'∞','&infin;'),(u'∠','&ang;'),(u'∧','&and;'),(u'∨','&or;'),(u'∩','&cap;'),(u'∪','&cup;'),
		(u'∫','&int;'),(u'∴','&there4;'),(u'∼','&sim;'),(u'≅','&cong;'),(u'≈','&asymp;'),(u'≠','&ne;'),(u'≡','&equiv;'),
		(u'≤','&le;'),(u'≥','&ge;'),(u'⊂','&sub;'),(u'⊃','&sup;'),(u'⊄','&nsub;'),(u'⊆','&sube;'),(u'⊇','&supe;'),
		(u'⊕','&oplus;'),(u'⊗','&otimes;'),(u'⊥','&perp;'),(u'⋅','&sdot;'),(u'Α','&Alpha;'),(u'Β','&Beta;'),(u'Γ','&Gamma;'),
		(u'Δ','&Delta;'),(u'Ε','&Epsilon;'),(u'Ζ','&Zeta;'),(u'Η','&Eta;'),(u'Θ','&Theta;'),(u'Ι','&Iota;'),(u'Κ','&Kappa;'),
		(u'Λ','&Lambda;'),(u'Μ','&Mu;'),(u'Ν','&Nu;'),(u'Ξ','&Xi;'),(u'Ο','&Omicron;'),(u'Π','&Pi;'),(u'Ρ','&Rho;'),
		(u'Σ','&Sigma;'),(u'Τ','&Tau;'),(u'Υ','&Upsilon;'),(u'Φ','&Phi;'),(u'Χ','&Chi;'),(u'Ψ','&Psi;'),(u'Ω','&Omega;'),
		(u'α','&alpha;'),(u'β','&beta;'),(u'γ','&gamma;'),(u'δ','&delta;'),(u'ε','&epsilon;'),(u'ζ','&zeta;'),(u'η','&eta;'),
		(u'θ','&theta;'),(u'ι','&iota;'),(u'κ','&kappa;'),(u'λ','&lambda;'),(u'μ','&mu;'),(u'ν','&nu;'),(u'ξ','&xi;'),
		(u'ο','&omicron;'),(u'π','&pi;'),(u'ρ','&rho;'),(u'ς','&sigmaf;'),(u'σ','&sigma;'),(u'τ','&tau;'),(u'υ','&upsilon;'),
		(u'φ','&phi;'),(u'χ','&chi;'),(u'ψ','&psi;'),(u'ω','&omega;'),(u'ϑ','&thetasym;'),(u'ϒ','&upsih;'),(u'ϖ','&piv;'),
		(u'Œ','&OElig;'),(u'œ','&oelig;'),(u'Š','&Scaron;'),(u'š','&scaron;'),(u'Ÿ','&Yuml;'),(u'ƒ','&fnof;'),(u'ˆ','&circ;'),
		(u'‎','&lrm;'),(u'‏','&rlm;'),(u'–','&ndash;'),(u'—','&mdash;'),(u'‘','&lsquo;'),(u'’','&rsquo;'),(u'‚','&sbquo;'),
		(u'“','&ldquo;'),(u'”','&rdquo;'),(u'„','&bdquo;'),(u'†','&dagger;'),(u'‡','&Dagger;'),(u'•','&bull;'),(u'…','&hellip;'),
		(u'‰','&permil;'),(u'′','&prime;'),(u'″','&Prime;'),(u'‹','&lsaquo;'),(u'›','&rsaquo;'),(u'‾','&oline;'),(u'€','&euro;'),
		(u'™','&trade;'),(u'←','&larr;'),(u'↑','&uarr;'),(u'→','&rarr;'),(u'↓','&darr;'),(u'↔','&harr;'),(u'↵','&crarr;'),
		(u'⌈','&lceil;'),(u'⌉','&rceil;'),(u'⌊','&lfloor;'),(u'⌋','&rfloor'),(u'◊','&loz;'),(u'♠','&spades;'),(u'♣','&clubs;'),
		(u'♥','&hearts;'),(u'♦','&diams;'))

levl = {'no|limit':0,'visitor|none':1,'visitor|member':2,'participant|none':3,'participant|member':4,
		'moderator|none':5,'moderator|member':6,'moderator|admin':7,'moderator|owner':8,'bot|owner':9}

unlevl = [L('no limit'),L('visitor/none'),L('visitor/member'), L('participant/none'),L('participant/member'),
		  L('moderator/none'),L('moderator/member'),L('moderator/admin'),L('moderator/owner'),L('bot owner')]

unlevltxt = [L('You should be at least %s to do it.'),L('You must be a %s to do it.')]

unlevlnum = [0,0,0,0,0,0,0,0,0,1]

iq_error = {'bad-request':L('Bad request'),
			'conflict':L('Conflict'),
			'feature-not-implemented':L('Feature not implemented'),
			'forbidden':L('Forbidden'),
			'gone':L('Gone'),
			'internal-server-error':L('Internal server error'),
			'item-not-found':L('Item not found'),
			'jid-malformed':L('Jid malformed'),
			'not-acceptable':L('Not acceptable'),
			'not-allowed':L('Not allowed'),
			'not-authorized':L('Not authorized'),
			'payment-required':L('Payment required'),
			'recipient-unavailable':L('Recipient unavailable'),
			'redirect':L('Redirect'),
			'registration-required':L('Registration required'),
			'remote-server-not-found':L('Remote server not found'),
			'remote-server-timeout':L('Remote server timeout'),
			'resource-constraint':L('Resource constraint'),
			'service-unavailable':L('Service unavailable'),
			'subscription-required':L('Subscription required'),
			'undefined-condition':L('Undefined condition'),
			'unexpected-request':L('Unexpected request')}

wday = [L('Mon'),L('Tue'),L('Wed'),L('Thu'),L('Fri'),L('Sat'),L('Sun')]
wlight = [L('Winter time'),L('Summer time')]
wmonth = [L('Jan'),L('Fed'),L('Mar'),L('Apr'),L('May'),L('Jun'),L('Jul'),L('Aug'),L('Sep'),L('Oct'),L('Nov'),L('Dec')]

def get_xnick(jid):
	tmppos = arr_semi_find(confbase, jid)
	if tmppos == -1: nowname = Settings['nickname']
	else:
		nowname = getResourse(confbase[tmppos])
		if nowname == '': nowname = Settings['nickname']
	return nowname

def get_xtype(jid):
	nowname = get_xnick(jid)
	for base in megabase:
		if base[0].lower() == jid and base[1] == nowname:
			xtype = base[3]
			break
	return xtype

def clean_user_and_server_hash():
	global user_hash, server_hash, server_hash_list
	timing = {}
	for tmp in user_hash.keys():
		try:
			tm = user_hash[tmp]
			gr = getRoom(tmp)
			try: tmo = get_config_int(gr,'muc_filter_hash_ban_by_rejoin_timeout')
			except: tmo = 3600
			if timing.has_key(gr): tmo = timing[gr]
			else: timing[gr] = tmo
			if time.time() > tm + tmo: user_hash.pop(tmp)
		except: pass
	for tmp in server_hash_list.keys():
		tm = server_hash_list[tmp]
		gr = getRoom(tmp)
		try: tmo = get_config_int(gr,'muc_filter_hash_ban_by_rejoin_timeout')
		except: tmo = 3600
		if timing.has_key(gr): tmo = timing[gr]
		else: timing[gr] = tmo
		if time.time() > tm + tmo: server_hash_list.pop(tmp)
	for tmp in server_hash.keys():
		tm = server_hash[tmp][0]
		gr = getRoom(tmp)
		try: tmo = get_config_int(gr,'muc_filter_hash_ban_by_rejoin_timeout')
		except: tmo = 3600
		if timing.has_key(gr): tmo = timing[gr]
		else: timing[gr] = tmo
		if time.time() > tm + tmo: server_hash.pop(tmp)


def ddos_info(type, room, nick, text):
	global ddos_ignore
	text = reduce_spaces_all(text.lower()).split()
	if text == []: text = ['']
	if text[0] in ['','show']:
		tmas = []
		for tmp in ddos_ignore.keys(): tmas.append('%s/%s [%s] %s' % (ddos_ignore[tmp][0],ddos_ignore[tmp][1],tmp,un_unix(ddos_ignore[tmp][2]-time.time())))
		if tmas: msg = L('Ignore list: %s') % '; '.join(tmas)
		else: msg = L('List is empty.')
	elif text[0] in ['del','remove'] and len(text) > 1:
		if ddos_ignore.has_key(text[1]):
			try:
				ddos_ignore.pop(text[1])
				msg = L('Removed: %s') % text[1]
			except: msg = L('Not found: %s') % text[1]
		else: msg = L('Not found: %s') % text[1]
	else: msg = L('Error in parameters. Read the help about command.')
	send_msg(type, room, nick, msg)

def atempt_to_shutdown(critical):
	if not critical:
		pprint('Close age base','dark_gray')
		close_age()
	conn.commit()
	conn.close()
	kill_all_threads()
	flush_stats()

def atempt_to_shutdown_with_reason(text,sleep_time,exit_type,critical):
	pprint(text,'red')
	send_presence_all(text)
	atempt_to_shutdown(critical)
	if sleep_time: time.sleep(sleep_time)
	sys.exit(exit_type)

def deidna(text):
	def repl(t): return t.group().lower().decode('idna')
	return re.sub(r'(xn--[-0-9a-z_]*)',repl,text,flags=re.S+re.U+re.I)

def enidna(text):
	idn = re.findall(u'http[s]?://([-0-9a-zа-я._]*)',text,flags=re.S+re.U+re.I)
	if idn: text = text.replace(idn[0],idn[0].lower().encode('idna'))
	return text.encode('utf-8')

def enidna_raw(text):
	def repl(t): return t.group().lower().encode('idna')
	return re.sub(u'([а-я][-0-9а-я_]*)',repl,text,flags=re.S+re.U+re.I)

def get_level(cjid, cnick):
	access_mode = -2
	jid = 'None'
	for base in megabase:
		if base[1] == cnick and base[0].lower()==cjid:
			jid = base[4]
			if '%s|%s' % (base[2],base[3]) in levl:
				access_mode = levl['%s|%s' % (base[2],base[3])]
				break
	for iib in ignorebase:
		grj = getRoom(jid.lower())
		if iib.lower() == grj:
			access_mode = -1
			break
		if not '@' in iib and iib.lower() in grj:
			access_mode = -1
			break
	rjid = getRoom(jid)
	if rjid in ownerbase: access_mode = 9
	if jid == 'None' and cjid in ownerbase: access_mode = 9
	return (access_mode, jid)

def show_syslogs(type, jid, nick, text):
	tmp = text.strip().split(' ', 1)
	lsz, txt = 10, ''
	if len(tmp) == 1:
		try: lsz = int(tmp[0])
		except: txt = tmp[0]
	elif len(tmp) == 2:
		try: lsz, txt = int(tmp[0]), tmp[1]
		except: txt = text
	lsz += 1
	lsz = 1 if lsz <= 0 else (last_logs_size if lsz > last_logs_size else lsz)
	msg = '\n'.join([tmp for tmp in last_logs_store if txt in tmp][1:lsz][::-1])
	send_msg(type, jid, nick, L('Last syslogs: %s') % '\n%s' % msg)

def set_locale(type, jid, nick, text):
	global locales
	if len(text) >= 2:
		text = text.lower()
		if text != 'en':
			lf = loc_folder+text+'.txt'
			if os.path.isfile(lf):
				locales = {}
				lf = readfile(lf).decode('UTF').replace('\r','').split('\n')
				for c in lf:
					if '#' not in c[:3] and len(c) and '\t' in c: locales[c.split('\t',1)[0].replace('\\n','\n').replace('\\t','\t')] = c.split('\t',1)[1].replace('\\n','\n').replace('\\t','\t')
				writefile(loc_file,unicode('\''+text+'\''))
				msg = L('Locale set to: %s') % text
				CURRENT_LOCALE = text
			else: msg = L('Locale not found!')
		else:
			locales = {}
			msg = L('Locale set to: en')
			writefile(loc_file,'\'en\'')
			CURRENT_LOCALE = 'en'
	else: msg = L('Current locale: %s') % getFile(loc_file,'\'en\'')
	send_msg(type, jid, nick, msg)

def match_room(room):
	for tmp in confbase:
		if getRoom(tmp) == room: return True
	return None

def shell_execute(cmd):
	if GT('paranoia_mode'): result = L('Command temporary blocked!')
	else:
		tmp_file = '%s.tmp' % int(time.time())
		try:
			error_answ = os.system('%s > %s' % (cmd.encode('utf-8'),tmp_file))
			if not error_answ:
				try: body = readfile(tmp_file)
				except: body = L('Command execution error.')
				if len(body):
					enc = chardet.detect(body)['encoding']
					result = remove_sub_space(unicode(body,enc))
				else: result = L('ok')
			else: result = L('Command execution error.')
		except Exception, SM:
			try: SM = str(SM)
			except: SM = unicode(SM)
			result = L('I can\'t execute it! Error: %s') % SM
		try: os.remove(tmp_file)
		except: pass
	return result

def concat(list): return ''.join(list)

def get_affiliation(jid,nick):
	xtype = ''
	for base in megabase:
		if base[0].lower() == jid and base[1] == nick:
			xtype = base[3]
			break
	return xtype

def comm_on_off(type, jid, nick, text):
	cof = getFile(conoff,[])
	if len(text):
		if text[:3] == 'on ':
			text = text[3:].lower()
			if len(text):
				if (jid,text) in cof:
					if get_affiliation(jid,nick) == 'owner' or get_level(jid,nick)[0] == 9:
						cof.remove((jid,text))
						writefile(conoff, str(cof))
						msg = L('Enabled: %s') % text
					else: msg = L('Only conference owner can enable commands!')
				else: msg = L('Command %s is not disabled!') % text
			else: msg = L('What enable?')
		if text[:4] == 'off ':
			if get_affiliation(jid,nick) == 'owner' or get_level(jid,nick)[0] == 9:
				text = text[4:].lower()
				if len(text):
					text = text.split(' ')
					msg_found = ''
					msg_notfound = ''
					msg_offed = ''
					for tex in text:
						fl = 0
						if tex != 'comm':
							for cm in comms:
								if cm[1] == tex:
									fl = 1
									break
						if fl:
							if (jid,tex) not in cof:
								cof.append((jid,tex))
								writefile(conoff, str(cof))
								msg_found += tex + ', '
							else: msg_offed += tex + ', '
						else: msg_notfound += tex + ', '
					if len(msg_found): msg = L('Disabled commands: %s') % msg_found[:-2]
					else: msg = ''
					if len(msg_offed):
						if msg != '': msg += '\n'
						msg += L('Commands disabled before: %s') % msg_offed[:-2]
					if len(msg_notfound):
						if msg != '': msg += '\n'
						msg += L('Commands not found: %s') % msg_notfound[:-2]
				else: msg = L('What disable?')
			else: msg = L('Only conference owner can disable commands!')
	else:
		msg = ''
		for tmp in cof:
			if tmp[0] == jid: msg += tmp[1] + ', '
		if len(msg): msg = L('Disabled commands: %s') % msg[:-2]
		else: msg = L('Disabled commands not found!')
	send_msg(type, jid, nick, msg)

def reduce_spaces_all(text):
	text,t = text.strip(),''
	if len(text):
		for tmp in text:
			if tmp != ' ' or t[-1] != ' ': t += tmp
	return t

def status(type, jid, nick, text):
	if text == '': text = nick
	is_found = None
	for tmp in megabase:
		if tmp[0] == jid and tmp[1] == text:
			is_found = True
			break
	if is_found:
		realjid = getRoom(get_level(jid,text)[1])
		stat = cur_execute_fetchone('select message,status from age where jid=%s and room=%s and nick=%s',(realjid,jid,text))
		if stat:
			if stat[1]: msg = L('leave this room.')
			else:
				stat = stat[0].split('\n',4)
				if stat[3] != 'None': msg = stat[3]
				else: msg = 'online'
				if stat[4] != 'None': msg += ' ('+stat[4]+')'
				if stat[2] != 'None': msg += ' ['+stat[2]+'] '
				else: msg += ' [0] '
				if stat[0] != 'None' and stat[1] != 'None': msg += stat[0]+'/'+stat[1]
			if text != nick: msg = text + ' - '+msg
		else: msg = L('Not found!')
	else: msg = L('I can\'t see %s here...') % text
	send_msg(type, jid, nick, msg)

def replacer(msg):
	def repl(t): return '%s\n' % re.findall('<div.*?>(.*?)</div>',t.group(0),re.S+re.U+re.I)[0]
	msg = rss_replace(msg)
	msg = re.sub(r'(<div.*?>).*?(</div>)',repl,msg,flags=re.S+re.U+re.I)
	for tmp in [['<br/>','\n'],['<br />','\n']]: msg = msg.replace(*tmp)
	msg = rss_del_html(msg)
	msg = rss_replace(msg)
	msg = rss_del_nn(msg)
	return msg.replace('...',u'…')

def svn_info(type, jid, nick):
	if os.path.isfile(ul):
		try: msg = L('Last update:\n%s') % readfile(ul).decode('utf-8').replace('\n\n','\n')
		except: msg = L('Error!')
	else: msg = L('File %s not found!') % ul
	while msg[-1] in ['\n',' ']: msg = msg[:-1]
	if msg.count('\n') == 1: msg = msg.replace('\n',' ')
	send_msg(type, jid, nick, msg[:msg_limit])

def unhtml_raw(page,mode):
	for a in range(0,page.count('<style')):
		ttag = get_tag_full(page,'style')
		page = page.replace(ttag,'')

	for a in range(0,page.count('<script')):
		ttag = get_tag_full(page,'script')
		page = page.replace(ttag,'')

	page = rss_replace(page)
	if mode: page = replace_ltgt(page)
	else: page = rss_repl_html(page)
	page = rss_replace(page)
	page = rss_del_nn(page)
	page = page.replace('\n ','')
	return page

def unhtml(page): return unhtml_raw(page,None)

def unhtml_hard(page): return unhtml_raw(page,True)

def del_space_both(t):
	return del_space_end(del_space_begin(t))

def alias(type, jid, nick, text):
	global aliases
	aliases = getFile(alfile,[])
	text = text.strip()
	while '  ' in text: text = text.replace('  ',' ')
	mode = del_space_both(text.lower().split(' ',1)[0])
	try: cmd = del_space_both(text.split(' ',1)[1].split('=',1)[0])
	except: cmd = ''
	try: cbody = del_space_both(text.split(' ',1)[1].split('=',1)[1])
	except: cbody = ''
	msg = L('Mode %s not detected!') % mode
	if mode=='add':
		am,amm = get_level(jid,nick)[0],-1
		tcmd = cbody.split(' ',1)[0].lower()
		for tmp in comms:
			if tmp[1] == tcmd:
				amm = tmp[0]
				break
		if amm < 0: msg = L('Command not found: %s') % tcmd
		elif amm > am: msg = L('Not allowed create alias for: %s') % tcmd
		else:
			fl = 0
			for i in aliases:
				if i[1] == cmd and i[0] == jid:
					aliases.remove(i)
					fl = 1
			aliases.append([jid, cmd, cbody])
			if fl: msg = L('Updated:')
			else: msg = L('Added:')
			msg += ' '+cmd+'='+cbody
	if mode=='del':
		msg = L('Unable to remove %s') % cmd
		for i in aliases:
			if i[1] == cmd and i[0] == jid:
				am,amm = get_level(jid,nick)[0],-1
				tcmd = i[2].split(' ',1)[0].lower()
				for tmp in comms:
					if tmp[1] == tcmd:
						amm = tmp[0]
						break
				if amm > am: msg = L('Not allowed remove alias for: %s') % tcmd
				else:
					aliases.remove(i)
					msg = L('Removed: %s') % cmd
	if mode=='show':
		msg = ''
		if cmd == '':
			for i in aliases:
				if i[0] == jid: msg += i[1] + ', '
			if len(msg): msg = L('Aliases: %s') % msg[:-2]
			else: msg = L('Aliases not found!')
		else:
			for i in aliases:
				if cmd.lower() in i[1].lower() and i[0] == jid: msg += '\n'+i[1]+' = '+i[2]
			if len(msg): msg = L('Aliases: %s') % msg
			else: msg = L('Aliases not found!')
	writefile(alfile,str(aliases))
	send_msg(type, jid, nick, msg)

def fspace(mass):
	bdd = []
	for b in mass:
		if len(b) and len(b) != b.count(' '):
			while b[0] == ' ': b = b[1:]
		bdd.append(b)
	return bdd

def del_space_begin(text):
	if len(text):
		while text[:1] == ' ': text = text[1:]
	return text

def del_space_end(text):
	if len(text):
		while text[-1:] == ' ': text = text[:-1]
	return text

def un_unix(val):
	tt = map(lambda q,a: q-a, time.gmtime(val), time.gmtime(0))[:6]
	ret = '%02d:%02d:%02d' % tuple(tt[3:6])
	if sum(tt[:3]):
		day_h,day_l = tt[2]/10%10,tt[2] % 10
		if day_h == 1: ret = L('%s days %s') % (tt[2],ret)
		else:
			if day_l in [0,5,6,7,8,9]: ret = L('%s days %s') % (tt[2],ret)
			elif day_l in [2,3,4]: ret = L('%s Days %s').lower() % (tt[2],ret)
			else: ret = L('%s day %s') % (tt[2],ret)
	if sum(tt[:2]):
		if tt[1] in [0,5,6,7,8,9,10,11,12]: ret = L('%s months %s') % (tt[1],ret)
		elif tt[1] in [2,3,4]: ret = L('%s Months %s').lower() % (tt[1],ret)
		else: ret = L('%s month %s') % (tt[1],ret)
	if tt[0]:
		ty = tt[0] % 100
		if ty >= 20: ty = ty % 10
		if ty in [0]+range(5,21): ret = L('%s years %s') % (tt[0],ret)
		elif ty in [2,3,4]: ret = L('%s Years %s').lower() % (tt[0],ret)
		else: ret = L('%s year %s') % (tt[0],ret)
	return ret

def close_age_null():
	cur_execute("delete from age where jid ilike '<temporary>%'")
	ccu = cur_execute_fetchall('select * from age where status=0 order by room')
	cur_execute('delete from age where status=0')
	for ab in ccu: cur_execute('insert into age values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (ab[0],ab[1],ab[2],ab[3],ab[4],1,ab[6],ab[7],ab[1].lower()))

def close_age():
	cur_execute('delete from age where jid ilike %s',('<temporary>%',))
	ccu = cur_execute_fetchall('select * from age where status=%s order by room',(0,))
	cur_execute('delete from age where status=%s', (0,))
	tt = int(time.time())
	for ab in ccu: cur_execute('insert into age values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (ab[0],ab[1],ab[2],tt,ab[4]+(tt-ab[3]),1,ab[6],ab[7],ab[1].lower()))


def close_age_room(room):
	cur_execute('delete from age where jid ilike %s',('<temporary>%',))
	ccu = cur_execute_fetchall('select * from age where status=%s and room=%s order by room',(0,room))
	cur_execute('delete from age where status=%s and room=%s',(0,room))
	tt = int(time.time())
	for ab in ccu: cur_execute('insert into age values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (ab[0],ab[1],ab[2],tt,ab[4]+(tt-ab[3]),1,ab[6],ab[7],ab[1].lower()))


def sfind(mass,stri):
	for a in mass:
		if stri in a: return a
	return ''

def get_local_prefix(jid):
	lprefix = get_config(getRoom(jid),'prefix')
	if lprefix == None: return prefix
	return lprefix

def get_prefix(lprefix):
	if lprefix != '': return lprefix
	else: return L('absent')

def set_prefix(type, jid, nick, text):
	access_mode = get_level(jid,nick)[0]
	if access_mode >= 7:
		lprefix = get_config(getRoom(jid),'prefix')
		if text.lower() == 'none': lprefix = ''
		elif text.lower() == 'del': lprefix = prefix
		elif text != '': lprefix = text
		if lprefix == None: lprefix = prefix
		put_config(getRoom(jid),'prefix',lprefix)
		prf = get_prefix(lprefix)
	else: prf = get_prefix(get_local_prefix(jid))
	send_msg(type, jid, nick, L('Command prefix: %s') % prf)

def uptime(type, jid, nick): send_msg(type, jid, nick, L('Uptime: %s, Last session: %s') % (get_uptime_str(), un_unix(int(time.time())-sesstime)))

def show_error(type, jid, nick, text):
	if text.lower() == 'clear': writefile(LOG_FILENAME,'')
	try: cmd = int(text)
	except: cmd = 1
	if os.path.isfile(LOG_FILENAME) and text.lower() != 'clear':
		log = readfile(LOG_FILENAME).decode('UTF')
		log = log.split('ERROR:')
		lll = len(log)
		if cmd > lll: cmd = lll
		msg = L('Total Error(s): %s\n') % str(lll-1)
		if text != '':
			for aa in range(lll-cmd,lll): msg += log[aa]+'\n'
		else: msg += ' '
		msg = msg[:-2]
	else: msg = L('No Errors')
	send_msg(type, jid, nick, msg)

def get_nick_by_jid(room, jid):
	for tmp in megabase:
		if tmp[0] == room and getRoom(tmp[4]) == jid: return tmp[1]
	return None

def get_nick_by_jid_res(room, jid):
	for tmp in megabase:
		if tmp[0] == room and tmp[4] == jid: return tmp[1]
	return None

def info_whois(type, jid, nick, text):
	if text != '': msg = raw_who(jid, text)
	else: msg = L('What?')
	send_msg(type, jid, nick, msg)

def info_access(type, jid, nick):
	msg = raw_who(jid, nick)
	send_msg(type, jid, nick, msg)

def raw_who(room,nick):
	access_mode = get_level(room,nick)[0]
	if access_mode == -2: msg = L('Who do you need?')
	else:
		realjid = get_level(room,nick)[1]
		msg = L('Access level: %s') % access_mode
		msg += ', ' + [L('Ignored'),L('Minimal'),L('Visitor'),L('Visitor and Member'),L('Participant'),L('Member'), L('Moderator'),L('Moderator and member'),L('Admin'),L('Owner'),L('Bot\'s owner')][access_mode+1]
		if realjid != 'None':
			msg = L('%s, jid detected') % msg
			if ddos_ignore.has_key(getRoom(realjid)): msg = '%s, %s' % (msg,L('temporary ignored (%s)') % un_unix(ddos_ignore[getRoom(realjid)][2]-time.time()))
	return msg

def info_comm(type, jid, nick):
	global comms
	msg = ''
	ta = get_level(jid,nick)
	access_mode = ta[0]
	tmp = sqlite3.connect(':memory:')
	cu = tmp.cursor()
	cu.execute('''create table tempo (comm text, am integer)''')
	for i in comms:
		if access_mode >= i[0]: cu.execute('insert into tempo values (?,?)', (unicode(i[1]),i[0]))
	for j in range(0,access_mode+1):
		cm = cu.execute('select * from tempo where am=? order by comm',(j,)).fetchall()
		if cm:
			msg += u'\n• '+str(j)+u' … '
			for i in cm: msg += i[0] +', '
			msg = msg[:-2]
	msg = L('Total commands: %s | Prefix: %s | Your access level: %s | Available commands: %s%s') % (str(len(comms)), get_prefix(get_local_prefix(jid)), str(access_mode), str(len(cu.execute('select * from tempo where am<=?',(access_mode,)).fetchall())), msg)
	tmp.close()
	send_msg(type, jid, nick, msg)

def helpme(type, jid, nick, text):
	text = text.strip().lower()
	if text == 'about': msg = u'Isida Jabber Bot | © 2oo9-%s Disabler Production Lab. | http://isida-bot.com' % str(time.localtime()[0]).replace('0','o')
	elif text in ['donation','donations']: msg = L('Send donation to: %sBest regards, %s') % ('\nYandexMoney: 41001384336826\nWMZ: Z392970180590\nWMR: R378494692310\nWME: E164241657651\n','Disabler')
	elif text in [L('access'),'access']: msg = L('Bot has next access levels:\n-1 - ignored\n0 - minimal access\n1 - at least visitor and none\n2 - at least visitor and member\n3 - at least participant and none\n4 - at least participant and member\n5 - at least moderator and none\n6 - at least moderator and member\n7 - at least moderator and admin\n8 - at least moderator and owner\n9 - bot owner')
	elif len(text) > 1:
		tm,cm = [],[]
		for tmp in comms:
			if tmp[1] == text:
				cm = (tmp[1],tmp[0],tmp[4])
				break
			elif text in tmp[1].lower() or text in tmp[4].lower(): tm.append((tmp[0], tmp[1], tmp[4]))
		if cm: msg = '%s. ' % cm[0].capitalize() + L('Access level: %s. %s') % (cm[1],cm[2])
		elif len(tm) == 1: msg = '%s. ' % tm[0][1].capitalize() + L('Access level: %s. %s') % (tm[0][0],tm[0][2])
		elif not len(tm+cm): msg = L('"%s" not found') % text
		else:
			tm.sort()
			msg = L('Prefix: %s, Available help for commands:\n') % get_prefix(get_local_prefix(jid))
			for i in range(0,10):
				tmsg = []
				for tmp in tm:
					if tmp[0] == i and tmp[2] != '': tmsg.append(unicode(tmp[1]))
				if len(tmsg): msg += u'[%s]…%s\n' % (i,', '.join(tmsg))
	else: msg = L('%s Help for command: help command | Commands list: commands') % (u'Isida Jabber Bot | http://isida-bot.com | © 2oo9-'+str(time.localtime()[0]).replace('0','o')+' Disabler Production Lab. | ')
	send_msg(type, jid, nick, msg)

def bot_rejoin(type, jid, nick, text):
	global lastserver, lastnick, confbase
	text=unicode(text)
	domain = getServer(Settings['jid'])
	if len(text): text=unicode(text)
	else: text=jid
	if '\n' in text: text, passwd = text.split('\n', 1)
	else: passwd = ''
	if '@' not in text: text+='@'+lastserver
	if '/' not in text: text+='/'+lastnick
	old_text = '%s\n%s' % (text,passwd)
	lastserver = getServer(text.lower())
	lastnick = getResourse(text)
	lroom = text
	if arr_semi_find(confbase, getRoom(lroom)) >= 0:
		sm = L('Rejoin by %s') % nick
		leaveconf(text, domain, sm)
		time.sleep(1)
		zz = joinconf(text, domain, passwd)
		while unicode(zz)[:3] == '409':
			time.sleep(1)
			text += '_'
			zz = joinconf(text, domain, passwd)
		time.sleep(1)
		if zz != None: send_msg(type, jid, nick, L('Error! %s') % zz)
		else:
			confbase = remove_by_half(confbase, getRoom(lroom))
			confbase.append(old_text)
			writefile(confs,json.dumps(confbase))
	else: send_msg(type, jid, nick, L('I have never been in %s') % getRoom(lroom))

def remove_by_half(cb,rm):
	for tmp in cb:
		if tmp[:len(rm)] == rm:
			cb.remove(tmp)
			break
	return cb

def bot_join(type, jid, nick, text):
	global lastserver, lastnick, confs, confbase, blacklist_base
	text = unicode(text)
	domain = getServer(Settings['jid'])
	blklist = getFile(blacklist_base, [])
	if not text or ' ' in getRoom(text): send_msg(type, jid, nick, L('Wrong arguments!'))
	else:
		if '\n' in text: text, passwd = text.split('\n', 1)
		else: passwd = ''
		if '@' not in text: text += '@%s' % lastserver
		if '/' not in text: text += '/%s' % lastnick
		old_text = '%s\n%s' % (text, passwd) if passwd else text
		if getRoom(text) in blklist: send_msg(type, jid, nick, L('Denied!'))
		else:
			lastserver = getServer(text.lower())
			lastnick = getResourse(text)
			lroom = text.lower().split('/')[0]
			if arr_semi_find(confbase, lroom) == -1:
				zz = joinconf(text, domain, passwd)
				while unicode(zz)[:3] == '409':
					time.sleep(1)
					text += '_'
					zz = joinconf(text, domain, passwd)
				if zz != None: send_msg(type, jid, nick, L('Error! %s') % zz)
				else:
					confbase.append(old_text)
					writefile(confs, json.dumps(confbase))
					send_msg(type, jid, nick, L('Joined to %s') % text)
			elif text in confbase: send_msg(type, jid, nick, L('I\'m already in %s with nick %s') % (lroom, lastnick))
			else:
				zz = joinconf(text, domain, passwd)
				while unicode(zz)[:3] == '409':
					time.sleep(0.1)
					text += '_'
					zz = joinconf(text, domain, passwd)
				if zz != None: send_msg(type, jid, nick, L('Error! %s') % zz)
				else:
					confbase = remove_by_half(confbase, lroom)
					confbase.append(old_text)
					#time.sleep(1)
					#send_msg(type, jid, nick, L('Changed nick in %s to %s') % (lroom,getResourse(text)))
					writefile(confs, json.dumps(confbase))

def bot_leave(type, jid, nick, text):
	global confs, confbase, lastserver, lastnick
	domain = getServer(Settings['jid'])
	if len(confbase) == 1: send_msg(type, jid, nick, L('I can\'t leave last room!'))
	else:
		if text == '': text = jid
		if '@' not in text: text+='@'+lastserver
		if '/' not in text: text+='/'+lastnick
		if '\n' in text: text, _ = text.split('\n', 1)
		lastserver = getServer(text)
		lastnick = getResourse(text)
		if len(text): text=unicode(text)
		else: text=jid
		lroom = text
		if getRoom(jid) in ownerbase: nick = getName(jid)
		if arr_semi_find(confbase, getRoom(lroom)) >= 0:
			confbase = arr_del_semi_find(confbase,getRoom(lroom))
			writefile(confs,json.dumps(confbase))
			send_msg(type, jid, nick, L('Leave room %s') % text)
			sm = L('Leave room by %s') % nick
			leaveconf(getRoom(text), domain, sm)
			hr = getFile(hide_conf,[])
			if getRoom(text) in hr:
				hr.remove(getRoom(text))
				writefile(hide_conf,str(hr))
		else: send_msg(type, jid, nick, L('I have never been in %s') % lroom)

def conf_limit(type, jid, nick, text):
	global msg_limit
	if text!='':
		try: msg_limit = int(text)
		except: msg_limit = default_msg_limit
	send_msg(type, jid, nick, L('Temporary message size limit %s') % str(msg_limit))

def bot_plugin(type, jid, nick, text):
	global plname, plugins, execute, gtimer, gpresence, gmassage
	text = text.split()
	opt = text[0]
	try: name = '%s.py' % text[1]
	except: name = ''
	msg = L('Wrong arguments!')
	pl_ignore = getFile(pliname,[])

	if opt == 'add' and os.path.isfile(pl_folder % name):
		if name in pl_ignore:
			pl_ignore.remove(name)
			writefile(pliname,str(pl_ignore))
		if name not in plugins: plugins.append(name)
		presence_control,message_control,message_act_control,iq_control,timer,execute = [],[],[],[],[],[]
		execfile(pl_folder % name)
		tmsg = ''
		for cm in execute:
			tmsg += '%s[%s], ' % (cm[1],cm[0])
			comms.append((cm[0],cm[1],cm[2],cm[3],L('Plugin %s. %s') % (name[:-3],cm[4])))
		msg = L('Loaded plugin: %s') % name[:-3]
		if tmsg: msg += L('\nAdd commands: %s') % tmsg[:-2]
		for tmr in timer: gtimer.append(tmr)
		for tmp in presence_control: gpresence.append(tmp)
		for tmp in message_control: gmessage.append(tmp)
		for tmp in message_act_control: gactmessage.append(tmp)

	elif opt == 'del' and name in plugins:
		if name not in pl_ignore:
			pl_ignore.append(name)
			writefile(pliname,str(pl_ignore))
		plugins.remove(name)
		presence_control,message_control,message_act_control,iq_control,timer,execute = [],[],[],[],[],[]
		execfile(pl_folder % name)
		tmsg = ''
		for cm in execute:
			tmsg += '%s[%s], ' % (cm[1],cm[0])
			for i in comms:
				if i[1] == cm[1]: comms.remove(i)
		msg = L('Unloaded plugin: %s') % name[:-3]
		if tmsg: msg += L('\nDel commands: %s') % tmsg[:-2]
		for tmr in timer: gtimer.remove(tmr)
		for tmp in presence_control: gpresence.remove(tmp)
		for tmp in message_control: gmessage.remove(tmp)
		for tmp in message_act_control: gactmessage.remove(tmp)

	elif opt == 'local':
		a = os.listdir(pl_folder % '')
		b = []
		for c in a:
			if c[-3:] == '.py' and c[0] != '.' and c != 'main.py': b.append(c[:-3].decode('utf-8'))
		msg = L('Available plugins: %s') % ', '.join(b)
		if len(pl_ignore):
			b = []
			for tmp in pl_ignore: b.append(tmp[:-3])
			msg += L('\nIgnored plugins: %s') % ', '.join(b)

	elif opt == 'show':
		msg = ''
		for jjid in plugins: msg += jjid[:-3]+', '
		msg = L('Active plugins: %s') % msg[:-2]
		if len(pl_ignore):
			b = []
			for tmp in pl_ignore: b.append(tmp[:-3])
			msg += L('\nIgnored plugins: %s') % ', '.join(b)

	plugins.sort()
	send_msg(type, jid, nick, msg)

def owner(type, jid, nick, text):
	global ownerbase, owners, god
	text = text.lower().strip()
	do = text.split(' ',1)[0]
	try: nnick = text.split(' ',1)[1].lower()
	except:
		if do != 'show':
			send_msg(type, jid, nick, L('Wrong arguments!'))
			return
	if do == 'add':
		if nnick not in ownerbase:
			if '@' in nnick:
				ownerbase.append(nnick)
				j = Presence(nnick, 'subscribed')
				j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
				sender(j)
				j = Presence(nnick, 'subscribe')
				j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
				sender(j)
				msg = L('Append: %s') % nnick
			else: msg = L('Wrong jid!')
		else: msg = L('%s is alredy in list!') % nnick
	elif do == 'del':
		if nnick in ownerbase and nnick != god:
			ownerbase.remove(nnick)
			j = Presence(nnick, 'unsubscribe')
			j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
			sender(j)
			j = Presence(nnick, 'unsubscribed')
			j.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
			sender(j)
			msg = L('Removed: %s') % nnick
		else: msg = L('Not found!')
	elif do == 'show':
		msg = ''
		for jjid in ownerbase: msg += jjid+', '
		msg = L('Bot owner(s): %s') % msg[:-2]
	else: msg = L('Wrong arguments!')
	writefile(owners,str(ownerbase))
	send_msg(type, jid, nick, msg)

def ignore(type, jid, nick, text):
	global ignorebase, ignores, god
	text = text.lower().strip()
	do = text.split(' ',1)[0]
	try: nnick = text.split(' ',1)[1].lower()
	except:
		if do != 'show':
			send_msg(type, jid, nick, L('Wrong arguments!'))
			return
	if do == 'add':
		if nnick not in ignorebase:
			ignorebase.append(nnick)
			if '@' in nnick: msg = L('Append: %s') % nnick
			else: msg = L('Append: %s') % '*'+nnick+'*'
		else: msg = L('%s alredy in list!') % nnick
	elif do == 'del':
		if nnick in ignorebase and nnick != god:
			ignorebase.remove(nnick)
			if '@' in nnick: msg = L('Removed: %s') % nnick
			else: msg = L('Removed: %s') % '*'+nnick+'*'
		else: msg = L('Not found!')
	elif do == 'show':
		msg = ''
		for jjid in ignorebase:
			if '@' in jjid: msg += jjid+', '
			else: msg += '*'+jjid+'*, '
		msg = L('Ignore list: %s') % msg[:-2]
	else: msg = L('Wrong arguments!')
	writefile(ignores,str(ignorebase))
	send_msg(type, jid, nick, msg)

def info_where(type, jid, nick):
	global confbase
	msg = L('Active conference(s): %s') % str(len(confbase))
	wbase = []
	for jjid in confbase:
		cnt = 0
		rjid = getRoom(jjid)
		for mega in megabase:
			if mega[0] == rjid: cnt += 1
		wbase.append((cnt, jjid))
	wbase.sort(reverse=True)
	nmb,hr_count = 1,0
	hr = getFile(hide_conf,[])
	for i in wbase:
		if getRoom(i[1]) in hr: hr_count += 1
		else:
			msg += '\n%s. %s [%s]' % (nmb,i[1].split('\n')[0],i[0])
			nmb += 1
	if hr_count: msg += L('\nHidden conference(s): %s') % str(hr_count)
	send_msg(type, jid, nick, msg)

def info_where_plus(type, jid, nick):
	global confbase
	msg = L('Active conference(s): %s') % str(len(confbase))
	wbase = []
	for jjid in confbase:
		cnt,rjid,ra = 0,getRoom(jjid),L('unknown')
		for mega in megabase:
			if mega[0] == rjid:
				cnt += 1
				if mega[0]+'/'+mega[1] == jjid: ra = L(mega[2]+'/'+mega[3])
		wbase.append((cnt, jjid, ra))
	wbase.sort(reverse=True)
	nmb,hr_count = 1,0
	hr = getFile(hide_conf,[])
	for i in wbase:
		if getRoom(i[1]) in hr: hr_count += 1
		else:
			msg += '\n%s. %s (%s) [%s]' % (nmb,i[1].split('\n')[0],i[2],i[0])
			nmb += 1
	if hr_count: msg += L('\nHidden conference(s): %s') % str(hr_count)
	send_msg(type, jid, nick, msg)


def get_uptime_str():
	return un_unix(int(time.time()-starttime))

def info(type, jid, nick):
	global confbase
	msg = L('Conference(s): %s (for more info use \'where\' command)\n') % str(len(confbase))
	msg += L('Server: %s | Nick: %s\n') % (lastserver,lastnick)
	msg += L('Message size limit: %s\n') % str(msg_limit)
	msg += L('Local time: %s\n') % timeadd(tuple(time.localtime()))
	msg += L('Uptime: %s, Last session: %s') % (get_uptime_str(), un_unix(int(time.time())-sesstime))
	floods = get_config(getRoom(jid),'flood')
	censors = get_config(getRoom(jid),'censor')
	msg += L('\nFlood: %s | Censor: %s | Prefix: %s') % (onoff(floods),onoff(censors),get_prefix(get_local_prefix(jid)))
	msg += L('\nExecuted threads: %s | Error(s): %s') % (th_cnt,thread_error_count)
	msg += L('\nMessage in: %s | out: %s') % (message_in,message_out)
	msg += L('\nPresence in: %s | out: %s') % (presence_in,presence_out)
	msg += L('\nIq in: %s | out: %s') % (iq_in,iq_out)
	msg += L('\nUnknown out: %s') % unknown_out
	msg += L('\nCycles used: %s | unused: %s') % (cycles_used,cycles_unused)
	send_msg(type, jid, nick, msg)

# 0 - конфа
# 1 - ник
# 2 - роль
# 3 - аффиляция
# 4 - jid

def info_base(type, jid, nick):
	msg = L('What need find?')
	if nick != '':
		msg = ''
		fl = 1
		for base in megabase:
			if base[1] == (nick) and base[0].lower() == jid:
				msg = L('I see you as %s/%s') % (base[2],base[3])
				break
	send_msg(type, jid, nick, msg)

def real_search_owner(type, jid, nick, text):
	msg = L('What need find?')
	if text != '':
		msg = L('Found:')
		fl = 1
		for mega1 in megabase:
			if mega1[2] != 'None' and mega1[3] != 'None':
				for mega2 in mega1:
					if text.lower() in mega2.lower():
						msg += u'\n'+unicode(mega1[1])+u' is '+unicode(mega1[2])+u'/'+unicode(mega1[3])
						if mega1[4] != 'None': msg += u' ('+unicode(mega1[4])+u')'
						msg += ' '+unicode(mega1[0])
						fl = 0
						break
		if fl: msg = L('\'%s\' not found!') % text
	send_msg(type, jid, nick, msg)

def real_search(type, jid, nick, text):
	msg = L('What do you need to find?')
	if text != '':
		msg = L('Found:')
		fl = 1
		for mega1 in megabase:
			if mega1[2] != 'None' and mega1[3] != 'None':
				for mega2 in mega1:
					if text.lower() in mega2.lower():
						msg += u'\n'+unicode(mega1[1])+u' - '+unicode(mega1[2])+u'/'+unicode(mega1[3])+ ' '+unicode(mega1[0])
						fl = 0
						break
		if fl: msg = L('\'%s\' not found!') % text
	send_msg(type, jid, nick, msg)

def isNumber(text):
	try:
		it = int(text,16)
		if it >= 32 and it <= 127: return chr(int(text,16))
		else: return '?'
	except: return 'None'

def unescape(text):
	def fixup(m):
		text = m.group(0)
		if text[:2] == '&#':
			try:
				if text[:3] == '&#x': return unichr(int(text[3:-1], 16))
				else: return unichr(int(text[2:-1]))
			except ValueError: pass
		else:
			try: text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
			except KeyError: pass
		return text
	return re.sub('&#?\w+;', fixup, text)

def html_escape(text):
	def link(text): return '<a href="%s">%s</a>' % (text.group(0),text.group(0))
	#def email(text): return '<a href="mailto:%s">%s</a>' % (text.group(0),text.group(0))
	def brnbsp(text): return '<br>' + '&nbsp;' * len(text.group(0))
	def nbsp(text): return '&nbsp;' * len(text.group(0))
	for tmp in ((u'&','&amp;'),(u'<','&lt;'),(u'>','&gt;'),(u'˜\'','&tilde;'),('\t','&nbsp;'*8)): text = text.replace(tmp[0],tmp[1])
	text = re.sub(u'^(\ +)',nbsp,text)
	text = re.sub(u'http[s]?://[-a-zA-Z0-9а-яА-Я._/?&#=;@%:()+]+',link,text)
	#text = re.sub(u'[-a-zA-Z._0-9?:а-яА-Я]+@[-a-zA-Z._0-9а-яА-Я/?:]+',email,text)
	text = text.replace('\n','<br>')
	text = re.sub(u'<br>\ +',brnbsp,text)
	#for tmp in ((u'\"','&quot;'),(u'\'','&apos;')): text = text.replace(tmp[0],tmp[1])
	return text

def esc_max2(ms):
	for tmp in rlmas_min: ms = ms.replace(tmp[0],tmp[1])
	return ms

def esc_min2(ms):
	for tmp in rlmas_min: ms = ms.replace(tmp[1],tmp[0])
	return ms

def esc_max(ms):
	for tmp in rmass: ms = ms.replace(tmp[0],tmp[1])
	return ms

def esc_min(ms):
	for tmp in rmass: ms = ms.replace(tmp[1],tmp[0])
	return ms

def rss_replace(ms):
	for tmp in lmass: ms = ms.replace(tmp[1],tmp[0])
	return unescape(esc_min(ms))

def rss_repl_del_html(ms,item):
	DS,SP,T = '<%s>','/%s',re.findall('<(.*?)>', ms, re.S)
	if len(T):
		for tmp in T:
			if (tmp[:3] == '!--' and tmp[-2:] == '--') or tmp[-1:] == '/':
				pattern = DS % tmp
				pos = ms.find(pattern)
				ms = ms[:pos] + item + ms[pos+len(pattern):]
	T = re.findall('<(.*?)>', ms, re.S)
	if len(T):
		for tmp in range(0,len(T)-1):
			pos = None
			TT = T[tmp].split(' ')[0]
			if TT and TT[0] != '/':
				try: pos = T.index(SP % TT,tmp)
				except: pass
				if pos:
					pat1,pat2 = DS % T[tmp],DS % T[pos]
					pos1 = ms.find(pat1)
					pos2 = ms.find(pat2,pos1)
					ms = ms[:pos1] + item + ms[pos1+len(pat1):pos2] + item + ms[pos2+len(pat2):]
	for tmp in ('hr','br','li','ul','img','dt','dd','p'):
		T = re.findall('<%s.*?>' % tmp, ms, re.S)
		for tmp1 in T: ms = ms.replace(tmp1,item,1)
	return ms

def rss_repl_html(ms): return rss_repl_del_html(ms,' ')

def rss_del_html(ms): return rss_repl_del_html(ms,'')

def remove_replace_ltgt(text,item):
	T = re.findall('<.*?>', text, re.S)
	for tmp in T: text = text.replace(tmp,item,1)
	return text

def remove_ltgt(text): return remove_replace_ltgt(text,'')

def replace_ltgt(text): return remove_replace_ltgt(text,' ')

def rss_del_nn(ms):
	ms = ms.replace('\r',' ').replace('\t',' ')
	while '\n ' in ms: ms = ms.replace('\n ','\n')
	while len(ms) and (ms[0] == '\n' or ms[0] == ' '): ms = ms[1:]
	while '\n\n' in ms: ms = ms.replace('\n\n','\n')
	while '  ' in ms: ms = ms.replace('  ',' ')
	while u'\n\n•' in ms: ms = ms.replace(u'\n\n•',u'\n•')
	while u'• \n' in ms: ms = ms.replace(u'• \n',u'• ')
	return ms.strip()

def html_encode(body):
	encidx = re.findall('encoding=["\'&]*(.*?)["\'& ]{1}',body[:1024])
	if encidx: enc = encidx[0]
	else:
		encidx = re.findall('charset=["\'&]*(.*?)["\'& ]{1}',body[:1024])
		if encidx: enc = encidx[0]
		else: enc = chardet.detect(body)['encoding']
	if body == None: body = ''
	if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
	if enc == 'ISO-8859-2':
		tx,splitter = '','|'
		while splitter in body: splitter += '|'
		tbody = body.replace('</','<'+splitter+'/').split(splitter)
		cntr = 0
		for tmp in tbody:
			try:
				enc = chardet.detect(tmp)['encoding']
				if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
				tx += unicode(tmp,enc)
			except:
				ttext = ''
				for tmp2 in tmp:
					if (tmp2<='~'): ttext+=tmp2
					else: ttext+='?'
				tx += ttext
			cntr += 1
		return tx
	else:
		try: return smart_encode(body,enc)
		except: return L('Encoding error!')

#[room, nick, role, affiliation, jid]

def rss_flush(jid,link,break_point):
	global feedbase, feeds
	tstop = []
	feedbase = getFile(feeds,[])
	for tmp in feedbase:
		if tmp[4] == jid and tmp[0] == link:
			try: tstop = tmp[5]
			except: pass
			feedbase.remove(tmp)
			if not break_point: break_point = tstop
			feedbase.append([tmp[0], tmp[1], tmp[2], int(time.time()), tmp[4], break_point])
			writefile(feeds,str(feedbase))
			break
	return tstop

def smart_concat(text):
	#while ' \n' in text: text = text.replace(' \n','\n')
	#while '\n ' in text: text = text.replace('\n ','\n')
	text = [' ']+text.split('\n')
	tmp = 1
	while tmp < len(text):
		if not (' ' in text[tmp] or '/' in text[tmp] or '.' in text[tmp] or '\\' in text[tmp]): text = text[:tmp-1]+[text[tmp-1]+' '+text[tmp]]+text[tmp+1:]
		else: tmp += 1
	return '\n'.join(text)

def rss(type, jid, nick, text):
	global feedbase, feeds,	lastfeeds
	msg = u'rss show|add|del|clear|new|get'
	nosend = None
	text = text.split(' ')
	tl = len(text)
	if tl < 5: text.append('!')
	mode = text[0].lower() # show | add | del | clear | new | get
	if mode == 'add' and tl < 4: msg,mode = 'rss add [http://]url timeH|M [full|body|head][-url]',''
	elif mode == 'del' and tl < 2: msg,mode = 'rss del [http://]url',''
	elif mode == 'new' and tl < 4: msg,mode = 'rss new [http://]url max_feed_humber [full|body|head][-url]',''
	elif mode == 'get' and tl < 4: msg,mode = 'rss get [http://]url max_feed_humber [full|body|head][-url]',''
	#lastfeeds = getFile(lafeeds,[])
	if mode == 'clear':
		if get_level(jid,nick)[0] == 9 and tl > 1: tjid = text[1]
		else: tjid = jid
		feedbase = getFile(feeds,[])
		msg, tf = L('All RSS was cleared!'), []
		for taa in feedbase:
			if taa[4] != tjid: tf.append(taa)
		feedbase = tf
		writefile(feeds,str(feedbase))
	elif mode == 'all':
		feedbase = getFile(feeds,[])
		msg = L('No RSS found!')
		if feedbase != []:
			msg = L('All schedule feeds:')
			for rs in feedbase:
				msg += '\n%s\t%s (%s) %s' % (getName(rs[4]),rs[0],rs[1],rs[2])
				try: msg += ' - %s' % disp_time(rs[3])
				except: msg += ' - Unknown'
	elif mode == 'show':
		feedbase = getFile(feeds,[])
		msg = L('No RSS found!')
		if feedbase != []:
			msg = ''
			for rs in feedbase:
				if rs[4] == jid:
					msg += '\n%s (%s) %s' % tuple(rs[0:3])
					try: msg += u' - %s' % disp_time(rs[3])
					except: msg += u' - Unknown'
			if len(msg): msg = L('Schedule feeds for %s:%s') % (jid,msg)
			else: msg = L('Schedule feeds for %s not found!') % jid
	elif mode == 'add':
		mdd = ['full','body','head']
		if text[3].split('-')[0] not in mdd:
			send_msg(type, jid, nick, L('Mode %s not detected!') % text[3])
			return
		feedbase = getFile(feeds,[])
		link = text[1]
		if '://' not in link[:10]: link = 'http://'+link
		for dd in feedbase:
			if dd[0] == link and dd[4] == jid:
				feedbase.remove(dd)
				break
		timetype = text[2][-1:].lower()
		if not timetype in ('h','m'): timetype = 'h'
		try: ofset = int(text[2][:-1])
		except: ofset = 4
		if timetype == 'm' and ofset < GT('rss_min_time_limit'): timetype = '%sm' % GT('rss_min_time_limit')
		else: timetype = str(ofset)+timetype
		feedbase.append([link, timetype, text[3], int(time.time()), getRoom(jid),[]]) # url time mode
		writefile(feeds,str(feedbase))
		msg = L('Add feed to schedule: %s (%s) %s') % (link,timetype,text[3])
		rss(type, jid, nick, 'get %s 1 %s' % (link,text[3]))
	elif mode == 'del':
		feedbase = getFile(feeds,[])
		link = text[1]
		if '://' not in link[:10]: link = 'http://'+link
		msg = L('Can\'t find in schedule: %s') % link
		for rs in feedbase:
			if rs[0] == link and rs[4] == jid:
				feedbase.remove(rs)
				msg = L('Delete feed from schedule: %s') % link
				writefile(feeds,str(feedbase))
				break
	elif mode == 'new' or mode == 'get':
		link = text[1]
		if '://' not in link[:10]: link = 'http://'+link
		try:
			req = urllib2.Request(link.encode('utf-8'))
			req.add_header('User-Agent',GT('user_agent'))
			feed = urllib2.urlopen(url=req,timeout=GT('rss_get_timeout')).read(GT('size_overflow'))
		except: feed = L('Unable to access server!')
		is_rss_aton,fc = 0,feed[:256]
		if '<?xml version=' in fc:
			if '<feed' in fc:
				is_rss_aton = 2
				t_feed = feed.split('<title>')
				feed = t_feed[0]
				for tmp in t_feed[1:]:
					tm = tmp.split('</title>',1)
					if ord(tm[0][-1]) == 208: tm[0] = tm[0][:-1] + '...'
					feed += '<title>%s</title>%s' % tuple(tm)
			elif '<rss' in fc or '<rdf' in fc: is_rss_aton = 1
			feed = html_encode(feed)
			feed = re.sub(u'(<span.*?>.*?</span>)','',feed)
			feed = re.sub(u'(<div.*?>)','',feed)
			feed = re.sub(u'(</div>)','',feed)
		if is_rss_aton and feed != L('Encoding error!') and feed != L('Unable to access server!'):
			if is_rss_aton == 1:
				if '<item>' in feed: fd = feed.split('<item>')
				else: fd = feed.split('<item ')
				feed = [fd[0]]
				for tmp in fd[1:]: feed.append(tmp.split('</item>')[0])
			else:
				if '<entry>' in feed: fd = feed.split('<entry>')
				else: fd = feed.split('<entry ')
				feed = [fd[0]]
				for tmp in fd[1:]: feed.append(tmp.split('</entry>')[0])
			if len(text) > 2 and text[2].isdigit(): lng = int(text[2])
			else: lng = len(feed)-1
			if len(feed)-1 <= lng: lng = len(feed)-1
			if lng > GT('rss_max_feed_limit'): lng = GT('rss_max_feed_limit')
			elif len < 1: lng = 1
			if len(text) > 3: submode = text[3]
			else: submode = 'full'
			msg = L('Feeds for')+' '
			if 'url' in submode.split('-'): submode,urlmode = submode.split('-')[0],True
			else:
				urlmode = None
				msg += link+' '
			msg += get_tag(feed[0],'title')
			try:
				break_point = []
				for tmp in feed[1:GT('rss_max_feed_limit')+1]:
					ttitle = get_tag(tmp,'title').replace('&lt;br&gt;','\n')
					break_point.append(hashlib.md5(ttitle.encode('utf-8')).hexdigest())
				tstop = rss_flush(jid,link,break_point)
				t_msg, new_count = [], 0
				for mmsg in feed[1:GT('rss_max_feed_limit')+1]:
					ttitle = get_tag(mmsg,'title').replace('&lt;br&gt;','\n')
					if mode == 'get' or not (hashlib.md5(ttitle.encode('utf-8')).hexdigest() in tstop):
						if is_rss_aton == 1: tbody,turl = get_tag(mmsg,'description').replace('&lt;br&gt;','\n'),get_tag(mmsg,'link')
						else:
							tbody = get_tag(mmsg,'content').replace('&lt;br&gt;','\n')
							try:
								tu1 = mmsg.find('href=\"',mmsg.index('<link'))+6
								tu2 = mmsg.find('\"',tu1)
								turl = mmsg[tu1:tu2].replace('&lt;br&gt;','\n')
							except: turl = 'URL %s' % L('Not found!')
						tsubj,tmsg,tlink = '','',''
						if submode == 'full': tsubj,tmsg = replacer(ttitle),replacer(tbody)
						elif submode == 'body': tmsg = replacer(tbody)
						elif submode == 'head': tsubj = replacer(ttitle)
						else: return
						if urlmode: tlink = urllib.unquote(turl.encode('utf8')).decode('utf8','ignore')
						t_msg.append((tsubj.replace('\n','; '),smart_concat(tmsg),tlink))
						new_count += 1
						if new_count >= lng: break
				if new_count:
					t_msg.reverse()
					tmp = ''
					for tm in t_msg: tmp += '!'.join(tm)
					if len(tmp+msg)+len(t_msg)*12 >= msg_limit:
						over = 100 * msg_limit / (len(tmp+msg)+len(t_msg)*12.0) # overflow in persent
						tt_msg = []
						for tm in t_msg:
							tsubj,tmsg,tlink = tm
							cut = int(len(tsubj+tmsg+tlink)/100*over)
							if cut < len(tlink): tsubj,tmsg,tlink = tsubj[:cut]+u'[]','',''
							elif cut < len(tsubj+tlink): tsubj,tmsg = tsubj[:cut-len(tlink)]+u'[…]',''
							else: tmsg = tmsg[:cut-len(tlink+tsubj)]+u'[…]'
							tt_msg.append((tsubj,tmsg,tlink))
						t_msg = tt_msg
					tmp = ''
					for tm in t_msg:
						if submode == 'full': tmp += u'\n• %s\n%s' % tm[0:2]
						elif submode == 'body': tmp += u'\n• %s' % tm[1]
						elif submode == 'head': tmp += u'\n• %s' % tm[0]
						if len(tm[2]): tmp += '\n'+tm[2]
					msg = unhtml(msg+tmp)
				elif mode == 'new':
					if text[4] == 'silent': nosend = True
					else: msg = L('New feeds not found!')
			except Exception,SM:
				rss_flush(jid,link,None)
				if text[4] == 'silent': nosend = True
				else: msg = L('Error! %s') % SM
		else:
			rss_flush(jid,link,None)
			if text[4] == 'silent': nosend = True
			else:
				if feed in [L('Encoding error!'),L('Unable to access server!')]: title = feed
				else: title = html_encode(get_tag(feed,'title'))
				msg = L('Bad url or rss/atom not found at %s - %s') % (link,title)
	if not nosend: send_msg(type, jid, nick, msg)

def configure(type, jid, nick, text):
	text = text.lower().replace('\n',' ').replace('\r',' ').replace('\t',' ')
	while '  ' in text: text = text.replace('  ',' ')
	text = text.split(' ',1)
	to_conf = text[0]
	try: param = text[1]
	except: param = ''
	if to_conf in ['show','item','items','it','sh']:
		if param in ['status','info','st']:
			tmp = config_prefs.keys()
			tmp.sort()
			msg = ''
			for t in tmp: msg += u'\n[%s] - ' % t + config_prefs[t][0] % onoff(get_config(getRoom(jid),t))
			msg = L('Current status: %s') % msg
		elif param in config_prefs: msg = config_prefs[param][0] % onoff(get_config(getRoom(jid),param))
		else:
			tmp = config_prefs.keys()
			tmp.sort()
			msg = L('Available items: %s') % ', '.join(tmp)
	elif to_conf == 'help' or to_conf == '':
		if param in config_prefs: msg = config_prefs[param][1]
		elif param == '':
			tmp = config_prefs.keys()
			tmp.sort()
			msg = L('Available items: %s') % ', '.join(tmp)
		else: msg = L('Help for %s not found!') % param
	elif to_conf in config_prefs:
		if param.lower() in ['show','item','items','it','sh']:
			msg = ''
			if config_prefs[to_conf][2]:
				for tmp in config_prefs[to_conf][2]: msg += ['%s (%s), ' % (onoff_no_tr(tmp),onoff(tmp)),'%s, ' % onoff_no_tr(tmp)][onoff_no_tr(tmp) == onoff(tmp)]
			else: msg += L('text field') + '  '
			msg = L('Available items: %s') % msg[:-2]
		elif param == '': msg = config_prefs[to_conf][0] % onoff(get_config(getRoom(jid),to_conf))
		else:
			if not config_prefs[to_conf][2]: ssta = param
			else:
				ssta = get_config(getRoom(jid),to_conf)
				if (param.lower() in [L('on'),'on','true']) and not param in config_prefs[to_conf][2]: param = True
				elif (param.lower() in [L('off'),'off','false','none']) and not param in config_prefs[to_conf][2]: param = False
				else: param = param.lower()
				if param in config_prefs[to_conf][2]: ssta = param
				else: ssta = ''
			if len(str(ssta)):
				put_config(getRoom(jid),to_conf,ssta)
				msg = config_prefs[to_conf][0] % onoff(ssta)
			else: msg = L('Unknown item!')
	else: msg = L('Unknown item!')
	send_msg(type, jid, nick, msg)

def muc_filter_lock(type, jid, nick, text):
	realjid = getRoom(get_level(jid,nick)[1])
	tmp = cur_execute_fetchall('select * from muc_lock where room=%s and jid=%s', (jid,realjid))
	if text in ['on','off']:
		if tmp: cur_execute('delete from muc_lock where room=%s and jid=%s', (jid,realjid))
		if text == 'on':
			cur_execute('insert into muc_lock values (%s,%s)', (jid, realjid))
			st = L('on')
		else: st = L('off')
	elif tmp: st = L('on')
	else: st = L('off')
	msg = L('Ignore messages from unaffiliated participants in private - %s') % st
	send_msg(type, jid, nick, msg)

def get_opener(page_name, parameters=None):
	socket.setdefaulttimeout(GT('rss_get_timeout'))
	try:
		proxy_support = urllib2.ProxyHandler({'http' : 'http://%(user)s:%(password)s@%(host)s:%(port)d' % http_proxy})
		opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
		urllib2.install_opener(opener)
	except: opener = urllib2.build_opener(urllib2.HTTPHandler)
	opener.addheaders = [('User-agent', GT('user_agent'))]
	if parameters: page_name += urllib.urlencode(parameters)
	try: data, result = opener.open(page_name), True
	except Exception, SM:
		try: SM = str(SM)
		except: SM = unicode(SM)
		data, result = L('Error! %s') % SM.replace('>','').replace('<','').capitalize(), False
	return data, result

def load_page(page_name, parameters=None):
	data, result = get_opener(page_name, parameters)
	if result: return data.read(GT('size_overflow'))
	else: return data

config_prefs = {'url_title': [L('Url title is %s'), L('Automatic show title of urls in conference'), [True,False], False],
				'content_length': [L('Content length %s'), L('Automatic show lenght of content in conference'), [True,False], False],
				'censor': [L('Censor is %s'), L('Censor'), [True,False], False],
				#'censor_message': [L('Censor message is %s'), L('Censor message'), None, censor_text],
				'censor_warning': [L('Censor warning is %s'), L('Warning for moderators and higher') ,[True,False], False],
				'censor_action_member': [L('Censor action for member is %s'), L('Censor action for member'), ['off','visitor','kick','ban'], 'off'],
				'censor_action_non_member': [L('Censor action for non member is %s'), L('Censor action for non member'), ['off','visitor','kick','ban'], 'off'],
				'censor_custom': [L('Custom censor is %s'), L('Custom censor'), [True,False], False],
				'censor_custom_rules': [L('Custom rules for censor is %s'), L('Custom rules for censor'), None, '\n'],
				'parse_define': [L('Parse define is %s'), L('Automatic parse definition via google'), ['off','full','partial'], 'off'],
				'clear_answer':[L('Clear notification by %s'),L('Clear notification by presence or message'), ['presence','message'],'presence'],
				'smiles':[L('Smiles in logs is %s'), L('Smiles in logs'), ['off'] + smiles_dirs, 'off'],
				'autoturn': [L('Autoturn layout of text is %s'), L('Turn text from one layout to another.'), [True,False], False],
				'make_stanza_jid_count':[L('Jid\'s per stanza for affiliations in backup is %s'),L('Count of jid\'s per stanza for affiliations change in backup'),None,'100'],
				'acl_multiaction': [L('ACL multiaction is %s'), L('Execute more than one action per pass in ACL.'), [True,False], False],

				# MUC-Filter messages

				'muc_filter': [L('Muc filter is %s'), L('Message filter for participants'), [True,False], False],
				'muc_filter_newbie': [L('Mute newbie %s'), L('Mute all messages from newbie'), [True,False], False],
				'muc_filter_newbie_time': [L('Mute newbie time %s'), L('Time of mute all messages from newbie'), None, '60'],
				'muc_filter_adblock': [L('Adblock muc filter is %s'), L('Adblock filter'), ['off','visitor','kick','ban','replace','mute'], 'off'],
				'muc_filter_repeat': [L('Repeat muc filter is %s'), L('Repeat same messages filter'), ['off','visitor','kick','ban','mute'], 'off'],
				'muc_filter_match': [L('Match muc filter is %s'), L('Repeat text in message filter'), ['off','visitor','kick','ban','mute'], 'off'],
				'muc_filter_large': [L('Large muc filter is %s'), L('Large message filter'), ['off','visitor','kick','ban','paste','truncate','mute'], 'off'],
				'muc_filter_censor': [L('Censor muc filter is %s'), L('Censor filter'), ['off','visitor','kick','ban','replace','mute'], 'off'],
				'muc_filter_adblock_raw': [L('Raw adblock muc filter is %s'), L('Raw adblock filter'), ['off','visitor','kick','ban','mute'], 'off'],
				'muc_filter_censor_raw': [L('Raw censor muc filter is %s'), L('Raw censor filter'), ['off','visitor','kick','ban','mute'], 'off'],
				'muc_filter_raw_percent': [L('Persent of short words for raw actions is %s'), L('Persent of short words for raw actions'), None, '40'],
				'muc_filter_reduce_spaces_msg': [L('Reduce spaces in message %s'), L('Reduce duplicates of spaces in message'), [True,False], False],

				# MUC-Filter presence

				'muc_filter_adblock_prs': [L('Adblock muc filter for presence is %s'), L('Adblock filter for presence'), ['off','kick','ban','replace','mute'], 'off'],
				'muc_filter_rejoin': [L('Repeat join muc filter is %s'), L('Repeat join muc filter'), [True,False], False],
				'muc_filter_whitelist': [L('Whitelist is %s'), L('Whitelist via muc filter'), [True,False], False],
				'muc_filter_blacklist': [L('Blacklist is %s'), L('Blacklist via muc filter'), [True,False], False],
				'muc_filter_blacklist_rules_jid': [L('Blacklist rules for jid\'s %s'), L('Jid\'s rules for blacklist via muc filter.'), None, ''],
				'muc_filter_blacklist_rules_nick': [L('Blacklist rules for nick\'s %s'), L('Nick\'s rules for blacklist via muc filter.'), None, ''],
				'muc_filter_newline': [L('New line in presence muc filter is %s'), L('New line muc filter'), ['off','kick','ban','mute','replace'], 'off'],
				'muc_filter_newline_count': [L('New line count in presence muc filter is %s'), L('Count of new line muc filter'), None, '2'],
				'muc_filter_newline_msg': [L('New line in message muc filter is %s'), L('New line muc filter'), ['off','kick','ban','mute','replace'], 'off'],
				'muc_filter_newline_msg_count': [L('New line count in message muc filter is %s'), L('Count of new line muc filter'), None, '2'],
				'muc_filter_repeat_prs': [L('Repeat presence muc filter is %s'), L('Repeat presence muc filter'), ['off','kick','ban','mute'], 'off'],
				'muc_filter_large_nick': [L('Large nick muc filter is %s'), L('Large nick muc filter'), ['off','visitor','kick','ban','truncate','mute'], 'off'],
				'muc_filter_large_status': [L('Large status muc filter is %s'), L('Large status muc filter'), ['off','visitor','kick','ban','truncate','mute'], 'off'],
				'muc_filter_censor_prs': [L('Censor muc filter for presence is %s'), L('Censor muc filter for presence'), ['off','kick','ban','replace','mute'], 'off'],
				'muc_filter_deny_hash': [L('Deny by hash %s'), L('Lock joins via hash'), [True,False], False],
				'muc_filter_deny_hash_list': [L('Deny hashes list %s'), L('Hashes list for lock joins'), None, ''],
				'muc_filter_hash': [L('Hash. Check activity %s'), L('Actions by hash activity'), [True,False], False],
				'muc_filter_hash_ban_by_rejoin': [L('Hash. Ban if hash activity %s'), L('Actions for ban by hash activity'), [True,False], True],
				'muc_filter_hash_ban_by_rejoin_timeout': [L('Hash. Timeout for clean hash activity %s'), L('Time period for clean hash activity'), None, '600'],
				'muc_filter_hash_ban_server_by_rejoin': [L('Hash. Ban server by hash activity %s'), L('Ban server by hash activity'), [True,False], True],
				'muc_filter_hash_ban_server_by_rejoin_exception': [L('Hash. Exception for ban servers %s'), L('Exception for ban servers'), None, ''],
				'muc_filter_hash_ban_server_by_rejoin_notify_jid': [L('Hash. Jid\'s for servers ban notify %s'), L('Jid\'s for servers ban notify'), None, ''],
				'muc_filter_hash_ban_server_by_rejoin_rejoins': [L('Hash. Count of rejoins from server for ban %s'), L('Count of rejoins from server for ban'), None, '5'],
				'muc_filter_hash_ban_server_by_rejoin_timeout': [L('Hash. Timeout of rejoins from server for ban %s'), L('Timeout of rejoins from server for ban'), None, '60'],
				'muc_filter_hash_time': [L('Hash. Time for events %s'), L('Time period for events'), None, '20'],
				'muc_filter_hash_events': [L('Hash. Events count %s'), L('Events count per time period'), None, '10'],
				'muc_filter_hash_action': [L('Hash. Action type %s'), L('Type of action'), ['whitelist','lock by hash'], 'whitelist'],
				'muc_filter_hash_action_time': [L('Hash. Time to disable action %s'), L('Time to disable action'), None, '1800'],
				'muc_filter_hash_action_current': [L('Hash. Action for already joined %s'), L('Action for already joined'), ['off','kick','ban'], 'off'],
				'muc_filter_censor_prs_raw': [L('Raw censor muc filter for presence is %s'), L('Raw censor muc filter for presence'), ['off','kick','ban','mute'], 'off'],
				'muc_filter_adblock_prs_raw': [L('Raw adblock muc filter for presence is %s'), L('Raw adblock filter for presence'), ['off','kick','ban','mute'], 'off'],
				'muc_filter_reduce_spaces_prs': [L('Reduce spaces in presence %s'), L('Reduce duplicates of spaces in presence'), [True,False], False],

				# Bomb

				'bomb': [L('Bomb. Allow take a bomb %s'), L('Allow take a bomb in current conference'), [True,False], True],
				'bomb_fault': [L('Bomb. Allow random unexplosive bombs %s'), L('Allow some times take unexplosive bombs'), [True,False], True],
				'bomb_fault_persent': [L('Bomb. Persent of fault bombs %s'), L('Persent of fault bombs'), None, '25'],
				'bomb_random': [L('Bomb. Allow bot take a bomb to random user %s'), L('Allow bot take a bomb to random user'), [True,False], False],
				'bomb_random_active': [L('Bomb. Allow random bombs only in active room %s'), L('Allow random bombs only in active room'), [True,False], True],
				'bomb_random_active_timer': [L('Bomb. Time for detect room as unactive %s'), L('Time for detect room as unactive'), None, '1200'],
				'bomb_random_timer': [L('Bomb. Time between random bombs %s'), L('Time between random bombs'), None, '1800'],
				'bomb_random_timer_persent': [L('Bomb. Persent of mistakes for time between random bombs %s'), L('Persent of mistakes for time between random bombs'), None, '25'],
				'bomb_random_timer_skip_persent': [L('Bomb. Persent of skiped random bombs %s'), L('Persent of mistakes skiped random bombs'), None, '25'],
				'bomb_timer': [L('Bomb. Timer is %s'), L('Time to deactivate a bomb'), None, '45'],
				'bomb_wire': [L('Bomb. Wire count is %s'), L('Wire count for bomb'), None, '4'],
				'bomb_action': [L('Bomb. Action for bomb explode %s'), L('Type of action for bomb explode'), ['off','kick'], 'kick'],
				'bomb_action_level': [L('Bomb. Don\'t use action when access level lower than or equal %s'), L('Ignore bomb action depends from access level'), ['4','5','6','7','8','9'], '4'],
				'bomb_reason': [L('Bomb. Reason %s'), L('Reason for bomb explode'), None, L('KA-BO-OM!!!111')],
				'bomb_idle': [L('Bomb. Idle for unable get the bomb %s'), L('Idle for unable get the bomb'), None, '900'],

				# Karma actions

				'karma_action': [L('Karma. Actions for karma change is %s'), L('Allow change role/affiliation by karma change'), [True,False], False],
				'karma_action_reason': [L('Karma. Reason for actions by karma change is %s'), L('Reason for change role/affiliation by karma change'), None, L('by karma change!')],
				'karma_action_1ban': [L('Karma. Ban when karma is lower than %s'), L('Ban when karma is lower than defined value'), None, '-50'],
				'karma_action_2kick': [L('Karma. Kick when karma is lower than %s'), L('Kick when karma is lower than defined value'), None, '-20'],
				'karma_action_3visitor': [L('Karma. Revoke voice when karma is lower than %s'), L('Revoke voice when karma is lower than defined value'), None, '-10'],
				'karma_action_4none': [L('Karma. None affiliation when karma is lower than %s'), L('Revoke affiliation when karma is lower than defined value'), None, '-5'],
				'karma_action_5participant': [L('Karma. Participant affiliation when karma is higher than %s'), L('Give a participant affiliation when karma is higher than defined value'), None, '5'],
				'karma_action_6member': [L('Karma. Member affiliation when karma is higher than %s'), L('Give a member affiliation when karma is higher than defined value'), None, '20'],
				'karma_action_7moderator': [L('Karma. Moderator role when karma is higher than %s'), L('Give a moderator role when karma is higher than defined value'), None, '50'],
				'karma_hard': [L('Hard rule for karma is %s'), L('Not allow any symbols between nick and karma digit') ,[True,False], False],
				'karma_limit': [L('Limits for karma change is %s'), L('Limitation of karma\'s change. Depends of access level') ,[True,False], True],
				'karma_limit_size': [L('Value of limits for karma change %s'), L('Value of limitation of karma\'s change. Depends of access level') ,None, '[3,5]'],

				# Flood
				'flood': [L('Flood is %s'), L('Autoanswer'), ['off','random','smart'], 'off'],
				'autoflood': [L('Autoflood is %s'), L('Autoflood'), [True,False], False],
				'floodcount': [L('Number of message for autoflood\'s start: %s'), L('Number of message for autoflood\'s start'), None, '3'],
				'floodtime': [L('Time period for autoflood\'s start: %s'), L('Time period for autoflood\'s start'), None, '1800']

				}

config_group_other = [L('Other settings'),'#room-other',
				['url_title','parse_define','clear_answer','smiles','autoturn','make_stanza_jid_count','content_length','acl_multiaction'],None]

config_group_censor = [L('Censor settings'),'#room-censor',
				['censor','censor_warning','censor_action_member','censor_action_non_member',
				'censor_custom','censor_custom_rules'],None]

config_group_mucfilter = [L('General Muc-filter settings'),'#room-mucfilter',
				['muc_filter'],None]

config_group_mucfilter_newbie = [L('Muc-filter settings for newbie'),'#room-mucfilter-newbie',
				['muc_filter_newbie','muc_filter_newbie_time'],None]

config_group_mucfilter_hash = [L('Muc-filter settings for hash'),'#room-mucfilter-hash',
				['muc_filter_hash','muc_filter_hash_time','muc_filter_hash_events','muc_filter_hash_action','muc_filter_hash_action_time',
				'muc_filter_hash_action_current','muc_filter_deny_hash','muc_filter_deny_hash_list','muc_filter_hash_ban_server_by_rejoin',
				'muc_filter_hash_ban_server_by_rejoin_exception','muc_filter_hash_ban_server_by_rejoin_notify_jid',
				'muc_filter_hash_ban_server_by_rejoin_rejoins','muc_filter_hash_ban_server_by_rejoin_timeout','muc_filter_hash_ban_by_rejoin',
				'muc_filter_hash_ban_by_rejoin_timeout'],None]

config_group_mucfilter_content = [L('Muc-filter settings by content'),'#room-mucfilter-content',
				['muc_filter_newline','muc_filter_newline_count','muc_filter_newline_msg_count','muc_filter_newline_msg',
				'muc_filter_large','muc_filter_repeat','muc_filter_match','muc_filter_reduce_spaces_msg','muc_filter_reduce_spaces_prs',
				'muc_filter_rejoin','muc_filter_repeat_prs','muc_filter_large_nick','muc_filter_large_status'],None]

config_group_mucfilter_raw = [L('Muc-filter settings for raw-actions'),'#room-mucfilter-raw',
				['muc_filter_adblock_raw','muc_filter_adblock_prs_raw',
				'muc_filter_censor_raw','muc_filter_censor_prs_raw','muc_filter_raw_percent'],None]

config_group_mucfilter_censor = [L('Muc-filter settings for censor/ad-block'),'#room-mucfilter-censor',
				['muc_filter_adblock_prs','muc_filter_adblock','muc_filter_censor','muc_filter_censor_prs'],None]

config_group_mucfilter_lists = [L('Muc-filter settings for while/black lists'),'#room-mucfilter-lists',
				['muc_filter_whitelist','muc_filter_blacklist','muc_filter_blacklist_rules_jid','muc_filter_blacklist_rules_nick'],None]

config_group_bomb = [L('Settings for bomb-joke'),'#room-bombjoke',
				['bomb','bomb_fault','bomb_fault_persent','bomb_random','bomb_random_timer',
				'bomb_timer','bomb_wire','bomb_action','bomb_action_level','bomb_reason','bomb_random_active',
				'bomb_random_active_timer','bomb_random_timer_persent',
				'bomb_random_timer_skip_persent','bomb_idle'],None]

config_group_karma = [L('Actions for karma change'),'#room-karma-action',
				['karma_action','karma_action_1ban','karma_action_2kick','karma_action_3visitor',
				'karma_action_4none','karma_action_5participant','karma_action_6member','karma_action_7moderator','karma_hard',
				'karma_limit','karma_limit_size'],None]

config_group_flood = [L('Flood settings'),'#room-flood',
				['flood','autoflood','floodcount','floodtime'],None]

config_groups = [config_group_mucfilter,config_group_mucfilter_newbie,config_group_mucfilter_hash,config_group_mucfilter_content,
				config_group_mucfilter_raw,config_group_mucfilter_censor,config_group_mucfilter_lists,config_group_other,config_group_bomb,
				config_group_karma,config_group_censor,config_group_flood]

# type:
# b - binary (true\false)
# i - integer
# f - float
# tXX - text[:XX]
# mXX - multiline text[:XX]
# lXX - len(list) == XX
# d - droplist
# XXe - execute latest field by eval

owner_prefs = {'syslogs_enable': [L('Logger. Enable system logs'),'b',True],
				'status_logs_enable':[L('Logger. Enable status change logging'),'b',True],
				'aff_role_logs_enable':[L('Logger. Enable role and affiliation logging'),'b',True],
				'html_logs_enable':[L('Logger. Html logs. Otherwize in text'),'b',True],
				'html_logs_end_text':[L('Logger. Additional text for logs'),'m512',''],
				'karma_limit':[L('Karma. Minimal karma for allow krama change for participants'),'i',5],
				'karma_show_default_limit':[L('Karma. Default length of list karma top+/-'),'i',10],
				'karma_show_max_limit':[L('Karma. Maximal length of list karma top+/-'),'i',20],
				'watch_size':[L('Watcher. Frequency of requests in watcher'),'i',900],
				'user_agent':[L('Www. User-agent for web queries'),'m256','Mozilla/5.0 (X11; U; Linux x86_64; ru; rv:1.9.0.4) Gecko/2008120916 Gentoo Firefox/3.0.4'],
				'size_overflow':[L('Www. Limit of page in bytes for www command'),'i',262144],
				'youtube_max_videos':[L('Youtube. Maximal links number'),'i',10],
				'youtube_default_videos':[L('Youtube. Default links number'),'i',3],
				'youtube_max_page_size':[L('Youtube. Page size limit'),'i',131072],
				'youtube_default_lang':[L('Youtube. Default language'),'t2','ru'],
				'age_default_limit':[L('Age. Default number of users for age commands'),'i',10],
				'age_max_limit':[L('Age. Maximal number of users for age commands'),'i',100],
				'anek_private_limit':[L('Anek. Anekdote size for private send'),'i',500],
				'troll_default_limit':[L('Troll. Default message number for troll command'),'i',10],
				'troll_max_limit':[L('Troll. Maximal message number for troll command'),'i',100],
				'troll_sleep_time':[L('Troll. Delay between messages for troll command'),'f',0.05],
				'backup_sleep_time':[L('Backup. Requests delay for backup command'),'f',0.1],
				'calendar_default_splitter':[L('Calendar. Default splitter for calendar'),'t10','_'],
				'clear_delay':[L('Clear. Delay between massages in clear command'),'f',1.3],
				'clear_default_count':[L('Clear. Default message number for clear command'),'i',20],
				'clear_max_count':[L('Clear. Maximal message number for clear command'),'i',100],
				'ping_digits':[L('Iq. Number after point in ping'),'i',3],
				'lfm_api':[L('LastFM. Api for lastfm plugin'),'t64','no api'],
				'lastfm_max_limit':[L('LastFM. Number of answers for lastfm plugin'),'i',10],
				'reboot_time':[L('Kernel. Restart timeout for error at bot initial (no connection, auth error)'),'i',180],
				'timeout':[L('Iq. Timeout for iq queries'),'i',600],
				'schedule_time':[L('Kernel. Schedule time'),'i',10],
				'sayto_timeout':[L('Sayto. Age of message in sayto before delete it from base with undelivered'),'i',1209600],
				'sayto_cleanup_time':[L('Sayto. Timeout for sayto base cleanup'),'i',86400],
				'scan_time':[L('Spy. Time for spy scan'),'i',1800],
				'spy_action_time':[L('Spy. Time for reaction on spy scan'),'i',86400],
				'rss_max_feed_limit':[L('Rss. Maximum rss count'),'i',10],
				'rss_min_time_limit':[L('Rss. Minimal time for rss check in minutes'),'i',10],
				'rss_get_timeout':[L('Rss. Timeout for rss request from server in seconds'),'i',15],
				'whereis_time_dec':[L('Whereis. Frequency for answer check for whereis command'),'f',0.5],
				'watcher_room_activity':[L('Watcher. Try rejoin in rooms with low activity'),'b',True],
				'watcher_self_ping':[L('Watcher. Allow self ping'),'b',True],
				'disco_max_limit':[L('Disco. Maximus andwers count for disco command'),'i',10],
				'juick_user_post_limit':[L('Juick. Number of posts'),'i',10],
				'juick_user_post_size':[L('Juick. Number of symbols in post'),'i',50],
				'juick_msg_answers_default':[L('Juick. Number of answers'),'i',10],
				'juick_user_tags_limit':[L('Juick. Number of tags'),'i',10],
				'iq_time_enable':[L('Iq. Allow answer to time request'),'b',True],
				'iq_uptime_enable':[L('Iq. Allow answer to uptime request'),'b',True],
				'iq_version_enable':[L('Iq. Allow answer to version request'),'b',True],
				'iq_disco_enable':[L('Iq. Allow answer to service discovery'),'b',True],
				'iq_ping_enable':[L('Iq. Allow answer to ping'),'b',True],
				'paranoia_mode':[L('Kernel. Paranoic mode. Disable all execute possibles on bot'),'b',False],
				'show_loading_by_status':[L('Kernel. Bot status. Show different status for bot loading'),'b',True],
				'show_loading_by_status_show':[L('Kernel. Bot status. Status while loading'),'d','dnd',['chat','online','away','xa','dnd']],
				'show_loading_by_status_message':[L('Kernel. Bot status. Message while loading'),'t256',L('Loading...')],
				'show_loading_by_status_percent':[L('Kernel. Bot status. Show percent of loading'),'b',True],
				'show_loading_by_status_room':[L('Kernel. Bot status. Show join to room while loading'),'b',True],
				'kick_ban_notify':[L('Kernel. Notify when bot is kicked or banned'),'b',True],
				'kick_ban_notify_jid':[L('Kernel. Notify jid for bot kick or ban'),'t1024',''],
				'watch_activity_timeout':[L('Watcher. Timeout for no actions in room for rejoin'),'i',1800],
				'muc_filter_large_message_size':[L('Muc-filter. Message size for filter'),'i',512],
				'muc_filter_match_count':[L('Muc-filter. A kind words count'),'i',3],
				'muc_filter_match_warning_match':[L('Muc-filter. Number of kind parts in message'),'i',3],
				'muc_filter_match_warning_space':[L('Muc-filter. Number of empty parts in message'),'i',5],
				'muc_filter_match_view':[L('Muc-filter. Message limit'),'i',512],
				'muc_filter_match_warning_nn':[L('Muc-filter. Number of empty new lines'),'i',3],
				'muc_filter_rejoin_count':[L('Muc-filter. Number of reconnects for monitoring'),'i',3],
				'muc_filter_rejoin_timeout':[L('Muc-filter. Time for reconnect count'),'i',120],
				'muc_filter_status_count':[L('Muc-filter. Number of precences per time'),'i',3],
				'muc_filter_status_timeout':[L('Muc-filter. Time between presences'),'i',600],
				'muc_filter_large_status_size':[L('Muc-filter. Maximux status-message size'),'i',50],
				'muc_filter_large_nick_size':[L('Muc-filter. Maximum nick size'),'i',20],
				'muc_filter_repeat_count':[L('Muc-filter. Repeat count'),'i',3],
				'muc_filter_repeat_time': [L('Muc-filter. Timeout for repeat message'), 'i', 3600],
				'html_paste_enable':[L('Paste. Paste as html. Otherwize as text'),'b',True],
				'yandex_api_key':[L('City. Yandex.Map API-key'),'t128','no api'],
				'bing_api_key':[L('Bing. Translator API-key'),'t128','no api'],
				'new_year_text':[L('NewYear. Congratulations text'),'t256',L('Happy New Year!')],
				'censor_text':[L('Kernel. Text for hide censore'),'t32','[censored]'],
				'ddos_limit':[L('Kernel. Time of ignore for anti-ddos'),'l10','[1800,1800,1800,1800,1800,600,300,150,60,0]'],
				'ddos_diff':[L('Kernel. Anti-ddos time delay between messages'),'l10','[30,30,30,30,20,20,15,10,5,0]'],
				'ddos_iq_requests':[L('Kernel. Iq anti-ddos. Requests number'),'i',30],
				'ddos_iq_limit':[L('Kernel. Iq anti-ddos. Time limits for requests'),'i',10],
				'amsg_limit_size':[L('Msgtoadmin. Size limit for msgtoadmin'),'i',1024],
				'amsg_limit':[L('Msgtoadmin. Time limit for next message for msgtoadmin'),'l10','[86400,86400,86400,86400,86400,86400,43200,3600,1800,60]'],
				'karma_timeout':[L('Karma. Time for karma change from access level'),'l10','[86400,86400,86400,86400,86400,86400,43200,3600,1800,5]'],
				'karma_discret':[L('Karma. Difference between two action in karma'),'i',5],
				'karma_discret_lim_up':[L('Karma. Upper value of karma for control action'),'i',100],
				'karma_discret_lim_dn':[L('Karma. Lower value of karma for control action'),'i',-100],
				'disco_exclude':[L('Disco. Exclude from disco by regexps'),'m256e',u'([؀-ݭ)\n(ﭐ-ﻼ])\n(syria|arab)','disco_exclude_update()'],
				'exclude_messages':[L('Kernel. Exclude symbols from bot\'s messages'),'m256e',u'([؀-ۿ])\n([ݐ-ݿ])\n([ﭐ-﷿])\n([ﹰ-﻿])','message_exclude_update()'],
				}

owner_group_mucfilter = [L('Muc-filter settings'),'#owner-mucfilter',
				['muc_filter_large_message_size','muc_filter_match_count','muc_filter_match_warning_match',
				'muc_filter_match_warning_space','muc_filter_match_view','muc_filter_match_warning_nn',
				'muc_filter_rejoin_count','muc_filter_rejoin_timeout','muc_filter_status_count',
				'muc_filter_status_timeout','muc_filter_large_status_size','muc_filter_large_nick_size',
				'muc_filter_repeat_count','muc_filter_repeat_time']]

owner_group_iq = [L('Iq requests settings'),'#owner-iq',
				['iq_time_enable','iq_uptime_enable','iq_version_enable','iq_disco_enable',
				'iq_ping_enable','ping_digits','timeout']]

owner_group_juick = [L('Juick settings'),'#owner-juick',
				['juick_user_post_limit','juick_user_post_size','juick_msg_answers_default','juick_user_tags_limit']]

owner_group_logs = [L('Logs settings'),'#owner-logs',
				['syslogs_enable','status_logs_enable','aff_role_logs_enable','html_logs_enable','html_logs_end_text']]

owner_group_youtube = [L('Youtube settings'),'#owner-youtube',
				['youtube_max_videos','youtube_default_videos','youtube_max_page_size','youtube_default_lang']]

owner_group_other = [L('Other settings'),'#owner-other',
				['anek_private_limit','backup_sleep_time','calendar_default_splitter',
				'disco_max_limit','disco_exclude','html_paste_enable','yandex_api_key','bing_api_key',
				'new_year_text']]

owner_group_karma = [L('Karma settings'),'#owner-karma',
				['karma_limit','karma_show_default_limit','karma_show_max_limit','karma_timeout','karma_discret','karma_discret_lim_up','karma_discret_lim_dn']]

owner_group_www = [L('WWW settings'),'#owner-www',
				['size_overflow','user_agent']]

owner_group_troll = [L('Antitroll settings'),'#owner-troll',
				['troll_default_limit','troll_max_limit','troll_sleep_time']]

owner_group_kernel = [L('Kernel settings'),'#owner-kernel',
				['censor_text','ddos_limit','ddos_diff','paranoia_mode','reboot_time','schedule_time',
				'show_loading_by_status','show_loading_by_status_show','show_loading_by_status_message',
				'show_loading_by_status_percent','kick_ban_notify','kick_ban_notify_jid',
				'ddos_iq_requests','ddos_iq_limit','exclude_messages']]

owner_group_lastfm = [L('LastFM settings'),'#owner-lastfm',
				['lfm_api','lastfm_max_limit']]

owner_group_whereis = [L('Whereis settings'),'#owner-whereis',
				['whereis_time_dec']]

owner_group_watcher = [L('Watcher settings'),'#owner-watcher',
				['watch_size','watcher_room_activity','watch_activity_timeout','watcher_self_ping']]

owner_group_clear = [L('Clear settings'),'#owner-clear',
				['clear_delay','clear_default_count','clear_max_count']]

owner_group_rss = [L('RSS settings'),'#owner-rss',
				['rss_max_feed_limit','rss_min_time_limit','rss_get_timeout']]

owner_group_amsg = [L('Message for admin settings'),'#owner-amsg',
				['amsg_limit_size','amsg_limit']]

owner_group_age = [L('Age settings'),'#owner-age',
				['age_default_limit','age_max_limit']]

owner_group_sayto = [L('Sayto settings'),'#owner-sayto',
				['sayto_timeout','sayto_cleanup_time']]

owner_group_spy = [L('Spy settings'),'#owner-spy',
				['scan_time','spy_action_time']]

owner_groups = [owner_group_amsg,owner_group_rss,owner_group_clear,
				owner_group_kernel,owner_group_lastfm,owner_group_whereis,
				owner_group_watcher,owner_group_troll,owner_group_www,
				owner_group_karma,owner_group_sayto,owner_group_age,
				owner_group_mucfilter,owner_group_iq,owner_group_juick,
				owner_group_logs,owner_group_youtube,owner_group_other]

comms = [
	 (0, 'help', helpme, 2, L('Help system. Helps without commands: about, donation, access')),
	 (9, 'join', bot_join, 2, L('Join conference.\njoin room[@conference.server.ru[/nick]]\n[password]')),
	 (9, 'leave', bot_leave, 2, L('Leave conference.\nleave room[@conference.server.ru[/nick]]')),
	 (9, 'rejoin', bot_rejoin, 2, L('Rejoin conference.\nrejoin room[@conference.server.ru[/nick]]\n[password]')),
	 (9, 'bot_owner', owner, 2, L('Bot owners list.\nbot_owner show\nbot_owner add|del jid')),
	 (9, 'bot_ignore', ignore, 2, L('Black list.\nbot_ignore show\nbot_ignore add|del jid')),
	 (9, 'syslogs', show_syslogs, 2, L('Show bot\'s syslogs.\nsyslogs [number of records] [text]')),
	 (6, 'where', info_where, 1, L('Show conferences.')),
	 (6, 'where+', info_where_plus, 1, L('Show conferences.')),
	 (0, 'inbase', info_base, 1, L('Your identification in global base.')),
	 (9, 'look', real_search, 2, L('Search user in conferences where the bot is.')),
	 (9, 'glook', real_search_owner, 2, L('Search user in conferences where the bot is. Also show jid\'s')),
	 (7, 'rss', rss, 2, L('News:\nrss show - show current.\nrss add url time mode - add news.\nrss del url - remove news.\nrss get url feeds mode - get current news.\nrss new url feeds mode - get unread news only.\nrss clear - clear all news in current conference.\nrss all - show all news in all conferences.\n\nurl - url of rss/atom chanel. can set without http://\ntime - update time. number + time identificator. h - hour, m - minute. allowed only one identificator.\nfeeds - number of messages to receive. 10 max.\nmode - receive mode. full - full news, head - only headers, body - only bodies.\nwith -url to be show url of news.')),
	 (7, 'alias', alias, 2, L('Aliases.\nalias add new=old\nalias del|show text')),
	 (0, 'commands', info_comm, 1, L('Show commands list.')),
	 (8, 'comm', comm_on_off, 2, L('Enable/Disable commands.\ncomm - show disable commands\ncomm on command - enable command\ncomm off command1[ command2 command3 ...] - disable one or more command')),
	 (0, 'bot_uptime', uptime, 1, L('Show bot uptime.')),
	 (6, 'info', info, 1, L('Misc information about bot.')),
	 (3, 'new', svn_info, 1, L('Last svn update log')),
	 (9, 'limit', conf_limit, 2, L('Set temporary message limit.')),
	 (9, 'plugin', bot_plugin, 2, L('Plugin system.\nplugin show|local\nplugin add|del name')),
	 (9, 'error', show_error, 2, L('Show error(s).\nerror [number|clear]')),
	 (0, 'whoami', info_access, 1, L('Your identification.')),
	 (0, 'whois', info_whois, 2, L('Identification.')),
	 (0, 'status', status, 2, L('Show status.')),
	 (3, 'prefix', set_prefix, 2, L('Set command prefix. Use \'none\' for disable prefix')),
	 (9, 'set_locale', set_locale, 2, 'Change bot localization.\nset_locale en|%s' % '|'.join([tmp[:-4] for tmp in os.listdir(loc_folder) if tmp[-4:]=='.txt'])),
	 (7, 'config', configure, 2, L('Conference configure.\nconfig [show[ status]|help][ item]')),
	 (4, 'pmlock', muc_filter_lock, 2, L('Deny recieve messages from unaffiliated participants in private')),
	 (9, 'ddos', ddos_info, 2, L('Temporary ignore with ddos detect.\nddos [show|del jid]'))]
