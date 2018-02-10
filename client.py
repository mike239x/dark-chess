import socket
import sys, pygame
pygame.init()

#TODO set things up
size = width, height = 320, 240
# black = 0, 0, 0
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Dark Chess 2.0')


# from select import select
# sock.setblocking(0)
# # hang for 1 minute trying to connect
# ready = select([sock], [], [], 60)
# if ready[0]:
#     data = sock.recv(4096)
# else:
#     # welp, we couldn't connect

#TODO add GUI

#TODO add proper IP adress
TCP_IP = '127.0.0.1'
#TCP_IP = 'R2D2'
TCP_PORT = 5005

#TODO think of this one
BUFFER_SIZE = 1024

# connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

# open save file for reading/appending
save = open('current.game', 'a+')
# save.close()
color = save.readline().strip()
if color == '':
    # very start of the game, no color assigned
    # get color
    data = s.recv(BUFFER_SIZE)
    if data == 0:
        # well we screwed up
        return 1
    else:
        color = data
        save.write(color+'\n')
    # s.close()

#game started
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save.close()
            sock.close()
            pygame.quit()
            sys.exit()
