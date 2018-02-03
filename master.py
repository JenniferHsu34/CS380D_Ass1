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
    clients.append(c)


def printStore(sid):
    servers[sid].printStore()

def put(cid, key, value):
    clients[cid].run("put", key, value)
    if clients[cid].is_alive():
        clients[cid].join()
    return 0

def breakConnection(id1, id2):
    clients[id1].run("break")
    if clients[id1].is_alive():
        clients[id1].join()
    return 0

def createConnection(id1, id2):
    clients[id1].run("connect", serverPort - id2)
    if clients[id1].is_alive():
        clients[id1].join()
    return 0

joinServer(0)
joinServer(1)
joinClient(0,0)


time.sleep(0.1)
put(0,1,1)
put(0,2,4)
put(0,3,3)
breakConnection(0,0)
createConnection(0,1)
put(0,3,3)
time.sleep(0.1)
print(id(servers[0].dicts[0]))
print(id(servers[1].dicts[1]))
printStore(0)
printStore(1)
