import socket
import threading
from client import client
from server import server
from random import randint
import time
from ctypes import c_int, addressof

serverPort = randint(2000,26000)

servers = []
clients = []

clientPort = randint(30000, 40000)
print(serverPort,clientPort)
def joinServer (sid):
    s=server(sid, serverPort - sid)
    servers.append(s)
    s.start()

    #new_thread = threading.Thread(target=s.run, args=(sid, serverPort - sid))
    #new_thread.start()  # run the thread

def killServer (sid):
   for t in threading.enumerate():
       if t.get_ident()== sid:
           t.exit()
   return 0


def joinClient (cid, sid):
    c=client(cid, clientPort - cid, serverPort-sid)
    clients.append(c)
    c.start()



def printStore(sid):
    servers[sid].printStore()

def put(cid, key, value):
    return 0

def breakConnection(id1, id2):
    return 0

def createConnection(id1, id2):
    clients[id1].wait()
    clients[id1].printError()
    clients[id1].cond.notify()
    id2 =2
    return 0

joinServer(0)
joinServer(1)
#joinClient(0,0)
joinClient(2,1)
joinClient(3,1)
#joinClient(4,0)
#joinClient(5,0)
#joinClient(6,0)
#clients[2].connect(1)
#%createConnection(0,0)

time.sleep(1)
printStore(0)
printStore(1)
