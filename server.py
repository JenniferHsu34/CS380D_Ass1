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
        while True:
            s = socket.socket()  # Create a socket object
            host = socket.gethostname()  # Get local machine name
            print('Server started!')
            print('Server address:', host, ':', self.port)
            print('Waiting for clients...')
            s.bind((host, self.port))  # Bind to the port
            s.listen(5)  # Now wait for client connection.


            self.clientM, self.addr = s.accept()  # Establish connection with client.
            print('Server', self.sid, 'receive from', self.addr, ' >> ', )
            threading.Thread(target = self.on_new_client).run()
            s.close()

    def on_new_client(self):
        print("HEre")
        while True:
            msg = self.clientM.recv(4096)

            if (msg != b''):
                print('Server', self.sid, 'receive from', self.addr, ' >> ', msg)
                insert1 = pickle.loads(msg)
                self.dicts[self.sid][self.sid].update(insert1)

        self.printStore()



