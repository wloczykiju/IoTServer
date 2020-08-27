#!/bin/bash

# Update & Install all requirements:
apt-get update
apt-get install -y python-pip libmysqlclient-dev python-mysqldb git sqlite3 apache2

git clone https://github.com/Phype/telnet-iot-honeypot.git # clone from GitHub repo
cd telnet-iot-honeypot
pip install -r requirements.txt # install packages from reqirements.txt

apt-get install -y python-setuptools python-werkzeug \ 
	python-flask python-flask-httpauth python-sqlalchemy \
	python-requests python-decorator python-dnspython \
	python-ipaddress python-simpleeval python-yaml

# Create a config:
bash create_config.sh

# Start the backend:
python backend.py &

# Now, start the honeypot:
python honeypot.py &

#To test the honeypot
#telnet 127.0.0.1 2323

# Frontend

cp -R html /var/www
chown www-data:www-data /var/www -R

# tell apache to listen on port 8090 instead of 80 ( enables installation of other honeypots on port 80 )
sed -i -e '/Listen/s/80/8090/' /etc/apache2/ports.conf
sed -i -e '/Listen/s/80/8090/' /etc/apache2/sites-enabled/000-default.conf
# start apache
systemctl start apache2

