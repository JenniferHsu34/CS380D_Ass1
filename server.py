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


#ports for communication between servers
receivePorts = [randint(2602,29999),randint(2602,29999),randint(2602,29999),randint(2602,29999),randint(2602,29999)]
sendFromPorts  = [randint(2602,29999),randint(2602,29999),randint(2602,29999),randint(2602,29999),randint(2602,29999)]


debugV = 0
def debug(s):
    global  debugV
    lsss = [str(debugV) for i in range(20)]
    #print(str(s)  + str(lsss))
    debugV = debugV +1

class server(threading.Thread):

    def __init__(self, sid, clientPort):
        self.sid = sid
        self.vclock = vclock(5, sid)
        self.writeLog = []
        self.history = {}
        self.clientM  = ""
        self.clientPort = clientPort
        self.host = socket.gethostname()
        self.lock = threading.Lock()
        self.receiveLock = threading.Lock()
        self.received = False

        threading.Thread.__init__(self)


    def printStore(self):
        dict = self.history
        for entry in self.writeLog:
            dict[entry[3][0]] = entry[3][1]
        print(str(dict))
        del dict



    def run(self):

        self.s = socket.socket()  # Create a socket object
        self.s.bind((self.host, self.clientPort))  # Bind to the clientPort
        self.s.listen(5)  # Now wait for client connection.
        threading.Thread(target=self.receiveWriteLog, args=()).start()
        while True:
            clientM, addr = self.s.accept()  # Establish connection with client.
            threading.Thread(target=self.on_new_client, args=(clientM, addr)).start()
            #print('Server', self.sid, 'receive from', addr, ' >> ', "connected")



    def on_new_client(self, clientM, addr):
        #print("HEre")
        while True:
            msg = recvAll(clientM, 4096)
            if (msg != b''):
                self.lock.acquire()
                #print('Server', self.sid, 'receive from', addr, ' >> ', msg)
                file = io.BytesIO(msg)
                while True:
                    try:
                        entry = pickle.load(file)
                        debug(entry)
                        if (entry[0] == "stabilize"):
                            debug("fff")
                            self.stabilize(entry[1])
                        elif (entry[0] == 'writeLog'):
                            self.update(entry)
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
            if key == self.writeLog[idx][3][0]:
                return self.writeLog[idx][3][1]
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
            elif self.writeLog[i] == otherLog[j]:
                merged.append(otherLog[j])
                j += 1
                i += 1
            else:
                merged.append(self.writeLog[i])
                i += 1
            #print((i,j,total))
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




    def sendWriteLog(self,toPort):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, sendFromPorts[self.sid]))
        s.connect((self.host, toPort))
        s.send(pickle.dumps(("writeLog",self.writeLog,self.vclock)))
        return 0

    def receiveWriteLog(self):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host,receivePorts[self.sid]))
        s.listen(3)
        while True:
            msg, addr = s.accept()
            threading.Thread(target=self.on_otherWriteLog, args=(msg,) ).start()




    def on_otherWriteLog(self,msg):
        a = recvAll(msg, 4096)
        recvM = pickle.loads(a)
        self.antiEntropy(recvM[1], recvM[2])



    def finish_receive(self):
        while True:
            if self.received == True:
                self.received = False
                break

    '''
    We will send the information to all connected servers and let the sid=0 server start
    '''
    def stabilize(self, connectedSids):

        if self.sid == 0:
            for toSid in connectedSids:
                self.sendWriteLog(receivePorts[toSid])
            self.finish_receive()
        else:

            self.finish_receive()
            a = self.recv
            print(a)
            self.antiEntropy(a[1], a[2])
            self.sendWriteLog(receivePorts[connectedSids[0]])




        #time.sleep(1)
        return 0


