import urllib.request

import urllib.parse

url = 'http://where_was_ip:81/dude/main.html'

values = { 'process':'login',
           'page':'start',
           'user':'xtipacko',
           'password':'svwk74jjfnRw2H' }
data = urllib.parse.urlencode(values)
data = data.encode('utf-8')
req = urllib.request.Request(url,data)
resp = urllib.request.urlopen(req)


headers = dict(resp.info())
Cookie = headers['Set-Cookie']

url = 'http://where_was_ip:81/dude/backupbackup-2017.01.23.tgz'

headers = { 'Cookie':Cookie  }
values = { 'page':'savefile',
           'download':'yes' }
data = urllib.parse.urlencode(values)
data = data.encode('utf-8')
req = urllib.request.Request(url, data, headers=headers)
resp = urllib.request.urlopen(req)

fl = resp.read()

with open('backupbackup-2017.01.23.tgz', 'wb+') as f:
    f.write(fl)
    f.close()




