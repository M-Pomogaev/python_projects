from screan_cleaner import clean_screen

clean_screen()

import socket
import sys

def is_valid_port(port):
    try:
        return 0 <= int(port) <= 65535
    except ValueError:
        return False

if (len(sys.argv) != 2):
    print("Too many or too little arguments")
    sys.exit()
elif (not is_valid_port(sys.argv[1])):
    print("Invalid port")
    sys.exit()
else:
    server_port = int(sys.argv[1])

# Создаем серверный сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Связываем сокет с хостом и портом
server_host = "127.0.0.1"
server_socket.bind((server_host, server_port))

# Начинаем прослушивать
server_socket.listen(5)
print(f"Listen on {server_host}:{server_port}")

from server_threads import server_thread, server_stop_event
from threading import Thread

(server := Thread(target=server_thread, args=(server_socket,))).start()
try:
    while (input() != "exit"):
        pass
except KeyboardInterrupt:
    pass
server_stop_event.set()
server_socket.close()
server.join()
# Закрываем серверный сокет
