import socket  # Import socket module
import threading
import pickle
from vclock import vclock
import io
import sys
import time
from random import randint

def recvAll(socket, length):
    data = b''
    while True:
        packet = socket.recv(length)
        data += packet
        if len(packet) < length:
            return data

sendPorts = [randint(2602,29999),randint(2602,29999)]
receivePorts  = [randint(2602,29999),randint(2602,29999)]


debugV = 0
def debug(s):
    global  debugV
    lsss = [str(debugV) for i in range(20)]
    print(str(s)  + str(lsss))
    debugV = debugV +1

class server(threading.Thread):

    def __init__(self, sid, port):
        self.sid = sid
        self.vclock = vclock(5, sid)
        self.writeLog = []
        self.history = {}
        self.clientM  = ""
        self.port = port
        self.host = socket.gethostname()
        self.lock = threading.Lock()
        self.bindport = self.port -1
        '''
        #socket for all servers
        self.sSockets  = [socket.socket() for i in range(10)]
        self.sSockets[sid].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #send
        self.sSockets[sid].bind((self.host, sendPorts[sid]))
        '''



        threading.Thread.__init__(self)

    def printStore(self):
        dict = self.history
        for entry in self.writeLog:
            dict[entry[3][0]] = entry[3][1]
        print(str(dict))
        del dict



    def run(self):
        self.s = socket.socket()  # Create a socket object
        print('Server started!')
        print('Server address:', self.host, ':', self.port)
        print('Waiting for clients...')
        self.s.bind((self.host, self.port))  # Bind to the port
        self.s.listen(5)  # Now wait for client connection.

        while True:
            clientM, addr = self.s.accept()  # Establish connection with client.
            threading.Thread(target=self.on_new_client, args=(clientM, addr)).start()
            print('Server', self.sid, 'receive from', addr, ' >> ', "connected")


    def on_new_client(self, clientM, addr):
        print("HEre")
        while True:
            msg = recvAll(clientM, 4096)
            if (msg != b''):
                self.lock.acquire()
                print('Server', self.sid, 'receive from', addr, ' >> ', msg)
                file = io.BytesIO(msg)
                while True:
                    try:
                        entry = pickle.load(file)
                        debug(entry)
                        if (isinstance(entry, str)):
                            debug("fff")
                            self.stabilize()
                        elif (isinstance(entry, tuple)):
                            '''
                            if (entry[0] == "server"):
                            # assume entry is the sid
                            # bind with the current bind port and output
                                sid = entry[1]
                                sport = entry[2]
                                self.sSockets[sid].bind((self.host, self.bindport))
                                self.sSockets[sid].connect((self.host, sport))
                                text = pickle.dumps(("receive",sid))
                                self.sSockets[sid].send(text)
                            elif(entry[0] == "receive"):
                                print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                clientM.send(b'ffff')
                                self.sSockets[entry[1]] = clientM
                                self.sSockets[entry[1]].send(b'ffff')
                                '''
                            self.update(entry)
                            print("!!!!!!str" + str(entry))
                        else:
                            value = self.get(entry)
                            clientM.send(pickle.dumps(value))
                    except EOFError:
                        break

                    #self.dicts[self.sid][self.sid].update(insert1)
                self.lock.release()

    def update(self, insertPair):
        """
        update writeLog and vClock, called when a write occurs
        """
        self.vclock.increment()
        self.updateItem(insertPair)
        return 0

    def get(self, key):
        """
        get value by checking wLog and history
        """
        # check wLog
        self.vclock.increment()
        idx = len(self.writeLog) - 1
        while idx >= 0:
            if key in self.writeLog[idx][3]:
                return self.writeLog[idx][3][key]
            else:
                idx -= 1
        # check history
        if key in self.history:
            return self.history[key]
        return 'ERR_KEY'

    def antiEntropy(self, otherLog, otherVclock):
        """
        Update wLog and vClock from exchanging with other server.
        """
        l1, l2 = len(self.writeLog), len(otherLog)
        merged = []
        i, j, total = 0, 0, 0
        while i < l1 and j < l2:
            if self.writeLog[i] > otherLog[j]:
                merged.append(otherLog[j])
                j += 1
            else:
                merged.append(self.writeLog[i])
                i += 1
            print((i,j,total))
        if i < l1:
            merged.extend(self.writeLog[i:])
        else:
            merged.extend(otherLog[j:])
        self.writeLog = merged
        del merged

        self.vclock.merge(otherVclock.vclock)
        historyTime = min(self.vclock.vclock)
        while self.writeLog[0][1] <= historyTime:
            insertPair = self.writeLog[0][3]
            self.history[insertPair[0]] = insertPair[1]
            self.writeLog.pop()


    def updateItem(self, insertPair): #### what's CLK here ???
        newRow = (sys.maxsize, self.vclock.getTimestamp(), self.sid, insertPair)
        self.writeLog.append(newRow)




    def sendWriteLog(self,sid):
        #connect !!!!!need transfor sid to sport
        # receive
        debug(sid)
        debug(self.sid)
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, sendPorts[0]))
        s.connect((self.host, receivePorts[1]))

        s.send(pickle.dumps(("writeLog",self.writeLog,self.vclock)))
        return 0

    def receiveWriteLog(self):
        #time.sleep(0.1)
        #debug(sid)
        debug(self.sid)
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host,receivePorts[1]))
        print("!!!!!!!!!!################!!!!!!!!!!!!!!!")
        s.listen(3)
        while True:
            tt, addr = s.accept()
            a = recvAll(tt, 4096)
            self.recv = pickle.loads(a)
            return 0


    def stabilize(self):
        print("stablestablestablestablestablestablestablestablestable")
        if self.sid == 0:
            time.sleep(0.1)
            self.sendWriteLog(1)
            #self.receiveWriteLog()
        elif self.sid == 1:
            threading.Thread(target = self.receiveWriteLog(), args=()).start()
            recvM = self.recv
            debug(str(recvM))
            self.antiEntropy(recvM[1],recvM[2])
            #self.sendWriteLog(0)


        '''
            self.broadcast() # 4 sendWriteLog
        else:
            self.receiveWriteLog()
            self.antiEntropy()
            self.sendWriteLog(self.sid+1)
            self.receiveWriteLog()
        '''

        print("stablestablestablestablestablestablestablestablestable")
        time.sleep(1)
        return 0


