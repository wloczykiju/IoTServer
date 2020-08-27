#!/bin/bash
# Install git and python dependencies 
apt-get update
apt install git
apt install python3-pip
apt-get install -y python3-venv

# Setup a new venv for Kako (this may require python3-pip and python3-venv to be installed via apt)
mkdir ~/honeypot
cd ~/honeypot
python3 -m venv kakovenv
source ~/honeypot/kakovenv/bin/activate
    
# Clone Kako and simulations.
git clone https://github.com/darkarnium/kako.git 
cd kako
cd sample
git clone https://github.com/darkarnium/kako-simulations.git simulations
    
# Install
cd ..
python3 -m pip install wheel
python3 -m pip install .
    
# Run and watch the log. Results (interactions) are be written to /tmp/ - per sample/kako.yaml
kako-master --configuration-file ./sample/kako.yaml &
tail -F kako.log


