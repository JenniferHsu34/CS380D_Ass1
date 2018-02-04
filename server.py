import socket  # Import socket module
import threading
import pickle



class server(threading.Thread):
    dicts = threading.local()
    dicts = [[{},{}], [{},{}]]

    def __init__(self, sid, port):
        self.sid = sid
        self.clientM, self.addr = "", 0
        self.port = port
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
            if addr[1]!=27000:
                print('Server', self.sid, 'receive from', addr, ' >> ', "connected")
                threading.Thread(target = self.on_new_client, args=(clientM, addr)).start()
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            else:
                self.stabilize()

    def on_new_client(self, clientM, addr):
        print("HEre")
        while True:
            msg = clientM.recv(4096)

            if (msg != b''):
                print('Server', self.sid, 'receive from', addr, ' >> ', msg)
                insert1 = pickle.loads(msg)
                self.dicts[self.sid][self.sid].update(insert1)

    def stabilize(self):
        return 0

