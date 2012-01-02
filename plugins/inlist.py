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

def inban(type, jid, nick, text): inlist_raw(type, jid, nick, text, 'outcast', L('Total banned: %s'))
def inowner(type, jid, nick, text): inlist_raw(type, jid, nick, text, 'owner', L('Total owners: %s'))
def inadmin(type, jid, nick, text): inlist_raw(type, jid, nick, text, 'admin', L('Total admins: %s'))
def inmember(type, jid, nick, text): inlist_raw(type, jid, nick, text, 'member', L('Total members: %s'))

def inlist_raw(type, jid, nick, text, affil, message):
	global banbase,iq_request
	iqid = get_id()
	i = Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':affil})])])
	iq_request[iqid]=(time.time(),inlist_raw_async,[type, jid, nick, text, message])
	sender(i)
	
def inlist_raw_async(type, jid, nick, text, message, iq_stanza):
	is_answ = unicode(iq_stanza[1][0])
	if is_answ.startswith(L('Error!')): msg = is_answ
	else:
		bb = [[tmp.getAttr('jid'),['',tmp.getTagData('reason')][tmp.getTagData('reason') != None]] for tmp in iq_stanza[1][0].getTag('query',namespace=xmpp.NS_MUC_ADMIN).getTags('item')]
		bb.sort()
		msg = message % len(bb)
		if text != '':
			text = text.strip().split()
			if len(text) == 1: text,nt = text[0], 0
			elif text[0] == '!': text,nt = ' '.join(text[1:]), 1
			elif text[0] == '=': text,nt = ' '.join(text[1:]), 2
			else: text,nt = ' '.join(text[1:]), False
			msg += ', '
			mmsg, cnt = '', 1
			for i in bb:
				if [text.lower() in i[0].lower() or text.lower() in i[1].lower(), text.lower() not in i[0].lower(),text.lower() == i[0].lower() or text.lower() == i[1].lower()][nt]:
					mmsg += '\n%s. %s' % (cnt,i[0])
					if len(i[1]): mmsg += ' - %s' % i[1]
					cnt += 1
			if len(mmsg): msg += L('Found:') + ' %s%s' % (mmsg.count('\n'),mmsg)
			else: msg += L('no matches!')
	send_msg(type, jid, nick, msg)

global execute

execute = [(7, 'inban', inban, 2, L('Search in outcast list of conference.')),
	 (7, 'inmember', inmember, 2, L('Search in members list of conference.')),
	 (7, 'inadmin', inadmin, 2, L('Search in admins list of conference.')),
	 (7, 'inowner', inowner, 2, L('Search in owners list of conference.'))]
