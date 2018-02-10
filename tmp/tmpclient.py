import socket
from select import select

# linear client
# connects to server, reads ID, sends ID back

#TODO add proper IP adress
TCP_IP = '127.0.0.1'
#TCP_IP = 'R2D2'
TCP_PORT = 5005

#TODO think of this one
BUFFER_SIZE = 1024

# connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))

# timeout in seconds
TIMEOUT = 5

def ready(sock, timeout):
    # sock.setblocking(0)
    ready = select([sock], [], [], 60)
    return ready[0]
if not ready(sock, TIMEOUT):
    self.sock.close()
    print "couldn't connect"
    exit(0)
msg = sock.recv(BUFFER_SIZE)
if not msg: # shouldn't happen cuz the sock is ready to be read
    sock.close()
    print "received empty msg"
    exit(0)
print "received msg: ", msg
sock.send(msg)
print "send msg back, closing"
