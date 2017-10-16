from pysnmp.hlapi import *

obj = {'casnUserId':ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnUserId')),
       'casnIpAddr':ObjectType(ObjectIdentity('CISCO-AAA-SESSION-MIB', 'casnIpAddr'))}


#Can replace it with class' object with more meaningful structure
braslist = [ UdpTransportTarget(('where_was_ip', 161)),
             UdpTransportTarget(('10.1.1.2'   , 161)),
             UdpTransportTarget(('10.1.1.3'   , 161)),
             UdpTransportTarget(('10.1.1.4'   , 161)),
             UdpTransportTarget(('10.1.1.5'   , 161)),
             UdpTransportTarget(('10.1.1.6'   , 161)),
             UdpTransportTarget(('10.1.1.7'   , 161)),
             UdpTransportTarget(('10.1.1.8'   , 161))
           ]
brasiplist = [ 'where_was_ip',
               '10.1.1.2',
               '10.1.1.3',
               '10.1.1.4',
               '10.1.1.5',
               '10.1.1.6',
               '10.1.1.7',
               '10.1.1.8'
             ]

brasiptonum = {'where_was_ip' :0,
               '10.1.1.2'    :1,
               '10.1.1.3'    :2,
               '10.1.1.4'    :3,
               '10.1.1.5'    :4,
               '10.1.1.6'    :5,
               '10.1.1.7'    :6,
               '10.1.1.8'    :7
              }

vpn_subnets = {'vpn':
                     ['10.6.0.0/20' , 
                      '10.6.16.0/20',
                      '10.6.32.0/20',
                      '10.6.48.0/20',
                      '10.6.64.0/20',
                      '10.6.80.0/20',
                      '10.6.96.0/20',
                      '10.6.112.0/20'],
               'blocked':
                     ['10.6.128.0/20',
                      '10.6.144.0/20',
                      '10.6.160.0/20',
                      '10.6.176.0/20',
                      '10.6.192.0/20',
                      '10.6.208.0/20',
                      '10.6.224.0/20',
                      '10.6.240.0/20']
              }