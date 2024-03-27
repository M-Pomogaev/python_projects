import os
from screan_cleaner import clean_screen
from sys import getsizeof
from time import sleep
        
clean_screen()

import socket
import sys

def is_valid_port(port):
    try:
        return 0 <= int(port) <= 65535
    except ValueError:
        return False
    
def get_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

def send_message(socket, message):
    socket.send(message.encode())
    if (socket.recv(1024).decode() != "OK"):
        print("Error")
        socket.close()
        sys.exit() 

if (len(sys.argv) != 4 ):
    print("Too many or too little arguments")
    sys.exit()
    
if (not is_valid_port(sys.argv[3])):
    print("Invalid port")
    sys.exit()
    
if (not os.path.exists(sys.argv[1])):
    print("File not found")
    sys.exit()
    
if ((server_host := get_ip(sys.argv[2])) == None):
    print("Invalid hostname")
    sys.exit()
    
server_port = int(sys.argv[3])
file_name = sys.argv[1];
file_size = os.path.getsize(file_name)
print(f"Listen on {server_host}:{server_port}, file: {file_name}")
try:
    # Создаем клиентский сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Подключаемся к серверу
    client_socket.connect((server_host, server_port))
    # Отправляем имя файла на сервер
    send_message(client_socket, file_name)
    send_message(client_socket, str(file_size))
    # Открываем файл для чтения
    count = 0
    with open(file_name, "rb") as file:
        while True:
            # Читаем данные из файла
            data = file.read(1024)
            count += getsizeof(data)
            if not data:
                break
            client_socket.send(data)
except ConnectionRefusedError:
    print("Connection refused")

print(f"Файл {file_name} успешно отправлен на сервер {server_host}:{server_port}")

# Закрываем клиентский сокет
client_socket.close()
