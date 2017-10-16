#import urllib.request as urllib2
#import json
#import codecs
#import sys
#import timeit
#
#def mac_lookup(mac_address):
#    try:
#        request = urllib2.Request('http://macvendors.co/api/%s' %mac_address, headers={'User-Agent' : "API Browser"}) 
#        response = urllib2.urlopen(request)
#        #Fix: json object must be str, not 'bytes'
#        reader = codecs.getreader("utf-8")
#        obj = json.load(reader(response))
#        return (True, obj['result']['company'])
#    except:
#        return (False, 'Error with access to http://macvendors.co/api/')
#
#if __name__ == '__main__':
#    start = timeit.default_timer()
#    mac_addr = sys.argv[1]
#    print('\n',mac_lookup(mac_addr)[1])
#    print('\n[%.3fs]' %(timeit.default_timer()-start))

from subprocess import check_output
import sys
if __name__ == '__main__':
    directory = 'C:\\Users\\evgeni\\Desktop\\getuser'
    mac = sys.argv[1]
    output = check_output(['ml.py', mac], cwd=directory, shell=True)
    print(output.replace(b'\r',b'').decode('utf-8', 'ignore'))
