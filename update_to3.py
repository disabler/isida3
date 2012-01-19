#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Update iSida Jabber Bot from version 2.x to 3.x                          #
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

import os, sys, sqlite3, psycopg2, re

set_folder = u'settings/%s'

agestat = set_folder % 'agestat.db'
jidbase = set_folder % 'jidbase.db'
talkers = set_folder % 'talkers.db'
wtfbase = set_folder % 'wtfbase2.db'
answers = set_folder %'answers.db'
saytobase = set_folder % 'sayto.db'
distbase = set_folder % 'dist.db'
distbase_user = set_folder % 'dist_user.db'
karmabase = set_folder % 'karma.db'
acl_base = set_folder %'acl.db'
wzbase = set_folder % 'wz.db'
gisbase = set_folder % 'gis.db'
def_phone_base = set_folder % 'defcodes.db'
muc_lock_base = set_folder % 'muclock.db'

configname = 'settings/config.py'

def convert_base(filename,from_base,to_base):
	global conn
	if os.path.isfile(filename):
		s_conn = sqlite3.connect(filename)
		s_cur = s_conn.cursor()
		tmp = s_cur.execute('select * from %s' % from_base).fetchall()
		print 'Import %s, Base %s->%s, %s records' % (filename, from_base, to_base, len(tmp))
		s_conn.close()
		if tmp:
			for t in tmp:
				req = 'insert into %s values(%s);' % (to_base,','.join(['%'+a for a in 's'*len(t)]))
				cur.execute(req,t)
		conn.commit()
	
print 'Updater for Isida Jabber Bot from 2.x to 3.x'
print '(c) Disabler Production Lab.'

if os.path.isfile(configname): execfile(configname)
else:
	print '%s is missed.' % configname
	sys.exit()
	
try: _,_,_,_,_ = base_name,base_user,base_host,base_pass,base_port
except:
	print 'Missed settings for PostgreSQL!'
	sys.exit()

conn=psycopg2.connect(database=base_name, user=base_user, host=base_host, password=base_pass, port=base_port)
cur = conn.cursor()

bases_arr = [[jidbase,'jid','jid'],[talkers,'talkers','talkers'],[wtfbase,'wtf','wtf'],
			 [answers,'answer','answer'],[saytobase,'st','sayto'],[distbase,'dist','dist'],[distbase_user,'dist','dist_user'],
			 [karmabase,'karma','karma'],[karmabase,'commiters','karma_commiters'],[karmabase,'limits','karma_limits'],
			 [acl_base,'acl','acl'],[wzbase,'wz','wz'],[gisbase,'gis','gis'],[def_phone_base,'ru_stat','def_ru_stat'],
			 [def_phone_base,'ua_stat','def_ua_stat'],[def_phone_base,'ru_mobile','def_ru_mobile'],[muc_lock_base,'muc','muc_lock']]

from_base = to_base = 'age'
if os.path.isfile(agestat):
	s_conn = sqlite3.connect(agestat)
	s_cur = s_conn.cursor()
	tmp = s_cur.execute('select * from %s' % from_base).fetchall()
	print 'Import %s, Base %s->%s, %s records' % (agestat, from_base, to_base, len(tmp))
	s_conn.close()
	if tmp:
		for t in tmp:
			req = 'insert into %s values(%s);' % (to_base,','.join(['%'+a for a in 's'*9]))
			cur.execute(req,list(t)+[t[1].lower()])
	conn.commit()
			 
for t in bases_arr: convert_base(t[0],t[1],t[2])

cur.close()
conn.commit()
conn.close()

print 'Finished!'
