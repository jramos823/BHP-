import scapy.all as scapy 
import argparse 

#Goal is to discover clients IPs and Macs on the same network. Developed for educational purposes.  

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest = 'targetIP', help = 'Please enter an IP or a range. (192.168.60.1/24  <---- mask optional)')
    options = parser.parse_args() # returns values from command line 
    if not options.targetIP:
        parser.error('[*]Please enter a Target IP or an Target Network. ')
    return options.targetIP


def scan(ip):
    arp_request = scapy.ARP(pdst = ip) #creating arp packet
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff") #Creating Frame setting dst address 
    arp_broadcast = broadcast/arp_request #Appending Frame and Arp together (scapy functionall)
    answerList = scapy.srp(arp_broadcast, timeout = 1, verbose = False)[0] #Allows us to send packets returns two items in a list [0] to only extract responses that had answers 
    
    listfor_IpMac = [] 
    for element in answerList: 
        answerdict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
        listfor_IpMac.append(answerdict)    
    return listfor_IpMac 
    

def print_results(results):    
    border = "-" * 50
    print("\nIP\t\t\tMAC ADDRESS\n" + border )
    for info in results:
        print(info['ip'] + "\t\t" + info['mac'])


if __name__ == "__main__":
    
    userinput = get_args()
    scanresults = scan(userinput)
    print_results(scanresults)
