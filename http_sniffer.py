import os
import socket
import json

from scapy.all import *
from scapy.layers.http import HTTPRequest

import logging

# Set up the logger
logger = logging.getLogger('wibeee_sniffer')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# CONFIGURATION
iface = os.getenv('IFACE') or "qvs1"
filtre = os.getenv('FILTER') or "(host 10.2.8.224 or host 10.2.8.225) and (port 8080)"
# send URL QS params to NodeRED using UDP
UDP_IP = os.getenv('UDP_IP') or "10.2.10.11"
UDP_PORT = os.getenv('UDP_PORT') or 58088
UDP_PORT = int(UDP_PORT)

def process_packet(packet):
    if packet.haslayer(HTTPRequest):
        # if this packet is an HTTP Request
        # get the requested URL
        url = packet[HTTPRequest].Host.decode() + packet[HTTPRequest].Path.decode()
        # get the requester's IP Address
        ip = packet[IP].src
        # get the request method
        method = packet[HTTPRequest].Method.decode()
        
        logger.info(f"\n{ip} {method} {url}")
        if packet.haslayer(Raw) and method == "POST":
            logger.debug(f"\n{packet[Raw].load}")
            return

        # packet empty return
        if len(url) < 400:
            logger.debug('URL too short, less than 400 bytes.')
            return
        
        # getting the URL querystring
        aux = url.split("?")[1]
        logger.debug(f"URL: {aux}")

        # creating object with query string parameters
        buf = {}
        for item in aux.split("&"):
            i = item.split("=")
            buf[i[0]] = i[1]

        payload = bytes(json.dumps(buf), "utf-8")
        sock.sendto(payload, (UDP_IP, UDP_PORT))
        logger.debug(f"{UDP_IP}:{UDP_PORT} {payload}")

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

    sniff(filter=filtre, prn=process_packet, iface=iface, store=False)
