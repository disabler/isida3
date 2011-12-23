short howto for isida-bot

- installation -

no need. download by svn in any folder from official repository by:
svn co svn://isida-bot.com/svn/trunk isida
or
git clone git://github.com/disabler/isida.git isida

- launch -

1. rename defaul_config.py to config.py and fill look inside
2. create startup databases with "python create_databases.py" command
3. indexate databases "python indexate_databases.py"
4. type in console: sh launch.sh for launch

- update -

after global bot update - launch "sh update" script for correct update.


- fast install and launch -

svn co svn://isida-bot.com/svn/trunk isida or git clone git://github.com/disabler/isida.git isida
cd isida/settings
cp demo_config.py config.py
nano config.py
cd ..
python create_databases.py
python indexate_databases.py
sh launch.sh &

that's all :)

(c) Disabler Producion Lab.
