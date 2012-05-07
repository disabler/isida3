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

currency_conv_list = ['ATS','AUD','BEF','BYR','CAD','CHF','CNY','DEM','DKK','EEK',\
					  'EGP','ESP','EUR','FIM','FRF','GBP','GRD','IEP','ISK','ITL',\
					  'JPY','KGS','KWD','KZT','LTL','NLG','NOK','PTE','SDR','SEK',\
					  'SGD','TRL','TRY','UAH','USD','XDR','YUN','BASE']

def currency_converter(type, jid, nick, text):
	msg = L('Error in parameters. Read the help about command.')
	text = text.strip().upper()
	if text == 'LIST': msg = L('Available values:\n%s') % ', '.join(currency_conv_list).replace('BASE','RUR')
	else:
		repl_curr = ((u'€','EUR'),('$','USD'),(u'¥','JPY'),(u'£','GBP'),('RUR','BASE'),(',','.'))
		for tmp in repl_curr: text = text.replace(tmp[0],' %s ' % tmp[1])
		c_from,c_to,c_summ = '','',''
		val = [t for t in re.findall('[A-Z]{3,4}', text, re.S) if t in currency_conv_list]
		if len(val) >= 2: c_from,c_to = val[:2]
		val = ''.join(re.findall('[0-9\.]',text))
		if val.replace('.','').isdigit() and val.count('.') <= 1:
			if val.startswith('.'): c_summ = '0%s' % val
			elif val.endswith('.'): c_summ = '%s0' % val
			else: c_summ = val
		print c_from,c_to,c_summ
		if c_from and c_to and c_summ:
			date = tuple(time.localtime())[:3]
			url = 'http://cash.rbc.ru/converter.shtml?mode=calc&source=cb.0&tid_from=%s&commission=1&tid_to=%s&summa=%s&day=%s&month=%s&year=%s' % (c_from,c_to,c_summ,date[2],date[1],date[0])
			body = html_encode(load_page(url))
			try: body = body.split('<table id="rTable" class="table">',1)[1]
			except: body = ''
			regex = '<tbody>.*?<td>(.*?)</td>.*?<td class="b">(.*?)</td>.*?<td class="b">(.*?)</td>.*?<td>(.*?)</td>.*?<td class="b">(.*?)</td>'
			mt = re.findall(regex, body, re.S)
			if mt != []:
				mt = [t.strip() for t in mt[0]]
				msg = '%s %s (%s) = %s %s (%s) | 1 %s = %s %s' % (c_summ,c_from,mt[0],mt[4],c_to,mt[3],c_from,mt[2],c_to)
				msg = msg.replace('BASE','RUR')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'convert', currency_converter, 2, L('Currency converter\nconvert from to count\nconvert list'))]
