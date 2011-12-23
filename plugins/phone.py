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

def_phone_base = '%sdefcodes.db' % set_folder

def phonecode(type, jid, nick, text):
	if len(text):
		db = sqlite3.connect(def_phone_base)
		cu = db.cursor()
		def_info,country = L('Not found!'),L('Unknown')
		if text[0] == '+': text = text[1:]
		if text.isdigit():
			if text[0] == '7':
				if len(text) > 1 and text[1] == '9':
					country = L('Russia, Mobile')
					if len(text) >= 5:
						dc = text[1:4]
						pn = text[4:]
						if len(pn) < 7: pn = pn.ljust(7, '0')
						elif len(pn) > 11: pn = pn[:7]
						result = cu.execute('select * from ru_mobile where def=? and begin<=? and end>=?', (dc,pn,pn)).fetchall()
						if result:
							di = []
							for res in result: di += ['%s, %s (%s) %s..%s, %s ' % res]
							def_info = '\n'.join(di)
					else: def_info = L('Too many results!')
				else:
					country = L('Russia')
					if len(text) < 11: text = text.ljust(12, '2')
					elif len(text) > 11: text = text[:11]
					text = text[:7] + 'x'*4
					pos = 7
					while pos:
						result = cu.execute('select * from ru_stat where phone like ?', ('%s%%'%text,)).fetchall()
						if result:
							def_info = []
							for res in result:
								res = list(res)
								while '' in res: res.remove('')
								res[0] = '+%s (%s%s%s) %s%s%s-%s%s-%s%s' % tuple(res[0])
								def_info += [', '.join(res)]
							def_info = '\n'.join(def_info)
							break
						else:
							text = list(text)
							text[pos] = 'x'
							text = ''.join(text)
							pos -= 1
			elif text[:3] == '380':
				country = L('Ukraine')
				if len(text) < 12: text = text.ljust(12, '2')
				elif len(text) > 12: text = text[:12]
				text = text[:8]+'x'*4
				pos = 8
				while pos > 2:
					result = cu.execute('select * from ua_stat where phone like ?', ('%s%%'%text,)).fetchall()
					if result:
						def_info = []
						for res in result:
							res = list(res)
							while '' in res: res.remove('')
							res[0] = '+%s%s (%s%s%s) %s%s%s-%s%s-%s%s' % tuple(res[0])
							def_info += [', '.join(res)]
						def_info = '\n'.join(def_info)
						break
					else:
						text = list(text)
						text[pos] = 'x'
						text = ''.join(text)
						pos -= 1
			if country == L('Unknown'): result = def_info
			elif def_info == L('Not found!'): result = L('Country: %s, Phone number not found') % (country,)
			else: result = L('Country: %s\n%s') % (country,def_info)
		else:
			text = '%s%%'%text.lower().capitalize()
			def_info = []
			result = cu.execute('select * from ru_stat where city like ?', (text,)).fetchall()
			if result:
				di = []
				for res in result:
					res = list(res)
					while '' in res: res.remove('')
					res[0] = '+%s (%s%s%s) %s%s%s-%s%s-%s%s' % tuple(res[0])
					di += [', '.join(res)]
				di = '\n'.join(di)
				def_info += [L('Country: %s\n%s') % (L('Russia'),di)]
			result = cu.execute('select * from ua_stat where city like ?', (text,)).fetchall()
			if result:
				di = []
				for res in result:
					res = list(res)
					while '' in res: res.remove('')
					res[0] = '+%s%s (%s%s%s) %s%s%s-%s%s-%s%s' % tuple(res[0])
					di += [', '.join(res)]
				di = '\n'.join(di)
				def_info += [L('Country: %s\n%s') % (L('Ukraine'),di)]
			#result = cu.execute('select * from ru_mobile where provider like ? or region like ?', (text,text)).fetchall()
			#if result:
			#	di = []
			#	for res in result: di += ['%s, %s (%s) %s..%s, %s ' % res]
			#	di = '\n'.join(di)
			#	def_info += [L('Country: %s\n%s') % (L('Russia, Mobile'),di)]
			if def_info: result = '\n\n'.join(def_info)
			else: result = L('Not found!')
		db.close()
		msg = result
	else: msg = L('What?')
   	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'phone', phonecode, 2, L('Information about telephone city code, DEF code or search code for city.'))]
