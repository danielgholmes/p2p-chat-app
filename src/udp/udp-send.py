import socket

UDP_IP = "127.0.0.1" # 
UDP_PORT = 5678
MESSAGE = "HELO"

print "Welcome!"

protocol = raw_input("Please enter either TCP or UDP protocol: ")

if protocol == "UDP":
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT)) # send out the HELO
	# sock.bind((UDP_IP, UDP_PORT)) 

	while True:
		data, addr = sock.recvfrom(1024)
		if data == "REPLY":
			print "Contact online! Received reply from " + addr

elif protocol == "TCP":
	print "Not supported yet :P"
