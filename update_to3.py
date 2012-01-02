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

def values_validator(tp):
	ins_vals = []
	for t in tp:
		ud = '%s' % t
		val = ["'%s'" % t,ud][ud == ''.join(re.findall('([-]?[0-9]+)',ud))]
		if "'" in val[1:-1]: val = val[0] + val[1:-1].replace("'","''") + val[-1]
		if not len(val): val = "''"
		val = val.replace('\\','\\\\')
		ins_vals.append(val)
	return ','.join(ins_vals)

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
				req = 'insert into %s values(%s);' % (to_base,values_validator(t))
				cur.execute(req)
		conn.commit()
	
print 'Updater for Isida Jabber Bot from 2.x to 3.x'
print '(c) Disabler Production Lab.'

if os.path.isfile(configname): execfile(configname)
else:
	print '%s is missed.' % configname
	sys.exit()
	
try: _,_,_,_ = base_name,base_user,base_host,base_pass
except:
	print 'Missed settings for PostgreSQL!'
	sys.exit()

conn=psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (base_name,base_user,base_host,base_pass));
cur = conn.cursor()

bases_arr = [[agestat,'age','age'],[jidbase,'jid','jid'],[talkers,'talkers','talkers'],[wtfbase,'wtf','wtf'],
			 [answers,'answer','answer'],[saytobase,'st','sayto'],[distbase,'dist','dist'],[distbase_user,'dist','dist_user'],
			 [karmabase,'karma','karma'],[karmabase,'commiters','karma_commiters'],[karmabase,'limits','karma_limits'],
			 [acl_base,'acl','acl'],[wzbase,'wz','wz'],[gisbase,'gis','gis'],[def_phone_base,'ru_stat','def_ru_stat'],
			 [def_phone_base,'ua_stat','def_ua_stat'],[def_phone_base,'ru_mobile','def_ru_mobile'],[muc_lock_base,'muc','muc_lock']]

for t in bases_arr: convert_base(t[0],t[1],t[2])

cur.close()
conn.commit()
conn.close()

print 'Finished!'
