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

def sokr(type, jid, nick, text):
	target = ''
	text = text.strip()
	if not text: msg = L('What?')
	else:
		if re.search('\A\d+?(-\d+?)? ', text): target, text = text.split(' ', 1)
		if re.match('[a-zA-Z]+\Z', text):
			data = load_page('http://www.abbreviations.com/bs2.aspx?st=%s&o=p' % text)
			results = re.findall('<td class="dsc">(.+?)</td>', data)
			results = [i for k,i in enumerate(results) if results.index(i) == k]
		else:
			data = load_page("http://www.sokr.ru/search/?", {'abbr': text.encode('utf-8'), 'abbr_exact': '1'})
			results = re.findall('em class="got_clear">.+?</em></a>.+?<p class="value">(.+?)</p>' , data, re.S)
		cr = len(results)
		if not results: msg = L('I don\'t know!')
		else:
			if not target:
				if cr == 1: target = '1'
				elif cr < 6:  target = '1-%s' % cr
				else: target = '1-5'
			try: n1 = n2 = int(target)
			except: n1, n2 = map(int, target.split('-'))
			if 0 < n1 <= n2 <= cr:
				msg = L('Total found %s matches. Result(s) %s:\n') % (cr, target)
				msg += '\n'.join(['%s. %s' % (i[0]+n1, i[1]) for i in enumerate(results[n1-1: n2])]).decode('utf8')
				msg = msg.replace('<br>', '')
			else: msg = L('I don\'t know!')
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'sokr', sokr, 2, L('Abbreviations.\nExamples: sokr abbr, sokr 6 abbr, sokr 3-7 abbr'))]
