short howto for isida-bot


-------- depends --------

1. python-psycopg2 >= 2.4.2
2. python >= 2.7
3. git-core >= 1.7.1 or subversion >= 1.6.12
4. postgresql >= 8.4
5. openssl >= 1.0.0e
6. python-crontab >= 0.12


-------- download --------

from git: git clone git://github.com/disabler/isida3.git isida
from svn: svn co http://isida-bot.com/svn/branch isida


--------- create bases --------

su postgres
createuser -P isidabot
createdb isidabot -E UTF8 -T template0
psql -U isidabot isidabot -f pgsql.schema
exit


-------- launch --------

1. copy demo_config.py to config.py and fill look inside
2. create startup databases with "python create_databases.py" command
3. indexate databases "python indexate_databases.py"
4. python update_to3.py
5. type in console: "sh launch.sh &" for launch


-------- update to 3rd version --------

1. copy all files from old_bots_version/settings/ to isida3/settings/
2. copy demo_config.py to config.py and fill look inside
3. python update_to3.py
4. type in console: "sh launch.sh &" for launch


-------- fast install and launch --------

git clone git://github.com/disabler/isida3.git isida
# or
# svn co http://isida-bot.com/svn/branch isida
cd isida
su postgres
createuser -P isidabot
createdb isidabot -E UTF8 -T template0
psql -U isidabot isidabot -f pgsql.schema
exit
cd settings
cp demo_config.py config.py
nano config.py
cd ..
python create_databases.py
python indexate_databases.py
python update_to3.py
sh launch.sh &

that's all :)

(c) Disabler Producion Lab.
