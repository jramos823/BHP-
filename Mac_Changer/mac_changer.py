import os
import subprocess
import optparse

parser = optparse.OptionParser()

parser.add_option('-i', '--interface', dest = 'interface', help = 'Interface to change the MAC address.')
parser.add_option('-m', '--mac', dest = 'newmac', help = 'Specify MAC address. EX: 00:11:22:33:44:55')
(options, arguments) = parser.parse_args()

#subprocess.call('echo this is also a test', shell=True)

interface = options.interface
newmac = options.newmac

subprocess.call(['ifconfig', interface, 'down'])
print('[*] Shutting down',interface, 'interface.')
subprocess.call(['ifconfig', interface, 'hw', 'ether',newmac])
print('[*] Changing Mac Address to', newmac)
subprocess.call(['ifconfig', interface, 'up'])
print('Interface is now up.\nYour mac address has changed.')
subprocess.call('ifconfig ' + interface , shell=True)
