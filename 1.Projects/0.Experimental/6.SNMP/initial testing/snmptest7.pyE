from pysnmp.hlapi import *
import timeit

startini = timeit.default_timer()
snmp_engine = SnmpEngine()
usm_auth_data = UsmUserData('there_was_snmpv3username', 'there_was_snmpv3pa')
context = ContextData()

obj = {'casnUserId':ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnUserId')),
       'casnIpAddr':ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnIpAddr'))}

brases = [ UdpTransportTarget(('where_was_ip', 161)),
           UdpTransportTarget(('10.1.1.2', 161)),
           UdpTransportTarget(('10.1.1.3', 161)),
           UdpTransportTarget(('10.1.1.4', 161)),
           UdpTransportTarget(('10.1.1.5', 161)),
           UdpTransportTarget(('10.1.1.6', 161))]
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
stopini = timeit.default_timer()

def finduser(username, braslist):
    #start = timeit.default_timer()
    userfound = False
    userip = ''
    brasnumber = None
    for bras in braslist:        
        bulkquery = bulkCmd( snmp_engine,
                             usm_auth_data,
                             bras,
                             context,
                             0, 22,
                             obj['casnUserId'],
                             obj['casnIpAddr'],
                             lexicographicMode=False)
        for row in bulkquery:
            if row[3][0][1].prettyPrint() == username:
                userip = row[3][1][1].prettyPrint()
                brasnumber = braslist.index(bras)
                userfound = True
                return userfound, userip, brasnumber # for found
    #stop = timeit.default_timer()
    #print('Search process took: ',round(stop-start, 3), 's' )
    return userfound, userip, brasnumber # for not found


    
        

    #print('n')
    #print(('{:<25}'*2).format('casnUserId', 'casnIpAddr'))
    #for row in fulltable:
    #    print (('{:<25}'*2).format(  row[3][0][1].prettyPrint(),
    #                                 row[3][1][1].prettyPrint()  ))
    
    #print('Users in total: ', len(fulltable))
username = '90192'
userfound, userip, brasnumber = finduser(username,brases)
if userfound:
    print('User found on Bras %d\nUser IP is %s' %(brasnumber+1,userip))
else:
    print('User %s not found' %username)
