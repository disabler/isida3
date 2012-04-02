#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2012 diSabler <dsy@dsy.name>                               #
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

last_url_watch = ''
url_watch_ignore = ['pdf','sig','spl','class','ps','torrent','dvi','gz','pac','swf','tar','tgz','tar','zip','mp3','m3u','wma',\
					'wax','ogg','wav','gif','jar','jpg','jpeg','png','xbm','xpm','xwd','css','asc','c','cpp','log','conf','text',\
					'txt','dtd','xml','mpeg','mpg','mov','qt','avi','asf','asx','wmv','bz2','tbz','tar','so','dll','exe','bin',\
					'img','usbimg','rar','deb','rpm','iso','ico','apk','patch','svg','7z','tcl']

def netheader(type, jid, nick, text):
	if text:
		try:
			regex = text.split('\n')[0].replace('*','*?')
			text = text.split('\n')[1]
		except: regex = None
		if '://' not in text[:10]: text = 'http://%s' % text
		text = enidna(text).decode('utf-8')
		body, result = get_opener(text)
		if result: body = '%s\n%s' %(text.decode('utf-8'),unicode(body.headers))
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
		text = enidna(text).decode('utf-8')
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
				if '<title' in page: msg = '%s\n%s' % (rss_replace(get_tag(page,'title')), msg)
	else: msg = L('What?')
	send_msg(type, jid, nick, msg[:msg_limit])

def parse_url_in_message(room,jid,nick,type,text):
	global last_url_watch
	if type != 'groupchat' or text == 'None' or nick == '' or getRoom(jid) == getRoom(selfjid): return
	if get_level(room,nick)[0] < 4: return
	was_shown = False
	if get_config(getRoom(room),'url_title'):
		try:
			link = re.findall(r'(http[s]?://.*)',text)[0].split(' ')[0]
			if link and last_url_watch != link and pasteurl not in link:
				ll = link.lower()
				for t in url_watch_ignore:
					if ll.endswith('.%s' % t): raise
				last_url_watch = link = enidna(link)
				pprint('Show url-title: %s in %s' % (link,room))
				original_page = load_page(urllib2.Request(link))[:4192]
				page = html_encode(original_page)
				if '<title' in page: tag = 'title'
				elif '<TITLE' in page: tag = 'TITLE'
				else: raise
				text = remove_sub_space(get_tag(page,tag).replace('\n',' ').replace('\r',' ').replace('\t',' '))
				while '  ' in text: text = text.replace('  ',' ')
				if text:
					cnt = 0
					for tmp in text: cnt += int(ord(tmp) in [1056,1057])
					if cnt >= len(text)/3: text = remove_sub_space(html_encode(get_tag(original_page,tag)).replace('\n',' ').replace('\r',' ').replace('\t',' '))
				if text:
					was_shown = True
					send_msg(type, room, '', L('Title: %s') % rss_del_html(rss_replace(text)))
		except: pass
	if not was_shown and get_config(getRoom(room),'content_length'):
		try:
			link = re.findall(u'(http[s]?://[-0-9a-zа-я.]+\/[-a-zа-я0-9._?#=@%/]+\.[a-z0-9]{2,7})',text,re.I+re.U+re.S)[0]
			if link and last_url_watch != link and pasteurl not in link:
				is_file = False
				ll = link.lower()
				for t in url_watch_ignore:
					if ll.endswith('.%s' % t):
						is_file = True
						break
				if is_file:
					last_url_watch = link = enidna(link)
					body, result = get_opener(link)
					pprint('Show content length: %s in %s' % (link,room))
					if result:
						body = unicode(body.headers)
						mt = float(re.findall('Content-Length.*?([0-9]+)', body, re.S+re.U+re.I)[0])
						for t in ['','Kb','Mb','Gb']:
							tt = t
							if mt < 1024: break
							mt = mt / 1024.0
						if tt: mt = '%.2f%s' % (mt,tt)
						else: mt = '%sb' % int(mt)
						if mt: send_msg(type, room, '', L('Length of %s is %s') % (u'…/%s' % link.rsplit('/',1)[-1],mt))
		except: pass

global execute

message_act_control = [parse_url_in_message]

execute = [(3, 'www', netwww, 2, L('Show web page.\nwww regexp\n[http://]url - page after regexp\nwww [http://]url - without html tags')),
		   (3, 'header',netheader,2, L('Show net header'))]
