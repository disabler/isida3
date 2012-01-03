short howto for isida-bot

- installation -

#download by svn in any folder from official repository by:
git clone git://github.com/disabler/isida3.git isida

#create bases:
su postgres
createuser -P isidabot
createdb isidabot -E UTF8 -T template0
psql -U isidabot isidabot -f pgsql.schema
exit

- launch -

1. rename defaul_config.py to config.py and fill look inside
2. create startup databases with "python create_databases.py" command
3. indexate databases "python indexate_databases.py"
4. python update_to3.py
5. type in console: "sh launch.sh &" for launch


- fast install and launch -

git clone git://github.com/disabler/isida3.git isida
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
