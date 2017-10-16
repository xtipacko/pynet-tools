import threading
from queue import Queue
import time
print_lock = threading.Lock() # we have to have lock per thing

def exampleJob(worker):
    i = 1
    while i < 1000000:
        i+=1 
    with print_lock:
    	print(threading.current_thread().name, worker)

def threader():
    while True: #continue to work until the main thread dies
        worker = q.get()
        exampleJob(worker)
        q.task_done() # The count of unfinished tasks  goes -1 to indicate that the item was retrieved and all work on it is complete.

q = Queue()

for x in range(10):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

start = time.time()

for worker in range(200):
    q.put(worker)

q.join() #Queue's method waits til the thread terminates

print('Entire job took:', time.time()-start)
