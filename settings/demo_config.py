# -*- coding: utf-8 -*-

#------------------------------------------------
#			 Isida-bot Config file
#					v1.6ru
#------------------------------------------------

Settings = {
'nickname': 		u'<пишем сюда ник бота>',					# Ник бота в конференциях
'jid':				u'isida-jabber-bot@domain.tld/isida-bot',	# Jid бота с ресурсом
'password':			u'********',								# Пароль
'status':			u'online',									# Статус бота chat|online|away|xa|dnd
'priority':			0,											# Приоритет
'message':			u'Йа аццкое железко!'}						# Статус-сообщение
#proxy = {'host':'localhost','port':3128,'user':'me','password':'secret'}	# Прокси
#proxy = {'host':'127.0.0.1','port':3128,'user':'','password':''}
#proxy = {'host':'localhost','port':3128}
#server = 'allports.jabber.ru:443'								# Подключение минуя ресольвер
#secure = True													# Включение ssl/tls
#http_proxy = {'host':'localhost','port':3128,'user':'me','password':'secret'}	# Http-прокси
#http_proxy = {'host':'127.0.0.1','port':3128,'user':None,'password':None}
SuperAdmin		=	u'aaa@bbb.ru'								# Jid владельца бота
defaultConf		=	u'isida@conference.jabber.ru'				# Стартовая конференция
prefix			=	u'_'										# Префикс команд по умолчанию
msg_limit		=	2048										# Лимит размера сообщений
#ignore_owner	=	True										# не исполнять для владельца бота отключенные команды
#debugmode		=	True										# режим _не_игнорировать_ошибки_
#dm				=	True										# режим отладки xmpppy
#dm2			=	True										# режим показа действий бота в консоле
CommandsLog		=	True										# Логгирование команд бота
#thread_type	=	None										# тип тредов thread/threading. по умолчанию - threading
#ENABLE_TLS		=	None										# если бот падает при обзоре сервисов jid'а в ростере - надо принудительно отключить TLS

#----- Настройка баз данных -----
base_name = 'isidabot'  # название базы для PostgreSQL
base_user = 'isidabot'  # пользователь базы для PostgreSQL
base_host = 'localhost' # хост базы для PostgreSQL
base_pass = '******'    # пароль базы для PostgreSQL
base_port = '5432'		# порт для подключения к PostgreSQL

#-------------- Файлы, пути к файлам -----------#
slog_folder = 'log/'							# папка системных логов
set_folder 	= 'settings/'						# папка настроек
back_folder = 'backup/'							# папка хранения резервных копий
loc_folder 	= 'locales/'						# папка локализаций
log_folder 	= 'logs/'							# папка логов конференций
LOG_FILENAME = slog_folder+'error.txt'			# логи ошибок
c_file = set_folder+'conference.config'			# конфиг конференции
ow_file = set_folder+'owner.config'				# системный конфиг бота
ver_file = set_folder+'version'					# версия бота
alfile = set_folder+'aliases'					# сокращения
owners = set_folder+'owner'						# база владельцев
ignores = set_folder+'ignore'					# черный список
confs = set_folder+'conf'						# список активных конф
feeds = set_folder+'feed'						# список rss каналов + md5 последниx новостей по каждому каналу
cens = set_folder+'censor.txt'					# список "запрещенных" слов для болтуна
conoff = set_folder+'commonoff'					# список "запрещенных" команд для бота
saytobase = set_folder+'sayto.db'				# база команды "передать"
agestatbase = set_folder+'agestat.db'			# статистика возрастов
talkersbase = set_folder+'talkers.db'			# статистика болтунов
wtfbase = set_folder+'wtfbase2.db'				# определения
answersbase = set_folder+'answers.db'			# ответы бота
scrobblebase = set_folder+'scrobble.db'			# база PEP скробблера
loc_file = set_folder+'locale'					# файл локализации
time_limit_base = set_folder+'saytoowner.db'	# файл ограничений команды msgtoadmin
wzbase = set_folder+'wz.db'						# база кодов для команд wz*
gisbase = set_folder+'gis.db'					# база кодов для команд gis*
hide_conf = set_folder+'hidenroom.db'			# файл скрытых конференций
jid_base = set_folder+'jidbase.db'				# статистика jid'ов
top_base = set_folder+'topbase.db'				# активность конференции
blacklist_base = set_folder + 'blacklist.db'	# черный список конференций
karmabase = set_folder+'karma.db'				# база кармы
log_conf = set_folder+'logroom.db'				# список конференций с логами
tban = set_folder+'temporary.ban'				# лог временного бана
ignoreban = set_folder+'ignoreban.db'			# список игнора при глобальном бане
spy_base = set_folder+'spy.db'					# база слежения
public_log = log_folder+'chatlogs'				# папка для записи публичных логов конференций
system_log = log_folder+'syslogs'				# папка для записи системных логов конференций
logs_css_path = '../../../.css/isida.css'		# путь к css файлу для логов
tld_list = 'tld/tld.list'						# список tld кодов
poke_file = 'plugins/poke.txt'					# список ответов для команды poke
answers_file = 'answers.txt'					# имя файла по умолчанию для импорта/экспорта ответов
date_file = 'plugins/date.txt'					# список праздников
pastepath = 'paste/'							# Путь для больших сообщений
pasteurl  = 'http://isida-bot.com/paste/'		# Url для сообщений
paste_css_path = '.css/isida.css'				# Путь к css
default_msg_limit = msg_limit					# Размер сообщений по умолчанию
smile_folder = '.smiles'						# папка со смайлами в чатлогах
smile_descriptor = 'icondef.xml'				# дескриптор смайлов
#-----------------------------------------------#
adblock_regexp = [u'([-0-9a-zа-я_+]+@c[-0-9a-z-.]+)', # Регекспы для блокиратора рекламы, регистронезависимые
				  #u'зайди.*? .*?конф.*? .*?([-0-9a-zа-я_+]+@?)',
				  #u'заходи.*? .*?конф.*? .*?([-0-9a-zа-я_+]+@?)',
				  #u'зайди.*? .*?в.*? .*?([-0-9a-zа-я_+]+@?)',
				  #u'заходи.*? .*?в.*? .*?([-0-9a-zа-я_+]+@?)',
				  #u'конф.*? .*?([-0-9a-zа-я_+]+@?).*?зайди',
				  #u'конф.*? .*?([-0-9a-zа-я_+]+@?).*?заходи',
				  #u'все.*? .*?в.*? .*?([-0-9a-zа-я_+]+@?)',
				  u'https?://(.*?icq.*?/[-a-z0-9?+./=?&]*?)']
#-----------------------------------------------#
