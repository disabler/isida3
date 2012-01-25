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

def thread_info(type, jid, nick):
	if thread_type:
		msg,tmas = '',[]
		for tmp in threading.enumerate(): tmas.append(unicode(tmp).split('(',1)[1].split(')',1)[0])
		tmas.sort()
		for tmp in tmas: msg += '\n' + tmp
		msg = '\nActive: %s%s' % (threading.activeCount(),msg)
	else: msg = ''
	msg = L('Executed threads: %s | Error(s): %s') % (th_cnt,thread_error_count) + msg
	send_msg(type, jid, nick, msg)

global execute

execute = [(7, 'th', thread_info, 1, L('Threads statistic'))]
