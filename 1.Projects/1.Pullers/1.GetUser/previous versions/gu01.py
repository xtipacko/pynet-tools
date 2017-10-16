#gu stands for Get User's session from BRAS
import timeit
mainstart = timeit.default_timer()
from pysnmp.hlapi import *
from customsnmpdata import *
from ipaddress import *
#from queue import Queue
import threading
import sys

def check_on_bras(username, bras):
    brasnumber = braslist.index(bras) 
    bulkquery = bulkCmd( SnmpEngine(),
                         usm_user_data,
                         bras,
                         context,
                         0, 22,
                         obj['casnUserId'],
                         obj['casnIpAddr'],
                         lexicographicMode=False)
    for row in bulkquery:
        if result: # for one result optimisation
            break
        gotusername = row[3][0][1].prettyPrint()        
        if  gotusername == username:
            tunnelremoteip = row[3][1][1].prettyPrint()  
            result.append((tunnelremoteip, brasnumber) )#ADD LOCK!
            break

def finduser(username):
    threads = []
    for bras in braslist:
        t = threading.Thread(target=check_on_bras, args=(username, bras))
        t.daemon = True
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

def printinfo(result, username):
    for bras_excerpt in result:
        tunnelremoteip, brasnumber = bras_excerpt
        brasnumber+=1
        subnet_purpose = 'Unknown Subnet' # 
        for subnet in vpn_subnets['vpn']:
            if IPv4Address(tunnelremoteip) in IPv4Network(subnet):
                subnet_purpose = 'OK'
        for subnet in vpn_subnets['blocked']:
            if IPv4Address(tunnelremoteip) in IPv4Network(subnet):
                subnet_purpose = 'BLOCKED'
        print('{username} on Bras {brasnumber},\n'
              '  IP: {ip} (VPN {purpose})'.format(username   = username,
                                                  brasnumber = brasnumber,
                                                  ip         = tunnelremoteip,
                                                  purpose    = subnet_purpose)   )

if __name__ == '__main__':
    #entry point here
    print('Get User v0.1')
    if len(sys.argv) < 2:
        print('\n') 
        print('You forgot to specify username')
        exit()
    elif len(sys.argv) > 2:        
        print('\n') 
        print('Theese are extra arguments:', ', '.join(sys.argv[2:]))
    username = sys.argv[1]
    result = [] # [(tunnelremoteip, brasnumber),...]
    usm_user_data = UsmUserData('there_was_snmpv3username', 'there_was_snmpv3pa')
    context = ContextData()
    print('Checking vpn session for %s on BRASes: 1 - %d' %(username, len(braslist)))
    finduser(username)    
    if result:
        print('\n') 
        printinfo(result, username)
    else:    
        print('User %s not found' %username)
    
mainstop = timeit.default_timer()
input('\n\n[%.3fs]' %(mainstop - mainstart))
