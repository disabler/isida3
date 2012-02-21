#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida Jabber Bot                                                         #
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

from __future__ import with_statement
from xmpp import *
from random import *
from pdb import *
from subprocess import Popen, PIPE, STDOUT
from time import gmtime, localtime, sleep

import atexit
import calendar
import chardet
import datetime
import gc
import json
import hashlib
import htmlentitydefs
import httplib
import logging
import operator
import os
import math
import pdb
import psycopg2
import psycopg2.extensions
import random
import re
import select
import socket
import sqlite3
import subprocess
import string
import sys
import thread
import threading
import time
import urllib
import urllib2
import xmpp

global execute, prefix, comms, hashlib, trace

sema = threading.BoundedSemaphore(value=30)

class KThread(threading.Thread):
	def __init__(self, *args, **keywords):
		threading.Thread.__init__(self, *args, **keywords)
		self.killed = False

	def start(self):
		self.__run_backup = self.run
		self.run = self.__run
		threading.Thread.start(self)

	def __run(self):
		sys.settrace(self.globaltrace)
		self.__run_backup()
		self.run = self.__run_backup

	def globaltrace(self, frame, why, arg):
		if why == 'call': return self.localtrace
		else: return None

	def localtrace(self, frame, why, arg):
		if self.killed:
			if why == 'line': raise SystemExit()
		return self.localtrace

	def kill(self): self.killed = True

def cur_execute(*params):
	cur = conn.cursor()
	psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, cur)
	par = None
	try:
		cur.execute(*params)
		prm = params[0].split()[0].lower()
		if prm in ['update','insert','delete']: conn.commit()
	except Exception, par:
		if pg_debug:
			try: par = str(par)
			except: par = unicode(par)
		conn.rollback()
	cur.close()
	return par

def cur_execute_fetchone(*params):
	cur = conn.cursor()
	psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, cur)
	par = None
	try:
		cur.execute(*params)
		try: par = cur.fetchone()
		except Exception, par:
			if pg_debug:
				try: par = str(par)
				except: par = unicode(par)
	except Exception, par:
		if pg_debug:
			try: par = str(par)
			except: par = unicode(par)
		conn.rollback()
	cur.close()
	return par
	
def cur_execute_fetchall(*params):
	cur = conn.cursor()
	psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, cur)
	par = None
	try:
		cur.execute(*params)
		try: par = cur.fetchall()
		except Exception, par:
			if pg_debug:
				try: par = str(par)
				except: par = unicode(par)
	except Exception, par:
		if pg_debug:
			try: par = str(par)
			except: par = unicode(par)
		conn.rollback()
	cur.close()
	return par
	
def cur_execute_fetchmany(*params):
	cur = conn.cursor()
	psycopg2.extensions.register_type(psycopg2.extensions.UNICODE, cur)
	try:
		cur.execute(params[0],params[1])
		try: par = cur.fetchmany(params[-1])
		except: par = None
	except:
		conn.rollback()
		par = None
	cur.close()
	return par
	
def get_color(c):
	color = os.environ.has_key('TERM')
	colors = {'clear':'[0m','blue':'[34m','red':'[31m','magenta':'[35m','green':'[32m','cyan':'[36m','brown':'[33m','light_gray':'[37m','black':'[30m','bright_blue':'[34;1m','bright_red':'[31;1m','purple':'[35;1m','bright_green':'[32;1m','bright_cyan':'[36;1m','yellow':'[33;1m','dark_gray':'[30;1m','white':'[37;1m'}
	return ['','\x1b%s' % colors[c]][color]

def thr(func,param,name):
	global th_cnt, thread_error_count
	th_cnt += 1
	try:
		if thread_type:
			with sema:
				tmp_th = KThread(group=None,target=log_execute,name='%s_%s' % (str(th_cnt),name),args=(func,param))
				tmp_th.start()
		else: thread.start_new_thread(log_execute,(func,param))
	except SystemExit: pass
	except Exception, SM:
		try: SM = str(SM)
		except: SM = unicode(SM)
		if 'thread' in SM.lower(): thread_error_count += 1
		else: logging.exception(' [%s] %s' % (timeadd(tuple(time.localtime())),unicode(proc)))
		if thread_type:
			try: tmp_th.kill()
			except: pass

def log_execute(proc, params):
	try: proc(*params)
	except SystemExit: pass
	except: logging.exception(' [%s] %s' % (timeadd(tuple(time.localtime())),unicode(proc)))

def send_count(item):
	global message_out, presence_out, iq_out, unknown_out, last_stanza
	last_stanza = unicode(item)
	if last_stanza[:2] == '<m': message_out += 1
	elif last_stanza[:2] == '<p': presence_out += 1
	elif last_stanza[:2] == '<i': iq_out += 1
	else: unknown_out += 1
	cl.send(item)

def sender(item):
	global last_stream
	if last_stream != []: last_stream.append(item)
	else:
		time.sleep(time_nolimit)
		send_count(item)

'''
def sender(item):
	time.sleep(time_nolimit)
	send_count(item)
'''

'''def sender(item):
	global last_sender_activity
	while time.time() - last_sender_activity < time_nolimit: time.sleep(time_nolimit)
	last_sender_activity = time.time()
	send_count(item)
'''

def sender_stack():
	global last_stream
	last_item = {}
	while not game_over:
		if last_stream != []:
			time_tmp = time.time()
			tmp = last_stream[0]
			u_tmp = unicode(tmp)
			to_tmp = get_tag(u_tmp,'to')
			type_tmp = get_tag(u_tmp,'type')
			if type_tmp == 'groupchat':
				time_diff = time_tmp - last_item[to_tmp]
				last_item[to_tmp] == time_tmp
				if time_diff < time_limit: time.sleep(time_limit - time_diff)
				else: time.sleep(time_limit)
			else: time.sleep(time_nolimit)
			last_stream = last_stream[1:]
			send_count(tmp)
		else: time.sleep(1)

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

def getFile(filename,default):
	if os.path.isfile(filename):
		try: filebody = eval(readfile(filename))
		except:
			if os.path.isfile(filename+'.back'):
				while True:
					try:
						filebody = eval(readfile(filename+'.back'))
						break
					except: pass
			else:
				filebody = default
				writefile(filename,str(default))
	else:
		filebody = default
		writefile(filename,str(default))
	writefile(filename+'.back',str(filebody))
	return filebody

def get_config(room,item):
	setup = getFile(c_file,{})
	try: return setup[room][item]
	except:
		try: return config_prefs[item][3]
		except: return None

def get_config_int(room,item):
	setup = getFile(c_file,{})
	try: return int(setup[room][item])
	except: return int(config_prefs[item][3])

def get_config_float(room,item):
	setup = getFile(c_file,{})
	try: return float(setup[room][item])
	except: return float(config_prefs[item][3])

def put_config(room,item,value):
	setup = getFile(c_file,{})
	try: t = setup[room]
	except: setup[room] = {}
	setup[room][item] = value
	writefile(c_file,str(setup))

def GT(item):
	setup = getFile(ow_file,{})
	try: gt_result = setup[item]
	except:
		try: gt_result = owner_prefs[item][2]
		except: gt_result = None
	try: return eval(gt_result)
	except: return gt_result

def PT(item,value):
	setup = getFile(ow_file,{})
	setup[item] = value
	writefile(ow_file,str(setup))

def get_subtag(body,tag):
	T = re.findall('%s=\"(.*?)\"' % tag,body,re.S)
	if T: return T[0]
	else: return ''

def get_tag(body,tag):
	T = re.findall('<%s.*?>(.*?)</%s>' % (tag,tag),body,re.S)
	if T: return T[0]
	else: return ''

def get_tag_full(body,tag):
	T = re.findall('(<%s[^>]*?>|</%s>)' % (tag,tag),body,re.S)
	if T and len(T)==1: return T[0]
	elif len(T) >= 2 and T[0][1:len(tag)+1] == T[1][-len(tag)-1:-1]:
		T1 = re.findall('(%s.*?%s)' % (re.escape(T[0]),re.escape(T[1])),body,re.S)
		if T1: return T1[0]
		else: return ''
	elif len(T): return T[0]
	else: return ''

def get_tag_item(body,tag,item):
	body = get_tag_full(body,tag)
	return get_subtag(body,item)

def parser(t): return ''.join([['?',l][l<='~'] for l in unicode(t)])

def remove_sub_space(t): return ''.join([['?',l][l>=' ' or l in '\t\r\n'] for l in unicode(t)])

def smart_encode(text,enc):
	tx,splitter = '','|'
	while splitter in text: splitter += '|'
	ttext = text.replace('</','<%s/' % splitter).split(splitter)
	for tmp in ttext:
		try: tx += unicode(tmp,enc)
		except: pass
	return tx

def tZ(val): return '%02d' % val

def timeadd(lt): return '%02d.%02d.%02d %02d:%02d:%02d' % (lt[2],lt[1],lt[0],lt[3],lt[4],lt[5])

def onlytimeadd(lt): return '%02d:%02d:%02d' % (lt[3],lt[4],lt[5])

def pprint(*text):
	global last_logs_store
	if len(text) > 1: c,wc = get_color(text[1]),get_color('clear')
	else: c,wc = '',''
	text = text[0]
	lt = tuple(time.localtime())
	zz = parser('%s[%s]%s %s%s' % (wc,onlytimeadd(lt),c,text,wc))
	last_logs_store = ['[%s] %s' % (onlytimeadd(lt),text)] + last_logs_store[:last_logs_size]
	if dm2: print zz
	if CommandsLog:
		fname = '%s%02d%02d%02d.txt' % (slog_folder,lt[0],lt[1],lt[2])
		fbody = '%s|%s\n' % (onlytimeadd(lt),text)
		fl = open(fname, 'a')
		fl.write(fbody.encode('utf-8'))
		fl.close()

def send_presence_all(sm):
	pr=xmpp.Presence(typ='unavailable')
	pr.setStatus(sm)
	sender(pr)
	time.sleep(2)

def errorHandler(text):
	c,wc = get_color('bright_red'),get_color('clear')
	print('%s*** Error ***' % c)
	print('%s%s' % (c,text))
	print('%smore info at http://isida-bot.com%s' % (c,wc))
	sys.exit('exit')

def arr_semi_find(array, string):
	pos = 0
	for arr in array:
		if string.lower() in arr.lower(): break
		pos += 1
	if pos != len(array): return pos
	else: return -1

def arr_del_by_pos(array, position):
	return array[:position] + array[position+1:]

def arr_del_semi_find(array, string):
	pos = arr_semi_find(array, string)
	if pos >= 0: array = arr_del_by_pos(array,pos)
	return array

def get_joke(text):

	def joke_blond(text):
		b = ''
		cnt = randint(0,1)
		for tmp in text.lower():
			if cnt: b += tmp.upper()
			else: b += tmp
			cnt = not cnt
		return b

	def joke_upyachka(text):
		upch = [u'пыщь!!!111адын',u'ололололо!!11',u'ГОЛАКТЕКО ОПАСНОСТЕ!!11',u'ТЕЛОИД!!',u'ЖАЖА1!',u'ОНОТОЛЕЙ!!!!!',u'ПОТС ЗОХВАЧЕН11!!!',
				u'ПыЩЩЩЩЩЩЩЩЩь!!!!!!!1111',u'ПыЩЩЩЩЩЩЩЩЩь11111адинадин1адин']
		return '%s %s' % (text,choice(upch))

	def no_joke(text): return text

	jokes = [joke_blond,no_joke,joke_upyachka]
	return choice(jokes)(text)

def msg_validator(t): return ''.join([[l,'?'][l<' ' and l not in '\n\t\r'] for l in unicode(t)])

def message_exclude_update():
	global messages_excl
	excl = GT('exclude_messages').replace('\r','').replace('\t','').split('\n')
	messages_excl = []
	for c in excl:
		if '#' not in c and len(c): messages_excl.append(c)

def message_validate(item):
	if messages_excl:
		for c in messages_excl:
			cn = re.findall(c,' %s ' % item,re.I+re.S+re.U)
			for tmp in cn: item = item.replace(tmp,[GT('censor_text')*len(tmp),GT('censor_text')][len(GT('censor_text'))>1])
	return item

def send_msg(mtype, mjid, mnick, mmessage):
	global between_msg_last,time_limit
	if mmessage:
		mmessage = message_validate(mmessage)
		mnick = message_validate(mnick)
		while True:
			try: lm = between_msg_last[mjid]
			except: between_msg_last[mjid],lm = 0,0
			tt = time.time()
			if lm and tt-lm < time_limit: time.sleep(tt-lm)
			if between_msg_last[mjid]+time_limit <= time.time(): break
		between_msg_last[mjid] = time.time()
		# 1st april joke :)
		if time.localtime()[1:3] == (4,1): mmessage = get_joke(mmessage)
		no_send = True
		if len(mmessage) > msg_limit:
			cnt = 0
			maxcnt = int(len(mmessage)/msg_limit) + 1
			mmsg = mmessage
			while len(mmsg) > msg_limit:
				tmsg = u'[%s/%s] %s[…]' % (cnt+1,maxcnt,mmsg[:msg_limit])
				cnt += 1
				sender(xmpp.Message('%s/%s' % (mjid,mnick), tmsg, 'chat'))
				mmsg = mmsg[msg_limit:]
				time.sleep(1)
			tmsg = '[%s/%s] %s' % (cnt+1,maxcnt,mmsg)
			sender(xmpp.Message('%s/%s' % (mjid,mnick), tmsg, 'chat'))
			if mtype == 'chat': no_send = None
			else: mmessage = mmessage[:msg_limit] + u'[…]'
		if no_send:
			if mtype == 'groupchat' and mnick != '': mmessage = '%s: %s' % (mnick,mmessage)
			else: mjid += '/' + mnick
			while mmessage[-1:] in ['\n','\t','\r',' ']: mmessage = mmessage[:-1]
			mmessage = msg_validator(mmessage)
			if len(mmessage): sender(xmpp.Message(mjid, mmessage, mtype))

