#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2011 diSabler <dsy@dsy.name>                               #
#    Copyright (C) 2011 ferym <ferym@jabbim.org.ru>                           #
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

def price(type, jid, nick, parameters):
	parameters = parameters.replace('http://', '').strip()
	try:
		if len(parameters):
			parameters = parameters.split('.')[-2].lower()+'.'+parameters.split('.')[-1].lower()
			target = load_page('http://www.webvaluer.org/ru/www.'+parameters)
			od = re.search('<span style=\"color:green; font-weight:bold;\">',target)
			message = target[od.end():]
			message = message[:re.search('</span></h1>',message).start()]
			message = message.replace(',','')
			message = unicode(message.strip(),'utf-8')
			try: pos = message.find(re.findall(r'[0-9]',message)[0])
			except: pos = None
			if pos:
				if pos >= 2: message = message[pos:]+' '+message[:pos]
			send_msg(type, jid, nick, L('Estimated value %s is %s') % (parameters.strip(), message))
		else: send_msg(type, jid, nick, L('What site be evaluated?'))
	except: send_msg(type, jid, nick, L('I can\'t process your request.'))

def bizinfo(type, jid, nick, text):
	text = text.replace('http://', '').strip()
	try:
		if text:
			text = '.'.join(text.split('.')[-2:])
			req = 'http://bizinformation.org/ru/www.%s' % text
			body = load_page(req)
			if 'Error:' in body: msg = L('site input format is domain.tld')
			else:
				domain_price = re.search('<table class="content_table_main"><tr><th>.+?</th><td>(.+?) \*</td>', body).group(1)
				msg = L('Estimated value %s is %s') % (text, domain_price.decode('utf-8'))
		else: msg = L('What site be evaluated?')
	except: msg = L('I can\'t process your request.')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'price', price, 2, L('Show estimated value of domain | Author: ferym')),
		   (3, 'bizinfo', bizinfo, 2, L('Show estimated value of domain | Author: Disabler'))]
