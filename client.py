import socket
import threading
from random import randint
import pickle

'''
lastOpDict = {key:[cid, cTime, sTime, sid],}
'''

class client(threading.Thread):

    def __init__(self, cid, cport, sport):
        threading.Thread.__init__(self)

        self.cid = cid
        self.cport = cport
        self.sport = sport
        self.cTime = 0
        self.lastOpDict = {}
        self.host = socket.gethostname()
        self.addr = (self.host, self.cport)

        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.addr)
        self.s.connect((self.host, self.sport))
        self.counter = 0

    def get(self, key):
        if not self.lastOpDict.has_key(key):
            self.lastOpDict[key] = [self.cid, 0, 0, 0]
        self.s.send(pickle.dumps(("get", key, self.lastOpDict[key])))
        msg = self.s.recv(4096)
        value = pickle.loads(msg)
        if value == "ERR_DEP" or value == "ERR_KEY":
            return value
        else:
            self.lastOpDict[key][2:4] = value[1:3]
            return value[0]


    def put(self, key, value):
        self.cTime += 1
        if not self.lastOpDict.has_key(key):
            self.lastOpDict[key] = [self.cid, self.cTime, 0, 0]
        else:
            self.lastOpDict[key][1] = self.cTime
        insertTuple = ("put", key, value, self.cid, self.cTime)
        self.s.sendall(pickle.dumps(insertTuple))


    def connect(self, sport):
        self.sport = sport
        self.s.close()
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.addr)
        self.s.connect((self.host, self.sport))

    def close(self):
        self.s.close()

    def run(self, status, arg0=None, arg1=None):
        if status == "put":
            self.put(arg0, arg1)
        elif status == "get":
            print(self.get(arg0))
        elif status == "break":
            self.close()
        elif status == "connect":
            self.connect(arg0)



    def printError(self):
        print(self.cid)

