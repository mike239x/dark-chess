import socket
from random import getrandbits
from select import select
from threading import Thread, Lock
import protocol
import chess
import string

# timeout in seconds
TIMEOUT = 5

def ready(sock, timeout):
    # sock.setblocking(0)
    ready = select([sock], [], [], 60)
    return ready[0]

class Player:
    ID_SIZE = 16
    def __init__(self, color):
        self.color = color
        # we will try to keep the socket opened, if we DC client should re
        self.sock = None
        self.id = str(getrandbits(Player.ID_SIZE))
    def reroll(self):
        self.id = str(getrandbits(Player.ID_SIZE))
    def connect(self, s):
        sock, (ip, port) = s.accept()
        self.sock = sock
        # send players ID
        self.sock.send(self.id)
        # receive confirmation (same ID)
        #TODO add timeout
        if not ready(self.sock, TIMEOUT):
            self.sock.close()
            return 0
        msg = sock.recv(BUFFER_SIZE)
        if not msg: # shouldn't happen cuz the sock is ready to be read
            #TODO mb raise an exeption
            self.sock.close()
            return 0
        if msg != self.id:
            #TODO mb raise an exeption
            self.sock.close()
            return 0
        return 1
    def refresh(self, sock):
        #TODO think if confirmation is needed
        self.sock = sock
    def echo(self, msg):
        self.sock.send(msg)

class Game(Thread):
    def __init__(self):
        self.white = None
        self.black = None
        self.game = chess.Game()
    def add_player(self, player):
        if player.color == 'white':
            self.white = player
        if player.color == 'black':
            self.black = player
    # handle a socket that is ready to write
    def handle(self, sock):
        try:
            msg = sock.recv(BUFFER_SIZE).strip().split(' ')
            player = None
            if msg[0] == self.white.id:
                player = self.white
            if msg[0] == self.black.id:
                player = self.black
            if player == None:
                return 0
            if msg[1] not in protocol.QUERIES:
                return 0
            if msg[1] == protocol.GET_COLOR:
                player.echo(player.color)
            if msg[1] == protocol.RECONNECT:
                player.refresh(sock)
            if msg[1] == protocol.GET_POSITION:
                player.echo(board.view(player.color))
            if msg[1] == protocol.ECHO:
                text = string.join(msg[1:], ' ')
                self.white.echo(text)
                self.black.echo(text)
            if msg[1] == protocol.MOVE:
                if player.color == self.game.active_player:
                    if self.game.can_move(msg[2]):
                        self.game.make_move(msg[2])
                        #TODO if win is achived, inform players
                        #TODO also send them full info on this game
                        # with all the positions opened
                        return 0
                    #TODO mb send new info to the opponent
            return 0
        except Exception as e:
            return 1
    def run(self):
        #TODO init mb
        while 1:
            # listening to both players at the same time
            # 'refresh' every 0.5 seconds
            ready = select([white.sock, black.sock], [], [], 0.5)
            for sock in ready[0]:
                self.handle(sock)

#TODO set things up with proper IP adress
TCP_IP = '127.0.0.1'
# TCP_IP = socket.gethostname()
TCP_PORT = 5005

#TODO think of this one
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, TCP_PORT))
server.listen(2)

# chose who is playing white
coin = getrandbits(1)==1
# create player classes
p1 = Player('white' if coin else 'black')
p2 = Player('black' if coin else 'white')
while p1.id == p2.id:
    p2.reroll()
# create game class, add players
game = Game()
game.add_player(p1)
game.add_player(p2)

# connect both players...
while not p1.connect(server): pass
print "player 1 connected"
while not p2.connect(server): pass
print "player 2 connected"

game.start()
#TODO think of it
game.join()

class Listener(Thread):
    def __init__(self, server):
        self.server = server
    def run(self):
        # listen to the server socket
        #f.e. if one of players DC-ed we need him to connect back using this
        sock, (ip, port) = self.server.accept()
        if not ready(sock, TIMEOUT):
            sock.close()
            continue
        game.handle(sock)

l = Listener(server)
l.start()
#TODO think of it, mb no join is needed
l.join()

# if __name__ == '__main__':
    # print 'Thanks for executing me!'
