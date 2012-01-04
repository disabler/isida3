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

def hidden_clear(type, jid, nick, text):
	text = reduce_spaces_all(text).lower().split()
	if len(text) == 2: arg,match = text
	else: arg,match = '',text[0]
	if arg in ['all','total','global']: req,par = 'select message from age where message like %s order by -time,-status',('%\r%',)
	else: req,par = 'select message from age where room=%s message like %s order by -time,-status',(jid,'%\r%')
	st = cur_execute_fetchall(req,par)
	if st:
		ns = {}
		for t in st:
			k = t.split('\r',1)[1].split(' // ')[0]
			if not k.startswith(L('Error! %s')%''):
				if ns.has_key(k): ns[k] += 1
				else: ns[k] = 1
		ns = [(ns[t],t) for t in ns.keys()]
		ns.sort()
		msg = L('Client statistic:\n%s') % '\n'.join(['%s\t%s' % (t[1],t[0]) for t in ns[:10]])
	else: msg = L('Clients statistic not available.')
	send_msg(type, jid, nick, msg)

global execute

execute = [(4, 'clients', clients_stats, 2, L('Show clients statistic when available.'))]
