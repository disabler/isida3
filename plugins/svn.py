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

def svn_get(type, jid, nick,text):
	if len(text):
		if text[:7] !='http://' and text[:8] !='https://' and text[:6] !='svn://': text = 'http://'+text
		count = 1
		revn = 0
		if ' ' in text:
			text = text.split(' ')
			url = text[0]
			try: count = int(text[1])
			except:
				try:
					if 'r' in text[1].lower(): revn = int(text[1][text[1].find('r')+1:])
				except: revn = 0
		else: url=text
		if revn != 0: sh_exe = 'sh -c \"LANG='+L('en_EN.UTF8')+' svn log '+url+' -r'+str(revn)+'\"'
		else:
			if count > 10: count = 10
			sh_exe = 'sh -c \"LANG='+L('en_EN.UTF8')+' svn log '+url+' --limit '+str(count)+'\"'
		svn_log = shell_execute(sh_exe).replace('\n\n','\n')
		while svn_log[-1] in ['-','\n']: svn_log = svn_log[:-1]
		rpl = re.findall('-{10,}',svn_log)
		if rpl: svn_log = svn_log.replace(rpl[0],'-'*3)
		msg = 'SVN from %s\n%s' % (url,svn_log)
	else: msg = L('Read user manual for commands...')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'svn', svn_get, 2, L('Show svn log.\nsvn [http://]url [limit] - show last revision(s) limit\nsvn [http://]url rXXX - show XXX revision'))]
