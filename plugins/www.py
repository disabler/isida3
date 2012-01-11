#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2011 diSabler <dsy@dsy.name>                               #
#    Copyright (C) 2011 Vit@liy <vitaliy@root.ua>                             #
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

last_url_watch = ''
url_watch_ignore = ['pdf','sig','spl','class','ps','torrent','dvi','gz','pac','swf','tar','tgz','tar','zip','mp3','m3u','wma',\
					'wax','ogg','wav','gif','jar','jpg','jpeg','png','xbm','xpm','xwd','css','asc','c','cpp','log','conf','text',\
					'txt','dtd','xml','mpeg','mpg','mov','qt','avi','asf','asx','wmv','bz2','tbz','tar']

def netheader(type, jid, nick, text):
	if text:
		try:
			regex = text.split('\n')[0].replace('*','*?')
			text = text.split('\n')[1]
		except: regex = None
		if '://' not in text[:10]: text = 'http://%s' % text
		text = enidna(text)
		body, result = get_opener(text)
		if result: body = text + '\n' + unicode(body.headers)
		if regex:
			try:
				mt = re.findall(regex, body, re.S+re.U+re.I)
				if mt != []: body = ''.join(mt[0])
				else: body = L('RegExp not found!')
			except: body = L('Error in RegExp!')
		body = deidna(body)
	else: body = L('What?')
	send_msg(type, jid, nick, body)

def netwww(type, jid, nick, text):
	if text:
		try:
			regex = text.split('\n')[0].replace('*','*?')
			text = text.split('\n')[1]
		except: regex = None
		if '://' not in text[:10]: text = 'http://%s' % text
		text = enidna(text)
		msg, result = get_opener(text)
		if result:
			page = remove_sub_space(html_encode(load_page(text)))
			if regex:
				try:
					mt = re.findall(regex, page, re.S+re.U+re.I)
					if mt != []: msg = unhtml_hard(''.join(mt[0]))
					else: msg = L('RegExp not found!')
				except: msg = L('Error in RegExp!')
			else:
				msg = urllib.unquote(unhtml_hard(page).encode('utf8')).decode('utf8', 'ignore')
				if '<title' in page: msg = '%s\n%s' % (get_tag(page,'title'), msg)
	else: msg = L('What?')
	send_msg(type, jid, nick, msg[:msg_limit])

def parse_url_in_message(room,jid,nick,type,text):
	global last_url_watch
	if type != 'groupchat' or text == 'None' or nick == '' or getRoom(jid) == getRoom(selfjid): return
	if not get_config(getRoom(room),'url_title'): return
	if get_level(room,nick)[0] < 4: return
	try:
		link = re.findall(r'(http[s]?://.*)',text)[0].split(' ')[0]
		if link and last_url_watch != link and pasteurl not in link:
			for t in url_watch_ignore:
				if link.endswith('.%s' % t): return
			last_url_watch = link = enidna(link)
			pprint('Show url-title: %s in %s' % (link,room))
			original_page = load_page(urllib2.Request(link))[:4192]
			page = html_encode(original_page)
			if '<title' in page: tag = 'title'
			elif '<TITLE' in page: tag = 'TITLE'
			else: return
			text = remove_sub_space(get_tag(page,tag).replace('\n',' ').replace('\r',' ').replace('\t',' '))
			while '  ' in text: text = text.replace('  ',' ')
			if text:
				cnt = 0
				for tmp in text: cnt += int(ord(tmp) in [1056,1057])
				if cnt >= len(text)/3: text = remove_sub_space(html_encode(get_tag(original_page,tag)).replace('\n',' ').replace('\r',' ').replace('\t',' '))
			if text: send_msg(type, room, '', L('Title: %s') % rss_del_html(rss_replace(text)))
	except: pass

global execute

message_act_control = [parse_url_in_message]

execute = [(3, 'www', netwww, 2, L('Show web page.\nwww regexp\n[http://]url - page after regexp\nwww [http://]url - without html tags')),
		   (3, 'header',netheader,2, L('Show net header'))]
