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

def net_ping(type, jid, nick, text):
	text = text.strip().lower().encode('idna')
	if '.' in text and len(text) > 4 and re.match(r'[-0-9a-z.]+\Z', text, re.U+re.I): msg = deidna(shell_execute('ping -c4 %s' % text))
	else: msg = L('Smoke help about command!')
	send_msg(type, jid, nick, msg)

def get_tld(type, jid, nick, text):
	if len(text) >= 2:
		tld = readfile(tld_list).decode('utf-8')
		tld = tld.split('\n')
		msg = L('Not found!')
		for tl in tld:
			if tl.split('\t')[0].lower()==text.lower():
				msg = '.'+tl.replace('\t',' - ',1).replace('\t','\n')
				break
	else: msg = L('What do you want to find?')
	send_msg(type, jid, nick, msg)

def get_dns(type, jid, nick, text):
	is_ip = None
	if text.count('.') == 3:
		is_ip = True
		for ii in text:
			if not nmbrs.count(ii):
				is_ip = None
				break
	if is_ip:
		try: msg = socket.gethostbyaddr(text)[0]
		except: msg = L('I can\'t resolve it')
	else:
		try:
			ans = socket.gethostbyname_ex(text.encode('idna'))[2]
			msg = text+' - '
			for an in ans: msg += an + ' | '
			msg = msg[:-2]
		except: msg = L('I can\'t resolve it')
	send_msg(type, jid, nick, msg)

def srv_nslookup(type, jid, nick, text):
	srv_raw_check(type, jid, nick, 'nslookup '+text)

def srv_dig(type, jid, nick, text):
	srv_raw_check(type, jid, nick, 'dig '+text)

def srv_host(type, jid, nick, text):
	srv_raw_check(type, jid, nick, 'host '+text)

def srv_raw_check(type, jid, nick, text):
	text = enidna_raw(text)
	text = ''.join(re.findall(u'[-a-z0-9._?#=@% ]+',text,re.S+re.I)[0])
	send_msg(type, jid, nick, deidna(shell_execute(text)))

def chkserver(type, jid, nick, text):
	for a in ':;&/|\\\n\t\r': text = text.replace(a,' ')
	t = re.findall(u'[-a-zа-я0-9._?#=@%]+',text,re.S+re.I)
	if len(t) >= 2:
		port = []
		for a in t:
			if a.isdigit(): port.append(a)
		for a in port: t.remove(a)
		if len(t)==1 and len(port)>=1:
			t = t[0]
			port.sort()
			msg = shell_execute('nmap %s -p%s -P0 -T5' % (t.encode('idna'),','.join(port)))
			try: msg = '%s\n%s' % (t.encode('idna'),reduce_spaces_all(re.findall('SERVICE(.*)Nmap',msg,re.S+re.U)[0][1:-2]))
			except:
				try:
					msg = ''
					for a in port:
						sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
						try:
							sock.connect((t.encode('idna'),int(a)))
							s = L('on')
						except: s = L('off')
						msg += '\n%s %s' % (a,s)
						sock.close()
					msg = '%s%s' % (t,msg)
				except: msg = '%s - %s' % (t,L('unknown'))
			msg = L('Port status at %s') % msg
		else: msg = L('What?')
	else: msg = L('What?')
	send_msg(type, jid, nick, msg)

global execute

if not paranoia_mode: execute = [(6, 'nslookup', srv_nslookup, 2, L('Command nslookup')),
		   (6, 'host', srv_host, 2, L('Command host')),
		   (6, 'dig', srv_dig, 2, L('Command dig')),
		   (4, 'port', chkserver, 2, L('Check port activity\nport server port1 [port2 ...]')),
		   (4, 'net_ping', net_ping, 2, L('Net Ping.\nnet_ping ip|domain'))]
else: execute = []

execute += [(3, 'dns', get_dns, 2, L('DNS resolver.')),
			(3, 'tld', get_tld, 2, L('Search domain zones TLD.'))]