def os_version():
	iSys = sys.platform
	iOs = os.name
	isidaPyVer = '%s [%s]' % (sys.version.split(' (')[0],sys.version.split(')')[0].split(', ')[1])
	if iOs == 'posix':
		osInfo = os.uname()
		isidaOs = '%s (%s-%s) / Python %s' % (osInfo[0],osInfo[2],osInfo[4],isidaPyVer)
	elif iSys == 'win32':
		def get_registry_value(key, subkey, value):
			import _winreg
			key = getattr(_winreg, key)
			handle = _winreg.OpenKey(key, subkey)
			(value, type) = _winreg.QueryValueEx(handle, value)
			return value
		def get(key): return get_registry_value("HKEY_LOCAL_MACHINE", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",key)
		osInfo = get("ProductName")
		buildInfo = get("CurrentBuildNumber")
		try:
			spInfo = get("CSDVersion")
			isidaOs = '%s %s (Build: %s) / Python %s' % (osInfo,spInfo,buildInfo,isidaPyVer)
		except: isidaOs = '%s (Build: %s) / Python %s' % (osInfo,buildInfo,isidaPyVer)
	else: isidaOs = 'unknown'
	return isidaOs

def joinconf(conference, server, passwd):
	node = unicode(JID(conference.lower()).getResource())
	jid = JID(node=node, domain=server.lower(), resource=getResourse(Settings['jid']))
	if dm: cl = Client(jid.getDomain())
	else: cl = Client(jid.getDomain(), debug=[])
	conf = unicode(JID(conference))
	return join(conf,passwd)

def leaveconf(conference, server, sm):
	node = unicode(JID(conference).getResource())
	jid = JID(node=node, domain=server)
	if dm: cl = Client(jid.getDomain())
	else: cl = Client(jid.getDomain(), debug=[])
	conf = unicode(JID(conference))
	leave(conf, sm)
	time.sleep(0.1)

def caps_and_send(tmp):
	tmp.setTag('c', namespace=NS_CAPS, attrs={'node':capsNode,'ver':capsVersion})
	sender(tmp)

def join(conference,passwd):
	global pres_answer,cycles_used,cycles_unused
	id = get_id()
	if Settings['status'] == 'online': j = Node('presence', {'id': id, 'to': conference}, payload = [Node('status', {},[Settings['message']]),\
																									 Node('priority', {},[Settings['priority']])])
	else: j = Node('presence', {'id': id, 'to': conference}, payload = [Node('show', {},[Settings['status']]),\
																		Node('status', {},[Settings['message']]),\
																		Node('priority', {},[Settings['priority']])])
	j.setTag('x', namespace=NS_MUC).addChild('history', {'maxchars':'0', 'maxstanzas':'0'})
	j.getTag('x').setTagData('password', passwd)
	caps_and_send(j)
	answered, Error, join_timeout = None, None, 3
	if is_start: join_timeout_delay = 0.3
	else: join_timeout_delay = 1
	while not answered and join_timeout >= 0 and not game_over:
		if is_start:
			cyc = cl.Process(1)
			if str(cyc) == 'None': cycles_unused += 1
			elif int(str(cyc)): cycles_used += 1
			else: cycles_unused += 1
		else: time.sleep(join_timeout_delay)
		join_timeout -= join_timeout_delay
		for tmp in pres_answer:
			if tmp[0]==id:
				Error = tmp[1]
				pres_answer.remove(tmp)
				answered = True
				break
	return Error

def leave(conference, sm):
	j = Presence(conference, 'unavailable', status=sm)
	sender(j)

def muc_filter_action(act,jid,room,reason):
	if act in ['visitor','kick']:
		nick = get_nick_by_jid(room,getRoom(jid))
		if nick and act=='visitor': sender(Node('iq',{'id': get_id(), 'type': 'set', 'to':room},payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'role':'visitor', 'nick':nick},[Node('reason',{},reason)])])]))
		elif nick and act=='kick': sender(Node('iq',{'id': get_id(), 'type': 'set', 'to':room},payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'role':'none', 'nick':nick},[Node('reason',{},reason)])])]))
		elif not nick and act=='visitor': sender(Node('iq',{'id': get_id(), 'type': 'set', 'to':room},payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'role':'visitor', 'jid':jid},[Node('reason',{},reason)])])]))
		elif not nick and act=='kick': sender(Node('iq',{'id': get_id(), 'type': 'set', 'to':room},payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'role':'none', 'jid':jid},[Node('reason',{},reason)])])]))
	elif act=='ban': sender(Node('iq',{'id': get_id(), 'type': 'set', 'to':room},payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'outcast', 'jid':jid},[Node('reason',{},reason)])])]))
	return None

def paste_text(text,room,jid):
	nick = get_nick_by_jid_res(room,jid)
	if GT('html_paste_enable'): text = html_escape(text)
	paste_header = ['','<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><link href="%s" rel="stylesheet" type="text/css" /><title>\n' % paste_css_path][GT('html_paste_enable')]
	url = '%s%s' % (str(hex(int(time.time()*100)))[2:-1],['.txt','.html'][GT('html_paste_enable')])
	lt = tuple(time.localtime())
	ott = onlytimeadd(tuple(time.localtime()))
	paste_body = ['%s','<p><span class="paste">%s</span></p>\n'][GT('html_paste_enable')] % (text)
	lht = '%s [%s] - %02d/%02d/%02d %02d:%02d:%02d' % (nick,room,lt[0],lt[1],lt[2],lt[3],lt[4],lt[5])
	paste_he = ['%s\t\thttp://isida-bot.com\n\n' % lht,'%s%s</title></head><body><div class="main"><div class="top"><div class="heart"><a href="http://isida-bot.com">http://isida-bot.com</a></div><div class="conference">%s</div></div><div class="container">\n' % (paste_header,lht,lht)][GT('html_paste_enable')]
	fl = open(pastepath+url, 'a')
	fl.write(paste_he.encode('utf-8'))
	fl.write(paste_body.encode('utf-8'))
	paste_ender = ['','</div></div></body></html>'][GT('html_paste_enable')]
	fl.write(paste_ender.encode('utf-8'))
	fl.close()
	return pasteurl+url

def disp_time(t):
	lt=tuple(time.localtime(t))
	return '%02d:%02d:%02d, %02d.%s\'%02d, %s' % (lt[3],lt[4],lt[5],lt[2],wmonth[lt[1]-1],lt[0],wday[lt[6]])
	
def nice_time(ttim):
	gt=tuple(time.gmtime())
	lt=tuple(time.localtime(ttim))
	timeofset = int(round(int(time.mktime(lt[:5]+(0,0,0,0))-time.mktime(gt[:5]+(0,0,0,0)))/3600.0))
	if timeofset < 0: t_gmt = 'GMT%s' % timeofset
	else: t_gmt = 'GMT+%s' % timeofset
	t_utc='%02d%02d%02dT%02d:%02d:%02d' % (gt[0],gt[1],gt[2],gt[3],gt[4],gt[5])
	t_display = '%02d:%02d:%02d, %02d.%s\'%02d, %s, ' % (lt[3],lt[4],lt[5],lt[2],wmonth[lt[1]-1],lt[0],wday[lt[6]])
	#t_tz = time.tzname[time.localtime()[8]]
	#enc = chardet.detect(t_tz)['encoding']
	#if t_tz == None: body = ''
	#if enc == None or enc == '' or enc.lower() == 'unicode': enc = 'utf-8'
	#t_tz = unicode(t_tz,enc)
	#t_display += '%s, %s' % (t_tz,t_gmt)
	#return t_utc,t_tz,t_display
	t_display += t_gmt
	return t_utc,t_gmt,t_display

def get_valid_tag(body,tag):
	if tag in body: return get_subtag(body,tag)
	else: return 'None'

def get_eval_item(mess,string):
	try:
		result = eval('mess.%s' % string)
		if result: return result.encode('utf-8')
	except: pass
	return ''

def match_for_raw(original,regexp,gr):
	orig_drop = orig_reg = re.findall(regexp, original.replace('\n',' '), re.S+re.U+re.I)
	while '' in orig_drop: orig_drop.remove('')
	orig_join = ''.join(orig_reg)
	if orig_join:
		#orig_split = original.split()
		#match_percent = 100.0 / len(original) * len(orig_join)
		#match_percent = 100.0 / len(orig_drop) * len(orig_split)
		match_percent = 100.0 / len(orig_drop) * sum([len(tmp) <= 2 for tmp in orig_drop])
		
		raw_percent = get_config(gr,'muc_filter_raw_percent')
		if raw_percent.isdigit(): raw_percent = int(raw_percent)
		else: raw_percent = int(config_prefs['muc_filter_raw_percent'][3])
		return ['',orig_join][match_percent >= raw_percent]
	else: return ''

