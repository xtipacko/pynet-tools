from  telnetlib import Telnet
from time import sleep
from pprint import pprint, PrettyPrinter
import re
import timeit

def regex_mac_extr(mac_table):
    eltex_mac_ptrn = re.compile('\s+\S+\s+(?P<serial>ELTX\S{8})\s+(?P<ontid>\S+)\s+(?P<gponport>\S+)\s+\S+\s+\S*\s+\S*\s+(?P<vlan>\S+)\s+(?P<mac>\S*)')
    mac_table_dict = {}
    for line in mac_table:
        match = eltex_mac_ptrn.match(line)
        if match:
            mac_table_dict[match.group('mac')] = match.groupdict()
    return mac_table_dict


def getmaceltex(ip,port=23):

    conn = Telnet(ip,port)
    printer = PrettyPrinter(width=500)
    sleep(1)
    try:
        #conn.read_very_eager().decode('utf-8','ignore')
        conn.write('xtipacko\r\n'.encode('ascii', 'ignore'))
        sleep(.5)
        #conn.read_very_eager().decode('utf-8','ignore')
        conn.write('there_was_password\r\n'.encode('ascii', 'ignore'))
        sleep(6)
        res = conn.read_very_eager().decode('utf-8','ignore')
        prompt = res.splitlines()[-1]
        #print('PROMPT IS: %s' %repr(prompt))
        conn.write('show mac interface gpon-port 0-3\r\n'.encode('ascii', 'ignore'))
        mac_table = []
        i=30
        while i > 0:
            sleep(1)
            i-=1
            read_page = conn.read_very_eager().decode('utf-8', 'ignore')
            mac_table.extend(read_page.splitlines())
            lastln_on_page = len(mac_table) -1 # index of last line on a new page = length of mac_table - 1
            #print(i, lastln_on_page, repr(mac_table[lastln_on_page]))
            if mac_table[lastln_on_page] == prompt:
                del mac_table[lastln_on_page]
                break
            conn.write(' '.encode('ascii', 'ignore'))
        start = timeit.default_timer()
        mac_table_dict = regex_mac_extr(mac_table)
        stop = timeit.default_timer()
        printer.pprint(mac_table_dict)
        print('Total: ', len(mac_table_dict))
        print('Parsing took: %.3f sec.' %(stop-start))
    finally:
        conn.close()
        print('CLOSED')

getmaceltex('where_was_ip', 23)
