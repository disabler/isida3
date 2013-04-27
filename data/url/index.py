#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Bug Tracker                                                              #
#    Copyright (C) diSabler <dsy@dsy.name>                                    #
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
#    along with this program.  If nоt, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
# --------------------------------------------------------------------------- #

import psycopg2,sys,time,os,cgi,urllib2

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

def disp_time(t):
	lt=tuple(time.localtime(t))
	return '%02d:%02d:%02d, %02d.%s\'%02d, %s' % (lt[3],lt[4],lt[5],lt[2],wmonth[lt[1]-1],lt[0],wday[lt[6]])

def L(text):
	if not len(text): return text
	try: return locales[text]
	except: return text

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

def issue_for_web(i):
	m = [['&','&amp;'],['<','&lt;'],['>','&gt;'],['\'','&apos;'],['"','&quot;'],['\n- ','\n <li>'],['\n - ','\n <li>'],['\n','<br>']]
	for t in m: i = i.replace(t[0],t[1])
	return i
	
html_head = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" lang="ru"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link href=".css/isida.css" rel="stylesheet" type="text/css" />
<link rel="shortcut icon" href="/icon.ico">
<title>List of URL</title></head>
<body>
<div class="title">%s</div>

<div class="main">
<p>'''
html_end = '''
</p></div><br>
%s</body></html>
'''

configname = '/usr/bots/isida/settings/config.py'
execfile(configname)
max_link_size = 64
url_count_limit = 100

conn = psycopg2.connect(database=base_name, user=base_user, host=base_host, password=base_pass, port=base_port)

form = cgi.FieldStorage()

try: room = form.getvalue('room').decode('utf8')
except: room = ' '
roomz = [t[0] for t in cur_execute_fetchall('select room from url group by room order by room;')]
roomz = [' '] + roomz
if not roomz: print 'Error! Stored URL not found!'
if not room or room not in roomz: room = roomz[0]

try: nick = form.getvalue('nick').decode('utf8')
except: nick = ' '
nickz = [t[0] for t in cur_execute_fetchall('select nick from url group by nick order by nick;')]
nickz = [' '] + nickz
if not nickz: print 'Error! Stored URL not found!'
if not nick or nick not in nickz: nick = nickz[0]

drop_list = '''<form action="/url/" method=post>
<select name="room">
%s</select>
<select name="nick">
%s</select>
<input type=submit value="&nbsp;apply&nbsp;">
</form>'''

drop_opt = '<option value="%s">%s\n'

dopt_r = drop_opt % (room,room) + ''.join([drop_opt % (t,t) for t in roomz if t != room])
dopt_n = drop_opt % (nick,nick) + ''.join([drop_opt % (t,t) for t in nickz if t != nick])

print html_head % (drop_list % (dopt_r.encode('utf8'),dopt_n.encode('utf8')),)

if room != ' ':
	if nick != ' ':
		url_count = cur_execute_fetchall('select count(*) from url where room=%s;',(room,))[0][0]
		url = cur_execute_fetchall('select jid,nick,time,url,title from url where room=%s and nick=%s order by -time limit %s;',(room,nick,url_count_limit))
	else:
		url_count = cur_execute_fetchall('select count(*) from url where room=%s;',(room,))[0][0]
		url = cur_execute_fetchall('select jid,nick,time,url,title from url where room=%s order by -time limit %s;',(room,url_count_limit))
else:
	if nick != ' ':
		url_count = cur_execute_fetchall('select count(*) from url;')[0][0]
		url = cur_execute_fetchall('select jid,nick,time,url,title from url where nick=%s order by -time limit %s;',(nick,url_count_limit,))
	else:
		url_count = cur_execute_fetchall('select count(*) from url;')[0][0]
		url = cur_execute_fetchall('select jid,nick,time,url,title from url order by -time limit %s;',(url_count_limit,))
if url:
	tm = []
	color = int('ccc',16)
	mask = color ^ int('eee',16)
	for t in url:
		ll = urllib2.unquote(t[3].encode('utf8')).decode('utf8')
		lnk = ll if len(ll) < max_link_size else '%s...' % ll[:max_link_size]
		if t[4]: text = t[4].strip()
		else: text = '-'
		if len(text) >= max_link_size: text = '%s...' % text[:max_link_size]
		tmp = '<tr bgcolor="#%s">\n<td align="center">&nbsp;%s&nbsp;</td>\n<td align="center">&nbsp;%s&nbsp;</td>\n<td>&nbsp;<a href="%s" target="_blank">%s</a></td>\n<td>&nbsp;%s</td>\n</tr>\n' % (hex(color)[2:],'%04d.%02d.%02d&nbsp;%02d:%02d:%02d' % time.localtime(t[2])[:6],t[1],t[3],lnk,text)
		tm.append(tmp.encode('utf-8'))
		color = color ^ mask
	print '''
<table border="1" class="urlbody" width="100%" cellpadding="0" cellspacing="0">
<tr align="center" class="urlheader">
'''
	print '<td><b>%s .. %s of %s</b></td>' % (1,len(url),url_count)
	print '''
</tr>
</table>
'''
	print '''
<table border="1" class="urlbody" width="100%" cellpadding="0" cellspacing="0">
<tr align="center" class="urltitle">
<td><b>Date</b></td>
<td><b>&nbsp;Nick&nbsp;</b></td>
<td><b>URL</b></td>
<td><b>Title</b></td>
</tr>
	'''
	print ''.join(tm)
	print '</table>'
else: 
	print '''
<table border="1" class="paste" width="100%" cellpadding="0" cellspacing="0">
<tr align="center" class="paste">
<td>&nbsp;URL not found!</td>
</tr>
</table>
	'''
print html_end % cur_execute_fetchall('select value from config_owner where option=%s;',('html_logs_end_text',))[0][0]
