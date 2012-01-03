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

backup_async = {}

def getMucItems(jid,affil,ns,back_id):
	iqid = get_id()
	if ns == NS_MUC_ADMIN: i = Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':affil})])])
	else: i = Node('iq', {'id': iqid, 'type': 'get', 'to':getRoom(jid)}, payload = [Node('query', {'xmlns': ns},[])])
	iq_request[iqid]=(time.time(),getMucItems_async,[ns,affil,back_id])
	sender(i)
	
def getMucItems_async(ns,affil,back_id,iq_stanza):
	global backup_async
	iq_stanza = iq_stanza[1][0]
	if ns == NS_MUC_ADMIN: backup_async[back_id][affil] = [[tmp.getAttr('jid'),['',tmp.getTagData('reason')][tmp.getTagData('reason') != None]] for tmp in iq_stanza.getTag('query',namespace=xmpp.NS_MUC_ADMIN).getTags('item')]
	else: backup_async[back_id]['room_config'] = [[tmp.getAttr('var'),tmp.getAttr('type'),tmp.getTagData('value')] for tmp in iq_stanza.getTag('query',namespace=xmpp.NS_MUC_OWNER).getTag('x',namespace=xmpp.NS_DATA).getTags('field')]

def make_stanzas_array(raw_back,jid,affil):
	stanza_array = []
	try: make_stanza_jid_count = get_config_int(jid,'make_stanza_jid_count')
	except: make_stanza_jid_count = 1
	for tmp in range(0,len(raw_back),make_stanza_jid_count):
		i = xmpp.Iq(typ='set',to=jid,xmlns=xmpp.NS_CLIENT)
		i.setTag('query',namespace=xmpp.NS_MUC_ADMIN)
		for t in raw_back[tmp:tmp+make_stanza_jid_count]:	
			i.getTag('query',namespace=xmpp.NS_MUC_ADMIN).\
					setTag('item',attrs={'affiliation':affil,'jid':t[0]}).\
					setTagData('reason',t[1])
		stanza_array.append(i)
	return stanza_array
	
