import pygame
from network import Network
from threading import Thread
from button import *
from lobby import *  
from menu import *
from player import *
from point import *
from game_end_screan import *
from number import *

class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.plNum = 2
        self.canvas = Canvas(self.width, self.height, "Life...")
        self.menu = Menu(self.canvas.get_center_x(130), 150, w, h, self.canvas, 130, 50, 5)
        self.lobby = Lobby(self.canvas, self.width, self.height)
        self.game_over = GameEndScreen(self.canvas, self.width, self.height)
        self.running = False
        self.game_is_created = False
    
    def set_players(self):
        print(self.costs)
        self.pl_id = int(self.net.id)
        self.players = [Player(self.positions[i][0], self.positions[i][1], i, (255 * (i != self.pl_id), 0, 255 * (i == self.pl_id))) for i in range(self.plNum)]
        self.points = [Point(self.positions[i][0], self.positions[i][1], i, self.costs[i-self.plNum], (0, 255, 0)) for i in range(self.plNum, self.plNum * 3)]
        
    def draw_gameplay_thread(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            self.canvas.draw_background()
            deleted = -1
            for point in self.points:
                if point.draw(self.canvas.get_canvas(), self.players[self.pl_id]):
                    deleted = self.points.index(point)
                    self.send_point_id(deleted)
            if deleted != -1:
                self.points.pop(deleted)
            for player in self.players:
                player.draw(self.canvas.get_canvas())
            self.canvas.update()
            self.send_player_position()
        print("Stoped drawing")
            
    def receive_positions_thread(self):
        while(self.running):
            data = self.net.receive()
            if data:
                #print(data)
                #print("data: ", end="")
                data = data.split(":")
                for d in data:
                    if (d == ""):
                        continue
                    if ("Stop" in d):
                        #print(d, end=" ")
                        stop, scores = d.split(";")
                        self.scores = scores.split(",")
                        self.running = False
                        break
                    d = d.split(",")
                    if (len(d) == 3):
                        plId, x, y = d
                        self.players[int(plId)].x, self.players[int(plId)].y = int(x), int(y)
                    elif(len(d) == 1):
                        print(d)
                        pointId = d[0]
                        self.points.pop(int(pointId))
        print("Stoped receiving")
                        
                        
                
    def check_escape(self):
        stop = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop = True
        return stop
    
    def playing(self):
        self.set_players()
        print(self.pl_id)
        self.running = True
        clock = pygame.time.Clock()
        drawing_thread = Thread(target=self.draw_gameplay_thread)
        receivin_thread = Thread(target=self.receive_positions_thread)
        for i in range(3, 0, -1):
            maxFont, minFont = 100, 10
            for j in range(100):
                self.canvas.draw_background()
                for point in self.points:
                    point.draw(self.canvas.get_canvas(), self.players[self.pl_id])
                for player in self.players:
                    player.draw(self.canvas.get_canvas())
                CountDownNumber(self.width/2, self.height/2, (0, 0, 0), i, int(maxFont - j * ((maxFont - minFont) / 60))).draw(self.canvas.get_canvas())
                self.canvas.update()
                clock.tick(100)
        drawing_thread.start()
        receivin_thread.start()
        player = self.players[self.pl_id]
        while self.running:
            clock.tick(60)
            if self.check_escape():
                self.running = False
                break
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                if player.x <= self.width - player.velocity - player.width:
                    player.move(0)
            if keys[pygame.K_LEFT]:
                if player.x >= player.velocity:
                    player.move(1)
            if keys[pygame.K_UP]:
                if player.y >= player.velocity:
                    player.move(2)
            if keys[pygame.K_DOWN]:
                if player.y <= self.height - player.velocity - player.height:
                    player.move(3)
        drawing_thread.join()
        self.net.close()
        receivin_thread.join()
        self.game_over.set_scores(self.scores, self.pl_id)
        while not self.check_escape():
            if (self.game_over.draw() == "Back"):
                return
            
            
            
        
    def creating_game_lobby(self):
        clicked = ""
        stop = False
        chosed = False
        while not stop:
            stop = self.check_escape()
            if (clicked == "Back"):
                return False
            if (clicked == "2" or clicked == "3" or clicked == "4"):
                self.plNum = int(clicked)
                chosed = True
            if (clicked == "Start" and chosed):
                return True
            clicked = self.lobby.draw_creating()
        self.net.close()
        return False
    def waiting_for_players_thread(self):
        mesege = "Waiting for players"
        while mesege == "Waiting for players":
            mesege = self.net.receive()
            mesege, plNum, positions, costs = mesege.split(":")
            self.net.send("Ok")
            if mesege == "Start":
                print(mesege)
                positions = positions.split(";")
                costs = costs.split(";")
                self.positions = [(int(x.split(",")[0]), int(x.split(",")[1])) for x in positions if x != ""]
                self.costs = [int(x) for x in costs if x != ""]
                self.plNum = int(plNum)
                self.game_is_created = True
                break
            
        print(mesege)
            
    def joining_game_lobby(self):
        self.game_is_created = False
        waiting_thr = Thread(target=self.waiting_for_players_thread)
        waiting_thr.start()
        clicked = ""
        stop = False
        while not stop:
            if (self.game_is_created):
                return True
            stop = self.check_escape()
            if (clicked == "Back"):
                return False
            clicked = self.lobby.draw_waiting()
        self.net.close()
        waiting_thr.join()
        return False
    def start_game(self):
        if (not self.net.start()):
            self.net.close()
            return
        if (not self.creating_game_lobby()):
            self.net.close()
            return
        self.net.send(str(self.plNum))
        if (not self.joining_game_lobby()):
            self.net.close()
            return
        self.playing()
        
    def join_game(self):
        if (not self.net.join()):
            self.net.close()
            return
        if (not self.joining_game_lobby()):
            self.net.close()
            return
        self.playing()

    def run(self):
        stop = False
        while (not stop):
            stop = self.check_escape()
            action = self.menu.draw()
            if (action == "Start"):
                self.start_game()
            if (action == "Join game"):
                self.join_game()
            if (action == "Exit"):
                stop = True
        pygame.quit()

    def send_player_position(self):
        player = self.players[self.pl_id]
        data = str(self.pl_id) + "," + str(player.x) + "," + str(player.y) + ":"
        reply = self.net.send(data)
        return reply
    
    def send_point_id(self, point_id):
        data = str(point_id) + ":"
        reply = self.net.send(data)
        return reply

class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)
        pygame.init()

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((255,255,255))
        
    def get_center_x(self, width):
        return int(self.width / 2 - width / 2)

    def get_center_y(self, height):
        return int(self.height / 2 - height / 2)
    