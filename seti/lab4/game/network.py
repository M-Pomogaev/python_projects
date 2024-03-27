import socket


class Network:

    def __init__(self):
        self.host = "localhost" # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                # ipv4 address. This feild will be the same for all your clients.
        self.port = 4545
        self.addr = (self.host, self.port)
        
    def join(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.addr)
        self.send("join")
        ans = self.receive()
        print(ans)
        if ans == "no game started":
            return False
        self.id = ans
        return True
    
    def start(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.addr)
        self.send("start")
        ans = self.receive()
        print(ans)
        if ans == "game already running":
            return False
        self.id = ans
        return True
    
    def close(self):
        self.client.close()
        print("Connection Closed")

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            return str(e)
        
    def receive(self):
        try:
            data = self.client.recv(2048).decode()
            return data
        except socket.error as e:
            return str(e)
