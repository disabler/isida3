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

last_new_year = time.localtime()[0]

def newyear_timer():
	global last_new_year, gtimer
	lt = tuple(time.localtime())
	if lt[1:3] not in [(12,31),(1,1)]: return
	if last_new_year < lt[0]:
		last_new_year = lt[0]
		gtimer.remove(newyear_timer)
		for jjid in confbase: send_msg('groupchat', getRoom(jjid), '', GT('new_year_text'))

global timer

timer = [newyear_timer]