#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2013 Vit@liy <vitaliy@root.ua>                             #
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

def wot(type, jid, nick, text):
	text = text.strip()
	if text:
		text = text.split(' ', 1)
		if len(text) == 1:
			name, tank = text[0], ''
		else:
			name, tank = text[0], text[1].lower()
		data = load_page('http://worldoftanks.ru/uc/accounts/api/1.0/?source_token=WG-WoT_Assistant-1.1.2&search=%s&offset=0&limit=1' % name)
		try:
			data = json.loads(data)
		except:
			data = {'status': ''}
		if data['status'] == 'ok' and data['data']['items']:
			wotname = data['data']['items'][0]['name'] + ('[%s]' % data['data']['items'][0]['clan']['tag'] if data['data']['items'][0]['clan'] else '')
			if tank:
				if len(tank) == 1:
					msg = L('Use more characters in the name of the tank','%s/%s'%(jid,nick))
				else:
					try:
						wot_id = data['data']['items'][0]['id']
						data = load_page('http://worldoftanks.ru/community/accounts/%s/api/1.2/?source_token=WG-WoT_Assistant-test' % wot_id)
						data = json.loads(data)
						tanks = data['data']['vehicles']
						msg = '%s:' % wotname
						for t in tanks:
							if tank in t['name'].lower() or tank in t['localized_name'].lower():
								tank_win = t['win_count']
								tank_battle = t['battle_count']
								if tank_battle:
									msg += '\n%s (%s/%s - %s%%)' % (t['localized_name'], tank_win, tank_battle, round(100.0*tank_win/tank_battle, 2))
								else:
									msg += '\n%s (%s/%s)' % (t['localized_name'], tank_win, tank_battle)
						if not msg.count('\n'):
							msg += L(' not founded tank','%s/%s'%(jid,nick))
					except:
						msg = L('Impossible to get tanks\' statistics','%s/%s'%(jid,nick))
			else:
				
				wins = data['data']['items'][0]['stats']['wins']
				battles = data['data']['items'][0]['stats']['battles']
				
				if not battles:
					msg = '%s: %s/%s' % (wotname, wins, battles)
					
				else:
					try:
						wot_id = data['data']['items'][0]['id']
						data2 = load_page('http://worldoftanks.ru/community/accounts/%s/api/1.2/?source_token=WG-WoT_Assistant-test' % wot_id)
						data2 = json.loads(data2)
						win_percent = round(100.0 * wins / battles, 2)
						msg = '%s: %s/%s  (%s%%)' % (wotname, wins, battles, win_percent)
						
						np = int(win_percent) + 1
						np_int = int((np * battles - 100 * wins) / (100 - np) + 1)
						np05 = int(win_percent + 0.5) + 0.5
						np_round = int((np05 * battles - 100 * wins) / (100 - np05) + 1)
						
						msg += L('\nTo next win percent: %s battles', '%s/%s'%(jid,nick)) % np_int
						msg += L('\nTo next win percent (rounding): %s battles', '%s/%s'%(jid,nick)) % np_round

						avg_exp = data2['data']['ratings']['battle_avg_xp']['value']
						
						DAMAGE = data2['data']['ratings']['damage_dealt']['value'] / float(battles)
						msg += L('\nAv. damage: %s','%s/%s'%(jid,nick)) % int(round(DAMAGE))
						FRAGS = data2['data']['ratings']['frags']['value'] / float(battles)
						msg += L('\nAv. destroyed: %s','%s/%s'%(jid,nick)) % round(FRAGS, 2)
						SPOT = data2['data']['ratings']['spotted']['value'] / float(battles)
						msg += L('\nAv. spotted: %s','%s/%s'%(jid,nick)) % round(SPOT, 2)
						CAP = data2['data']['ratings']['ctf_points']['value'] / float(battles)
						msg += L('\nAv. captured points: %s','%s/%s'%(jid,nick)) % round(CAP, 2)
						DEF = data2['data']['ratings']['dropped_ctf_points']['value'] / float(battles)
						msg += L('\nAv. defense points: %s','%s/%s'%(jid,nick)) % round(DEF, 2)
						
						tanks = data2['data']['vehicles']
						s = sum([t['battle_count'] * t['level'] for t in tanks])
						TIER = s / float(battles)
						
						WINRATE = wins / float(battles)
						
						msg += L('\nAv. tank lvl: %s','%s/%s'%(jid,nick)) % round(TIER, 2)
						
						er = DAMAGE * (10 / (TIER + 2)) * (0.23 + 2 * TIER / 100) + FRAGS * 250 + SPOT * 150 + math.log(CAP + 1) / math.log(1.732) * 150 + DEF * 150
						
						if er < 420:
							er_xvm = 0
						else:
							er_xvm = max(min(er*(er*(er*(er*(er*(4.5254e-17*er - 3.3131e-13) + 9.4164e-10) - 1.3227e-6) + 9.5664e-4) - 0.2598) + 13.23, 100), 0)
						
						msg += L('\nEfficiency rating: %s (XVM: %s)','%s/%s'%(jid,nick)) % (int(round(er)), round(er_xvm, 1))
						
						if er < 630:
							msg += L(' - bad player','%s/%s'%(jid,nick))
						elif er < 860:
							msg += L(' - player below average','%s/%s'%(jid,nick))
						elif er < 1140:
							msg += L(' - average player','%s/%s'%(jid,nick))
						elif er < 1460:
							msg += L(' - good player','%s/%s'%(jid,nick))
						elif er < 1735:
							msg += L(' - great player','%s/%s'%(jid,nick))
						elif er >= 1735:
							msg += L(' - unicum','%s/%s'%(jid,nick))
						
						wn6 = (1240 - 1040 / math.pow((min(TIER, 6)), 0.164)) * FRAGS + DAMAGE * 530 / (184 * math.exp(0.24 * TIER) + 130) + SPOT * 125 + min(DEF, 2.2) * 100 + ((185 / (0.17 + math.exp((WINRATE * 100 - 35) * -0.134))) - 500) * 0.45 + (6 - min(TIER, 6)) * (-60)

						if wn6 > 2160:
							wn6_xvm = 100
						else:
							wn6_xvm = max(min(wn6*(wn6*(wn6*(-1.268e-11*wn6 + 5.147e-8) - 6.418e-5) + 7.576e-2) - 7.25, 100), 0)
						
						msg += L('\nWN6 rating: %s (XVM: %s)','%s/%s'%(jid,nick)) % (int(round(wn6)), round(wn6_xvm, 1))
						
						if er < 425:
							msg += L(' - bad player','%s/%s'%(jid,nick))
						elif er < 795:
							msg += L(' - player below average','%s/%s'%(jid,nick))
						elif er < 1175:
							msg += L(' - average player','%s/%s'%(jid,nick))
						elif er < 1570:
							msg += L(' - good player','%s/%s'%(jid,nick))
						elif er < 1885:
							msg += L(' - great player','%s/%s'%(jid,nick))
						elif er >= 1885:
							msg += L(' - unicum','%s/%s'%(jid,nick))
						
						armor = math.log(battles) / 10 * (avg_exp + DAMAGE * (WINRATE * 2 + FRAGS * 0.9 + (SPOT + CAP + DEF) * 0.5))
						
						msg += L('\nArmor-rating: %s','%s/%s'%(jid,nick)) % int(round(armor))
						try:
							s = load_page('http://proxy.bulychev.net:1333/?0,WN,%s' % name)
							TWR = re.search('TWR: ([\d+?\.]+?)%', s).group(1)
							msg += L('\nTrue Win Rate (TWR): %s%%','%s/%s'%(jid,nick)) % TWR
						except:
							pass
					except:
						msg = L('Impossible to get statistics','%s/%s'%(jid,nick))
		elif not data['status']:
			msg = L('Query error','%s/%s'%(jid,nick))
		else:
			msg = L('Player not found','%s/%s'%(jid,nick))
	else:
		msg = L('What?','%s/%s'%(jid,nick))
	send_msg(type,jid,nick,msg)

global execute

execute = [(3, 'wot', wot, 2, 'World of Tanks - info about user. Usage: wot nick [tank]')]
