#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2011 diSabler <dsy@dsy.name>                               #
#    Copyright (C) 2011 dr.Schmurge <dr.schmurge@isida-bot.com>               #
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

def add_space_to_number(num):
	if num<10: return ' '+str(num)
	else: return str(num)

def month_cal(type, jid, nick, text):
	text = text.split()
	try: month = int(text[0])
	except: month = tuple(time.localtime())[1]
	try: year = int(text[1])
	except: year = tuple(time.localtime())[0]
	try: smbl = text[2]
	except: smbl = GT('calendar_default_splitter')
	try:
		msg = L('\nMon Tue Wed Thu Fri Sat Sun\n')
		for tmp in calendar.monthcalendar(year, month):
			for tmp2 in tmp:
				if tmp2: msg+=add_space_to_number(tmp2)+' '
				else: msg+='   '
			msg = msg[:-1]+'\n'
		msg = L('Now: %s%s') % (timeadd(tuple(time.localtime())), msg[:-1].replace(' ',smbl))
	except: msg = L('Error!')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'calendar', month_cal, 2, L('Calendar. Without parameters show calendar for current month.\ncalendar [month][year][symbol_splitter]'))]
