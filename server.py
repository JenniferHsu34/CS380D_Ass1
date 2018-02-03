import socket  # Import socket module
import threading
import pickle

def recvall(socket):
    BUFF_SIZE = 4096  # 4 KiB
    data = b''
    while True:
        part = socket.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

def on_new_client(sid, socket, addr):
    while True:
        msg = recvall(socket)
        insert1 = pickle.loads(msg)
        print('Server', sid, 'receive from', addr, ' >> ', msg)



class server(threading.Thread):
    dicts = threading.local()
    dicts = [[{},{}], [{},{}]]

    def __init__(self, sid, port):
        self.sid = sid
        self.port = port
        threading.Thread.__init__(self)

    def printStore(self):
        data = ""
        for dict in self.dicts[self.sid]:
            data += str(dict)
        print(data)

    def run(self):
        s = socket.socket()  # Create a socket object
        host = socket.gethostname()  # Get local machine name
        print('Server started!')
        print('Server address:', host, ':', self.port)
        print('Waiting for clients...')
        s.bind((host, self.port))  # Bind to the port
        s.listen(5)  # Now wait for client connection.


        clientM, addr = s.accept()  # Establish connection with client.
        print('Got connection from', addr)
        while True:
            msg = clientM.recv(4096)
            if (msg != b''):
                print('Server', self.sid, 'receive from', addr, ' >> ', msg)
                insert1 = pickle.loads(msg)
                # print('Server', self.sid, 'receive from', addr, ' >> ', insert1)
                self.dicts[self.sid][self.sid].update(insert1)
                # threading.Thread(on_new_client(self.sid, c, addr))
                #self.printStore()
        s.close()






