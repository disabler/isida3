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

def currency_converter(type, jid, nick, text):
	msg = L('Error in parameters. Read the help about command.')
	if text.lower() == 'list': msg = L('Available values:\n%s') % 'ATS AUD RUR BEF BYR CAD CHF CNY DEM DKK EEK EGP ESP EUR FIM FRF GBP GRD IEP ISK ITL JPY KGS KWD KZT LTL NLG NOK PTE RUR SDR SEK SGD TRL TRY UAH USD XDR YUN'
	else:
		repl_curr = ((u'€','EUR'),(u'$','USD'),(u'¥','JPY'),(u'£','GBP'),('RUR','BASE'))
		for tmp in repl_curr: text = text.upper().replace(tmp[0],' %s ' % tmp[1])
		mt = re.findall('[a-zA-Z]|[0-9]|[.,]|[ ]', text, re.S)
		text = ''.join(mt).strip()
		while '  ' in text: text = text.replace('  ',' ')
		text,date,c_from,c_to,c_summ = text.split(),tuple(time.localtime())[:3],None,None,None
		for tmp in text:
			try:
				c_summ = float(tmp.replace(',','.'))
				if int(c_summ) == c_summ: c_summ = int(c_summ)
				text.remove(tmp)
				break
			except: pass
		if len(text) > 1: (c_from,c_to) = text[:2]
		if c_from and c_to and c_summ:
			url = 'http://conv.rbc.ru/convert.shtml?mode=calc&source=cb.0&tid_from=%s&commission=1&tid_to=%s&summa=%s&day=%s&month=%s&year=%s' % (c_from,c_to,c_summ,date[2],date[1],date[0])
			body = html_encode(load_page(url))
			regex = '<TD class=background>.*?<TD class=background>.*?<TD he.*?>(.*?) </TD>.*?<B>(.*?)</B>.*?<B>(.*?)</B>.*?<TD he.*?>(.*?) </TD>.*?<B>(.*?)</B>'
			mt = re.findall(regex, body, re.S)
			if mt != []:
				msg = '%s %s (%s) = %s %s (%s) | 1 %s = %s %s' % (c_summ,c_from,mt[0][0],mt[0][4],c_to,mt[0][3],c_from,mt[0][2],c_to)
				msg = msg.replace('BASE','RUR')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'convert', currency_converter, 2, L('Currency converter\nconvert from to count\nconvert list'))]
