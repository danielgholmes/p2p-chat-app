import socket
import time

port = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.settimeout(5)

f = open('image.jpg', 'rb')
chunk = f.read(1024)

while(chunk):
	sock.sendto(chunk, ('127.0.0.1', port))
	time.sleep(0.001)
	chunk = f.read(1024)

f.close()
sock.close()