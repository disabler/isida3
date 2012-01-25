#!/usr/bin/python
# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------- #
#                                                                             #
#    Plugin for iSida Jabber Bot                                              #
#    Copyright (C) 2012 diSabler <dsy@dsy.name>                               #
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

turn_base = []

def turner_raw(text,jid,nick):
	global turn_base
	rtab = L('qwertyuiop[]asdfghjkl;\'zxcvbnm,.`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>~')
	ltab = L('QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>~qwertyuiop[]asdfghjkl;\'zxcvbnm,.`')
	to_turn = text
	if not text:
		for tmp in turn_base:
			if tmp[0] == jid and tmp[1] == nick:
				turn_base.remove(tmp)
				to_turn = tmp[2]
				break
	if to_turn:
		if to_turn[:3] == '/me': msg, to_turn = '*%s' % nick, to_turn[3:]
		elif ': ' in to_turn: msg, to_turn = '%s:' % to_turn.split(': ',1)[0], to_turn.split(': ',1)[1]
		else: msg = ''
		for tt in re.findall('\s+[^\s]*', ' ' + to_turn):
			if re.findall('\s+(svn|http[s]?|ftp)(://)',tt,re.I+re.S+re.U) or re.findall(u'\s+[A-ZА-Я\d\']{2,}$',tt,re.U): msg += tt
			else: msg += ''.join([ltab[rtab.find(x)] if x in rtab else x for x in tt])
		msg = msg.strip()
		if get_config(getRoom(jid),'censor'): msg = to_censore(msg,jid)
		return msg
	else: return None

def turner(type, jid, nick, text):
	if not text and type != 'groupchat':
		send_msg(type, jid, nick, L('Not allowed in private!'))
		return
	to_turn = turner_raw(text,jid,nick)
	if to_turn: send_msg(type, jid, [nick,''][type=='groupchat'], to_turn)
	else: send_msg(type, jid, nick, L('What?'))

def append_to_turner(room,jid,nick,type,text):
	global turn_base
	for tmp in turn_base:
		if tmp[0] == room and tmp[1] == nick:
			turn_base.remove(tmp)
			break
	turn_base.append((room,nick,text))

def remove_from_turner(room,jid,nick,type,text):
	global turn_base
	if type == 'unavailable':
		for tmp in turn_base:
			if tmp[0] == room and tmp[1] == nick:
				turn_base.remove(tmp)
				break

def autoturn(room,jid,nick,type,text):
	if get_config(room,'autoturn') and type == 'groupchat':
		cof = getFile(conoff,[])
		if (room,'turn') in cof: return
		nowname = get_xnick(room)
		if nick == nowname: return
		text = re.sub('^%s[,:]\ ' % re.escape(nowname), '', text.strip())
		two_en = ['aa', 'aq', 'bc', 'bd', 'bf', 'bg', 'bh', 'bk', 'bn', 'bp', 'bq', 'bw', 'bx', 'bz', 'cb', 'cd', 'cf', 'cg', 'cj', 'cm', 'cn', 'cp', 'cs', 'cv', 'cw', 'cx', 'cz', 'db', 'dc', 'dh', 'dj', 'dp', 'dq', 'dt', 'dx', 'dz', 'ej', 'fb', 'fc', 'fd', 'fg', 'fh', 'fj', 'fk', 'fm', 'fn', 'fp', 'fq', 'fs', 'fv', 'fx', 'fz', 'gb', 'gc', 'gf', 'gj', 'gk', 'gp', 'gq', 'gv', 'gw', 'gx', 'gz', 'hc', 'hg', 'hh', 'hj', 'hk', 'hp', 'hq', 'hs', 'hv', 'hx', 'hz', 'ih', 'ii', 'ij', 'iq', 'iw', 'iy', 'jb', 'jc', 'jd', 'jf', 'jg', 'jh', 'jj', 'jk', 'jl', 'jm', 'jn', 'jq', 'jr', 'js', 'jt', 'jv', 'jw', 'jx', 'jy', 'jz', 'kb', 'kc', 'kd', 'kj', 'kk', 'km', 'kp', 'kq', 'kr', 'ks', 'kt', 'kv', 'kx', 'kz', 'lh', 'lj', 'ln', 'lq', 'lx', 'lz', 'mc', 'md', 'mg', 'mh', 'mj', 'mk', 'mq', 'mv', 'mw', 'mx', 'mz', 'nb', 'nr', 'oq', 'pc', 'pf', 'pj', 'pk', 'pq', 'pv', 'px', 'pz', 'qa', 'qb', 'qc', 'qd', 'qe', 'qf', 'qg', 'qh', 'qi', 'qj', 'qk', 'ql', 'qm', 'qn', 'qo', 'qp', 'qq', 'qr', 'qs', 'qt', 'qv', 'qw', 'qx', 'qy', 'qz', 'rj', 'rq', 'rx', 'rz', 'sj', 'sv', 'sx', 'sz', 'tb', 'td', 'tg', 'tj', 'tk', 'tq', 'tv', 'tx', 'tz', 'uh', 'uj', 'uo', 'uq', 'uu', 'uv', 'uw', 'ux', 'vb', 'vc', 'vd', 'vf', 'vg', 'vh', 'vj', 'vk', 'vl', 'vm', 'vn', 'vp', 'vq', 'vr', 'vs', 'vt', 'vu', 'vv', 'vw', 'vx', 'vz', 'wb', 'wc', 'wg', 'wj', 'wm', 'wp', 'wq', 'wt', 'wu', 'wv', 'wx', 'wz', 'xb', 'xd', 'xg', 'xj', 'xk', 'xl', 'xn', 'xo', 'xq', 'xr', 'xs', 'xu', 'xv', 'xw', 'xx', 'xz', 'yc', 'yd', 'yf', 'yg', 'yj', 'yk', 'yn', 'yq', 'yu', 'yv', 'yx', 'yy', 'yz', 'zb', 'zc', 'zd', 'zf', 'zg', 'zh', 'zi', 'zj', 'zk', 'zm', 'zn', 'zp', 'zq', 'zr', 'zs', 'zt', 'zu', 'zv', 'zw', 'zx']
		tmp = text.lower()
		if ': ' in tmp: tmp = tmp.split(': ',1)[1]
		count_two = 0
		if not sum([int(ord(t)>127) for t in tmp]):
			for tt in re.findall('\s+[^\s]*', ' ' + tmp):
				if not re.findall('\s+(svn|http[s]?|ftp)(://)',tt,re.S+re.U) and not re.findall(u'\s+[A-ZА-Я\d\']{2,}$',tt,re.U): count_two += sum([1 for k in two_en if k in tt])
			if len(tmp.split()) < count_two:
				to_turn = turner_raw(text,room,nick)
				if to_turn and to_turn != text:
					pprint('Autoturn text: %s/%s [%s] %s > %s' % (room,nick,jid,text,to_turn),'dark_gray')
					send_msg(type, room, '', to_turn)
				return True

global execute, message_act_control

message_control = [append_to_turner]
presence_control = [remove_from_turner]
message_act_control = [autoturn]

execute = [(3, 'turn', turner, 2, L('Turn text from one layout to another.'))]