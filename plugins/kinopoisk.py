#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2012 Vit@liy <vitaliy@root.ua>                             #
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

kinopoisk_error_string = '<META HTTP-EQUIV="Pragma" CONTENT="no-cache">'
kinopoisk_error_regexp = '<td style="padding-left:10px">(.*?)<br><br><small>'

def kinopoisk(type, jid, nick, text):
	text=text.strip().split(' ', 1)
	if len(text) == 2 and not text[0] in ['id', 'search'] or len(text) == 1: text = [' ', ' '.join(text)]
	if text[0] == 'search' or text[0] == ' ' and not re.search('^\d+$', text[-1]):
		query=urllib.quote(text[-1].encode('cp1251'))
		data = html_encode(load_page('http://m.kinopoisk.ru/search/'+query))
		if kinopoisk_error_string in data: msg = unhtml_hard(re.findall(kinopoisk_error_regexp,data,re.I+re.U+re.S)[0])
		else:
			temp_urls = re.findall('<a href="http://m.kinopoisk.ru/movie/(\d+?)/">(.+?)</a>', data)
			if temp_urls:
				msg = L('Found:','%s/%s'%(jid,nick))
				for t_u in temp_urls:
					msg += '\n%s - %s' % (t_u[0], t_u[1])
			else: msg = L('Not found!','%s/%s'%(jid,nick))
	elif re.search('^\d+$', text[-1]):
		data = html_encode(load_page('http://m.kinopoisk.ru/movie/'+text[-1]))
		if kinopoisk_error_string in data: msg = unhtml_hard(re.findall(kinopoisk_error_regexp,data,re.I+re.U+re.S)[0])
		else:
			tmp = unhtml_hard(re.search('<p class="title">((?:.|\s)+?)</div>', data).group(1)).split('\n')
			msg = '\n'.join([i[0].upper()+i[1:] for i in tmp])
	else: msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type,jid,nick,msg)

global execute

execute = [(0, 'film', kinopoisk, 2, L('Search in www.kinopoisk.ru. Example:\nfilm [id] film_id\nfilm [search] film_name'))]
