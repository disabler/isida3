#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
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

horodb={L('aries'): '/aries/today', L('taurus'): '/taurus/today', L('gemini'): '/gemini/today', L('cancer'): '/cancer/today', L('leo'): '/leo/today', L('virgo'): '/virgo/today', L('libra'): '/libra/today', L('scorpio'): '/scorpio/today', L('sagittarius'): '/sagittarius/today', L('capricorn'): '/capricorn/today', L('aquarius'): '/aquarius/today', L('pisces'): '/pisces/today'}

def handler_horoscope(type, jid, nick, parameters):
  if parameters:
	if parameters=='list':
	  zod = [L('Aries'), L('Taurus'), L('Gemini'), L('Cancer'), L('Leo'), L('Virgo'), L('Libra'), L('Scorpio'), L('Sagittarius'), L('Capricorn'), L('Aquarius'), L('Pisces')]
	  send_msg(type, jid, nick, ', '.join(zod))
	  return
	if parameters=='date':
	  date = [L('Aries %s') % ('21.03-19.04'), L('Taurus %s') % ('20.04-20.05'), L('Gemini %s') % ('21.05-20.06'), L('Cancer %s') % ('21.06-22.07'), L('Leo %s') % ('23.07-22.08'), L('Virgo %s') % ('23.08-22.09'), L('Libra %s') % ('23.09-22.10'), L('Scorpio %s') % ('23.10-21.11'), L('Sagittarius %s') % ('22.11-21.12'), L('Capricorn %s') % ('22.12-19.01'), L('Aquarius %s') % ('20.01-18.02'), L('Pisces %s') % ('19.02-20.03')]
	  sp = ''
	  nm = 1
	  for tb in date:
		sp+=str(nm)+'. '+tb+'\n'
		nm+=1
	  if type=='groupchat':
		send_msg(type, jid, nick, L('Sent in private message'))
		send_msg('chat', jid, nick, L('List of dates:\n%s') % sp)
		return
	  send_msg('chat', jid, nick, L('List of dates:\n%s') % sp)
	  return
	if horodb.has_key(parameters.lower()):
	  target = html_encode(load_page('http://horo.mail.ru/prediction'+horodb[parameters.lower()]))
	  od = re.search('<div id="tm_today">',target)
	  message = target[od.end():]
	  message = message[:re.search('<div class="mb2">',message).start()]
	  message = rss_del_html(message)
	  message = rss_del_nn(message)
	  message = rss_replace(message)
	  message = message.replace('\n','')
	  if type=='groupchat':
		  send_msg(type,jid,nick,L('Message send to private'))
		  send_msg('chat',jid,nick,message)
		  return
	  send_msg('chat',jid,nick,message)
	else:
	  send_msg(type, jid, nick, L('What?'))
	  return
  else:
	send_msg(type,jid,nick,L('What?'))
	return

global execute

execute = [(3, 'horo', handler_horoscope, 2, L('Horoscope.\nhoro list - show all zodiacs.\nhoro date - show dates for zodiacs. | Author: ferym'))]
