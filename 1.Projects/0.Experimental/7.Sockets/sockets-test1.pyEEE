from socket import *
from time import sleep
def open_port(ip, port):
    s = socket(AF_INET, SOCK_STREAM)
    if not s.connect_ex((ip, port)): 
        print(f'{port} open')
    else:
        print(f'{port} closed')

for port in range(1,1025):
	open_port('where_was_ip', port)