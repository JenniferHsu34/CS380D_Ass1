import socket
import threading
from client import client
from server import server
from random import randint
import time
from ctypes import c_int, addressof
import pickle
import sys
import os
serverPort = randint(2000,26000)

servers = [-1]*5
clients = [-1]*10
clientPort = randint(30000, 40000)
masterPort = randint(26002, 29999)
connectedSids = [[],[],[],[],[]]
clientConnected = [-1]*10

'''
server id in [0, 1, 2, 3, 4],
client id in [5, 6, 7, 8, 9]
'''


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
    s = server(sid, sport(sid))
    for oldServer in servers:
        if oldServer != -1:
            oldSid = oldServer.sid
            connectedSids[oldSid].append(sid)
            connectedSids[sid].append(oldSid)
    s.start()
    servers[sid] = s
    time.sleep(0.05)


def killServer (sid):

    for i in connectedSids[sid]:
        connectedSids[i].remove(sid)
    connectedSids[sid].clear()
    servers[sid].exit()
    servers[sid] = -1
    for i in range(5):
        if clientConnected[i] == sid:
            clientConnected[i] = -1


def joinClient (cid, sid):
    c = client(cid, clientPort - cid, sport(sid))
    clientConnected[cid] = sid
    clients[cid] = c


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
    return clients[cid].getAnswer


def breakConnection(id1, id2):
    # id2 should be server id
    if id2 >= 5:
        id1, id2 = id2, id1
    if id1 <= 4:
        breakServers(id1, id2)
    else:
        breakClientServer(id1, id2)

def breakClientServer(cid, sid):
    if sid == clientConnected[cid]:
        clientConnected[cid] = -1
        clients[cid].run("break")
        if clients[cid].is_alive():
            clients[cid].join()

def breakServers(id1, id2):
    try:
        connectedSids[id1].remove(id2)
        connectedSids[id2].remove(id1)
    except OSError:
        pass

def createConnection(id1, id2):
    # id2 should be server id
    if id2 >= 5:
        id1, id2 = id2, id1
    if id1 <= 4:
        connectServers(id1, id2)
    else:
        connectClientServer(id1, id2)

def connectClientServer(cid, sid):
    if clientConnected[cid] == sid:
        print("client " + str(cid) + " already connected server " + str(sid))
        return 0
    clientConnected[cid] = sid
    clients[cid].run("connect", sport(sid))
    if clients[cid].is_alive():
        clients[cid].join()
    return 0

def connectServers (id1,id2):
    connectedSids[id1].append(id2)
    connectedSids[id2].append(id1)

def stabilize():
    nodes = []
    vis = {} # visited_list
    connectedComponents = [] #
    for server in servers:
        if server != -1:
            node = server.sid
            nodes.append(node)
            vis[node] = False
    for a in nodes:
        tempComponent = []
        if vis[a] == False:
            dfs(a,vis,tempComponent)
        if len(tempComponent) > 0:
            connectedComponents.append(tempComponent)

    for component in connectedComponents:
        centerId = min(component)
        component.remove(centerId)
        sendToServer(centerId, ("stabilizeCenter", component))
        for sendId in component:
            sendToServer(sendId, ("stabilizeSender", centerId))


# basic depth first search
def dfs(node,vis,tempComponent):
     vis[node] = True
     tempComponent.append(node)
     for neighbour in connectedSids[node]:
         if vis[neighbour] == False:
             dfs(neighbour, vis, tempComponent)


def process(line):
    print (line)
    command = line.split(' ')
    API = command[0]
    if API ==  'joinServer':
        joinServer(int(command[1]))
    elif API == 'killServer':
        killServer(int(command[1]))
    elif API == 'joinClient':
        print (int(command[1]), ' ',  int(command[2]))
        joinClient(int(command[1]), int(command[2]))
    elif API == 'breakConnection':
        breakconnection(int(command[1]), int(command[2]))
    elif API == 'createConnection':
        breakconnection(int(command[1]), int(command[2]))
    elif API == 'stabilize':
        stabilize()
    elif API == 'printStore':
        printStore(int(command[1]))
    elif API == 'put':
        put(int(command[1]), command[2], command[3])
    elif API == 'get':
        get(int(command[1]), command[2])
    else:
        print ('Invalid command')

if __name__ == "__main__":
    filename = sys.argv[1] #'command.txt'
    with open(filename, 'rb') as f:
        while True:
            line = f.readline()
            if not line: break
            process(line)
    os._exit(1)