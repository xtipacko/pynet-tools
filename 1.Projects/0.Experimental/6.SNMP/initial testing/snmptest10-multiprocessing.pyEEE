from pysnmp.hlapi import *
import timeit
from queue import Queue
import threading


##########################junk for file
obj = {'casnUserId':ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnUserId')),
       'casnIpAddr':ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnIpAddr'))}

braslist = [ UdpTransportTarget(('where_was_ip', 161)),
             UdpTransportTarget(('10.1.1.2', 161)),
             UdpTransportTarget(('10.1.1.3', 161)),
             UdpTransportTarget(('10.1.1.4', 161)),
             UdpTransportTarget(('10.1.1.5', 161)),
             UdpTransportTarget(('10.1.1.6', 161))
          ]
vpn_subnets = {
               'VPN':
                     ['10.6.0.0/20' , 
                      '10.6.16.0/20',
                      '10.6.32.0/20',
                      '10.6.48.0/20',
                      '10.6.64.0/20',
                      '10.6.80.0/20'],
               'blocked':
                     ['10.6.128.0/20',
                      '10.6.144.0/20',
                      '10.6.160.0/20',
                      '10.6.176.0/20',
                      '10.6.192.0/20',
                      '10.6.208.0/20']}
##########################junk for file

def check_on_bras(username, bras):
    brasnumber = braslist.index(bras) 
    #print(round(timeit.default_timer(),2), 'Bras', brasnumber, 'snmp queried')
    bulkquery = bulkCmd( SnmpEngine(),
                         usm_user_data,
                         bras,
                         context,
                         0, 22,
                         obj['casnUserId'],
                         obj['casnIpAddr'],
                         lexicographicMode=False)
    #print(round(timeit.default_timer(),2), 'Bras', brasnumber, 'gen created')
    for row in bulkquery:
        if result: # for one result optimisation
            break
        gotusername = row[3][0][1].prettyPrint()        
        #print(round(timeit.default_timer(),2), 'User', gotusername)
        if  gotusername == username:
            userip = row[3][1][1].prettyPrint()  
            result.append((userip, brasnumber) )#ADD LOCK!
            #print(round(timeit.default_timer(),2), 'Bras', brasnumber, 'snmp finished Succesfully')
            break
    #print(round(timeit.default_timer(),2), 'Bras', brasnumber, 'snmp finished unsuccesfully')

def finduser(username):
    threads = []
    for bras in braslist:
        t = threading.Thread(target=check_on_bras, args=(username, bras))
        t.daemon = True
        #print(round(timeit.default_timer(),2), 'Bras', braslist.index(bras), 'started')
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
        #print(round(timeit.default_timer(),2), 'Bras', threads.index(t), 'joined')

if __name__ == '__main__':
    #entry point here
    username = 'krugerrr'
    result = [] # [(userip, brasnumber),...]
    usm_user_data = UsmUserData('there_was_snmpv3username', 'there_was_snmpv3pa')
    context = ContextData()
    finduser(username)    
    if result: 
        print('\n'.join([ 'User found on Bras %d\nUser IP is %s' %(brasnumber+1,userip)
                          for userip, brasnumber in result]))
    else:    
        print('User %s not found' %username)
    
