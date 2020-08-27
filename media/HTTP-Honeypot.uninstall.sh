#!/bin/bash

#root     29922 14622  0 22:54 pts/0    00:00:00 python honeyserver.py
for MYPID in `ps -ef | grep "python.*honeyserver.py" | grep -v grep | awk '{print $2}'` # find all processes (id's) creted by honeypotserver.py with grep and stop them
do
  echo "kill honeyserver.py MYPID=$MYPID"
  test -n "$MYPID" && kill $MYPID
done

systemctl stop mysqld #stop mysql database process

rm -rf /var/lib/mysql # remove it

apt-get remove -y git mariadb-server mariadb-client python-mysql.connector python-mysqldb nmap httrack # remove other dependecies

apt-get autoremove -y # autoremove to clean the updates repo

rm -rf HTTP-Honeypot # remove the folder
