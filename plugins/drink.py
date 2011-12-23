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

def to_drink(type, jid, nick, text):
	dmas = [L('first'),L('second'),L('third'),L('fourth'),L('fifth'),L('sixth'),L('seventh'),L('eighth'),L('nineth'),L('tenth'),
		L('eleventh'),L('twelveth'),L('thirteenth'),L('fourteenth'),L('fivteenth'),L('sixteenth'),
		L('seventeenth'),L('eighteenth'),L('nineteenth'),('twentieth'),L('twenty-first'),L('twenty-second'),
		L('twenty-third'),L('twenty-fourth'),L('twenty-fifth'),L('twenty-sixth'),L('twenty-seventh'),
		L('twenty-eighth'),L('twenty-nineth'),L('thirtieth'),L('thirty-first')]
	mmas1 = [L('january'),L('february'),L('march'),L('april'),L('may'),L('june'),L('july'),L('august'),
		L('september'),L('october'),L('november'),L('december')]
	mmas2 = [L('January'),L('February'),L('March'),L('April'),L('May'),L('June'),L('July'),L('August'),
		L('September'),L('October'),L('November'),L('December')]
	wday = [L('monday'),L('tuesday'),L('wendesday'),L('thirsday'),L('friday'),L('saturday'),L('sunday')]
	lday = [L('last'),L('last'),L('Last'),L('last'),L('Last'),L('Last'),L('lAst')]
	if os.path.isfile(date_file):
		ddate = readfile(date_file).decode('UTF')
		week1 = ''
		week2 = ''
		if not ddate: msg = L('Read file error.')
		else:
			if len(text) <= 2:
				ltim = tuple(time.localtime())
				text = '%s %s' % (ltim[2], mmas2[ltim[1]-1])
				week1 = '%s %s %s' % (ltim[2]/7+(ltim[2]%7 > 0), wday[ltim[6]], mmas2[ltim[1]-1])
				if ltim[2]+7 > calendar.monthrange(ltim[0], ltim[1])[1]: week2 = '%s %s %s' % (lday[ltim[6]].lower(), wday[ltim[6]], mmas2[ltim[1]-1])
			or_text = text
			if text.count('.')==1: text = text.split('.')
			elif text.count(' ')==1: text = text.split(' ')
			else: text = [text]
			msg = ''
			ddate = ddate.split('\n')
			ltxt = len(text)
			for tmp in ddate:
				if or_text.lower() in tmp.lower(): msg += '\n'+tmp
				elif week1.lower() in tmp.lower() and week1 != '': msg += '\n'+tmp
				elif week2.lower() in tmp.lower() and week2 != '': msg += '\n'+tmp
				else:
					try:
						ttmp = tmp.split(' ')[0].split('.')
						tday = [ttmp[0]]
						tday.append(dmas[int(ttmp[0])-1])
						tmonth = [ttmp[1]]
						tmonth.append(mmas1[int(ttmp[1])-1])
						tmonth.append(mmas2[int(ttmp[1])-1])
						tmonth.append(str(int(ttmp[1])))
						t = tday.index(text[0])
						t = tmonth.index(text[1])
						msg += '\n'+tmp
					except: pass
			if msg == '': msg = L('Holiday: %s not found.') % or_text
			else: msg = L('I know holidays: %s') % msg
	else: msg = L('Database doesn\'t exist.')
	send_msg(type, jid, nick, msg)

def calend(type, jid, nick, text):
	msg, url, text = '', '', text.strip()
	if not text: url = 'http://www.calend.ru/day/%s-%s/' % tuple(time.localtime())[1:3]
	elif re.match('\d+\.\d+$', text): url = 'http://www.calend.ru/day/%s-%s/' % tuple(text.split('.')[::-1])
	elif len(text) > 1: url = 'http://www.calend.ru/search/?search_str=' + urllib.quote(text.encode('cp1251'))
	if url:
		data = html_encode(load_page(url))
		t = get_tag(data,'title')
		if t == u'Поиск':
			hl = re.findall('<a  href="(/holidays(?:/\d*?)+?)" title=".+?">(.+?)</a>(?:.|\s)+?/>\s+?(\d+ .+?)\s', data)
			if len(hl) == 1:
				d = re.search('class="img_small" /></a></td>\s+?<td>\s+?(.+?\.)\s+?</td>', data, re.S).group(1)
				d = re.sub('\s+', ' ', d.strip())
				msg += '%s (%s) - %s\nhttp://www.calend.ru%s' % (hl[0][1], hl[0][2], d, hl[0][0])
			elif hl:
				for a in hl: msg += '\n%s (%s)' % (a[1], a[2])
		else:
			d = get_tag(data,'h1')
			hl = re.findall('<a  href="/holidays(?:/\d*?)+?" title=".+?">(.+?)</a>', data)
			if hl: msg = '%s:\n%s' % (d, '\n'.join(hl))
	else: msg = L('What?')
	if not msg: msg = L('Holiday: %s not found.') % text
	send_msg(type, jid, nick, msg)

global execute

execute = [(3, 'drink', to_drink, 2, L('Find holiday\ndrink [name_holiday/date]')),
		(3, 'calend', calend, 2, L('Find holiday\ncalend [name_holiday/date]'))]