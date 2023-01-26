from scapy.all import *
from scapy.layers.http import HTTPRequest

import socket
import json

# sniffing parameters
iface = "qvs1"
filtre = "(host 10.2.8.224 or host 10.2.8.225) and (port 8080)"
# send URL QS params to NodeRED using UDP
UDP_IP = "10.2.10.11"
UDP_PORT = 58088

def process_packet(packet):
    if packet.haslayer(HTTPRequest):
        # if this packet is an HTTP Request
        # get the requested URL
        url = packet[HTTPRequest].Host.decode() + packet[HTTPRequest].Path.decode()
        # get the requester's IP Address
        ip = packet[IP].src
        # get the request method
        method = packet[HTTPRequest].Method.decode()
        
        print(f"\n{ip} {method} {url}")
        if packet.haslayer(Raw) and method == "POST":
            print(f"\n{packet[Raw].load}")
            return

        # packet empty return
        if len(url) < 400:
            return
        
        # getting the URL querystring
        aux = url.split("?")[1]
        # print(f"\n{aux}")

        # creating object with query string parameters
        buf = {}
        for item in aux.split("&"):
            i = item.split("=")
            buf[i[0]] = i[1]

        sock.sendto(bytes(json.dumps(buf), "utf-8"), (UDP_IP, UDP_PORT))

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

    sniff(filter=filtre, prn=process_packet, iface=iface, store=False)