def iqCB(sess,iq):
	global timeofset, iq_in, iq_request, last_msg_base, last_msg_time_base, ddos_ignore, ddos_iq, user_hash, server_hash, server_hash_list
	global disco_excl, message_excl
	iq_in += 1
	id = iq.getID()
	if id == None: return None
	room = unicode(iq.getFrom())
	if getRoom(room) in ownerbase: towh = selfjid
	else: towh = '%s/%s' % (getRoom(room),get_nick_by_jid_res(getRoom(room), selfjid))
	query = iq.getTag('query')
	was_request = id in iq_request
	al,tjid = get_level(getRoom(room),getResourse(room))
	acclvl = al >= 7 and GT('iq_disco_enable')
	nnj,tjid = False,getRoom(tjid)
	if room == selfjid: nnj = True
	else:
		for tmp in megabase:
			if '%s/%s' % tuple(tmp[0:2]) == room:
				nnj = True
				break

	if getServer(Settings['jid']) == room: nnj = True

	if iq.getType()=='error' and was_request:
		iq_err,er_name = get_tag(unicode(iq),'error').replace('\n',''),L('Unknown error!')
		detect_error = False
		for tmp in iq_error.keys():
			if tmp in iq_err:
				er_name = '%s %s!' % (L('Error!'),iq_error[tmp])
				detect_error = True
				break
		if not detect_error:
			if iq_err: er_name = '%s %s!' % (L('Error!'),iq_err)
			else: er_name = '%s %s!' % (L('Error!'),er_name)
		iq_async(id,time.time(),er_name,'error')

	elif iq.getType()=='result' and was_request:
		is_vcard = iq.getTag('vCard')
		if is_vcard: iq_async(id,time.time(), unicode(is_vcard))
		else:
			try: nspace = query.getNamespace()
			except: nspace = 'None'
			if nspace == NS_MUC_ADMIN: iq_async(id,time.time(),iq)
			elif nspace == NS_MUC_OWNER: iq_async(id,time.time(),iq)
			elif nspace == NS_VERSION:
				ver_client = query.getTagData(tag='name')
				ver_version = query.getTagData(tag='version')
				ver_os = query.getTagData(tag='os')
				for t in [ver_client,ver_version,ver_os]:
					if not t: t = 'None'
				t = cur_execute_fetchone('select * from versions where room=%s and jid=%s and client=%s and version=%s and os=%s',(getRoom(room),tjid,ver_client,ver_version,ver_os))
				if not t: cur_execute('insert into versions values (%s,%s,%s,%s,%s,%s)',(getRoom(room),tjid,ver_client,ver_version,ver_os,int(time.time())))
				iq_async(id,time.time(),ver_client,ver_version,ver_os)
			elif nspace == NS_TIME: iq_async(id,time.time(),query.getTagData(tag='display'),query.getTagData(tag='utc'),query.getTagData(tag='tz'))
			elif iq.getTag('time',namespace=xmpp.NS_URN_TIME): iq_async(id,time.time(),iq.getTag('time').getTagData(tag='utc'),iq.getTag('time').getTagData(tag='tzo'))
			elif iq.getTag('ping',namespace=xmpp.NS_URN_PING): iq_async(id,time.time(),unicode(iq))
			else: iq_async(id,time.time(),unicode(iq),iq)

	elif iq.getType()=='get' and nnj and not ddos_ignore.has_key(tjid):
		iq_ddos_requests,iq_ddos_limit = GT('ddos_iq_requests'),GT('ddos_iq_limit')
		nick = getResourse(room)		
		qry = unicode(iq.getTag(name='query'))
		if ddos_iq.has_key(tjid): time_tuple = [time.time()] + ddos_iq[tjid][:iq_ddos_requests-1]
		else: time_tuple = [time.time()]
		ddos_iq[tjid] = time_tuple
		if len(time_tuple) == iq_ddos_requests and (time_tuple[0]-time_tuple[-1]) < iq_ddos_limit:
			ddos_ignore[tjid] = [getRoom(room),nick,time.time()+GT('ddos_limit')[al]]
			pprint('!!! IQ-DDOS Detect: %s %s [%s] %s' % (al, room, tjid, qry),'bright_red')
			return

		if iq.getTag(name='query', namespace=xmpp.NS_VERSION) and GT('iq_version_enable'):
			pprint('*** iq:version from %s' % unicode(room),'magenta')
			i=xmpp.Iq(to=room, typ='result')
			i.setAttr(key='id', val=id)
			i.setQueryNS(namespace=xmpp.NS_VERSION)
			i.getTag('query').setTagData(tag='name', val=botName)
			i.getTag('query').setTagData(tag='version', val=botVersion)
			i.getTag('query').setTagData(tag='os', val=botOs)
			sender(i)
			raise xmpp.NodeProcessed

		elif iq.getTag(name='query', namespace=xmpp.NS_TIME) and GT('iq_time_enable'):
			pprint('*** iq:time from %s' % unicode(room),'magenta')
			t_utc,t_tz,t_display = nice_time(time.time())
			i=xmpp.Iq(to=room, typ='result')
			i.setAttr(key='id', val=id)
			i.setQueryNS(namespace=xmpp.NS_TIME)
			i.getTag('query').setTagData(tag='utc', val=t_utc)
			i.getTag('query').setTagData(tag='tz', val=t_tz)
			i.getTag('query').setTagData(tag='display', val=t_display)
			sender(i)
			raise xmpp.NodeProcessed

		elif iq.getTag(name='time', namespace=xmpp.NS_URN_TIME) and GT('iq_time_enable'):
			pprint('*** iq:urn:time from %s' % unicode(room),'magenta')
			if timeofset in [-12,-11,-10]: t_tz = '-%s:00' % timeofset
			elif timeofset in range(-9,-1): t_tz = '-0%s:00' % timeofset
			elif timeofset in range(0,9): t_tz = '+0%s:00' % timeofset
			else: t_tz = '+%s:00' % timeofset
			i=xmpp.Iq(to=room, typ='result')
			i.setAttr(key='id', val=id)
			i.setTag('time',namespace=xmpp.NS_URN_TIME)
			i.getTag('time').setTagData(tag='tzo', val=t_tz)
			i.getTag('time').setTagData(tag='utc', val=str(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
			sender(i)
			raise xmpp.NodeProcessed

		elif iq.getTag(name='ping', namespace=xmpp.NS_URN_PING) and GT('iq_ping_enable'):
			pprint('*** iq:urn:ping from %s' % unicode(room),'magenta')
			i=xmpp.Iq(to=room, typ='result')
			i.setAttr(key='id', val=id)
			sender(i)
			raise xmpp.NodeProcessed

		elif iq.getTag(name='query', namespace=xmpp.NS_LAST) and GT('iq_uptime_enable'):
			pprint('*** iq:uptime from %s' % unicode(room),'magenta')
			i=xmpp.Iq(to=room, typ='result')
			i.setAttr(key='id', val=id)
			i.setTag('query',namespace=xmpp.NS_LAST,attrs={'seconds':str(int(time.time())-starttime)})
			i.setTagData('query','%s (%s) [%s]' % (Settings['message'],Settings['status'],Settings['priority']))
			sender(i)
			raise xmpp.NodeProcessed

		elif iq.getTag(name='query', namespace=xmpp.NS_DISCO_INFO):
			node=get_tag_item(unicode(query),'query','node')
			if node.split('#')[0] in ['', disco_config_node, xmpp.NS_COMMANDS]:
				pprint('*** iq:disco_info from %s node "%s"' % (unicode(room),node),'magenta')
				i=xmpp.Iq(to=room, typ='result')
				i.setAttr(key='id', val=id)
				if node == '': i.setQueryNS(namespace=xmpp.NS_DISCO_INFO)
				else: i.setTag('query',namespace=xmpp.NS_DISCO_INFO,attrs={'node':node})
				i.getTag('query').setTag('feature',attrs={'var':xmpp.NS_DISCO_INFO})
				i.getTag('query').setTag('feature',attrs={'var':xmpp.NS_DISCO_ITEMS})
				i.getTag('query').setTag('feature',attrs={'var':xmpp.NS_COMMANDS})
				i.getTag('query').setTag('feature',attrs={'var':disco_config_node})
				if node == '':
					i.getTag('query').setTag('identity',attrs={'category':'client','type':'bot','name':'iSida Jabber Bot'})
					sender(i)
					raise xmpp.NodeProcessed

				elif node.split('#')[0] == disco_config_node or node == xmpp.NS_COMMANDS:
					i.getTag('query').setTag('feature',attrs={'var':xmpp.NS_COMMANDS})
					i.getTag('query').setTag('feature',attrs={'var':disco_config_node})
					try: tn = '#' + node.split('#')[1]
					except: tn = ''
					if tn:
						if tn.split('-',1)[0] == '#owner': settz = owner_groups
						elif tn.split('-',1)[0] == '#room': settz = config_groups
						else: settz = None
						if settz:
							for tmp in settz:
								if tn == tmp[1]:
									i.getTag('query').setTag('identity',attrs={'category':'automation','type':'command-node','name':tmp[0]})
									break
					sender(i)
					raise xmpp.NodeProcessed

		elif iq.getTag(name='query', namespace=xmpp.NS_DISCO_ITEMS) and acclvl:
			node=get_tag_item(unicode(query),'query','node')
			pprint('*** iq:disco_items from %s node "%s"' % (unicode(room),node),'magenta')
			if node.split('#')[0] in [disco_config_node, xmpp.NS_COMMANDS]:
				try: tn = '#' + node.split('#')[1]
				except: tn = ''
				i=xmpp.Iq(to=room, typ='result')
				i.setAttr(key='id', val=id)
				if node == '': i.setQueryNS(namespace=xmpp.NS_DISCO_ITEMS)
				else: i.setTag('query',namespace=xmpp.NS_DISCO_ITEMS,attrs={'node':node})
				if node == '' or node == xmpp.NS_COMMANDS:
					if towh == selfjid: settings_set = owner_groups
					else: settings_set = config_groups
					for tmp in settings_set: i.getTag('query').setTag('item',attrs={'node':disco_config_node+tmp[1], 'name':tmp[0],'jid':towh})
				sender(i)
				raise xmpp.NodeProcessed
			elif node == '':
				i=xmpp.Iq(to=room, typ='result')
				i.setAttr(key='id', val=id)
				i.setQueryNS(namespace=xmpp.NS_DISCO_ITEMS)
				i.getTag('query').setTag('item',attrs={'node':xmpp.NS_COMMANDS, 'name':L('AD-Hoc commands'),'jid':towh})
				sender(i)
				raise xmpp.NodeProcessed

	elif iq.getType()=='set':
		if iq.getTag(name='command', namespace=xmpp.NS_COMMANDS) and acclvl:
			node=get_tag_item(unicode(iq),'command','node')
			if get_tag_item(unicode(iq),'command','action') == 'execute' and node.split('#')[0] in ['', disco_config_node, xmpp.NS_COMMANDS]:
				pprint('*** iq:ad-hoc commands from %s node "%s"' % (unicode(room),node),'magenta')
				i=xmpp.Iq(to=room, typ='result')
				i.setAttr(key='id', val=id)
				if node == '': i.setQueryNS(namespace=xmpp.NS_DISCO_INFO)
				else: i.setTag('query',namespace=xmpp.NS_DISCO_INFO,attrs={'node':node})
				i.getTag('query').setTag('feature',attrs={'var':xmpp.NS_DISCO_INFO})
				i.getTag('query').setTag('feature',attrs={'var':xmpp.NS_DISCO_ITEMS})
				i.getTag('query').setTag('feature',attrs={'var':xmpp.NS_COMMANDS})
				i.getTag('query').setTag('feature',attrs={'var':disco_config_node})
				if node == '':
					i.getTag('query').setTag('identity',attrs={'category':'client','type':'bot','name':'iSida Jabber Bot'})
					sender(i)
					raise xmpp.NodeProcessed

				elif node.split('#')[0] == disco_config_node or node == xmpp.NS_COMMANDS:
					i.getTag('query').setTag('feature',attrs={'var':xmpp.NS_COMMANDS})
					i.getTag('query').setTag('feature',attrs={'var':disco_config_node})
					try: tn = '#' + node.split('#')[1]
					except: tn = ''
					try: tmpn = tn.split('-',1)[1]
					except: tmpn = ''
					if tmpn:
						action=get_tag_item(unicode(iq),'command','action')
						i=xmpp.Iq(to=room, typ='result')
						i.setAttr(key='id', val=id)
						if action == 'cancel': i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'canceled', 'node':disco_config_node+tn,'sessionid':id})
						elif towh == selfjid:
							if get_tag_item(unicode(iq),'x','type') == 'submit':
								varz = iq.getTag('command').getTag('x')
								sucess_label,unsucess = True,[]
								for t in owner_prefs.keys():
									try:
										tp = owner_prefs[t][1]
										tm = varz.getTag('field',attrs={'var':t}).getTags('value')
										tm = '\n'.join([tm2.getData() for tm2 in tm])
										old_tm = GT(t)
										try:
											if   tp[0] == 'b': tm = [False,True][int(tm)]
											elif tp[0] == 'f': tm = float(tm)
											elif tp[0] == 'i': tm = int(tm)
											elif tp[0] == 't': tm = tm[:int(tp.replace('e','')[1:])]
											elif tp[0] == 'm': tm = tm[:int(tp.replace('e','')[1:])]
											elif tp[0] == 'l' and len(json.loads(tm)) == int(tp.replace('e','')[1:]): tm = json.loads(tm)
											elif tp[0] == 'd' and tm not in owner_prefs[t][3]: tm = owner_prefs[t][2]
										except:
											tm,sucess_label = GT(t),False
											unsucess.append(owner_prefs[t][0])
										PT(t,tm)
										if tp[-1] == 'e' and old_tm != tm: eval(owner_prefs[t][-1])
									except: pass										
								sucess_answer = [L('Settings unsuccesfully accepted:\n%s') % '\n'.join(unsucess),L('Settings succesfully accepted')][sucess_label]
								i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'completed', 'node':disco_config_node+tn,'sessionid':id})						
								i.getTag('command').setTag('note',attrs={'type':'info'})
								i.getTag('command').setTagData('note',sucess_answer)
								i.getTag('command').setTag('x',namespace=xmpp.NS_DATA)
								i.getTag('command').getTag('x').setTagData('title',L('Settings'))
								i.getTag('command').getTag('x').setTagData('instrustion',sucess_answer)
								pprint('*** bot reconfigure by %s' % unicode(room),'purple')
							else:
								i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'executing', 'node':disco_config_node+tn,'sessionid':id})
								i.getTag('command').setTag('x',namespace=xmpp.NS_DATA,attrs={'type':'form'})
								#i.getTag('command').getTag('x').setTag('item',attrs={'node':disco_config_node+tn, 'name':'Configuration','jid':selfjid})
								#i.getTag('command').getTag('x').setTagData('instructions',L('For configure required x:data-compatible client'))
								tkeys = []
								for tmp in owner_groups: tkeys.append(tmp[1])
								if tn in tkeys:
									for tmp in owner_groups:
										if tn == tmp[1]:
											c_prefs,c_name = tmp[2],tmp[0]
											break
									i.getTag('command').getTag('x').setTagData('title',c_name)
									cnf_prefs = {}
									for tmp in c_prefs: cnf_prefs[tmp] = owner_prefs[tmp]
									tmp = cnf_prefs.keys()
									tt = []
									for t in tmp: tt.append((owner_prefs[t][0],t))
									tt.sort()
									tmp = []
									for t in tt: tmp.append(t[1])
									for t in tmp:
										itm = owner_prefs[t]
										itm_label = itm[0].replace('%s','').replace(':','').strip()
										if itm[1][0] == 'b':
											dc = GT(t) in [True,1,'1','on']
											i.getTag('command').getTag('x').setTag('field',attrs={'type':'boolean','label':itm_label,'var':t})\
											.setTagData('value',[0,1][dc])
										elif itm[1][0] in ['t','i','f','l']:
											i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-single','label':itm_label,'var':t})\
											.setTagData('value',unicode(GT(t)))
										elif itm[1][0] == 'm':
											tprm = [xmpp.Node('value',payload=prm) for prm in unicode(GT(t)).split('\n')]											
											i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-multi','label':itm_label,'var':t})\
											.setPayload(tprm)
										else:
											i.getTag('command').getTag('x').setTag('field',\
											attrs={'type':'list-single','label':itm_label,'var':t})\
											.setTagData('value',GT(t))
											for t2 in itm[3]:
												i.getTag('command').getTag('x').getTag('field',\
												attrs={'type':'list-single','label':itm_label,'var':t})\
												.setTag('option',attrs={'label':L(t2)})\
												.setTagData('value',t2)
						else:
							if get_tag_item(unicode(iq),'x','type') == 'submit':
								varz = iq.getTag('command').getTag('x')
								for t in config_prefs.keys():
									try:
										tmtype = varz.getTagAttr('field','type')
										tm = varz.getTag('field',attrs={'var':t}).getTags('value')
										tm = '\n'.join([tm2.getData() for tm2 in tm])
										if tmtype == 'boolean' and tm in ['0','1']: tm = [False,True][int(tm)]
										elif config_prefs[t][2] != None:
											if config_prefs[t][2] == [True,False] and tm in ['0','1']: tm = [False,True][int(tm)]
											elif tm in config_prefs[t][2]: pass
											else: tm = config_prefs[t][3]
										put_config(getRoom(room),t,tm)
									except: pass
								sucess_answer = L('Settings succesfully accepted')
								i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'completed', 'node':disco_config_node+tn,'sessionid':id})
								i.getTag('command').setTag('note',attrs={'type':'info'})
								i.getTag('command').setTagData('note',sucess_answer)
								i.getTag('command').setTag('x',namespace=xmpp.NS_DATA)
								i.getTag('command').getTag('x').setTagData('title',L('Settings'))
								i.getTag('command').getTag('x').setTagData('instrustion',sucess_answer)
								pprint('*** reconfigure by %s' % unicode(room),'purple')
							else:
								i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'executing', 'node':disco_config_node+tn,'sessionid':id})
								i.getTag('command').setTag('x',namespace=xmpp.NS_DATA,attrs={'type':'form'})
								#i.getTag('command').getTag('x').setTag('item',attrs={'node':disco_config_node+tn, 'name':'Configuration','jid':selfjid})
								#i.getTag('command').getTag('x').setTagData('instructions',L('For configure required x:data-compatible client'))
								tkeys = []
								for tmp in config_groups: tkeys.append(tmp[1])
								if tn in tkeys:
									for tmp in config_groups:
										if tn == tmp[1]:
											c_prefs,c_name = tmp[2],tmp[0]
											break
									i.getTag('command').getTag('x').setTagData('title',c_name)
									cnf_prefs = {}
									for tmp in c_prefs: cnf_prefs[tmp] = config_prefs[tmp]
									tmp = cnf_prefs.keys()
									tmp.sort()
									for t in tmp:
										itm = config_prefs[t]
										itm_label = itm[0].replace('%s','').replace(':','').strip()
										if itm[2] == [True,False]:
											dc = get_config(getRoom(room),t) in [True,1,'1','on']
											i.getTag('command').getTag('x').setTag('field',attrs={'type':'boolean','label':itm_label,'var':t})\
											.setTagData('value',[0,1][dc])
										elif itm[2] == None:
											if '\n' in itm[3]:
												tprm = [xmpp.Node('value',payload=prm) for prm in get_config(getRoom(room),t).split('\n')]											
												i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-multi','label':itm_label,'var':t})\
												.setPayload(tprm)
											else:
												i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-single','label':itm_label,'var':t})\
												.setTagData('value',get_config(getRoom(room),t))
										else:
											i.getTag('command').getTag('x').setTag('field',\
											attrs={'type':'list-single','label':itm_label,'var':t})\
											.setTagData('value',get_config(getRoom(room),t))

											for t2 in itm[2]:
												i.getTag('command').getTag('x').getTag('field',\
												attrs={'type':'list-single','label':itm_label,'var':t})\
												.setTag('option',attrs={'label':onoff(t2)})\
												.setTagData('value',t2)
								else: i.getTag('command').getTag('x').setTagData('title',L('Unknown configuration request!'))
						sender(i)
						raise xmpp.NodeProcessed
					else:
						if tn:
							if tn.split('-',1)[0] == '#owner': settz = owner_groups
							elif tn.split('-',1)[0] == '#room': settz = config_groups
							else: settz = None
							if settz:
								for tmp in settz:
									if tn == tmp[1]:
										i.getTag('query').setTag('identity',attrs={'category':'automation','type':'command-node','name':tmp[0]})
										break
						sender(i)
						raise xmpp.NodeProcessed

			else:
				pprint('*** iq:disco_set from %s node "%s"' % (unicode(room),node),'magenta')
				try: tn = '#' + node.split('#')[1]
				except: tn = ''
				if node.split('#')[0] == disco_config_node or node == xmpp.NS_COMMANDS:
					action=get_tag_item(unicode(iq),'command','action')
					i=xmpp.Iq(to=room, typ='result')
					i.setAttr(key='id', val=id)
					if action == 'cancel': i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'canceled', 'node':disco_config_node+tn,'sessionid':id})
					elif towh == selfjid:
						if get_tag_item(unicode(iq),'x','type') == 'submit':
							varz = iq.getTag('command').getTag('x')
							sucess_label,unsucess = True,[]
							for t in owner_prefs.keys():
								try:
									tp = owner_prefs[t][1]
									tm = varz.getTag('field',attrs={'var':t}).getTags('value')
									tm = '\n'.join([tm2.getData() for tm2 in tm])
									old_tm = GT(t)
									try:
										if   tp[0] == 'b': tm = [False,True][int(tm)]
										elif tp[0] == 'f': tm = float(tm)
										elif tp[0] == 'i': tm = int(tm)
										elif tp[0] == 't': tm = tm[:int(tp.replace('e','')[1:])]
										elif tp[0] == 'm': tm = tm[:int(tp.replace('e','')[1:])]
										elif tp[0] == 'l' and len(json.loads(tm)) == int(tp.replace('e','')[1:]): tm = json.loads(tm)
										elif tp[0] == 'd' and tm not in owner_prefs[t][3]: tm = owner_prefs[t][2]
									except:
										tm,sucess_label = GT(t),False
										unsucess.append(owner_prefs[t][0])
									PT(t,tm)
									if tp[-1] == 'e' and old_tm != tm: eval(owner_prefs[t][-1])
								except: pass
							sucess_answer = [L('Settings unsuccesfully accepted:\n%s') % '\n'.join(unsucess),L('Settings succesfully accepted')][sucess_label]
							i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'completed', 'node':disco_config_node+tn,'sessionid':id})
							i.getTag('command').setTag('note',attrs={'type':'info'})
							i.getTag('command').setTagData('note',sucess_answer)
							i.getTag('command').setTag('x',namespace=xmpp.NS_DATA)
							i.getTag('command').getTag('x').setTagData('title',L('Settings'))
							i.getTag('command').getTag('x').setTagData('instrustion',sucess_answer)
							pprint('*** bot reconfigure by %s' % unicode(room),'purple')
						else:
							i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'executing', 'node':disco_config_node+tn,'sessionid':id})
							i.getTag('command').setTag('x',namespace=xmpp.NS_DATA,attrs={'type':'form'})
							#i.getTag('command').getTag('x').setTag('item',attrs={'node':disco_config_node+tn, 'name':'Configuration','jid':selfjid})
							#i.getTag('command').getTag('x').setTagData('instructions',L('For configure required x:data-compatible client'))
							tkeys = []
							for tmp in owner_groups: tkeys.append(tmp[1])
							if tn in tkeys:
								for tmp in owner_groups:
									if tn == tmp[1]:
										c_prefs,c_name = tmp[2],tmp[0]
										break
								i.getTag('command').getTag('x').setTagData('title',c_name)
								cnf_prefs = {}
								for tmp in c_prefs: cnf_prefs[tmp] = owner_prefs[tmp]
								tmp = cnf_prefs.keys()
								tt = []
								for t in tmp: tt.append((owner_prefs[t][0],t))
								tt.sort()
								tmp = []
								for t in tt: tmp.append(t[1])
								for t in tmp:
									itm = owner_prefs[t]
									itm_label = itm[0].replace('%s','').replace(':','').strip()
									if itm[1] == 'b':
										dc = GT(t) in [True,1,'1','on']
										i.getTag('command').getTag('x').setTag('field',attrs={'type':'boolean','label':itm_label,'var':t})\
										.setTagData('value',[0,1][dc])
									elif itm[1][0] in ['t','i','f','l']:
										i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-single','label':itm_label,'var':t})\
										.setTagData('value',unicode(GT(t)))
									elif itm[1][0] == 'm':
										tprm = [xmpp.Node('value',payload=prm) for prm in unicode(GT(t)).split('\n')]											
										i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-multi','label':itm_label,'var':t})\
										.setPayload(tprm)
									else:
										i.getTag('command').getTag('x').setTag('field',\
										attrs={'type':'list-single','label':itm_label,'var':t})\
										.setTagData('value',GT(t))
										for t2 in itm[3]:
											i.getTag('command').getTag('x').getTag('field',\
											attrs={'type':'list-single','label':itm_label,'var':t})\
											.setTag('option',attrs={'label':L(t2)})\
											.setTagData('value',t2)
					else:
						if get_tag_item(unicode(iq),'x','type') == 'submit':
							varz = iq.getTag('command').getTag('x')
							for t in config_prefs.keys():
								try:
									tmtype = varz.getTagAttr('field','type')
									tm = varz.getTag('field',attrs={'var':t}).getTags('value')
									tm = '\n'.join([tm2.getData() for tm2 in tm])
									if tmtype == 'boolean' and tm in ['0','1']: tm = [False,True][int(tm)]
									elif config_prefs[t][2] != None:
										if config_prefs[t][2] == [True,False] and tm in ['0','1']: tm = [False,True][int(tm)]
										elif tm in config_prefs[t][2]: pass
										else: tm = config_prefs[t][3]
									put_config(getRoom(room),t,tm)
								except: pass
							sucess_answer = L('Settings succesfully accepted')
							i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'completed', 'node':disco_config_node+tn,'sessionid':id})
							i.getTag('command').setTag('note',attrs={'type':'info'})
							i.getTag('command').setTagData('note',sucess_answer)
							i.getTag('command').setTag('x',namespace=xmpp.NS_DATA)
							i.getTag('command').getTag('x').setTagData('title',L('Settings'))
							i.getTag('command').getTag('x').setTagData('instrustion',sucess_answer)

							pprint('*** reconfigure by %s' % unicode(room),'purple')
						else:
							i.setTag('command',namespace=xmpp.NS_COMMANDS,attrs={'status':'executing', 'node':disco_config_node+tn,'sessionid':id})
							i.getTag('command').setTag('x',namespace=xmpp.NS_DATA,attrs={'type':'form'})
							#i.getTag('command').getTag('x').setTag('item',attrs={'node':disco_config_node+tn, 'name':'Configuration','jid':selfjid})
							#i.getTag('command').getTag('x').setTagData('instructions',L('For configure required x:data-compatible client'))
							tkeys = []
							for tmp in config_groups: tkeys.append(tmp[1])
							if tn in tkeys:
								for tmp in config_groups:
									if tn == tmp[1]:
										c_prefs,c_name = tmp[2],tmp[0]
										break
								i.getTag('command').getTag('x').setTagData('title',c_name)
								cnf_prefs = {}
								for tmp in c_prefs: cnf_prefs[tmp] = config_prefs[tmp]
								tmp = cnf_prefs.keys()
								tmp.sort()
								for t in tmp:
									itm = config_prefs[t]
									itm_label = itm[0].replace('%s','').replace(':','').strip()
									if itm[2] == [True,False]:
										dc = get_config(getRoom(room),t) in [True,1,'1','on']
										i.getTag('command').getTag('x').setTag('field',attrs={'type':'boolean','label':itm_label,'var':t})\
										.setTagData('value',[0,1][dc])
									elif itm[2] == None:
										if '\n' in itm[3]:
											tprm = [xmpp.Node('value',payload=prm) for prm in get_config(getRoom(room),t).split('\n')]											
											i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-multi','label':itm_label,'var':t})\
											.setPayload(tprm)
										else:
											i.getTag('command').getTag('x').setTag('field',attrs={'type':'text-single','label':itm_label,'var':t})\
											.setTagData('value',get_config(getRoom(room),t))									
									else:
										i.getTag('command').getTag('x').setTag('field',\
										attrs={'type':'list-single','label':itm_label,'var':t})\
										.setTagData('value',get_config(getRoom(room),t))

										for t2 in itm[2]:
											i.getTag('command').getTag('x').getTag('field',\
											attrs={'type':'list-single','label':itm_label,'var':t})\
											.setTag('option',attrs={'label':onoff(t2)})\
											.setTagData('value',t2)
							else: i.getTag('command').getTag('x').setTagData('title',L('Unknown configuration request!'))
					sender(i)
					raise xmpp.NodeProcessed
		else:
			msg_xmpp = iq.getTag('query', namespace=xmpp.NS_MUC_FILTER)
			if msg_xmpp:
				msg,mute = get_tag(unicode(msg_xmpp),'query'), None
				if msg[:2] == '<m':
					if '<body>' in msg and '</body>' in msg:
						jid = rss_replace(get_tag_item(msg,'message','from'))
						tojid = rss_replace(getRoom(get_level(room,getResourse(get_tag_item(msg,'message','to')))[1]))
						nick = rss_replace(unicode(get_nick_by_jid_res(room,jid)))
						skip_owner = getRoom(jid) in ownerbase
						gr = getRoom(room)
						if get_tag_item(msg,'message','type') == 'chat' and not skip_owner:
							tmp = cur_execute_fetchall('select * from muc_lock where room=%s and jid=%s', (room,tojid))
							if tmp: mute = True
						if skip_owner: pass
						elif get_config(gr,'muc_filter') and not mute:
							body = get_tag(msg,'body')

							# Mute newbie
							if get_config(gr,'muc_filter_newbie') and msg and not mute:
								in_base = cur_execute_fetchone('select sum(%s-time+age) from age where room=%s and jid=%s and status=0',(int(time.time()),gr,getRoom(jid)))
								if not in_base: nmute = True
								else:
									newbie_time = get_config(gr,'muc_filter_newbie_time')
									if newbie_time.isdigit(): newbie_time = int(newbie_time)
									else: newbie_time = 60
									if in_base[0] < newbie_time: nmute = True
									else: nmute = False
								if nmute:
									pprint('MUC-Filter mute newbie: %s %s %s' % (gr,jid,body),'brown')
									mute = True

							# New Line
							if get_config(gr,'muc_filter_newline_msg') != 'off' and msg and not mute:
								act = get_config(gr,'muc_filter_newline_msg')
								try:
									nline_count = get_config_int(gr,'muc_filter_newline_msg_count')
									if not 2 <= nline_count <= 50: raise
								except:
									nline_count = int(config_prefs['muc_filter_newline_msg_count'][3])
									put_config(gr,'muc_filter_newline_msg_count',str(nline_count))
								if body.count('\n') >= nline_count:
									pprint('MUC-Filter msg new line (%s): %s [%s] %s' % (act,jid,room,nick+'|'+body.replace('\n','[LF]')),'brown')
									if act == 'replace':
										body = body.replace('\n',' ')
										msg = msg.replace(get_tag_full(msg,'body'),'<body>%s</body>' % body)
									elif act == 'mute': mute = True
									else: msg = muc_filter_action(act,jid,room,L('Blocked by content!'))

							# Reduce spaces
							if get_config(gr,'muc_filter_reduce_spaces_msg') and msg and not mute and '  ' in body:
								pprint('MUC-Filter msg reduce spaces: %s [%s] %s' % (jid,room,nick+'|'+body),'brown')
								body = reduce_spaces_all(body)
								msg = msg.replace(get_tag_full(msg,'body'),'<body>%s</body>' % body)

							# AD-Block filter
							need_raw = True
							if get_config(gr,'muc_filter_adblock') != 'off' and msg and not mute:
								f = []
								for reg in adblock_regexp:
									tmp = re.findall(reg,body,re.I+re.S+re.U)
									if tmp: f = f + tmp
								if f:
									act = get_config(gr,'muc_filter_adblock')
									need_raw = False
									pprint('MUC-Filter msg adblock (%s): %s [%s] %s' % (act,jid,room,body),'brown')
									if act == 'replace':
										for tmp in f: body = body.replace(tmp,[GT('censor_text')*len(tmp),GT('censor_text')][len(GT('censor_text'))>1])
										msg = msg.replace(get_tag_full(msg,'body'),'<body>%s</body>' % body)
									elif act == 'mute': mute = True
									else: msg = muc_filter_action(act,jid,room,L('AD-Block!'))

							# Raw AD-Block filter
							if need_raw and get_config(gr,'muc_filter_adblock_raw') != 'off' and msg and not mute:
								rawbody = match_for_raw(body,u'[a-zа-я0-9@.]*',gr)
								if rawbody:
									f = []
									for reg in adblock_regexp:
										tmp = re.findall(reg,rawbody,re.I+re.S+re.U)
										if tmp: f = f + tmp
									if f:
										act = get_config(gr,'muc_filter_adblock_raw')
										pprint('MUC-Filter msg raw adblock (%s): %s [%s] %s' % (act,jid,room,body),'brown')
										if act == 'mute': mute = True
										else: msg = muc_filter_action(act,jid,room,L('Raw AD-Block!'))

							# Repeat message filter
							if get_config(gr,'muc_filter_repeat') != 'off' and msg and not mute:
								grj = getRoom(jid)
								try: lm = last_msg_base[grj]
								except: lm = None
								if lm:
									rep_to = GT('muc_filter_repeat_time')
									try: lmt = last_msg_time_base[grj]
									except: lmt = 0
									if rep_to+lmt > time.time():
										action = False
										if body == lm: action = True
										elif lm in body:
											try: muc_repeat[grj] += 1
											except: muc_repeat[grj] = 1
											if muc_repeat[grj] >= (GT('muc_filter_repeat_count')-1): action = True
										else: muc_repeat[grj] = 0
										if action:
											act = get_config(gr,'muc_filter_repeat')
											pprint('MUC-Filter msg repeat (%s): %s [%s] %s' % (act,jid,room,body),'brown')
											if act == 'mute': mute = True
											else: msg = muc_filter_action(act,jid,room,L('Repeat message block!'))
									else: muc_repeat[grj] = 0
								last_msg_base[grj] = body
								last_msg_time_base[grj] = time.time()

							# Match filter
							if get_config(gr,'muc_filter_match') != 'off' and msg and not mute and len(body) >= GT('muc_filter_match_view'):
								tbody,warn_match,warn_space = body.split(),0,0
								for tmp in tbody:
									cnt = 0
									for tmp2 in tbody:
										if tmp in tmp2: cnt += 1
									if cnt > GT('muc_filter_match_count'): warn_match += 1
									if not len(tmp): warn_space += 1
								if warn_match > GT('muc_filter_match_warning_match') or warn_space > GT('muc_filter_match_warning_space') or '\n'*GT('muc_filter_match_warning_nn') in body:
									act = get_config(gr,'muc_filter_match')
									pprint('MUC-Filter msg matcher (%s): %s [%s] %s' % (act,jid,room,body),'brown')
									if act == 'mute': mute = True
									else: msg = muc_filter_action(act,jid,room,L('Match message block!'))

							# Censor filter
							need_raw = True
							if get_config(gr,'muc_filter_censor') != 'off' and body != to_censore(body,gr) and msg and not mute:
								act = get_config(gr,'muc_filter_censor')
								need_raw = False
								pprint('MUC-Filter msg censor (%s): %s [%s] %s' % (act,jid,room,body),'brown')
								if act == 'replace': msg = msg.replace(get_tag_full(msg,'body'),'<body>%s</body>' % to_censore(body,gr))
								elif act == 'mute': mute = True
								else: msg = muc_filter_action(act,jid,room,L('Blocked by censor!'))

							# Raw censor filter
							if need_raw and get_config(gr,'muc_filter_censor_raw') != 'off' and msg and not mute:
								rawbody = match_for_raw(body,u'[a-zа-я0-9]*',gr)
								if rawbody and rawbody != to_censore(rawbody,gr):
									act = get_config(gr,'muc_filter_censor_raw')
									pprint('MUC-Filter msg raw censor (%s): %s [%s] %s' % (act,jid,room,body),'brown')
									if act == 'mute': mute = True
									else: msg = muc_filter_action(act,jid,room,L('Blocked by raw censor!'))

							# Large message filter
							if get_config(gr,'muc_filter_large') != 'off' and len(body) > GT('muc_filter_large_message_size') and msg and not mute:
								act = get_config(gr,'muc_filter_large')
								pprint('MUC-Filter msg large message (%s): %s [%s] %s' % (act,jid,room,body),'brown')
								if act == 'paste' or act == 'truncate':
									url = paste_text(rss_replace(body),room,jid)
									if act == 'truncate': body = u'%s[…] %s' % (body[:GT('muc_filter_large_message_size')],url)
									else: body = L('Large message%s %s') % (u'…',url)
									msg = msg.replace(get_tag_full(msg,'body'),'<body>%s</body>' % body)
								elif act == 'mute': mute = True
								else: msg = muc_filter_action(act,jid,room,L('Large message block!'))

						if mute: msg = unicode(xmpp.Message(to=jid,body=L('Warning! Your message is blocked in connection with the policy of the room!'),typ='chat',frm='%s/%s' % (room,get_nick_by_jid(room,tojid))))
					else: msg = None

				elif msg[:2] == '<p':
					jid = rss_replace(get_tag_item(msg,'presence','from'))
					tojid = rss_replace(get_tag_item(msg,'presence','to'))
					skip_owner = getRoom(jid) in ownerbase
					if skip_owner: pass
					elif get_config(getRoom(room),'muc_filter') and not mute:

						show = ['online',get_tag(msg,'show')][int('<show>' in msg and '</show>' in msg)]
						if show not in ['chat','online','away','xa','dnd']: msg = msg.replace(get_tag_full(msg,'show'), '<show>online</show>')
						status = ['',get_tag(msg,'status')][int('<status>' in msg and '</status>' in msg)]
						nick = ['',tojid[tojid.find('/')+1:]]['/' in tojid]
						gr,newjoin = getRoom(room),True
						for tmp in megabase:
							if tmp[0] == gr and tmp[4] == jid:
								newjoin = False
								break

						# Hash lock
						if get_config(gr,'muc_filter_deny_hash') and msg and not mute:
							hashes_list = reduce_spaces_all(get_config(gr,'muc_filter_deny_hash_list').replace(',',' ').replace(';',' ').replace('|',' ')).split()
							if hashes_list:
								msg_xmpp = msg_xmpp.getTag('presence')

								id_ver = id_lang = id_photo = id_avatar = 'error!'
								hash_error = False
								try: id_node = get_eval_item(msg_xmpp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("node")').decode('utf-8')
								except: id_node,hash_error = get_eval_item(msg_xmpp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("node")'),True
								try: id_ver = get_eval_item(msg_xmpp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ver")').decode('utf-8')
								except: id_ver,hash_error = get_eval_item(msg_xmpp,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ver")'),True
								try:
									id_bmver = msg_xmpp.getAttr('ver').decode('utf-8')
									if id_bmver or id_bmver == '': id_bmver = '%s_' % id_bmver
									else: id_bmver = ''
								except: id_bmver = ''
								try: id_lang = get_eval_item(msg_xmpp,'getAttr("xml:lang")').decode('utf-8')
								except: id_lang,hash_error = get_eval_item(msg_xmpp,'getAttr("xml:lang")'),True
								try: id_photo = get_eval_item(msg_xmpp,'getTag("x",namespace=xmpp.NS_VCARD_UPDATE).getTagData("photo")').decode('utf-8')
								except: id_photo,hash_error = get_eval_item(msg_xmpp,'getTag("x",namespace=xmpp.NS_VCARD_UPDATE).getTagData("photo")'),True
								try: id_avatar = get_eval_item(msg_xmpp,'getTag("x",namespace=xmpp.NS_AVATAR).getTagData("hash")').decode('utf-8')
								except: id_avatar,hash_error = get_eval_item(msg_xmpp,'getTag("x",namespace=xmpp.NS_AVATAR).getTagData("hash")'),True

								hash_body = '<'.join([unicode(tmp) for tmp in id_avatar,id_photo,id_ver,id_bmver,id_lang]) + '<<'
								if hash_error:
									writefile('log/bad_stanza_%s.txt' % int(time.time()),unicode(msg_xmpp).encode('utf-8'))
									hash_body = parser(hash_body.decode('utf-8'))

								current_hash = hashlib.md5(hash_body.encode('utf-8')).digest().encode('base64').replace('\n','')
								hashes['%s/%s' % (gr,nick)] = current_hash
								if current_hash in hashes_list:
									pprint('MUC-Filter hash lock: %s/%s %s %s' % (gr,nick,jid,current_hash),'brown')
									msg,mute = unicode(Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',Node('error', {'type': 'auth','code':'403'}, payload=[Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Deny by hash lock!')])])])).replace('replace_it',get_tag(msg,'presence')),True
									tmp_server = getServer(jid)
									tmp2_server = '%s/%s' % (gr,tmp_server)
									if get_config(gr,'muc_filter_hash_ban_by_rejoin') and not server_hash.has_key(tmp2_server):
										if user_hash.has_key('%s/%s' % (gr,getRoom(jid))):
											user_hash.pop('%s/%s' % (gr,getRoom(jid)))
											sender(Node('iq',{'id': get_id(), 'type': 'set', 'to':gr},payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'outcast', 'jid':jid},[Node('reason',{},'Banned by hash activity at %s' % timeadd(tuple(time.localtime())))])])]))
											pprint('MUC-Filter ban by hash lock: %s/%s' % (gr,nick),'brown')
										else: user_hash['%s/%s' % (gr,getRoom(jid))] = time.time()
									if get_config(gr,'muc_filter_hash_ban_server_by_rejoin'):
										if tmp_server not in get_config(gr,'muc_filter_hash_ban_server_by_rejoin_exception').split():
											tmp_rejoins = get_config_int(gr,'muc_filter_hash_ban_server_by_rejoin_rejoins')
											if server_hash.has_key(tmp2_server): server_hash[tmp2_server] = [time.time()] + server_hash[tmp2_server][:tmp_rejoins-1]
											else: server_hash[tmp2_server] = [time.time()]
											tmp_times = server_hash[tmp2_server]
											if len(tmp_times) == tmp_rejoins and tmp_times[0]-tmp_times[-1] <= get_config_int(gr,'muc_filter_hash_ban_server_by_rejoin_timeout') and not server_hash_list.has_key(tmp2_server):
												server_hash_list[tmp2_server] = time.time()
												sender(Node('iq',{'id': get_id(), 'type': 'set', 'to':gr},payload = [Node('query', {'xmlns': NS_MUC_ADMIN},[Node('item',{'affiliation':'outcast', 'jid':tmp_server},[Node('reason',{},'Banned by hash activity at %s' % timeadd(tuple(time.localtime())))])])]))
												pprint('MUC-Filter server ban by hash lock: %s %s' % (gr,tmp_server),'brown')
												tmp_notify = get_config(gr,'muc_filter_hash_ban_server_by_rejoin_notify_jid')
												if len(tmp_notify):
													for tmp in tmp_notify.split():
														if len(tmp): send_msg('chat', tmp, '', L('Server %s was banned in %s') % (tmp_server,gr))
								else: pprint('User hash: %s %s/%s %s' % (current_hash,gr,nick,jid),'white')

						# Blacklist
						if get_config(gr,'muc_filter_blacklist') and msg and not mute:
								bl_jid = get_config(gr,'muc_filter_blacklist_rules_jid')
								try: re.compile(bl_jid)
								except: bl_jid = None
								bl_nick = get_config(gr,'muc_filter_blacklist_rules_nick')
								try: re.compile(bl_nick)
								except: bl_nick = None
								is_bl = None
								if bl_jid and re.findall(bl_jid,jid,re.S+re.U+re.I): is_bl = True
								if not is_bl and bl_nick and re.findall(bl_nick,nick,re.S+re.U+re.I): is_bl = True
								if is_bl:
									pprint('MUC-Filter blacklist: %s/%s %s' % (gr,nick,jid),'brown')
									msg,mute = unicode(Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',Node('error', {'type': 'auth','code':'403'}, payload=[Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Deny by blacklist!')])])])).replace('replace_it',get_tag(msg,'presence')),True

						# Whitelist
						if get_config(gr,'muc_filter_whitelist') and msg and not mute and newjoin:
							in_base = cur_execute_fetchone('select jid from age where room=%s and jid=%s',(gr,getRoom(jid)))
							if not in_base:
								pprint('MUC-Filter whitelist: %s/%s %s' % (gr,nick,jid),'brown')
								msg,mute = unicode(Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',Node('error', {'type': 'auth','code':'403'}, payload=[Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Deny by whitelist!')])])])).replace('replace_it',get_tag(msg,'presence')),True

						# AD-Block filter
						need_raw = True
						if get_config(gr,'muc_filter_adblock_prs') != 'off' and msg and not mute:
							fs,fn = [],[]
							for reg in adblock_regexp:
								tmps = [None,re.findall(reg,status,re.I+re.S+re.U)][status != '']
								tmpn = [None,re.findall(reg,nick,re.I+re.S+re.U)][nick != '']
								if tmps: fs = fs + tmps
								if tmpn: fn = fn + tmpn
							if fs:
								need_raw = False
								act = get_config(gr,'muc_filter_adblock_prs')
								pprint('MUC-Filter adblock prs status (%s): %s [%s] %s' % (act,jid,room,status),'brown')
								if act == 'replace':
									for tmp in fs: status = status.replace(tmp,[GT('censor_text')*len(tmp),GT('censor_text')][len(GT('censor_text'))>1])
									msg = msg.replace(get_tag_full(msg,'status'),'<status>%s</status>' % status)
								elif newjoin: msg,mute = unicode(Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',Node('error', {'type': 'auth','code':'403'}, payload=[Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('AD-Block!')])])])).replace('replace_it',get_tag(msg,'presence')),True
								elif act == 'mute': msg,mute = None,True
								else: msg = muc_filter_action(act,jid,room,L('AD-Block!'))
							if fn and msg:
								need_raw = False
								act = get_config(gr,'muc_filter_adblock_prs')
								pprint('MUC-Filter adblock prs nick (%s): %s [%s] %s' % (act,jid,room,nick),'brown')
								if act == 'replace':
									for tmp in fn: nick = nick.replace(tmp,[GT('censor_text')*len(tmp),GT('censor_text')][len(GT('censor_text'))>1])
									msg = msg.replace(esc_max2(tojid),'%s/%s' % (tojid.split('/',1)[0],nick))
								elif newjoin: msg,mute = unicode(Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',Node('error', {'type': 'auth','code':'403'}, payload=[Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('AD-Block!')])])])).replace('replace_it',get_tag(msg,'presence')),True
								elif act == 'mute': msg,mute = None,True
								else: msg = muc_filter_action(act,jid,room,L('AD-Block!'))

						# Raw AD-Block filter
						if need_raw and get_config(gr,'muc_filter_adblock_prs_raw') != 'off' and msg and not mute:
							rawstatus = match_for_raw(status,u'[a-zа-я0-9@.]*',gr)
							rawnick = match_for_raw(nick,u'[a-zа-я0-9@.]*',gr)
							fs,fn = [],[]
							for reg in adblock_regexp:
								tmps = [None,re.findall(reg,rawstatus,re.I+re.S+re.U)][status != '']
								tmpn = [None,re.findall(reg,rawnick,re.I+re.S+re.U)][nick != '']
								if tmps: fs = fs + tmps
								if tmpn: fn = fn + tmpn
							if rawstatus and fs:
								act = get_config(gr,'muc_filter_adblock_prs_raw')
								pprint('MUC-Filter raw adblock prs status (%s): %s [%s] %s' % (act,jid,room,status),'brown')
								if newjoin: msg,mute = unicode(Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',Node('error', {'type': 'auth','code':'403'}, payload=[Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('AD-Block!')])])])).replace('replace_it',get_tag(msg,'presence')),True
								elif act == 'mute': msg,mute = None,True
								else: msg = muc_filter_action(act,jid,room,L('Raw AD-Block!'))
							if rawnick and fn and msg:
								act = get_config(gr,'muc_filter_adblock_prs_raw')
								pprint('MUC-Filter raw adblock prs nick (%s): %s [%s] %s' % (act,jid,room,nick),'brown')
								if newjoin: msg,mute = unicode(Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',Node('error', {'type': 'auth','code':'403'}, payload=[Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('AD-Block!')])])])).replace('replace_it',get_tag(msg,'presence')),True
								elif act == 'mute': msg,mute = None,True
								else: msg = muc_filter_action(act,jid,room,L('Raw AD-Block!'))

						# New Line
						if get_config(gr,'muc_filter_newline') != 'off' and msg and not mute:
							act = get_config(gr,'muc_filter_newline')
							try:
								nline_count = get_config_int(gr,'muc_filter_newline_count')
								if not 2 <= nline_count <= 50: raise
							except:
								nline_count = int(config_prefs['muc_filter_newline_count'][3])
								put_config(gr,'muc_filter_newline_count',str(nline_count))
							if status.count('\n') >= nline_count:
								pprint('MUC-Filter prs new line (%s): %s [%s] %s' % (act,jid,room,nick+'|'+status.replace('\n','[LF]')),'brown')
								if act == 'replace': msg = msg.replace(get_tag_full(msg,'status'),'<status>%s</status>' % reduce_spaces_all(status.replace('\n',' ')))
								elif newjoin: msg,mute = unicode(Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',Node('error', {'type': 'auth','code':'403'}, payload=[Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Blocked by content!')])])])).replace('replace_it',get_tag(msg,'presence')),True
								elif act == 'mute': msg,mute = None,True
								else: msg = muc_filter_action(act,jid,room,L('Blocked by content!'))

						# Reduce spaces
						if get_config(gr,'muc_filter_reduce_spaces_prs') and msg and not mute and ('  ' in status or '  ' in nick):
							pprint('MUC-Filter prs reduce spaces: %s [%s] %s' % (jid,room,nick+'|'+status),'brown')
							if len(status):
								status = reduce_spaces_all(status)
								msg = msg.replace(get_tag_full(msg,'status'),'<status>%s</status>' % status).replace(esc_max2(tojid),'%s/%s' % (tojid.split('/',1)[0],reduce_spaces_all(esc_max2(nick))))
							else: msg = msg.replace(esc_max2(tojid),'%s/%s' % (tojid.split('/',1)[0],reduce_spaces_all(esc_max2(nick))))

						# Censor filter
						need_raw = True
						if get_config(gr,'muc_filter_censor_prs') != 'off' and '%s|%s' % (status,nick) != to_censore('%s|%s' % (status,nick),gr) and msg and not mute:
							act = get_config(gr,'muc_filter_censor_prs')
							need_raw = False
							pprint('MUC-Filter prs censor (%s): %s [%s] %s' % (act,jid,room,'%s|%s' % (status,nick)),'brown')
							if act == 'replace':
								if len(status): 
									status = esc_max2(to_censore(esc_min2(status),gr))
									msg = msg.replace(get_tag_full(msg,'status'),'<status>%s</status>' % status).replace(esc_max2(tojid),'%s/%s' % (tojid.split('/',1)[0],to_censore(esc_max2(nick),gr)))
								else: msg = msg.replace(esc_max2(tojid),'%s/%s' % (tojid.split('/',1)[0],to_censore(esc_max2(nick),gr)))
							elif newjoin: msg,mute = unicode(Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',Node('error', {'type': 'auth','code':'403'}, payload=[Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Blocked by censor!')])])])).replace('replace_it',get_tag(msg,'presence')),True
							elif act == 'mute': msg,mute = None,True
							else: msg = muc_filter_action(act,jid,room,L('Blocked by censor!'))

						# Raw censor filter
						if need_raw and get_config(gr,'muc_filter_censor_prs_raw') != 'off' and msg and not mute:
							rawstatus = match_for_raw(status,u'[a-zа-я0-9]*',gr)
							rawnick = match_for_raw(nick,u'[a-zа-я0-9]*',gr)
							if (rawstatus or rawnick) and '%s|%s' % (rawstatus,rawnick) != to_censore('%s|%s' % (rawstatus,rawnick),gr):
								act = get_config(gr,'muc_filter_censor_prs_raw')
								pprint('MUC-Filter prs raw censor (%s): %s [%s] %s' % (act,jid,room,nick+'|'+status),'brown')
								if newjoin: msg,mute = unicode(Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',Node('error', {'type': 'auth','code':'403'}, payload=[Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Blocked by censor!')])])])).replace('replace_it',get_tag(msg,'presence')),True
								elif act == 'mute': msg,mute = None,True
								else: msg = muc_filter_action(act,jid,room,L('Blocked by raw censor!'))

						# Large status filter
						if get_config(gr,'muc_filter_large_status') != 'off' and len(esc_min2(status)) > GT('muc_filter_large_status_size') and msg and not mute:
							act = get_config(gr,'muc_filter_large_status')
							pprint('MUC-Filter large status (%s): %s [%s] %s' % (act,jid,room,status),'brown')
							if act == 'truncate': msg = msg.replace(get_tag_full(msg,'status'),u'<status>%s…</status>' % esc_max2(esc_min2(status)[:GT('muc_filter_large_status_size')]))
							elif newjoin: msg,mute = unicode(Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',Node('error', {'type': 'auth','code':'403'}, payload=[Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Large status block!')])])])).replace('replace_it',get_tag(msg,'presence')),True
							elif act == 'mute': msg,mute = None,True
							else: msg = muc_filter_action(act,jid,room,L('Large status block!'))

						# Large nick filter
						if get_config(gr,'muc_filter_large_nick') != 'off' and len(esc_min2(nick)) > GT('muc_filter_large_nick_size') and msg and not mute:
							act = get_config(gr,'muc_filter_large_nick')
							if act == 'truncate': msg = msg.replace(esc_max2(tojid),u'%s/%s…' % (tojid.split('/',1)[0],esc_max2(esc_min2(nick)[:GT('muc_filter_large_nick_size')])))
							elif newjoin: msg,mute = unicode(Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',Node('error', {'type': 'auth','code':'403'}, payload=[Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('Large nick block!')])])])).replace('replace_it',get_tag(msg,'presence')),True
							elif act == 'mute': msg,mute = None,True
							else: msg = muc_filter_action(act,jid,room,L('Large nick block!'))

						# Rejoin filter
						if get_config(gr,'muc_filter_rejoin') and msg and not mute and newjoin:
							ttojid = '%s|%s' % (getRoom(tojid),getRoom(jid))
							try: muc_rejoins[ttojid] = [muc_rejoins[ttojid],muc_rejoins[ttojid][1:]][len(muc_rejoins[ttojid])==GT('muc_filter_rejoin_count')] + [int(time.time())]
							except: muc_rejoins[ttojid] = []
							if len(muc_rejoins[ttojid]) == GT('muc_filter_rejoin_count'):
								tmo = muc_rejoins[ttojid][GT('muc_filter_rejoin_count')-1] - muc_rejoins[ttojid][0]
								if tmo < GT('muc_filter_rejoin_timeout'):
									msg,mute = unicode(Node('presence', {'from': tojid, 'type': 'error', 'to':jid}, payload = ['replace_it',Node('error', {'type': 'auth','code':'403'}, payload=[Node('forbidden',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[]),Node('text',{'xmlns':'urn:ietf:params:xml:ns:xmpp-stanzas'},[L('To many rejoins! Wait %s sec.') % GT('muc_filter_rejoin_timeout')])])])).replace('replace_it',get_tag(msg,'presence')),True
									pprint('MUC-Filter rejoin: %s [%s] %s' % (jid,room,nick),'brown')

						# Status filter
						if get_config(gr,'muc_filter_repeat_prs') != 'off' and msg and not mute and not newjoin:
							ttojid = '%s|%s' % (getRoom(tojid),getRoom(jid))
							try: muc_statuses[ttojid] = [muc_statuses[ttojid],muc_statuses[ttojid][1:]][len(muc_statuses[ttojid])==GT('muc_filter_status_count')] + [int(time.time())]
							except: muc_statuses[ttojid] = []
							if len(muc_statuses[ttojid]) == GT('muc_filter_status_count'):
								tmo = muc_statuses[ttojid][GT('muc_filter_status_count')-1] - muc_statuses[ttojid][0]
								if tmo < GT('muc_filter_status_timeout'):
									act = get_config(gr,'muc_filter_repeat_prs')
									pprint('MUC-Filter status (%s): %s [%s] %s' % (act,jid,room,nick),'brown')
									if act == 'mute': msg,mute = None,True
									else: msg = muc_filter_action(act,jid,room,L('Status-flood block!'))

				if msg:
					i=xmpp.Iq(to=room, typ='result')
					i.setAttr(key='id', val=id)
					i.setTag('query',namespace=xmpp.NS_MUC_FILTER).setTagData(tag='message', val='')
					try: sender(unicode(i).replace('<message />',msg))
					except: pass
					raise xmpp.NodeProcessed

def iq_async_clean():
	global iq_reques
	while not game_over:
		to = GT('timeout')
		while to > 0 and not game_over:
			to -= 1
			time.sleep(1)
		if len(iq_request):
			for tmp in iq_request.keys():
				if iq_request[tmp][0] + GT('timeout') < time.time(): iq_request.pop(tmp)
				break

def presence_async_clean():
	global pres_answer
	while not game_over:
		to = GT('timeout')
		while to > 0 and not game_over:
			to -= 1
			time.sleep(1)
		if len(pres_answer):
			tm = []
			for tmp in pres_answer:
				if tmp[2] + GT('timeout') > time.time(): tm.append(tmp)
			pres_answer = tm

def iq_async(*answ):
	global iq_request
	req = iq_request.pop(answ[0])
	try: er_code = answ[3]
	except: er_code = None
	if er_code == 'error': answ = answ[0:3]
	is_answ = (answ[1]-req[0],answ[2:])
	req[2].append(is_answ)
	thr(req[1],(tuple(req[2])),'iq_async_%s' % answ[0])

def remove_ignore():
	global ddos_ignore
	while not game_over:
		if len(ddos_ignore):
			tt = time.time()
			for tmp in ddos_ignore.keys():
				if tt > ddos_ignore[tmp][2]:
					try:
						ddos_ignore.pop(tmp)
						pprint('!!! DDOS: Jid %s is removed from ignore!' % tmp,'red')
					except: pprint('!!! DDOS: Unable find jid %s in ignore list. Perhaps it\'s removed by bot\'s owner!' % tmp,'red')
		time.sleep(10)

def com_parser(access_mode, nowname, type, room, nick, text, jid):
	global last_command, ddos_ignore
	jjid = getRoom(jid)
	if ddos_ignore.has_key(jjid): return
	if last_command[1:7] == [nowname, type, room, nick, text, jid] and time.time() < last_command[7]+GT('ddos_diff')[access_mode]:
		ddos_ignore[jjid] = [room,nick,time.time()+GT('ddos_limit')[access_mode]]
		pprint('!!! DDOS Detect: %s %s/%s %s %s' % (access_mode, room, nick, jid, text),'bright_red')
		send_msg(type, room, nick, L('Warning! Exceeded the limit of sending the same commands. You to ignore for %s sec.') % GT('ddos_limit')[access_mode])
		return None
	no_comm = True
	cof = getFile(conoff,[])
	for parse in comms:
		if access_mode >= parse[0] and nick != nowname:
			not_offed = True
			if access_mode != 9 or ignore_owner:
				for co in cof:
					if co[0]==room and co[1]==text.lower()[:len(co[1])]:
						not_offed = None
						break
			if not_offed and (text.lower() == parse[1].lower() or text[:len(parse[1])+1].lower() == parse[1].lower()+' '):
				pprint('%s %s/%s [%s] %s' % (jid,room,nick,access_mode,text),'bright_cyan')
				no_comm = None
				if not parse[3]: thr(parse[2],(type, room, nick, parse[4:]),parse[1])
				elif parse[3] == 1: thr(parse[2],(type, room, nick),parse[1])
				elif parse[3] == 2: thr(parse[2],(type, room, nick, text[len(parse[1])+1:]),parse[1])
				last_command = [access_mode, nowname, type, room, nick, text, jid, time.time()]
				break
	return no_comm

def messageCB(sess,mess):
	global lfrom, lto, owners, ownerbase, confbase, confs, lastserver, lastnick, comms
	global ignorebase, ignores, message_in, no_comm, last_hash
	message_in += 1
	type=unicode(mess.getType())
	room=unicode(mess.getFrom().getStripped())
	text=unicode(mess.getBody())
	try:
		code = mess.getTag('x',namespace=NS_MUC_USER).getTagAttr('status','code')
		if code == '104':
			append_message_to_log(room,'','',type,L('Room\'s configuration changed.'))
			return
	except: pass
	if (text == 'None' or text == '') and not mess.getSubject(): return
	if mess.getTimestamp() != None: return
	nick=mess.getFrom().getResource()
	if nick != None: nick = unicode(nick)
	towh=unicode(mess.getTo().getStripped())
	lprefix = get_local_prefix(room)
	back_text = text
	rn = '%s/%s' % (room,nick)
	ft = text
	ta = get_level(room,nick)
	access_mode = ta[0]
	jid = ta[1]

	tmppos = arr_semi_find(confbase, room)
	if tmppos == -1: nowname = Settings['nickname']
	else:
		nowname = getResourse(confbase[tmppos])
		if nowname == '': nowname = Settings['nickname']
	if '@' not in jid and (jid == 'None' or jid.startswith('j2j.')) and getRoom(room) in ownerbase: access_mode = 9
	if type == 'groupchat' and nick != '' and access_mode >= 0 and jid not in ['None',Settings['jid']]: talk_count(room,jid,nick,text)
	if nick != '' and nick != None and nick != nowname and len(text)>1 and text != 'None' and text != to_censore(text,room) and access_mode >= 0 and get_config(getRoom(room),'censor'):
		cens_text = L('Censored!')
		lvl = get_level(room,nick)[0]
		if lvl >= 5 and get_config(getRoom(room),'censor_warning'): send_msg(type,room,nick,cens_text)
		elif lvl == 4 and get_config(getRoom(room),'censor_action_member') != 'off':
			act = get_config(getRoom(room),'censor_action_member')
			muc_filter_action(act,jid,room,cens_text)
		elif lvl < 4 and get_config(getRoom(room),'censor_action_non_member') != 'off':
			act = get_config(getRoom(room),'censor_action_non_member')
			muc_filter_action(act,jid,room,cens_text)
	no_comm = True
	if (text != 'None') and (len(text)>=1) and access_mode >= 0 and not mess.getSubject():
		no_comm = True
		is_par = False
		if text[:len(nowname)] == nowname:
			text = text[len(nowname)+2:]
			is_par = True
		btext = text
		if text[:len(lprefix)] == lprefix:
			text = text[len(lprefix):]
			is_par = True
		if type == 'chat': is_par = True
		if is_par: no_comm = com_parser(access_mode, nowname, type, room, nick, text, jid)
		if no_comm:
			for parse in aliases:
				if (btext.lower() == parse[1].lower() or btext[:len(parse[1])+1].lower() == parse[1].lower()+' ') and room == parse[0]:
					pprint('%s %s/%s [%s] %s' % (jid,room,nick,access_mode,text),'bright_cyan')
					argz = btext[len(parse[1])+1:]
					if not argz:
						ppr = parse[2].replace('%*', '').replace('%{reduce}*', '').replace('%{reduceall}*', '').replace('%{unused}*', '')
						cpar = re.findall('%([0-9]+)', ppr, re.S)
						if len(cpar):
							for tmp in cpar:
								try: ppr = ppr.replace('%'+tmp,'')
								except: pass
					else:
						ppr = parse[2].replace('%*', argz).replace('%{reduce}*', argz.strip()).replace('%{reduceall}*', reduce_spaces_all(argz))
						if '%' in ppr:
							cpar = re.findall('%([0-9]+)', ppr, re.S)
							if len(cpar):
								argz = argz.split()
								argzbk = argz
								for tmp in cpar:
									try:
										it = int(tmp)
										ppr = ppr.replace('%'+tmp,argz[it])
										argzbk = argzbk[:it]+argzbk[it+1:]
									except: pass
								ppr = ppr.replace('%{unused}*',' '.join(argzbk))

					if len(ppr) == ppr.count(' '): ppr = ''
					no_comm = com_parser(access_mode, nowname, type, room, nick, ppr, jid)
					break
	try:
		if '%s/%s' % (room,nick) == PSTO_JID: psto_parse(back_text)
	except: pass
	thr(msg_afterwork,(mess,room,jid,nick,type,back_text,no_comm,access_mode,nowname),'msg_afterwork')

def msg_afterwork(mess,room,jid,nick,type,back_text,no_comm,access_mode,nowname):
	global topics
	not_alowed_flood = False
	subj = unicode(mess.getSubject())
	text = back_text
	if subj != 'None':
		if '\n' in subj: subj = '\n%s'  % subj
		subj = L('*** Topic: %s') % subj
		if len(text) and text != 'None': subj = text.replace(': ',':\n',1) if '\n' in text else text
		topics[room],nick = subj,''
		text = subj
		not_alowed_flood, no_comm = True, False
	for tmp in gmessage: not_alowed_flood = tmp(room,jid,nick,type,text) or not_alowed_flood
	if no_comm:
		for tmp in gactmessage: not_alowed_flood = not_alowed_flood or tmp(room,jid,nick,type,text)
	if not not_alowed_flood and no_comm:
		if room != selfjid: is_flood = get_config(getRoom(room),'flood') not in ['off',False]
		else: is_flood = None
		if selfjid != jid and access_mode >= 0 and (back_text[:len(nowname)+2] == nowname+': ' or back_text[:len(nowname)+2] == nowname+', ' or type == 'chat') and is_flood:
			pprint('Send msg human: %s/%s [%s] <<< %s' % (room,nick,type,text),'dark_gray')
			if len(back_text)>100:
				taxt = L('Too many letters!')
				pprint('Send msg human: %s/%s [%s] >>> %s' % (room,nick,type,text),'dark_gray')
				send_msg(type, room, nick, text)
			else:
				if back_text[:len(nowname)] == nowname: back_text = back_text[len(nowname)+2:]
				try:
					text = getAnswer(type, room, nick, back_text)
					if text:
						pprint('Send msg human: %s/%s [%s] >>> %s' % (room,nick,type,text),'dark_gray')
						thr(send_msg_human,(type, room, nick, text),'msg_human')
				except: pass

def send_msg_human(type, room, nick, text):
	time.sleep(len(text)/4.0+randint(0,3))
	send_msg(type, room, nick, text)

def to_censore(text,room):
	ccn = []
	if get_config(getRoom(room),'censor_custom'):
		custom_censor = get_config(getRoom(room),'censor_custom_rules').replace('\r','').replace('\t','').split('\n')
		for c in custom_censor:
			if '#' not in c and len(c): ccn.append(c)
	wca = None
	for c in censor+ccn:
		cn = re.findall(c,' %s ' % text,re.I+re.S+re.U)
		for tmp in cn: text,wca = text.replace(tmp,[GT('censor_text')*len(tmp),GT('censor_text')][len(GT('censor_text'))>1]),True
	if wca: text = del_space_both(text)
	return text

def check_hash_actions():
	global hash_actions_list
	if hash_actions_list:
		for tmp in hash_actions_list.keys():
			if time.time() > hash_actions_list[tmp][1]:
				hal = hash_actions_list.pop(tmp)
				if hal[0] == L('whitelist'): put_config(tmp,'muc_filter_whitelist',False)
				elif hal[0] == L('lock by hash'):
					hashes_list = reduce_spaces_all(get_config(tmp,'muc_filter_deny_hash_list').replace(',',' ').replace(';',' ').replace('|',' ')).split()
					if hal[2] in hashes_list:
						hashes_list.remove(hal[2])
						put_config(tmp,'muc_filter_deny_hash_list',' '.join(hashes_list))
					if not hashes_list: put_config(tmp,'muc_filter_deny_hash',False)
				pprint('Removed hash action %s in %s' % (hal[0],tmp),'cyan')

def presenceCB(sess,mess):
	global megabase, ownerbase, pres_answer, confs, confbase, cu_age, presence_in, hashes, last_hash
	presence_in += 1
	room=unicode(mess.getFrom().getStripped())
	nick=unicode(mess.getFrom().getResource())
	text=unicode(mess.getStatus())
	type=unicode(mess.getType())
	affiliation=unicode(mess.getAffiliation())
	role=unicode(mess.getRole())
	jid=unicode(mess.getJid())	
	mss = unicode(mess)
	bad_presence = mss.count('<x xmlns=\"http://jabber') > 1 and mss.count(' affiliation=\"') > 1 and mss.count(' role=\"') > 1
	priority=unicode(mess.getPriority())
	show=unicode(mess.getShow())
	reason=unicode(mess.getReason())
	status=unicode(mess.getStatusCode())
	try: chg_nick = [None,mess.getTag('x',namespace=xmpp.NS_MUC_USER).getTagAttr('item','nick')][status == '303']
	except: chg_nick = None
	actor=unicode(mess.getActor())
	to=unicode(mess.getTo())
	id = mess.getID()
	tt = int(time.time())
	if type=='error':
		try: pres_answer.append((id,'%s: %s' % (get_tag_item(unicode(mess),'error','code'),mess.getTag('error').getTagData(tag='text')),tt))
		except:
			try: pres_answer.append((id,'%s: %s' % (get_tag_item(unicode(mess),'error','code'),mess.getTag('error')),tt))
			except: pres_answer.append((id,L('Unknown error!'),tt))
		return
	elif id != None: pres_answer.append((id,None,tt))
	if jid == 'None': jid = get_level(room,nick)[1]

	# Get Caps
	if '%s|%s' % (role,affiliation) in levl:
		id_ver = id_lang = id_photo = id_avatar = 'error!'
		hash_error = False
		try: id_node = get_eval_item(mess,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("node")').decode('utf-8')
		except: id_node,hash_error = get_eval_item(mess,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("node")'),True
		try: id_ver = get_eval_item(mess,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ver")').decode('utf-8')
		except: id_ver,hash_error = get_eval_item(mess,'getTag("c",namespace=xmpp.NS_CAPS).getAttr("ver")'),True
		try:
			id_bmver = mess.getAttr('ver').decode('utf-8')
			if id_bmver or id_bmver == '': id_bmver = '%s_' % id_bmver
			else: id_bmver = ''
		except: id_bmver = ''
		capses['%s/%s' % (room,nick)] = '%s\n%s\n%s' % (id_node,id_ver,id_bmver)

	# Hash control
	if '%s|%s' % (role,affiliation) in levl and levl['%s|%s' % (role,affiliation)] <= 3:
		try: id_lang = get_eval_item(mess,'getAttr("xml:lang")').decode('utf-8')
		except: id_lang,hash_error = get_eval_item(mess,'getAttr("xml:lang")'),True
		try: id_photo = get_eval_item(mess,'getTag("x",namespace=xmpp.NS_VCARD_UPDATE).getTagData("photo")').decode('utf-8')
		except: id_photo,hash_error = get_eval_item(mess,'getTag("x",namespace=xmpp.NS_VCARD_UPDATE).getTagData("photo")'),True
		try: id_avatar = get_eval_item(mess,'getTag("x",namespace=xmpp.NS_AVATAR).getTagData("hash")').decode('utf-8')
		except: id_avatar,hash_error = get_eval_item(mess,'getTag("x",namespace=xmpp.NS_AVATAR).getTagData("hash")'),True

		hash_body = '<'.join([unicode(tmp) for tmp in id_avatar,id_photo,id_ver,id_bmver,id_lang]) + '<<'
		if hash_error:
			writefile('log/bad_stanza_%s.txt' % int(time.time()),unicode(mess).encode('utf-8'))
			hash_body = parser(hash_body.decode('utf-8'))

		current_hash = hashlib.md5(hash_body.encode('utf-8')).digest().encode('base64').replace('\n','')
		hashes['%s/%s' % (room,nick)] = current_hash
		if type != 'unavailable' and not get_config(room,'muc_filter_whitelist') and get_config(room,'muc_filter_hash'):
			try: lh = last_hash[room]
			except: lh = [current_hash,[]]
			try:
				hash_ev = get_config_int(room,'muc_filter_hash_events')
				if not 3 <= hash_ev <= 1000: raise
			except:
				hash_ev = config_prefs['muc_filter_hash_events'][3]
				put_config(room,'muc_filter_hash_events',hash_ev)
			try:
				hash_tm = get_config_int(room,'muc_filter_hash_time')
				if not 3 <= hash_tm <= 1000: raise
			except:
				hash_tm = config_prefs['muc_filter_hash_time'][3]
				put_config(room,'muc_filter_hash_time',hash_tm)
			if current_hash == lh[0]:
				if lh[1]: lh[1] = [time.time()] + lh[1][:hash_ev-1]
				else: lh[1] = [time.time()]
				lh[0] = current_hash
			else: lh = [current_hash,[]]
			if lh[1] and len(lh[1]) == hash_ev and lh[1][0]-lh[1][-1] <= hash_tm:
				pprint('Hash high action: %s %s/%s' % (current_hash,room,nick),'red')
				h_action = get_config(room,'muc_filter_hash_action')
				try:
					h_action_time = get_config_int(room,'muc_filter_hash_action_time')
					if not 3 <= h_action_time <= 86400: raise
				except:
					h_action_time = config_prefs['muc_filter_hash_action_time'][3]
					put_config(room,'muc_filter_hash_action_time',h_action_time)
				hash_actions_list[room] = [h_action,h_action_time+time.time(),current_hash]
				if h_action == L('whitelist'): put_config(room,'muc_filter_whitelist',True)
				elif h_action == L('lock by hash'):
					put_config(room,'muc_filter_deny_hash',True)
					hashes_list = reduce_spaces_all(get_config(room,'muc_filter_deny_hash_list').replace(',',' ').replace(';',' ').replace('|',' ')).split()
					if not current_hash in hashes_list:
						hashes_list.append(current_hash)
						put_config(room,'muc_filter_deny_hash_list',' '.join(hashes_list))
				h_action_current = get_config(room,'muc_filter_hash_action_current')
				if h_action_current != L('off'):
					pprint('MUC-Filter initial flush by hash: %s %s' % (room,jid),'brown')
					muc_filter_action(h_action_current,jid,room,L('Deny by hash lock!'))
					for tmp in hashes.keys():
						tmp_room,tmp_nick = tmp.split('/',1)
						if tmp_room == room and hashes[tmp] == current_hash:
							tmp_access,tmp_jid = get_level(room,tmp_nick)
							if tmp_access <= 3 and tmp_jid != 'None':
								in_base = cur_execute_fetchone('select sum(%s-time+age) from age where room=%s and jid=%s and status=0',(int(time.time()),room,getRoom(tmp_jid)))
								if not in_base: nmute = True
								else:
									newbie_time = get_config(room,'muc_filter_newbie_time')
									if newbie_time.isdigit(): newbie_time = int(newbie_time)
									else: newbie_time = 60
									if in_base[0] < newbie_time: nmute = True
									else: nmute = False
								if nmute:
									pprint('MUC-Filter flush by hash: %s %s' % (room,tmp_jid),'brown')
									muc_filter_action(h_action_current,tmp_jid,room,L('Deny by hash lock!'))
				lh = [current_hash,[]]
			last_hash[room] = lh

	if bad_presence: send_msg('groupchat', room, '', L('/me detect bad stanza from %s') % nick)
	tmppos = arr_semi_find(confbase, room.lower())
	if tmppos == -1: nowname = Settings['nickname']
	else:
		nowname = getResourse(confbase[tmppos])
		if nowname == '': nowname = Settings['nickname']
	not_found,exit_type,exit_message = 0,'',''
	if type=='unavailable':
		if status=='307': exit_type,exit_message = L('kicked'),reason
		elif status=='301': exit_type,exit_message = L('banned'),reason
		elif status=='303': exit_type,exit_message = L('change nick to %s') % chg_nick,''
		else: exit_type,exit_message = L('leave'),text
		if exit_message == 'None': exit_message = ''
		try: exit_message += '\r' + acl_ver_tmp['%s/%s' % (room,nick)]
		except: pass
		if nick != '':
			for mmb in megabase:
				if mmb[0]==room and mmb[1]==nick:
					megabase.remove(mmb)
					break
			if to == selfjid and status in ['307','301'] and '%s/%s' % (room,nick) in confbase:
				if os.path.isfile(confs):
					confbase = json.loads(readfile(confs))
					confbase = arr_del_semi_find(confbase,getRoom(room))
					writefile(confs,json.dumps(confbase))
				pprint('*** bot was %s %s %s' % (['banned in','kicked from'][status=='307'],room,exit_message),'red')
				if GT('kick_ban_notify'):
					ntf_list = GT('kick_ban_notify_jid').replace(',',' ').replace('|',' ').replace(';',' ')
					while '  ' in ntf_list: ntf_list = ntf_list.replace('  ',' ')
					ntf_list = ntf_list.split()
					if len(ntf_list):
						ntf_msg = [L('banned in'),L('kicked from')][status == '307']
						ntf_msg = L('Bot was %s %s with reason: %s') % (ntf_msg,room,exit_message)
						for tmp in ntf_list: send_msg('chat', tmp, '', ntf_msg)
	else:
		if nick != '':
			for mmb in megabase:
				if mmb[0]==room and mmb[1]==nick:
					megabase.remove(mmb)
					megabase.append([room, nick, role, affiliation, jid])
					if role != mmb[2] or affiliation != mmb[3]: not_found = 1
					else: not_found = 2
					break
			if not not_found: megabase.append([room, nick, role, affiliation, jid])
	if jid == 'None': jid, jid2 = '<temporary>%s' % nick, 'None'
	else: jid2, jid = jid, getRoom(jid.lower())
	for tmp in gpresence: thr(tmp,(room,jid2,nick,type,(text, role, affiliation, exit_type, exit_message, show, priority, not_found, chg_nick)),'presence_afterwork')
	al = get_level(getRoom(room),nick)[0]
	if al == 9:
		if type == 'subscribe':
			caps_and_send(Presence(room, 'subscribed'))
			caps_and_send(Presence(room, 'subscribe'))
			pprint('Subscribe %s' % room,'light_gray')
		elif type == 'unsubscribed':
			caps_and_send(Presence(room, 'unsubscribe'))
			caps_and_send(Presence(room, 'unsubscribed'))
			pprint('Unsubscribe %s' % room,'light_gray')
	if nick != '' and nick != 'None' and nick != nowname and len(text)>1 and text != 'None' and al >= 0 and get_config(getRoom(room),'censor'):
		nt = '%s %s' % (nick,text)
		if nt != to_censore(nt,room):
			cens_text = L('Censored!')
			if al >= 5 and get_config(getRoom(room),'censor_warning'): send_msg('groupchat',room,nick,cens_text)
			elif al == 4 and get_config(getRoom(room),'censor_action_member') != 'off':
				act = get_config(getRoom(room),'censor_action_member')
				muc_filter_action(act,jid2,getRoom(room),cens_text)
			elif al < 4 and get_config(getRoom(room),'censor_action_non_member') != 'off':
				act = get_config(getRoom(room),'censor_action_non_member')
				muc_filter_action(act,jid2,getRoom(room),cens_text)
	ab = cur_execute_fetchone('select * from age where room=%s and jid=%s and nick=%s',(room, jid, nick))
	ttext = '%s\n%s\n%s\n%s\n%s' % (role,affiliation,priority,show,text)
	if ab:
		if type=='unavailable': cur_execute('update age set time=%s, age=%s, status=%s, type=%s, message=%s where room=%s and jid=%s and nick=%s', (tt,ab[4]+(tt-ab[3]),1,exit_type,exit_message,room, jid, nick))
		else:
			if ab[5]: cur_execute('update age set time=%s, status=%s, message=%s where room=%s and jid=%s and nick=%s', (tt,0,ttext,room, jid, nick))
			else: cur_execute('update age set status=%s, message=%s where room=%s and jid=%s and nick=%s', (0,ttext,room, jid, nick))
	else: cur_execute('insert into age values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (room,nick,jid,tt,0,0,'',ttext,nick.lower()))

def onoff_no_tr(msg):
	if msg == None or msg == False or msg == 0 or msg == '0': return 'off'
	elif msg == True or msg == 1 or msg == '1': return 'on'
	else: return msg

def onoff(msg): return L(onoff_no_tr(msg))

def getName(jid):
	jid = unicode(jid)
	if jid == 'None': return jid
	if '@' not in jid: return ''
	return jid[:jid.find('@')].lower()

def getServer(jid):
	jid = unicode(jid)
	if '/' not in jid: jid += '/'
	if jid == 'None': return jid
	return jid[jid.find('@')+1:jid.find('/')].lower()

def getResourse(jid):
	jid = unicode(jid)
	if jid == 'None': return jid
	try: return jid.split('/')[1]
	except: return ''

def getRoom(jid):
	jid = unicode(jid)
	if jid == 'None': return jid
	if '@' in jid: return '%s@%s' % (getName(jid),getServer(jid))
	else: return getServer(jid)

def now_schedule():
	while not game_over:
		to = GT('schedule_time')
		while to > 0 and not game_over:
			to -= 1
			time.sleep(1)
		if not game_over:
			for tmp in gtimer: log_execute(tmp,())

def check_rss():
	l_hl = int(time.time())
	feedbase = getFile(feeds,[])
	for fd in feedbase:
		ltime = fd[1]
		timetype = ltime[-1:].lower()
		if not timetype in ('h','m'): timetype = 'h'
		try: ofset = int(ltime[:-1])
		except: ofset = 4
		if timetype == 'h': ofset *= 3600
		elif timetype == 'm': ofset *= 60
		try: ll_hl = int(fd[3])
		except: ll_hl = 0
		in_room = None
		for tmp in confbase:
			if getRoom(tmp) == fd[4]:
				in_room = True
				break
		if ofset < 600: ofset = 600
		if in_room and ll_hl + ofset <= l_hl:
			pprint('check rss: %s in %s' % (fd[0],fd[4]),'green')
			rss('groupchat', fd[4], 'RSS', 'new %s 10 %s silent' % (fd[0],fd[2]))
			break

def talk_count(room,jid,nick,text):
	jid = getRoom(jid)
	ab = cur_execute_fetchone('select * from talkers where room=%s and jid=%s',(room,jid))
	wtext = len(reduce_spaces_all(text).split(' '))
	if ab: cur_execute('update talkers set nick=%s, words=%s, frases=%s where room=%s and jid=%s', (nick,ab[3]+wtext,ab[4]+1,room,jid))
	else: cur_execute('insert into talkers values (%s,%s,%s,%s,%s)', (room, jid, nick, wtext, 1))

def flush_stats():
	pprint('Executed threads: %s | Error(s): %s' % (th_cnt,thread_error_count),'bright_blue')
	pprint('Message in %s | out %s' % (message_in,message_out),'bright_blue')
	pprint('Presence in %s | out %s' % (presence_in,presence_out),'bright_blue')
	pprint('Iq in %s | out %s' % (iq_in,iq_out),'bright_blue')
	pprint('Unknown out %s' % unknown_out,'bright_blue')
	pprint('Cycles used %s | unused %s' % (cycles_used,cycles_unused),'bright_blue')

def disconnecter():
	global bot_exit_type, game_over
	pprint('--- Restart by disconnect handler! ---','bright_blue')
	pprint('--- Last stanza ---','bright_blue')
	pprint(last_stanza,'bright_blue')
	pprint('-'*19,'blue')
	game_over, bot_exit_type = True, 'restart'
	time.sleep(2)

def L(text):
	if not len(text): return text
	try: return locales[text]
	except: return text

def kill_all_threads():
	if thread_type:
		threading_list = threading.enumerate() 
		threading_list.remove(threading.currentThread())
		for tmp in threading_list:
			if not tmp.name.startswith('_MainThread'):
				try: tmp.kill()
				except: pass

def get_id():
	global id_count
	id_count += 1
	return 'request_%s' % id_count
	
def draw_warning(wt):
	wt = '!!! Warning! %s !!!' % wt
	pprint('!'*len(wt),'bright_red')
	pprint(wt,'bright_red')
	pprint('!'*len(wt),'bright_red')

def wait(conn):
	tt = time.time() + 10
	while tt > time.time():
		state = conn.poll()
		if state == psycopg2.extensions.POLL_OK:
			break
		elif state == psycopg2.extensions.POLL_WRITE:
			select.select([], [conn.fileno()], [])
		elif state == psycopg2.extensions.POLL_READ:
			select.select([conn.fileno()], [], [])
		else:
			raise psycopg2.OperationalError("poll() returned %s" % state)
# --------------------- Иницилизация переменных ----------------------

nmbrs = ['0','1','2','3','4','5','6','7','8','9','.']
ul = 'update.log'					# лог последнего обновление
debugmode = None					# остановка на ошибках
dm = None							# отладка xmpppy
dm2 = False							# отладка действий бота
CommandsLog = None					# логгирование команд
prefix = '_'						# префикс комманд
msg_limit = 1000					# лимит размера сообщений
botName = 'Isida-Bot'				# название бота
botVersion = u'v3.0β'				# версия бота
capsVersion = botVersion[1:-1]		# версия для капса
disco_config_node = 'http://isida-bot.com/config'
pres_answer = []					# результаты посылки презенсов
iq_request = {}						# iq запросы
th_cnt = 0							# счётчик тредов
thread_error_count = 0				# счётчик ошибок тредов
bot_exit_type = None				# причина завершения бота
last_stream = []					# очередь станз к отправке
last_command = []					# последняя исполненная ботом команда
thread_type = True					# тип тредов
time_limit = 1.1					# максимальная задержка между посылкой станз с одинаковым типом в groupchat
time_nolimit = 0.1					# задержка между посылкой станз с разными типами
message_in,message_out = 0,0		# статистика сообщений
iq_in,iq_out = 0,0					# статистика iq запросов
presence_in,presence_out = 0,0		# статистика презенсов
unknown_out = 0						# статистика ошибочных отправок
cycles_used,cycles_unused = 0,0		# статистика циклов
id_count = 0						# номер запроса
megabase = []						# главная временная база с полной информацией из презенсов
ignore_owner = None					# исполнять отключенные команды для владельца бота
configname = 'settings/config.py'	# конфиг бота
topics = {}							# временное хранение топиков
last_msg_base = {}					# последние сообщения
last_msg_time_base = {}				# время между последними сообщениями последние сообщения
paranoia_mode = False				# режим для параноиков. запрет любых исполнений внешнего кода
no_comm = True
muc_rejoins = {}
muc_statuses = {}
muc_repeat = {}
last_stanza = ''					# последняя станза, посланная ботом
ENABLE_TLS = True					# принудительное отключение TLS
base_timeout = 20					# таймаут на доступ ко всем базам
between_msg_last = {}				# время последнего сообщения
last_sender_activity = time.time()	# время последней отправки
hashes = {}							# хеши презенсов
capses = {}							# капсы клиентов
last_hash = {}						# хеш последнего события
hash_actions_list = {}				# список действий на хеш-события
smile_folder = '.smiles'			# папка со смайлами в чатлогах
smile_descriptor = 'icondef.xml'	# дескриптор смайлов
last_logs_store = []				# последние записи в логах
last_logs_size = 20					# максимальное количество последних записей в логах
ddos_ignore = {}					# данные при подозрении на ddos
ddos_iq = {}
CURRENT_LOCALE = 'en'
user_hash = {}
server_hash = {}
server_hash_list = {}
messages_excl = []
pg_debug = False

gt=tuple(time.gmtime())
lt=tuple(time.localtime())
if lt[0:3] == gt[0:3]: timeofset = int(lt[3])-int(gt[3])
elif lt[0:3] > gt[0:3]: timeofset = int(lt[3])-int(gt[3]) + 24
else: timeofset = int(gt[3])-int(lt[3]) + 24

if os.path.isfile(configname): execfile(configname)
else: errorHandler('%s is missed.' % configname)

if os.path.isfile(ver_file):
	bvers = readfile(ver_file).decode('utf-8').replace('\n','').replace('\r','').replace('\t','').replace(' ','')
	botVersion += '.%s' % bvers
if 'm' in botVersion.lower(): draw_warning('Launched bot\'s modification!')
try: tmp = botOs
except: botOs = os_version()

sm_f = os.path.join(public_log,smile_folder)
if os.path.isdir(sm_f):
	smiles_dirs_case = [sd for sd in os.listdir(sm_f) if sd[0] != '.' and os.path.isfile(os.path.join(sm_f,sd,smile_descriptor))]
	smiles_dirs = [sd.lower() for sd in smiles_dirs_case]
else: smiles_dirs, smiles_dirs_case = [], []

logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)	# включение логгирования
capsNode = 'http://isida-bot.com'
god = SuperAdmin
pprint('-'*50,'blue')
if(sys.argv[0]) != 'isida.py':
	draw_warning('Ugly launch detect! Read wiki!')
	sys.exit('exit')

conn = psycopg2.connect(database=base_name, user=base_user, host=base_host, password=base_pass, port=base_port)

pprint('*** Loading localization','white')
locales = {}
if os.path.isfile(loc_file):
	CURRENT_LOCALE = getFile(loc_file,'\'en\'')
	lf = '%s%s.txt' % (loc_folder,CURRENT_LOCALE)
	if os.path.isfile(lf):
		lf = readfile(lf).decode('UTF').replace('\r','').split('\n')
		for c in lf:
			if ('#' not in c[:3]) and len(c) and '\t' in c: locales[c.split('\t',1)[0].replace('\\n','\n').replace('\\t','\t')] = c.split('\t',1)[1].replace('\\n','\n').replace('\\t','\t')
pprint('*** Loading main plugin','white')

pl_folder	= 'plugins/%s'
execfile(pl_folder % 'main.py')

pliname		= pl_folder % 'ignored.txt'
gtimer		= [check_rss,check_hash_actions,clean_user_and_server_hash]
gpresence	= []
gmessage	= []
gactmessage	= []

pprint('*** Loading other plugins','white')

pl,pl_ignore,plugins = os.listdir(pl_folder % ''),getFile(pliname,[]),[]
for tmp in pl:
	if tmp[-3:] == '.py' and tmp[0] != '.' and tmp != 'main.py': plugins.append(tmp)
plugins.sort()

for pl in plugins:
	if pl in pl_ignore: pprint('Ignore plugin: %s' % pl,'red')
	else:
		presence_control,message_control,message_act_control,iq_control,timer,execute = [],[],[],[],[],[]
		pprint('Append plugin: %s' % pl,'cyan')
		execfile(pl_folder % pl)
		for cm in execute: comms.append((cm[0],cm[1],cm[2],cm[3],L('Plugin %s. %s') % (pl[:-3],cm[4]))+cm[5:])
		for tmr in timer: gtimer.append(tmr)
		for tmp in presence_control: gpresence.append(tmp)
		for tmp in message_control: gmessage.append(tmp)
		for tmp in message_act_control: gactmessage.append(tmp)

aliases = getFile(alfile,[])

'''
tmp,config_group_commands = comms,[]
for t in range(0,8): config_group_commands.append([L('Turn on/off commands, access %s') % t,'#room-commands%s' % t,[]])
tmp.sort()
for t in tmp:
	if t[0] <= 7:
		config_prefs['cmd_%s' % t[1]]=['%s - %s' % (t[1],t[4].split('\n',1)[0]) + ' %s',t[4],[True,False], True]
		config_group_commands[t[0]][2] = config_group_commands[t[0]][2] + ['cmd_%s' % t[1]]

for tmp in config_group_commands: config_groups.append(tmp)
'''

if os.path.isfile('settings/starttime'):
	try: starttime = int(readfile('settings/starttime'))
	except: starttime = readfile('settings/starttime')
else: starttime = int(time.time())
sesstime = int(time.time())
ownerbase = getFile(owners,[god])
ignorebase = getFile(ignores,[])
cu_age = []
close_age_null()
try:
	confbase = json.loads(readfile(confs))
except:
	confbase = ['%s/%s' % (defaultConf.lower(),Settings['nickname'])]
if os.path.isfile(cens):
	censor = readfile(cens).decode('UTF').replace('\r','').split('\n')
	cn = []
	for c in censor:
		if '#' not in c and len(c): cn.append(c)
	censor = cn
else: censor = []

pprint('*'*50,'blue')
pprint('*** Name: %s' % botName,'yellow')
pprint('*** Version: %s' % botVersion,'yellow')
pprint('*** OS: %s ' % botOs,'yellow')
pprint('*'*50,'blue')
pprint('*** (c) 2oo9-%s Disabler Production Lab.' % str(time.localtime()[0]).replace('0','o'),'bright_cyan')

float_pyver = float(sys.version[:3])

if float_pyver  < 2.7:
	draw_warning('Required Python >= 2.7')
	sys.exit('exit')

lastnick = Settings['nickname']
jid = JID(Settings['jid'])
if getResourse(jid) in ['None','']: jid = JID(Settings['jid'].split('/')[0]+'/my owner is stupid and can not complete the configuration')
selfjid = jid
pprint('JID: %s' % unicode(jid),'light_gray')

message_exclude_update()

try:
	try:
		Server = tuple(server.split(':'))
		Port = int(server.split(':')[1])
		pprint('Trying to connect to %s' % server,'yellow')
	except: Server,Port = None,5222
	if dm: cl = Client(jid.getDomain(),Port,ENABLE_TLS=ENABLE_TLS)
	else: cl = Client(jid.getDomain(),Port,debug=[],ENABLE_TLS=ENABLE_TLS)
	try:
		Proxy = proxy
		pprint('Using proxy %s' % Proxy['host'],'green')
	except NameError: Proxy = None
	try:
		Secure = secure
		pprint('Tryins secured connection','cyan')
	except NameError: Secure = None
	cl.connect(Server,Proxy,Secure,ENABLE_TLS=ENABLE_TLS)
	pprint('Connected','yellow')
	cl.auth(jid.getNode(), Settings['password'], jid.getResource())
	pprint('Autheticated','yellow')
except:
	pprint('Auth error or no connection. Restart in %s sec.' % GT('reboot_time'),'red')
	time.sleep(GT('reboot_time'))
	sys.exit('restart')
pprint('Registration Handlers','yellow')
cl.RegisterHandler('message',messageCB)
cl.RegisterHandler('iq',iqCB)
cl.RegisterHandler('presence',presenceCB)
cl.RegisterDisconnectHandler(disconnecter)
cl.UnregisterDisconnectHandler(cl.DisconnectHandler)
if GT('show_loading_by_status'):
	if GT('show_loading_by_status_show') == 'online': caps_and_send(Presence(status=GT('show_loading_by_status_message'), priority=Settings['priority']))
	else: caps_and_send(Presence(show=GT('show_loading_by_status_show'), status=GT('show_loading_by_status_message'), priority=Settings['priority']))
else:
	if Settings['status'] == 'online': caps_and_send(Presence(status=Settings['message'], priority=Settings['priority']))
	else: caps_and_send(Presence(show=Settings['status'], status=Settings['message'], priority=Settings['priority']))
#cl.sendInitPresence()

pprint('Wait conference','yellow')
time.sleep(0.5)
game_over = None
thr(sender_stack,(),'sender')
thr(remove_ignore,(),'ddos_remove')
cb = []
is_start = True
lastserver = getServer(confbase[0].lower())
setup = getFile(c_file,{})
join_percent, join_pers_add = 0, 100.0/len(confbase)

for tocon in confbase:
	tocon = tocon.strip()
	if '\n' in tocon: pprint('->- %s | pass: %s' % tuple(tocon.split('\n',1)),'green')
	else: pprint('->- %s' % tocon,'green')
	try: t = setup[getRoom(tocon)]
	except:
		setup[getRoom(tocon)] = {}
		writefile(c_file,str(setup))
	baseArg = unicode(tocon)
	if '/' not in baseArg: baseArg += '/%s' % unicode(Settings['nickname'])
	if '\n' in baseArg: baseArg,passwd = baseArg.split('\n',2)
	else: passwd = ''
	zz = joinconf(baseArg, getServer(Settings['jid']),passwd)
	while unicode(zz)[:3] == '409' and not game_over:
		time.sleep(1)
		baseArg += '_'
		zz = joinconf(baseArg, getServer(Settings['jid']),passwd)
	cb.append(baseArg)
	pprint('-<- %s' % baseArg,'bright_green')
	if GT('show_loading_by_status_percent'):
		join_percent += join_pers_add
		join_status = '%s %s%%' % (GT('show_loading_by_status_message'),int(join_percent))
		if GT('show_loading_by_status'):
			if GT('show_loading_by_status_room'): join_status = '%s [%s]' % (join_status,tocon)
			if GT('show_loading_by_status_show') == 'online': caps_and_send(Presence(status=join_status, priority=Settings['priority']))
			else: caps_and_send(Presence(show=GT('show_loading_by_status_show'), status=join_status, priority=Settings['priority']))
	if game_over: break
confbase = cb
is_start = None
pprint('Joined','white')

#pep = xmpp.Message(to=selfjid, frm=getRoom(selfjid), payload=[xmpp.Node('event',{'xmlns':'http://jabber.org/protocol/pubsub#event'},[xmpp.Node('items',{'node':'http://jabber.org/protocol/tune'},[xmpp.Node('item',{'id':'current'},[xmpp.Node('tune',{'xmlns':'http://jabber.org/protocol/tune'},[])])])])])
#sender(pep)

thr(now_schedule,(),'schedule')
thr(iq_async_clean,(),'async_iq_clean')
thr(presence_async_clean,(),'async_presence_clean')
try: thr(bomb_random,(),'bomb_random')
except: pass

if GT('show_loading_by_status'):
	if Settings['status'] == 'online': caps_and_send(Presence(status=Settings['message'], priority=Settings['priority']))
	else: caps_and_send(Presence(show=Settings['status'], status=Settings['message'], priority=Settings['priority']))

while 1:
	try:
		while not game_over:
			cyc = cl.Process(1)
			if str(cyc) == 'None': cycles_unused += 1
			elif int(str(cyc)): cycles_used += 1
			else: cycles_unused += 1
		atempt_to_shutdown(False)
		sys.exit(bot_exit_type)

	except KeyboardInterrupt: atempt_to_shutdown_with_reason(L('Shutdown by CTRL+C...'),0,'exit',False)

	except SystemShutdown: atempt_to_shutdown_with_reason(L('System Shutdown. Trying to restart in %s sec.') % GT('reboot_time'),GT('reboot_time'),'restart',False)

	except Exception, SM:
		try: SM = str(SM)
		except: SM = unicode(SM)
		pprint('*** Error *** %s ***' % SM,'red')
		logging.exception(' [%s] ' % timeadd(tuple(time.localtime())))
		if 'parsing finished' in SM.lower() or 'database is locked' in SM.lower(): atempt_to_shutdown_with_reason(L('Critical error! Trying to restart in %s sec.') % int(GT('reboot_time')/4),GT('reboot_time')/4,'restart',True)
		if debugmode: raise

# The end is near!
