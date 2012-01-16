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

google_last_res = {}

def replace_bold(t,b,e): return t.replace('<b>',b).replace('</b>',e)

def wiki_search(type, jid, nick, text):
	if text not in ['next','']: text = L('%s site:en.wikipedia.org') % text
	google(type, jid, nick, text)

def xep_show(type, jid, nick,text):
	ntext = 'xep '+text+' inurl:xmpp.org'
	url = 'http://ajax.googleapis.com/ajax/services/search/web?'
	search_results = html_encode(load_page(url, {'v': '1.0', 'q': ntext.encode("utf-8")}))
	jsonl = json.loads(search_results)
	try:
		results = jsonl['responseData']['results']
		title = results[0]['title']
		content = results[0]['content']
		noh_title = replace_bold(title,'','')
		content = replace_bold(content,'','')
		msg = '\n'.join((replacer(noh_title),replacer(content),results[0]['unescapedUrl']))
	except: msg = L('xep \"%s\" not found!') % text
	send_msg(type, jid, nick, msg)

def google(type, jid, nick, text):
	global google_last_res
	results = ''
	text = text.strip()
	if text in ['next','']:
		if google_last_res.has_key(jid) and google_last_res[jid].has_key(nick) and google_last_res[jid][nick]:
			first = google_last_res[jid][nick][0]
			google_last_res[jid][nick] = google_last_res[jid][nick][1:]
		else: results = L('No results!')
	else:
		try:
			url = 'http://ajax.googleapis.com/ajax/services/search/web?'
			search_results = html_encode(load_page(url, {'v': '1.0', 'q': text.encode("utf-8")}))
			jsonl = json.loads(search_results)
			data = jsonl['responseData']['results']
			first = data[0]
			if google_last_res.has_key(jid): google_last_res[jid].update({nick: data[1:]})
			else: google_last_res[jid] = {nick: data[1:]}
		except: results = L('Expression \"%s\" not found!') % text
	if not results:
		title = first['title']
		content = first['content']
		noh_title = replace_bold(title,u'«',u'»')
		content = replace_bold(content,u'«',u'»')
		url = urllib.unquote(first['unescapedUrl'].encode('utf8')).decode('utf8','ignore')
		results = replacer(noh_title)+'\n'+replacer(content)+'\n'+url
	send_msg(type, jid, nick, results)

def google_clear(room,jid,nick,type,arr):
	if type == 'unavailable' and google_last_res.has_key(room) and google_last_res[room].has_key(nick): del google_last_res[room][nick]

def translate(type, jid, nick, text):
	text = text.strip()
	trlang = {'sq':L('Albanian'),'en':L('English'),'ar':L('Arabic'),'af':L('Afrikaans'),
			'be':L('Belarusian'),'bg':L('Bulgarian'),'cy':L('Welsh'),'hu':L('Hungarian'),'vi':L('Vietnamese'),
			'gl':L('Galician'),'nl':L('Dutch'),'el':L('Greek'),'da':L('Danish'),'iw':L('Hebrew'),'yi':L('Yiddish'),
			'id':L('Indonesian'),'ga':L('Irish'),'is':L('Icelandic'),'es':L('Spanish'),'it':L('Italian'),
			'ca':L('Catalan'),'zh':L('Chinese'),'ko':L('Korean'),'lv':L('Latvian'),'lt':L('Lithuanian'),
			'mk':L('Macedonian'),'ms':L('Malay'),'mt':L('Maltese'),'de':L('German'),'no':L('Norwegian'),
			'fa':L('Persian'),'pl':L('Polish'),'pt':L('Portuguese'),'ro':L('Romanian'),'ru':L('Russian'),
			'sr':L('Serbian'),'sk':L('Slovak'),'sl':L('Slovenian'),'sw':L('Swahili'),'tl':L('Tagalog'),
			'th':L('Thai'),'tr':L('Turkish'),'uk':L('Ukrainian'),'fi':L('Finnish'),'fr':L('French'),'hi':L('Hindi'),
			'hr':L('Croatian'),'cs':L('Czech'),'sv':L('Swedish'),'et':L('Estonian'),'ja':L('Japanese'),'ht':L('Creole')}
	if text.lower() == 'list': msg = L('Available languages for translate:') + ' ' + ', '.join(sorted(trlang.keys()))
	elif text[:5].lower() == 'info ':
		text = text.lower().split(' ')
		msg = ''
		for tmp in text:
			if tmp in trlang: msg += '%s - %s, ' % (tmp,trlang[tmp])
		if len(msg): msg = L('Available languages: %s') % msg[:-2]
		else: msg = L('I don\'t know this language')
	elif text[:5].lower() == 'lang ' and text.count(' ')==1:
		text = text.lower().split(' ')[1]
		msg = ', '.join(['%s - %s' % (k,trlang[k]) for k in trlang.keys() if text in trlang[k].lower()])
		if len(msg): msg = L('Available languages: %s') % msg
		else: msg = L('I don\'t know this language')
	else:
		if ' ' in text:
			text = text.split(' ',2)
			url = 'http://translate.google.ru/translate_a/t?'
			if len(text)>1 and trlang.has_key(text[0].lower()):
				if len(text)>2 and trlang.has_key(text[1].lower()): lfrom,lto,tr_text = text[0].lower(),text[1].lower(),text[2]
				else: lfrom,lto,tr_text = '',text[0].lower(),' '.join(text[1:])
				search_results = html_encode(load_page(url, {'client':'x',\
															 'text':tr_text.encode("utf-8"),\
															 'hl':lfrom,\
															 'sl':lfrom,\
															 'tl':lto}))
				try: jsonl = json.loads(search_results)['sentences']
				except ValueError: jsonl = None
				if jsonl: msg = rss_replace(''.join(f['trans'] for f in jsonl))
				else: msg = L('I can\'t translate it!')
			else: msg = L('Incorrect language settings for translate. tr list - available languages.')
		else: msg = L('Command\'s format: tr [from] to text')
	send_msg(type, jid, nick, msg)

global execute, presence_control

presence_control = [google_clear]

execute = [(3, 'tr', translate, 2, L('Translator.\ntr [from_language] to_language text - translate text\ntr list - list for available languages for translate\ntr info <reduction> - get info about language reduction\ntr lang <expression> - get languages by expression')),
	 (3, 'google', google, 2, L('Search in google')),
	 (3, 'xep', xep_show, 2, L('Search XEP')),
	 (3, 'wiki', wiki_search, 2, L('Search in en.wikipedia.org'))]

