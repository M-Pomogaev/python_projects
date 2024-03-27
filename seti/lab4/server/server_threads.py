import socket
from _thread import *
import threading

game_is_running = False
mutex = threading.Lock()

ids = []
clients = []
numOfPlayers = 0
playersConnected = 0
playersReady = 0
playersStoped = 0

import itertools
import random
positions = [(i, j) for i, j in itertools.product(range(0, 500, 50), range(0, 500, 50))]
points_cost = []
scores = []

def find_new_id():
    global ids
    id = 0
    while True:
        if id not in ids:
            return id
        id += 1
        
def close_connection(conn):
    global playersConnected, clients, ids
    print(playersConnected)
    print("Connection Closed")
    if (conn in clients):
        clientInd = clients.index(conn)
        clients.pop(clientInd)
        ids.pop(clientInd)
        playersConnected -= 1
    print(playersConnected)
    conn.close()
    
def send(conn, data):
    try:
        conn.send(str.encode(data))
    except socket.error as e:
        close_connection(conn)

def receive(conn):
    try:
        data = conn.recv(2048).decode()
        if (not data):
            close_connection(conn)
            return
    except socket.error as e:
        close_connection(conn)
        raise e
    return data

def create_game(conn):
    global numOfPlayers, playersConnected, playersReady, scores, points_cost, playersStoped
    playersConnected = 0
    playersStoped = 0
    numOfPlayers = int(receive(conn))
    playersReady = 0
    print(numOfPlayers)
    random.shuffle(positions)
    print(positions[:3*numOfPlayers])
    scores = [0 for i in range(numOfPlayers)]
    points_cost = [random.randint(1, 5) for i in range(2*numOfPlayers)]
    
    
def connect_client(conn, id):
    global game_is_running, playersConnected
    reqv = receive(conn)
    if reqv == "start":
        if game_is_running:
            send(conn, "game already running")
            close_connection(conn)
            return False
            
    if reqv == "join" and not game_is_running:
        send(conn, "no game started")
        close_connection(conn)
        return False
    send(conn, str(id))
    ids.append(id)
    clients.append(conn)
    if (not game_is_running == True):
        game_is_running = True
        create_game(conn)
    playersConnected += 1
    return True
    
def send_score(conn):
    global scores
    stopstr = "Stop;"
    for score in scores:
        stopstr += f'{score},'
    stopstr = stopstr[:-1] + ":"
    send(conn, stopstr)
    close_connection(conn)
    
def threaded_client(conn, id):
    global game_is_running, playersReady, numOfPlayers, playersConnected, scores, points_cost, playersStoped
    if(not connect_client(conn, id)):
        return
    print(numOfPlayers, playersConnected)
    while(playersConnected < numOfPlayers):
        send(conn, f'Waiting for players:{numOfPlayers}'+"::")
        receive(conn)
    posStr = ""
    for x, y in positions[:3*numOfPlayers]:
        posStr += f'{x},{y};'
    posStr += ":"
    for cost in points_cost:
        posStr += f'{cost};'
    print(posStr)
    send(conn, f'Start:{numOfPlayers}:' + posStr)
    react = receive(conn)
    print(react[0:2])
    if (react[0:2] != "Ok"):
        close_connection(conn)
        return
    playersReady += 1
    print(playersReady, numOfPlayers)
    while(playersReady < numOfPlayers):
        pass
    while True:
        try:
            if (len(points_cost) == 0):
                break
            reply = conn.recv(2048).decode()
            if (not reply):
                break
            for d in reply.split(":"):
                d = d.split(",")
                if (d[0] == ""):
                    continue
                if (len(d) == 1):
                    print(d[0])
                    cost_id = int(d[0])
                    scores[ids.index(id)] += points_cost[cost_id]
                    points_cost.pop(cost_id)
                    print(scores)
            for c in clients:
                if c != conn:
                    c.send(str.encode(reply))
        except:
            break
    playersStoped += 1
    while(playersStoped < numOfPlayers):
        pass
    if (len(points_cost) == 0):
        send_score(conn)
    close_connection(conn)

def connections_threaded(s):
    while True:
        try:
            conn, addr = s.accept()
        except(KeyboardInterrupt, SystemExit):
            exit()
        id = find_new_id() #id игрока
        print("Connected to: ", addr)
        print(game_is_running)
        start_new_thread(threaded_client, (conn, id))
        
def game_control_threaded():
    global game_is_running
    while True:
        if (len(clients) == 0):
            game_is_running = False
        else:
            game_is_running = True