import socket
import threading
from random import randint
import pickle
from vclock import vclock

'''
lastOpDict = {key:(sTime, sid),}
'''

class client(threading.Thread):

    def __init__(self, cid, cport, sport):
        threading.Thread.__init__(self)
        self.cid = cid
        self.cport = cport
        self.sport = sport
        self.vclock = vclock(10, self.cid)

        self.lastOpDict = {}
        self.host = socket.gethostname()
        self.addr = (self.host, self.cport)

        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.addr)
        self.s.connect((self.host, self.sport))
        self.counter = 0
        #getAnswer store the value get from the server
        self.getAnswer = 0

    def get(self, key):
        '''
        valueTuple = (vclock, value, sTime, sid)
        '''
        if not key in self.lastOpDict:
            self.lastOpDict[key] = (0, 0)
        self.s.send(pickle.dumps(("get", key, self.vclock, self.lastOpDict[key])))
        msg = self.s.recv(4096)
        #print(self.addr, "receive ", msg)
        valueTuple = pickle.loads(msg)
        self.vclock.merge(valueTuple[0])
        if valueTuple[1] == "ERR_DEP" or valueTuple[1] == "ERR_KEY":
            return valueTuple[1]
        else:
            self.lastOpDict[key] = (valueTuple[2], valueTuple[3])
            return valueTuple[1]


    def put(self, key, value):
        '''
        timeTuple = (vclock, sTime, sid)
        '''
        self.vclock.increment()
        insertTuple = ("put", key, value, self.vclock)
        self.s.sendall(pickle.dumps(insertTuple))
        msg = self.s.recv(1024)
        #print(self.addr, "receive ", msg)
        timeTuple = pickle.loads(msg)
        self.vclock.merge(timeTuple[0])
        self.lastOpDict[key] = (timeTuple[1], timeTuple[2])



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
            self.getAnswer = self.get(arg0)
        elif status == "break":
            self.close()
        elif status == "connect":
            self.connect(arg0)



    def printError(self):
        print(self.cid)

