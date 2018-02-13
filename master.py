import socket
import threading
from client import client
from server import server
from random import randint
import time
from ctypes import c_int, addressof
import pickle

serverPort = randint(2000,26000)

servers = []
clients = []
clientPort = randint(30000, 40000)
masterPort = randint(26002,29999)

print(serverPort,clientPort)


def sport(sid):
    return serverPort - sid*20

def sendToServer (sid,text):
    host = socket.gethostname()
    s = socket.socket()
    global masterPort
    masterPort = masterPort - 1
    s.bind((host, masterPort))
    s.connect((host, sport(sid)))
    s.send(pickle.dumps(text))
    s.close()

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
    c=client(cid, clientPort - cid, sport(sid))
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
    sendToServer(id1,("server",id1,sport(id1)))
    #sendToServer(id2,("server",id2, sport(id2)))

def stabilize():

    for server in servers:
        sendToServer(server.sid,"stabilize")


joinServer(0)
joinServer(1)


joinClient(0,0)
joinClient(1,1)


#joinClient(1,0)




connectServers(0,1)

stabilize()
'''
for i in range(1000):
    for j in range(1):
        put(j,str(i),str(i))
'''