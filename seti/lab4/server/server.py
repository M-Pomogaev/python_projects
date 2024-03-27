import socket
from _thread import *
import sys
from server_threads import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = '127.0.0.1' # 'localhost'
port = 4545
server_ip = socket.gethostbyname(server)
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))
        
# number of connections that can be queued up
s.listen(4)
print("Waiting for a connection")
        
start_new_thread(connections_threaded, (s,))
start_new_thread(game_control_threaded, ())
while True:
    try:
        pass
    except(KeyboardInterrupt, SystemExit):
        s.close()
        exit()