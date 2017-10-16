#gu stands for Get User's session from BRAS
from pysnmp.hlapi import *
from customsnmpdata import *
from queue import Queue
import threading
import timeit

mainstart = timeit.default_timer()

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
            userip = row[3][1][1].prettyPrint()  
            result.append((userip, brasnumber) )#ADD LOCK!
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
    mainstop = timeit.default_timer()
    print('%3fs' %(mainstop - mainstart))
    input()