def conf_backup(type, jid, nick, text):
	global backup_async,conn
	if len(text):
		text = text.split(' ')
		mode = text[0]

		if mode == 'show':
			a = os.listdir(back_folder)
			b = []
			for c in a:
				if 'conference' in c: b.append((c,os.path.getmtime(back_folder+c)))
			if len(b):
				msg = L('Available copies:') + ' '
				for c in b: msg += c[0]+' ('+un_unix(time.time()-c[1])+')'+', '
				msg = msg[:-2]
			else: msg = L('Backup copies not found.')
		elif mode == 'now':
			
			if get_xtype(jid) != 'owner': msg = L('I need an owner affiliation for backup settings!')
			else:
				back_id = get_id()
				backup_async[back_id] = {}
				getMucItems(jid,'outcast',NS_MUC_ADMIN,back_id)
				getMucItems(jid,'member',NS_MUC_ADMIN,back_id)
				getMucItems(jid,'admin',NS_MUC_ADMIN,back_id)
				getMucItems(jid,'owner',NS_MUC_ADMIN,back_id)
				getMucItems(jid,'',NS_MUC_OWNER,back_id)
				bst = GT('backup_sleep_time')
				while len(backup_async[back_id]) != 5 and not game_over: time.sleep(bst)
				iqid = get_id()
				i = Node('iq', {'id': iqid, 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'admin', 'jid':getRoom(str(selfjid))},[])])])
				sender(i)
				backup_async[back_id]['alias'] = [tmp[1:] for tmp in getFile(alfile,[]) if tmp[0]==jid]
				setup = getFile(c_file,{})
				try: backup_async[back_id]['bot_config'] = setup[jid]
				except: backup_async[back_id]['bot_config'] = ''
				cur_execute('select action,type,text,command,time from acl where jid=%s',(jid,))
				backup_async[back_id]['acl'] = cur.fetchall()
				backup_async[back_id]['rss'] = [tmp[0:4]+[tmp[5]] for tmp in getFile(feeds,[]) if tmp[4]==jid]
				
				msg = L('Copying completed!')
				msg += L('\nOwners: %s | Admins: %s | Members: %s | Banned: %s') % (\
					len(backup_async[back_id]['owner'])-1,\
					len(backup_async[back_id]['admin'])+1,\
					len(backup_async[back_id]['member']),\
					len(backup_async[back_id]['outcast']))
					
				msg += L('\nRoom config: %s | Bot config: %s | Aliases: %s | Acl\'s: %s | RSS: %s') % (\
					len(backup_async[back_id]['room_config']),\
					len(backup_async[back_id]['bot_config']),\
					len(backup_async[back_id]['alias']),\
					len(backup_async[back_id]['acl']),\
					len(backup_async[back_id]['rss']))

				writefile(back_folder+unicode(jid),json.dumps(backup_async[back_id]))

		elif mode == 'restore':
			if len(text)>1:
				if text[1] in os.listdir(back_folder):
					if get_xtype(jid) != 'owner': msg = L('I need an owner affiliation for restore settings!')
					else:
						bst = GT('backup_sleep_time')
						raw_back=json.loads(readfile(back_folder+unicode(text[1])))
						for tmp in ['outcast','member','admin','owner']:
							for t in make_stanzas_array(raw_back[tmp],jid,tmp):
								sender(t)
								time.sleep(bst)				
						i = xmpp.Iq(typ='set',to=jid,xmlns=xmpp.NS_CLIENT)
						i.setTag('query',namespace=xmpp.NS_MUC_OWNER)
						i.getTag('query',namespace=xmpp.NS_MUC_OWNER).setTag('x',namespace=xmpp.NS_DATA).setAttr('type','submit')
						for tmp in raw_back['room_config']:
							i.getTag('query',namespace=xmpp.NS_MUC_OWNER).getTag('x',namespace=xmpp.NS_DATA).\
								setTag('field',attrs={'var':tmp[0],'type':tmp[1]}).\
								setTagData('value',tmp[2])
						sender(i)
						time.sleep(bst)
						sender(Node('iq', {'id': get_id(), 'type': 'set', 'to':jid}, payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'admin', 'jid':getRoom(unicode(selfjid))},[])])]))
						time.sleep(bst)
						setup = getFile(c_file,{})
						setup[jid] = raw_back['bot_config']
						writefile(c_file,str(setup))
						aliases = getFile(alfile,[])
						for tmp in raw_back['alias']:
							if [jid]+tmp not in aliases: aliases.append([jid]+tmp)
						writefile(alfile,str(aliases))
						for tmp in raw_back['acl']:
							cur_execute('select action,type,text,command,time from acl where jid=%s and action=%s and type=%s and text=%s',(jid,tmp[0],tmp[1],tmp[2]))
							isit = cur.fetchall()
							if not isit: cur_execute('insert into acl values (%s,%s,%s,%s,%s,%s)', tuple([jid]+list(tmp)))
							conn.commit()
						feedbase = getFile(feeds,[])
						for tmp in raw_back['rss']:
							isit = False
							for t in feedbase:
								if t[0] == tmp[0] and t[4] == jid:
									isit = True
									break
							if not isit: feedbase.append(tmp[0:4]+[jid]+[tmp[4]])
						writefile(feeds,str(feedbase))
						msg = L('Restore completed.')
						msg += L('\nOwners: %s | Admins: %s | Members: %s | Banned: %s') % (\
							len(raw_back['owner'])-1,\
							len(raw_back['admin'])+1,\
							len(raw_back['member']),\
							len(raw_back['outcast']))

						msg += L('\nRoom config: %s | Bot config: %s | Aliases: %s | Acl\'s: %s | RSS: %s') % (\
							len(raw_back['room_config']),\
							len(raw_back['bot_config']),\
							len(raw_back['alias']),\
							len(raw_back['acl']),\
							len(raw_back['rss']))
				else: msg = L('Copy not found. Use key "show" for lisen available copies.')
			else: msg = L('What do you want to restore?')
		else: msg = L('Unknown item!')
	else: msg = 'backup now|show|restore'
	send_msg(type, jid, nick, msg)

global execute

execute = [(8, 'backup', conf_backup, 2, L('Backup/restore conference settings.\nbackup show|now|restore\nshow - show available copies\nnow - backup current conference\nrestore name_conference - restore settings name_conference in current conference'))]
