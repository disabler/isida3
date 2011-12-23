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

def bing_translate(type, jid, nick, text):
	text = text.strip()
	trlang = {'id':L('Indonesian'), 'it':L('Italian'), 'ar':L('Arabic'), 'ja':L('Japanese'), 'bg':L('Bulgarian'),
			'ko':L('Korean'), 'ca':L('Catalan'), 'lv':L('Latvian'), 'zh-chs':L('Chinese Simplified'), 'lt':L('Lithuanian'),
			'zh-cht':L('Chinese Traditional'), 'no':L('Norwegian'), 'cs':L('Czech'), 'pl':L('Polish'), 'da':L('Danish'),
			'pt':L('Portuguese'), 'nl':L('Dutch'), 'ro':L('Romanian'), 'en':L('English'), 'ru':L('Russian'), 'et':L('Estonian'),
			'sk':L('Slovak'), 'fi':L('Finnish'), 'sl':L('Slovenian'), 'fr':L('French'), 'es':L('Spanish'), 'de':L('German'),
			'sv':L('Swedish'), 'el':L('Greek'), 'th':L('Thai'), 'ht':L('Haitian Creole'), 'tr':L('Turkish'), 'he':L('Hebrew'),
			'uk':L('Ukrainian'), 'hi':L('Hindi'), 'vi':L('Vietnamese'), 'hu':L('Hungarian')}
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
			url = 'http://api.microsofttranslator.com/V2/Ajax.svc/Translate?'
			bing_api = GT('bing_api_key')
			if bing_api == 'no api': msg = L('Not found Api-key for Bing translator')
			elif len(text)>1 and trlang.has_key(text[0].lower()):
				if len(text)>2 and trlang.has_key(text[1].lower()): lfrom,lto,tr_text = text[0].lower(),text[1].lower(),text[2]
				else: lfrom,lto,tr_text = '',text[0].lower(),' '.join(text[1:])
				translate_results = html_encode(load_page(url, {'oncomplete':'responseData',\
																'appId':bing_api,\
																'text':tr_text.encode("utf-8"),\
																'from':lfrom,\
																'to':lto}))
				try: msg = re.findall('responseData\(\"(.*?)\"\)\;$',unicode(translate_results),re.S+re.I+re.U)[0]
				except: msg = L('I can\'t translate it!')
			else: msg = L('Incorrect language settings for translate. tr list - available languages.')
		else: msg = L('Command\'s format: tr [from] to text')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'bt', bing_translate, 2, L('Bing translator.\nbt [from_language] to_language text - translate text\nbt list - list for available languages for translate\nbt info <reduction> - get info about language reduction\nbt lang <expression> - get languages by expression'))]

