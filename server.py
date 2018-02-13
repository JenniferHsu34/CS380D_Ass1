import socket  # Import socket module
import threading
import pickle
from vclock import vclock
import io
import sys

def recvAll(socket, length):
    data = b''
    while True:
        packet = socket.recv(length)
        data += packet
        if len(packet) < length:
            return data

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
        #socket for all servers
        self.sSockets  = [socket.socket() for i in range(10)]


        threading.Thread.__init__(self)

    def printStore(self):
        dict = self.history
        for entry in self.writeLog:
            dict[entry[3][0]] = entry[3][1]
        print(str(dict))
        del dict


    def connect(self,sport):
        self.sport = sport
        self.s.close()
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.addr)
        self.s.connect((self.host, self.sport))


    def run(self):
        s = socket.socket()  # Create a socket object
        print('Server started!')
        print('Server address:', self.host, ':', self.port)
        print('Waiting for clients...')
        s.bind((self.host, self.port))  # Bind to the port
        s.listen(5)  # Now wait for client connection.

        while True:
            clientM, addr = s.accept()  # Establish connection with client.
            print('Server', self.sid, 'receive from', addr, ' >> ', "connected")
            threading.Thread(target = self.on_new_client, args=(clientM, addr)).start()

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

                        if (isinstance(entry, str)):
                            self.stabilize()
                        elif (isinstance(entry, tuple)):
                            if (entry[0] == "server"):
                            # assume entry is the sid
                            # bind with the current bind port and output
                                sid = entry[1]
                                sport = entry[2]
                                self.sSockets[sid].bind((self.host, self.bindport))
                                self.sSockets[sid].connect((self.host, sport))
                                self.sSockets[sid].send()
                                self.bindport = self.bindport - 1
                            else:
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
        self.sSockets[sid].sendall(pickle.dumps(("writeLog",self.writeLog,self.vclock)))
        return 0

    def receiveWriteLog(self,sid):

        s = self.sSockets[sid]
        a = recvAll(s, 4096)
        return pickle.loads(a)

    def broadcast(self):
        for i in range(4):
            sendWriteLog(i)
        return 0

    def stabilize(self):
        print("stablestablestablestablestablestablestablestablestable")
        if self.sid == 0:
            self.sendWriteLog(1)
            self.receiveWriteLog(1)
        elif self.sid == 1:
            recvM  = self.receiveWriteLog(0)
            print(str(recvM))
            self.antiEntropy(revM[1].revM[2])
            self.sendWriteLog(0)

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


