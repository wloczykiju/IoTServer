apt-get install -y git mariadb-server mariadb-client python-mysql.connector python-mysqldb nmap httrack # install dependencies

git clone https://github.com/anouarbensaad/HTTP-Honeypot.git # clone repository

cd HTTP-Honeypot
# follow the author's instructions to create the database 
mysql -u root <<EOF  
CREATE DATABASE isetsohoney;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY 'isetso';
use isetsohoney;
CREATE TABLE log (id int NOT NULL PRIMARY KEY, date datetime, iphacker varchar(255), uri varchar(255));
EOF

#change login credentials to database
sed -i -e '/MySQLdb.connect/s/"honeydb".*/"localhost", "root", "isetso", "isetsohoney")/p' honeyserver.py

python2 honeyserver.py & # run honeypot
