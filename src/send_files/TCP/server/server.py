import socket               

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
host = socket.gethostname() 
port = 5000                 
s.bind((host, port))        
f = open('textrecv.txt','wb')
s.listen(5)                 
while True:
    c, addr = s.accept()     
    print 'Got connection from', addr
    print "Receiving..."
    l = c.recv(1024)
    while (l):
        print "Receiving..."
        f.write(l)
        l = c.recv(1024)
    f.close()
    print "Done Receiving"
    c.close()                