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
    # Just test git
    dicts = threading.local()
    dicts = [[{},{}], [{},{}]]

    def __init__(self, sid, port):
        self.sid = sid
        self.vclock = vclock(5, sid)
        self.writeLog = []
        self.history = {}
        self.clientM, self.addr = "", 0
        self.port = port
        self.lock = threading.Lock()

        #Socket for stablizing
        self.sendSocket = socket.socket()

        threading.Thread.__init__(self)

    def printStore(self):
        data = ""
        for dict in self.dicts[self.sid]:
            data += str(dict)
        print(data)


    def connect(self,sport):
        self.sport = sport
        self.s.close()
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(self.addr)
        self.s.connect((self.host, self.sport))


    def run(self):
        s = socket.socket()  # Create a socket object
        self.host = socket.gethostname()  # Get local machine name
        print('Server started!')
        print('Server address:', self.host, ':', self.port)
        print('Waiting for clients...')
        s.bind((self.host, self.port))  # Bind to the port
        s.listen(5)  # Now wait for client connection.

        while True:
            clientM, addr = s.accept()  # Establish connection with client.
            print('Server', self.sid, 'receive from', addr, ' >> ', "connected")
            threading.Thread(target = self.on_new_client, args=(clientM, addr)).start()
            print("################################3")

    def on_new_client(self, clientM, addr):
        print("HEre")
        while True:
            msg = recvAll(clientM, 4096)
            if (msg != b''):
                self.lock.acquire()
                if (msg == b'fffff'):
                    self.stabilize()
                else:
                    print('Server', self.sid, 'receive from', addr, ' >> ', msg)
                    file = io.BytesIO(msg)
                    while True:
                        try:
                            entry = pickle.load(file)
                            if (isinstance(entry, tuple)):
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
        return None

    def antiEntropty(self, otherLog, otherVclock):
        """
        Update wLog and vClock from exchanging with other server.
        """
        l1, l2 = len(self.writeLog), len(otherLog)
        merged = [] * (l1 + l2)
        i, j, total = 0, 0, 0
        while i < l1 and j < l2:
            if self.writeLog[i] > otherLog[j]:
                merged[total] = otherLog[j]
                j += 1
            else:
                merge[total] = self.writeLog[i]
                i += 1
            total += 1
        if i < l1:
            merge[total:] = self.writeLog[i:]
        else:
            merge[total:] = otherLog[j:]
        self.writeLog = merged
        del merged

        self.vclock.merge(otherVclock)
        historyTime = min(self.vclock)
        while writeLog[0][1] <= historyTime:
            insertPair = self.writeLog[0][3]
            self.history[insertPair[0]] = insertPair[1]
            self.writeLog.pop()


    def updateItem(self, insertPair): #### what's CLK here ???
        newRow = (sys.maxsize, self.vclock.getTimestamp(), self.sid, insertPair)
        self.writeLog.append(newRow)


    def sendWriteLog(self,sid):
        #connect !!!!!need transfor sid to sport
        connect(sid + 1)

        self.sendSocket
        return 0

    def receiveWriteLog(self):
        s = socket.socket()
        #s.listen()
        s.accept()
        return 0

    def broadcast(self):
        for i in range(4):
            sendWriteLog(i)
        return 0

    def stabilize(self):
        if self.sid == 0:
            self.sendWriteLog(self.sid+1)
            self.receiveWriteLog()
        elif self.sid == 4:
            self.receiveWriteLog()
            self.antiEntropy()
            self.broadcast() # 4 sendWriteLog
        else:
            self.receiveWriteLog()
            self.antiEntropy()
            self.sendWriteLog(self.sid+1)
            self.receiveWriteLog()

        time.sleep(1)
        print("stable")
        time.sleep(1)
        return 0

