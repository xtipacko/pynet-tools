from baseconnection import BaseConnection
from passextr import password
from pprint import pprint
from timeit import default_timer as now
import re
#Internet  10.10.231.237           0   2828.5dd4.9137  ARPA   Vlan256
#Protocol  Address          Age (min)  Hardware Addr   Type   Interface
def manualsplit(line):
    ipaddr = line[10:26].rstrip()
    age = line[32:35].lstrip()
    mac = line[38:54].rstrip()
    vlan = line[61:].rstrip()
    if vlan.startswith('Vlan'):
        return ipaddr, mac, vlan[4:], age
    else:
        return None



start = now()
c = BaseConnection('where_was_ip','xtipacko',password)
c.send_command('terminal length 0')
arptableraw = c.send_command('show ip arp')
print('%.3fs' %(now() - start))

start = now()
arptablelines = arptableraw.splitlines()
#rearp = re.compile(r'.+?\ +(?P<ip>.+?)\ +(?P<age>.+?)\ +(?P<mac>.+?)\ +.+?\ +Vlan(?P<vlan>.+)')
print('%.3fs' %(now() - start))

start = now()
arptable = []
for arpentry in arptablelines[1:]:
    #m = re.match(rearp, arpentry)
    #if m:
    #    arptable.append((m.group('ip'), m.group('mac'), m.group('vlan'), m.group('age')))
    entry = manualsplit(arpentry)
    #print(f'{entry!r}\n{arpentry}\n\n')

    if entry:
        arptable.append(entry)
print('%.3fs' %(now() - start))

arpdict = {}

for entry in arptable:
    if entry[0] not in arpdict:
        arpdict[entry[0]] = [(entry[1], entry[2], entry[3])]
    else:
        arpdict[entry[0]].append((entry[1], entry[2], entry[3]))

print(len(arptable), '\n\n')


for key in arpdict:
    if len(arpdict[key]) > 1:
        print(arpdict[key])
        break
else:
    print('notfound')

