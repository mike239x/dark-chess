import socket
from random import getrandbits
from select import select
from threading import Thread, Lock

# timeout in seconds
TIMEOUT = 5


def ready(sock, timeout):
    # sock.setblocking(0)
    # never try selecting closed socket!
    # sock.close()
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
    #TODO send color
    # self.sock.send(self.color)


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


# connect both players...
while not p1.connect(server): pass
print "player 1 connected"
while not p2.connect(server): pass
print "player 2 connected"


# if __name__ == '__main__':
    # print 'Thanks for executing me!'
