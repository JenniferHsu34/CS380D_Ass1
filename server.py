import socket  # Import socket module
import threading
import pickle
from vclock import vclock
import io
import sys
from random import randint
import time

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
                        if entry[0] == "stabilize":
                            debug("fff")
                            self.stabilize(entry[1])
                        elif entry[0] == 'put':
                            self.update(entry[1:])
                        elif entry[0] == 'get':
                            value = self.get(entry[1:])
                            clientM.send(pickle.dumps(value))
                    except EOFError:
                        break

                    #self.dicts[self.sid][self.sid].update(insert1)
                self.lock.release()

    def update(self, insertTuple):
        """
        update writeLog and vClock, called when a write occurs
        insertTuple = (key, value, cid, cTime)
        """
        self.updateItem(insertTuple)
        return 0

    def get(self, compTuple):
        """
        get value by checking wLog and history
        compTuple = (key, [cid, cTime, sTime, sid])
        """
        # check wLog
        self.vclock.increment()
        key = compTuple[0]
        idx = len(self.writeLog) - 1
        while idx >= 0:
            if key == self.writeLog[idx][3][0]:
                value = self.writeLog[idx][3][1]
                curVersion = self.writeLog[idx][3][2:] + (self.writeLog[idx][1], self.writeLog[idx][2])
                return compVersion(value, curVersion, tuple(compTuple[1]))
            else:
                idx -= 1
        # check history
        if key in self.history:
            value = self.history[key][0]
            return compVersion(value, self.history[key][1:], tuple(compTuple[1]))
        return 'ERR_KEY'

    def compVersion(self, value, curVersion, lastVersion):
        if curVersion[2] < lastVersion[2] or (curVersion[2] == lastVersion[2] and curVersion[3] < lastVersion[3]):
            return "ERR_DEP"
        elif curVersion[0] == lastVersion[0] and curVersion[1] < lastVersion[1]:
            return "ERR_DEP"
        else:
            retTumple = (value, curVersion[2], curVersion[3])
            return retTumple

    def antiEntropy(self, otherLog, otherVclock):
        """
        Update wLog and vClock from exchanging with other server.
        writeLog = [(sys.maxsize, sTime, sid, (key, value, cid, cTime))]
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
        if i < l1:
            merged.extend(self.writeLog[i:])
        else:
            merged.extend(otherLog[j:])
        self.writeLog = merged
        del merged

        self.vclock.merge(otherVclock.vclock)
        historyTime = min(self.vclock.vclock)
        while len(self.writeLog) > 0 and self.writeLog[0][1] <= historyTime:
            key = self.writeLog[0][3][0]
            insertTuple = self.writeLog[0][3][1:] + (self.writeLog[0][1], self.writeLog[0][2])
            self.history[key] = insertTuple
            self.writeLog.pop()


    def updateItem(self, insertTuple):
        self.vclock.increment()
        newRow = (sys.maxsize, self.vclock.getTimestamp(), self.sid, insertTuple)
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


