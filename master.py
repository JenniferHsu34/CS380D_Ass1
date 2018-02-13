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
masterPort = randint(26002,29999)
print(serverPort,clientPort)

def joinServer (sid):
    s=server(sid, sport(sid))
    s.start()
    servers.append(s)

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

def get(cid, key):
    print (clients[cid].run("get", key))
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
def connectServers (id1,id2):
    sendToServer(id1,[id1,sport(id1)])
    sendToServer(id2, [id2, sport(id2)])

def sport(sid):
    return serverPort - sid*20

def sendToServer (sid,text):
    host = socket.gethostname()
    s = socket.socket()
    s.bind((host, masterPort))
    s.connect((host, sport(sid)))
    s.send(text)
    s.close()
    masterPort = masterPort - 1
def stabilize():



    for server in servers:
        sendToServer(server.sid,b'fffff')


joinServer(0)
joinServer(1)
for i in range(5):
    joinClient(i,0)
#joinClient(1,0)

connectServers(0,1)

'''
for i in range(1000):
    for j in range(1):
        put(j,str(i),str(i))
'''