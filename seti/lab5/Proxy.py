import select
import socket

def recv(sock, addr, bufsize=1024):
    try:
        data = sock.recv(bufsize)
    except ConnectionError:
        print(f"Client suddenly closed while receiving")
        raise ConnectionError
    print(f"Received {data} from: {addr}")
    if not data:
        print("Disconnected by", addr)
    return data

def send(sock, addr, data):
    print(f"Send: {data} to: {addr}")
    try:
        sock.send(data) 
    except ConnectionError:
        print(f"Client suddenly closed, cannot send")
        return False
    return True

SOCKS_VERSION = 5
class Proxy: 
    def __init__(self): 
        self.username = "username" 
        self.password = "password"
            
    def disconnect(self, sock):
        del self.inputs[sock]
        sock.close()
        
    class Connection:
        def __init__(self, sock, addr):
            self.sock = sock
            self.addr = addr
            self.remote = None
            self.step = 0
        def get_available_methods(self, nmethods):
            methods = [] 
            for _ in range(nmethods):
                methods.append(ord(recv(self.sock, self.addr, 1))) 
            return methods
        def get_methods(self):
            data  = recv(self.sock, self.addr, 2)
            version, nmethods = data[0], data[1]
            print(f"Version: {version}, nmethods: {nmethods}")
            if (version != SOCKS_VERSION):
                return False
            methods = self.get_available_methods(nmethods) 
            if 2 not in set(methods):
                return False
            else:
                self.sock.sendall(bytes([SOCKS_VERSION, 2]))
                return True
                
        def verify_credentials(self, real_password, real_username):
            version = ord(recv(self.sock, self.addr, 1)) # should be 1 
            username_len = ord(recv(self.sock, self.addr, 1))
            username = recv(self.sock, self.addr, username_len).decode('utf-8')
            password_len = ord(recv(self.sock, self.addr, 1))
            password = recv(self.sock, self.addr, password_len).decode('utf-8') 
            if username == real_username and password == real_password:
                response = bytes([version, 0])
                self.sock.sendall(response)
                print(f'Successful login: {username}, {password}')
                return True
            response = bytes([version, 0xFF])
            self.sock.sendall(response)
            return False
        def set_remote(self):
            version, cmd, _, address_type = recv(self.sock, self.addr, 4)
            if address_type == 1: # IPv4 
                address = socket.inet_ntoa(recv(self.sock, self.addr, 4))
            elif address_type == 3: # Domain name
                domain_length = recv(self.sock, self.addr, 1)[0]
                address = recv(self.sock, self.addr, domain_length)
                address = socket.gethostbyname(address)
            else:
                return False
            port = int.from_bytes(recv(self.sock, self.addr, 2), 'big', signed=False)
            try: 
                if cmd == 1: # CONNECT
                    self.remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.remote.connect((address, port))
                    bind_address = self.remote.getsockname()
                    print("* Connected to {} {}".format(address, port))
                else: return False 

                addr = int.from_bytes(socket.inet_aton(bind_address[0]), 'big', signed=False)
                port = bind_address[1]
                reply = b''.join([ 
                    SOCKS_VERSION.to_bytes(1, 'big'),
                    int(0).to_bytes(1, 'big'),
                    int(0).to_bytes(1, 'big'),
                    int(1).to_bytes(1, 'big'),
                    addr.to_bytes(4, 'big'),
                    port.to_bytes(2, 'big') 
                ])
            except Exception as e:
                return False
            self.sock.sendall(reply) 
            if reply[1] == 0 and cmd == 1:
                return self.remote
            return False
        
        def exchange(self, sock):
            if self.sock == sock:
                data = self.sock.recv(4096)
                if self.remote.send(data) <= 0:
                    return False
            if self.remote == sock:
                data = self.remote.recv(4096)
                if self.sock.send(data) <= 0:
                    return False
            return True
    def run(self, host, port): 
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_sock.bind((host, port))
        serv_sock.listen(1)
        self.inputs = {serv_sock: None}
        self.outputs = {}
        while True:
            print("Waiting for connections or data...")
            readable, writeable, exceptional = select.select(self.inputs.keys(), self.outputs.keys(), self.inputs.keys())
            for sock in readable:
                if sock == serv_sock:
                    sock, addr = serv_sock.accept() 
                    print("Connected by", addr)
                    self.inputs[sock] = self.Connection(sock, addr)
                else:
                    try:
                        connection = self.inputs[sock]
                        if (connection.step == 0):
                            if (not connection.get_methods()):
                                self.disconnect(sock)
                            else: connection.step += 1
                        elif (connection.step == 1):
                            if (not connection.verify_credentials(self.password, self.username)):
                                self.disconnect(sock)
                            else: connection.step += 1
                        elif (connection.step == 2):
                            if (not (result := connection.set_remote())):
                                self.disconnect(sock)
                            else: 
                                connection.step += 1
                                self.inputs[result] = connection
                        else:
                            if (not connection.exchange(sock)):
                                self.disconnect(connection.sock)
                                self.disconnect(connection.remote)
                    except Exception as e:
                        self.disconnect(sock)