import socket
import threading
from random import randint
import pickle


##fffff
#ffefefe
# create a socket object
#######
class client(threading.Thread):

    def __init__(self, cid, cport, sport):
        self.cid = cid
        self.cport = cport
        self.sport = sport
        threading.Thread.__init__(self)

    def put(self, key, value):

        insert1 = {key: value}
        self.s.send(pickle.dumps(insert1))


    def run(self):
        self.s = socket.socket()

        # get local machine name
        host = socket.gethostname()
        # print(tid)
        # print(host)

        self.s.bind((host, self.cport))

        # connection to hostname on the port.
        self.s.connect((host, self.sport))
        for i in range(2):
            self.put(self.cid,1)
        self.s.close()




