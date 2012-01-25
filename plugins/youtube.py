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

def youtube(type, jid, nick, text):
	if '\n' in text:
		try: lim = int(text.split('\n',1)[1])
		except: lim = GT('youtube_default_videos')
		if lim > GT('youtube_max_videos'): lim = GT('youtube_max_videos')
		if lim < 1: lim = 1
		text = text.split('\n',1)[0]
	else: lim = GT('youtube_default_videos')
	regex = '<a accesskey=".*&amp;v=(.*?)">(.*?)</a>.*?<div style="color:#333;font-size:80%">([0-9:]{4,}).*?</div>.*?<div style="color:#333;font-size:80%">.*?</div>.*?<div style="color:#333;font-size:80%">(.*?)</div>'
	url = 'http://m.youtube.com/results?'
	page = html_encode(load_page(url, {'hl': GT('youtube_default_lang'),'q': text.lower().encode("utf-8").replace(' ','+')})).split('<td style="width:100%;font-size:13px">')
	if len(page) == 1: msg = L('Not found!')
	else:
		try:
			msg = L('Found:')
			for tmp in page[1:lim+1]:
				mt = re.findall(regex, tmp, re.S+re.I+re.U)
				if mt: msg += unescape('\nhttp://youtu.be/%s - %s [%s] %s' % tuple([t.replace('\t','').replace('\n','').replace('\r','').strip() for t in mt[0]]))
		except: msg = L('Not found!')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'youtube', youtube, 2, L('Search at YouTube'))]
