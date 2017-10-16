import urllib.request as urllib2
import json
import codecs
import sys

def mac_lookup(mac_address):
    try:
        request = urllib2.Request('http://macvendors.co/api/%s' %mac_address, headers={'User-Agent' : "API Browser"}) 
        response = urllib2.urlopen(request)
        #Fix: json object must be str, not 'bytes'
        reader = codecs.getreader("utf-8")
        obj = json.load(reader(response))
        return obj['result']['company']
    except:
        return 'Error with access to http://macvendors.co/api/'

if __name__ = '__main__':
    mac_addr = sys.argv[1]
    print(mac_lookup(mac_addr))