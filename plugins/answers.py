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

def answers_ie(type, jid, nick, text):
	if text.lower().strip().split(' ',1)[0] == 'export':
		try: fname = text.lower().split(' ',1)[1]
		except: fname = answers_file
		base_size = len(cur_execute_fetchall('select * from answer'))
		fnd = cur_execute_fetchall('select body from answer where body like %s group by body order by body',('%',))
		answer = ''
		msg = L('Export to file: %s | Total records: %s | Unique records: %s') % (fname,str(base_size),str(len(fnd)))
		for i in fnd:
			if i[0] != '': answer += i[0].strip() +'\n'
		writefile(fname,answer.encode('utf-8'))
	elif text.lower().strip().split(' ',1)[0] == 'import':
		try: fname = text.lower().split(' ',1)[1]
		except: fname = answers_file
		if os.path.isfile(fname):
			answer = readfile(fname).decode('utf-8')
			answer = answer.split('\n')
			cur_execute('delete from answer where body like %s',('%',))
			msg = L('Import from file: %s | Total records: %s') % (fname,str(len(answer)))
			idx = 1
			for i in answer:
				if i != '':
					cur_execute('insert into answer values (%s,%s)', (idx,unicode(i.strip())))
					idx += 1
			conn.commit()
		else: msg = L('File %s not found!') % fname
	else: msg = L('What?')
	send_msg(type, jid, nick, msg)

global execute

execute = [(9, 'answers', answers_ie, 2, L('Import/Export answers base.\nanswers import [filename] - import from file\nanswers export [filename] - export to file'))]
