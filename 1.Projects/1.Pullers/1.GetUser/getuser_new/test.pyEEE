from netconnect.nettypes import *
from netconnect.connection.ciscolike import Ciscolike
from netconnect.connection.base import Connection
from timeit import default_timer as now
from passextr import password
from time import sleep
from threading import Thread
import logging
import netconnect.logaux as logaux

def cgte(ip, l):
        
        l.append()
        con.disconnect()
        

if __name__ == '__main__':
    start= now()
    #logging.basicConfig(format='[%(asctime)s] %(levelname)s LEVEL: %(message)s', datefmt='%d.%m.%Y %H:%M:%S', level=logging.WARNING)
    #logging.debug(f'{logaux.generic} {logaux.started}: module test.py')
    con = Ciscolike('where_was_ip', 'xtipacko', password)
    duration = now() - start
    print(f'connected in            {duration:.3f}s')
    mac_tbl = con.send_command('show ip route')

    duration = now() - start
    print(f'table retrieved in      {duration:.3f}s')

    print(mac_tbl)




    



    #eltxlst = [ 'where_was_ip',
    #            'where_was_ip',
    #            'where_was_ip',
    #            'where_was_ip',
    #            'where_was_ip',
    #            'where_was_ip',
    #            'where_was_ip',
    #            'where_was_ip',
    #            'where_was_ip'   ]
#
#    #for eltx in eltxlst:
#    #    con = Eltex_LTP(eltx, 'xtipacko', password)
#    #    ver = con.send_command('reconfigure interface ont 0-3')
#    #    sleep(2)
#    #    con.disconnect()
#    #    with open('eltextest.txt','a') as f:
    #        print(f'{eltx} DONE', file=f)
    #print('\n\n\n\noutput', '\n', ver)
    #print('PROMPT: ', con.prompt)
    #print('PROMPTSIGN: ', con.promptsign)
    #print('MODE: ', con.mode)
#
#    #ver = con.send_command('show mac interface gpon-port 0-3')
#    #
#    #print('\n\n\n\noutput', '\n', ver)
#
#
#    #print('PROMPT: ', con.prompt)
#    #print('PROMPTSIGN: ', con.promptsign)
    #print('MODE: ', con.mode)

    


     #print(con.banner)
 