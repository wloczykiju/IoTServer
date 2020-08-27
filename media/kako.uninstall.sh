#!/bin/bash


for MYPID in `ps -ef | grep "kako-master" | grep -v grep | awk '{print $2}'`
do
  echo "kill kako-master MYPID=$MYPID"
  test -n "$MYPID" && ps --no-header -fp $MYPID && kill $MYPID
done

apt-get -y remove python3-venv python3-pip git 

