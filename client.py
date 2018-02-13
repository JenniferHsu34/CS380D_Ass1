import socket
import threading
from random import randint
import pickle


class client(threading.Thread):

    def __init__(self, cid, cport, sport):
        threading.Thread.__init__(self)

        self.cid = cid
        self.cport = cport
        self.sport = sport

        self.host = socket.gethostname()
        self.addr = (self.host, self.cport)

        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.addr)
        self.s.connect((self.host, self.sport))
        self.counter = 0

    def get(self, key):
        self.s.send(pickle.dumps(key))
        msg = self.s.recv(4096)
        value = pickle.loads(msg)
        return value

    def put(self, key, value):
        insert1 = {key:value}
        self.s.sendall(pickle.dumps(insert1))
        #-----------------debug------------
        # self.counter = self.counter +1
        # self.s.send(pickle.dumps(str(self.counter)))


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

