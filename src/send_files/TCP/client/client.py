import socket               

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
host = socket.gethostname() 
port = 5000                 
s.connect((host, port))

f = open('textsend.txt','rb')
print 'Sending...'
l = f.read(1024)
while (l):
    print 'Sending...'
    s.send(l)
    l = f.read(1024)
f.close()
print "Done Sending"
s.shutdown(socket.SHUT_WR)
s.close()