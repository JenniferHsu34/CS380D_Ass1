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
    clients[cid].run("get", key)
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
    sendToServer(id1,("server",id2,sport(id2)))
    #sendToServer(id2,("server",id2, sport(id2)))

def stabilize():

    for server in servers:
        sendToServer(server.sid,"stabilize")





# TESTING

joinServer(0)
joinServer(1)
time.sleep(1)
joinClient(0, 0)
joinClient(1, 1)
print 'here?################'
connectServers(0,1)
print 'here??#########'
get(0, "z")
put(0, "x", 0)
#get(0, "x")

put(1, "x", 1)
put(0,"x", 2)
put(0,"y", 3)
time.sleep(1)
print '-----before stablize'
print '[s0]', servers[0].vclock.vclock, servers[0].writeLog
print '[s1]', servers[1].vclock.vclock, servers[1].writeLog
print 'get x from s0: (exp 2) '
get(0, "x") # should get 2
print 'get x from s1: (exp 1)'
get(1, "x") # should get 1
stabilize()
time.sleep(1)
print '-----after stablize'
print '[s0]', servers[0].vclock.vclock, servers[0].writeLog #vclock -> 3, 1, 0, 0
print '[s1]', servers[1].vclock.vclock, servers[1].writeLog #vclock -> 3, 1, 0, 0
print 'get x from s1: (exp 2 since it did anti entropy) '
get(1, "x") # should get 1