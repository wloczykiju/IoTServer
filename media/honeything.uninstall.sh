#!/bin/bash

/etc/init.d/honeything stop # stop honeypot

xargs rm -rf < honeything/installation.files.txt  # remove all packages from requirements.txt
rm -rf /opt/honeything /var/log/honeything /etc/init.d/honeything #  remove installed honeypot and it's logs

apt remove -y git python-setuptools python-pycurl # remove dependencies

apt-get autoremove -y # autoremove to clean the updates repo

rm -rf honeything # remove the folder


