import socket
import threading
from random import randint
import pickle


##fffff
#ffefefe
# create a socket object
#######
# changeServer (sport) : change socket's connect
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
        print(cid, "client  ", self.sport)
        self.s.connect((self.host, self.sport))


    def put(self, key, value):
        insert1 = {key: value}
        self.s.send(pickle.dumps(insert1))

    def connect(self, sport):
        self.sport = sport

        self.s.close()

        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.addr)
        self.s.connect((self.host, self.sport))

    def close(self):
        self.s.close()

    def run(self):

        for i in range(1):
            self.put(self.cid,1)
        self.s.close()

    def printError(self):
        print (self.cid)


