import socket  # Import socket module
import threading
import pickle
import time
import io


class server(threading.Thread):
    dicts = threading.local()
    dicts = [[{},{}], [{},{}]]

    def __init__(self, sid, port):
        self.sid = sid
        self.clientM, self.addr = "", 0
        self.port = port
        self.lock = threading.Lock()
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
            msg = clientM.recv(4096)
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

                            if (isinstance(entry, dict)):
                                self.update(entry)
                                print("!!!!!!str" + str(entry))
                            else:
                                value = self.get(entry)
                                clientM.send(pickle.dumps(value))
                        except EOFError:
                            break

                    #self.dicts[self.sid][self.sid].update(insert1)
                self.lock.release()

    def update(self,insertPair):
        return 0
    def get(self,key):
        return 0


    def stabilize(self):
        time.sleep(1)
        print("stable")
        time.sleep(1)
        return 0

