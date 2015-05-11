import socket

port = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', port))

f = open('image.jpg', 'wb')

chunk = sock.recvfrom(1024) 

while (chunk):
	f.write(chunk[0])
	chunk = sock.recvfrom(1024)

f.close()
c.close()