#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    iSida Jabber Bot                                                         #
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

import os, sys, time, re
pid_file = 'isida.pid'
updatelog_file = 'update.log'

def readfile(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def writefile(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

def tZ(val):
	val = str(val)
	if len(val) == 1: val = '0'+val
	return val

def printlog(text):
	print text
	lt = tuple(time.localtime())
	fname = 'log/crash_'+tZ(lt[0])+tZ(lt[1])+tZ(lt[2])+'.txt'
	fbody = tZ(lt[3])+tZ(lt[4])+tZ(lt[5])+'|'+text+'\n'
	fl = open(fname, 'a')
	fl.write(fbody.encode('utf-8'))
	fl.close()

def crash(text):
	printlog(text)
	sys.exit()

def rm(file):
	try: os.remove(file)
	except: pass

if os.name == 'nt': printlog('Warning! Correct work only on *NIX system!')

try: writefile('settings/starttime',str(int(time.time())))
except:
	printlog('\n'+'*'*50+'\n Isida is crashed! Incorrent launch!\n'+'*'*50+'\n')
	raise

if os.path.isfile(pid_file) and os.name != 'nt':
	try: last_pid = int(readfile(pid_file))
	except: crash('Unable get information from %s' % pid_file)
	try:
		os.getsid(last_pid)
		crash('Multilaunch detected! Kill pid %s before launch bot again!' % last_pid)
	except Exception, SM:
		if not str(SM).lower().count('no such process'): crash('Unknown exception!\n%s' % SM)

writefile(pid_file,str(os.getpid()))

rm('settings/version')
if os.name == 'nt': os.system('svnversion >> settings/version')
else: os.system('echo `svnversion` >> settings/version')
rm(updatelog_file)
os.system('echo Just Started! >> %s' % updatelog_file)

while 1:
	try: execfile('kernel.py')
	except KeyboardInterrupt: break
	except SystemExit, mode:
		mode = str(mode)
		if mode == 'update':
			rm('settings/ver')
			rm('settings/version')
			if os.name == 'nt':
				os.system('svnversion >> settings/ver')
				os.system('svn up')
				os.system('svnversion >> settings/version')
			else:
				os.system('echo `svnversion` >> settings/ver')
				os.system('svn up')
				os.system('echo `svnversion` >> settings/version')
			try: ver = int(re.findall('[0-9]+',readfile('settings/version'))[0]) - int(re.findall('[0-9]+',readfile('settings/ver'))[0])
			except: ver = -1
			rm(updatelog_file)
			if ver > 0:	 os.system('svn log --limit %s >> %s' % (ver,updatelog_file))
			elif ver < 0: os.system('echo Failed to detect version! >> %s' % updatelog_file)
			else: os.system('echo No Updates! >> %s' % updatelog_file)
		elif mode == 'exit': break
		elif mode == 'restart': pass
		else:
			printlog('unknown exit type!')
			break
	except Exception, SM:
		try: SM = str(SM)
		except: SM = unicode(SM)
		printlog('\n'+'*'*50+'\n Isida is crashed! It\'s imposible, but You do it!\n'+'*'*50+'\n')
		printlog(SM+'\n')
		raise
