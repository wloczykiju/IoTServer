#!/bin/bash

apt-get update # update the server

apt install -y git python-setuptools python-pycurl # install python packages

git clone https://github.com/omererdem/honeything # clone the project from GitHub repo

cd honeything # go to the folder

python2 setup.py install --record installation.files.txt # install along with packages required

# tell /etc/init.d to use python2 - as it differs depending on ubuntu server distributions 
sed -i -e '/nohup/s/python /python2 /' /etc/init.d/honeything

/etc/init.d/honeything start # start honeypot
