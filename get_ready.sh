!/bin/bash

sudo apt update
sudo apt install -y net-tools wget libpcap-dev

pip3 -m venv venv
. venv/bin/activate
sudo pip3 install scapy colorama

wget https://raw.githubusercontent.com/x4nth055/pythoncode-tutorials/master/scapy/http-sniffer/http_sniffer.py

sudo python3 http_sniffer.py -i eht0
