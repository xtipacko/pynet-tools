from passextr import password
import urllib.request as urllib2
import pymysql
import json
import codecs
import sys
import timeit
import logging


db_table = 'macvendors'

class MacAddress:
	#this is a Kludge
    def __init__(self, mac_address):
        self.commonformat = mac_address.replace(':','').replace('.','').replace('-','').lower()


def local_lookup(mac_address):
    global db_table
    try:
        connection = pymysql.connect(host='localhost', 
                                     user='root',
                                     password=password,
                                     charset='utf8mb4',
                                     database='pptpclients',
                                     cursorclass=pymysql.cursors.DictCursor)
        mac_oui = MacAddress(mac_address).commonformat[:6]
        with connection.cursor() as cursor:
            query = (f'SELECT mac,company FROM {db_table}\n'
                     f'WHERE mac="{mac_oui}";')
            cursor.execute(query)
            macdata = cursor.fetchall()
            if macdata:
                return macdata[0]['company']
            else:
                return None
    except:
        logging.debug('Module: ml.py, local_lookup: unknown problem during db access')
        print('db exception')
        return None
        #raise Exception('unknown problem during db access')
    finally:
        connection.close()

def write_mac_db(mac_address, vendor):
    global db_table
    try:
        connection = pymysql.connect(host='localhost', 
                                     user='root',
                                     password=password,
                                     charset='utf8mb4',
                                     database='pptpclients',
                                     cursorclass=pymysql.cursors.DictCursor)
        mac_oui = mac_address.commonformat[:6] # OUI is of only interest 
        
        company = vendor[:256] #restrict to fit in db

        with connection.cursor() as cursor:

            query = (f'REPLACE INTO `{db_table}` (mac,company) VALUES\n'
                     f'("{mac_oui}","{company}");')
            cursor.execute(query)
            connection.commit()
    except:
        logging.debug('Module: ml.py, local_lookup: unknown problem during db access')
        return None
        #raise Exception('unknown problem during db access')
    finally:
        connection.close()
    

def online_lookup(mac_address):
    try:
        request = urllib2.Request('http://macvendors.co/api/%s' %mac_address, headers={'User-Agent' : "API Browser"}) 
        response = urllib2.urlopen(request)
        #Fix: json object must be str, not 'bytes'
        reader = codecs.getreader("utf-8")
        obj = json.load(reader(response))
        return obj['result']['company']
    except:
        logging.debug('Module: ml.py, online_lookup: access to http://macvendors.co/api/ UNSUCCESSFUL')
        return None

def mac_lookup(mac_address):
    vendor_in_db = local_lookup(mac_address)
    if vendor_in_db:        
        return vendor_in_db
    #else
    vendor_online = online_lookup(mac_address)
    if vendor_online:
        write_mac_db(mac_address, vendor_online)
        return vendor_online
    else:
        return 'Unknown vendor'


if __name__ == '__main__':   
    start = timeit.default_timer()
    mac_addr = sys.argv[1]
    print('\n',mac_lookup(mac_addr))
    print('\n[%.3fs]' %(timeit.default_timer()-start))