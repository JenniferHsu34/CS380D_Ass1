import socket
import threading
from client import client
from server import server
from random import randint
import time
from ctypes import c_int, addressof

serverPort = randint(2000,26000)

servers = []

clientPort = randint(30000, 40000)
print(serverPort,clientPort)
def joinServer (sid):
    s=server(sid, serverPort - sid)
    s.start()
    servers.append(s)
    #new_thread = threading.Thread(target=s.run, args=(sid, serverPort - sid))
    #new_thread.start()  # run the thread

def killServer (sid):
   for t in threading.enumerate():
       if t.get_ident()== sid:
           t.exit()
   return 0


def joinClient (cid, sid):
    c=client(cid, clientPort - cid, serverPort-sid)
    c.start()


def printStore(sid):
    servers[sid].printStore()

def put(cid, key, value):
    return 0

def breakConnection(id1, id2):
    return 0

def createConnection(id1, id2):
    return 0

joinServer(0)
joinServer(1)
#joinClient(0,0)
joinClient(1,1)


time.sleep(1)
print(id(servers[0].dicts[0]))
print(id(servers[1].dicts[1]))
printStore(0)
printStore(1)
