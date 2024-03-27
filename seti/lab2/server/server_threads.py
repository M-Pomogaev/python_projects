from concurrent.futures import ThreadPoolExecutor
import time
from threading import Thread, Event
from sys import getsizeof
from tqdm import tqdm

client_pool = ThreadPoolExecutor(max_workers=4)

def socket_receive_speed(count, file_size, file_name, stop_event):
    progress = tqdm(desc=file_name, unit="B", total=file_size, unit_scale=True)
    prev_count = 0
    while (True):
        time.sleep(3)
        new_count = count[0]
        progress.update(new_count - prev_count)
        prev_count = count[0]
        if (stop_event.is_set() != False):
            progress.close()
            break

def reqv_message(socket):
    message = socket.recv(1024).decode()
    socket.send("OK".encode())
    return message
    

def client_socket_handler(client_socket, client_address):
    # Получаем имя файла от клиента
    file_name = reqv_message(client_socket)
    file_size = int(reqv_message(client_socket))
    print(f"Получен файл: {file_name}")
    count = [0]
    stop_event = Event()
    thread = Thread(target=socket_receive_speed, args=(count, file_size, file_name, stop_event))
    thread.start()
    # Открываем файл для записи
    with open(".\\uploads\\"+ file_name, "wb") as file:
        while True:
            time.sleep(0.01)
            # Получаем данные от клиента
            data = client_socket.recv(1024)
            if not data:
                break
            count[0] += getsizeof(data)
            file.write(data)
    stop_event.set()
    thread.join()
    print(f"Файл {file_name} успешно принят от клиента {client_address}")
    client_socket.close()
    client_socket.connect(client_address)

server_stop_event = Event()
def server_thread(server_socket):
    try:
        while server_stop_event.is_set() == False:
            # Принимаем входящее соединение
            client_socket, client_address = server_socket.accept()
            print(f"Подключено клиентом {client_address}")
            client_pool.submit(client_socket_handler, client_socket, client_address)
    except OSError:
        print("Closing server")
    client_pool.shutdown(wait=True)