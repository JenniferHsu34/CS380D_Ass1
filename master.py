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
connectedSids = [[],[],[],[],[]]
#print(serverPort,clientPort)


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
   for server in servers:
       if server.sid== sid:
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
    clients[cid].run("get", key)
    if clients[cid].is_alive():
        clients[cid].join()
    return 0

def breakConnection(id1, id2):
    clients[id1].run("break")
    if clients[id1].is_alive():
        clients[id1].join()
    return 0


def breakServers(id1, id2):
    connectedSids[id1].remove(id2)
    connectedSids[id2].remove(id1)

def createConnection(id1, id2):
    clients[id1].run("connect", sport(id2))
    if clients[id1].is_alive():
        clients[id1].join()
    return 0
def connectServers (id1,id2):
    sendToServer(id1,("server",id2,sport(id2)))
    connectedSids[id1].append(id2)
    connectedSids[id2].append(id1)
    #sendToServer(id2,("server",id2, sport(id2)))

def stabilize():

    for server in servers:
        sendToServer(server.sid,("stabilize",connectedSids[server.sid]))




