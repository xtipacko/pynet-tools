from socket import *
from time import sleep
import asyncio

loop = asyncio.get_event_loop()
async def client(address):
	sock = socket(AF_INET, SOCK_STREAM)
	#sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	#sock.bind(address)
	#sock.listen(5)
	sock.setblocking(False)
	while True:
		await loop.sock_connect(sock, address)
		print(f'Connection to {address}')
		data = await loop.sock_recv(sock, 10000)


#async def echo_handler(client):
#	with client:
#		while True:
#			
#			if not data:
#				break
#			await loop.sock_sendall(client, b'Got:'+data)
#	print('Connection closed')

loop.create_task(client(('where_was_ip',23)) )

loop.run_forever()