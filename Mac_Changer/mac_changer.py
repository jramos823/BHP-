import os
import subprocess
import optparse
import re 

def get_arguments():
    testmac = len("00:11:22:33:44:55")
    parser = optparse.OptionParser() #Creates object to add options to be executed at CLI
    parser.add_option('-i', '--interface', dest = 'interface', type='string', help = 'Interface to change the MAC address.')
    parser.add_option('-m', '--mac', dest = 'newmac', help = 'Specify MAC address. EX: 00:11:22:33:44:55')
    (options, arguments) = parser.parse_args() #Returning values in parse_args()
    if not options.interface:
         #code to handle errors
         parser.error("[?]Please specify a interface. E.g -i 'eth0'. ")
    if not options.newmac:
         parser.error("[?]Please specify a mac address. ")
         #code to handle errors
    if len(options.newmac) != testmac:
         parser.error("[?] Please enter a mac address in this format --> (00:11:22:33:44:55)")
    return options, arguments 


def mac_changer(interface, newmac):
    #Takes cariables from user input and excutes command to change Mac Address
    subprocess.call(['ifconfig', interface, 'down'])
    print('[*] Shutting down',interface, 'interface.')
    subprocess.call(['ifconfig', interface, 'hw', 'ether',newmac])
    print('[*] Attempting to change Mac Address to', newmac)
    subprocess.call(['ifconfig', interface, 'up'])


def get_current_mac(interface):
    ifconf_out = subprocess.check_output(['ifconfig', interface])
    newifconf_out = ifconf_out.decode('utf8')
    ifconfig_filter = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", newifconf_out)
    if ifconfig_filter:
        return ifconfig_filter.group(0) #If variable is filled return it 
    else:
        print("[*] Could not find Mac Address on specified interface.")  
    #This is necessary becuaes we canot give errors for invalid interfaces.
    #Interfaces can be up to 16 characters. 

if __name__ == "__main__":

    options, arguments = get_arguments()

    currentMac = get_current_mac(options.interface)
    print("\n[*] Current mac is:",currentMac) 

    mac_changer(options.interface, options.newmac)

    currentMac = get_current_mac(options.interface)
    if currentMac == options.newmac:
        print("[*] Mac Address was sucessfully changed to "  + currentMac)
    else:
        print("[*] Mac Address did not get changed. ")
