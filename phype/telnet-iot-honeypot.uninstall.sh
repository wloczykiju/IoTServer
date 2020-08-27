#!/bin/bash

systemctl stop apache2 #stop apache server

for MYPID in `ps -ef | grep "python.*honeypot.py" | grep -v grep | awk '{print $2}'` # find all processes (id's) creted by honeypot.py with grep and stop them
do
  echo "kill honeypot.py MYPID=$MYPID"
  test -n "$MYPID" && kill $MYPID
done

# root     19142 19052  2 20:56 pts/1    00:00:00 /usr/bin/python /root/telnet-iot-honeypot/backend.py
for MYPID in `ps -ef | grep "python.*backend.py" | grep -v grep | awk '{print $2}'` # do the same for the backend.py processes
do
  echo "kill backend.py MYPID=$MYPID"
  test -n "$MYPID" && kill $MYPID
done

apt-get remove -y python-setuptools python-werkzeug \ # remove dependencies
	python-flask python-flask-httpauth python-sqlalchemy \
	python-requests python-decorator python-dnspython \
	python-ipaddress python-simpleeval python-yaml

pip uninstall -r telnet-iot-honeypot/requirements.txt  # remove requirements

apt-get remove -y python-pip libmysqlclient-dev python-mysqldb git sqlite3 apache2  

apt-get autoremove -y  # autoremove to clean the updates repo

rm -rf telnet-iot-honeypot  # remove the folder
