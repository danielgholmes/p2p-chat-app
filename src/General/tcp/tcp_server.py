# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 18:45:26 2015

@author: Jonathan Gerrand
"""
import socket
#TCP_IP = '127.0.0.1'
#TCP_PORT = 5005
#BUFFER_SIZE = 1024  
#
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((TCP_IP, TCP_PORT))
#s.listen(1)
#
#conn, addr = s.accept()
#print 'Connection address:', addr
#while 1:
#    data = conn.recv(BUFFER_SIZE)
#    if not data: break
#    print "received data:", data
#    conn.send(data)  # echo
#    
#conn.close()

class Server:

    def __init__(self, Ip_address = '127.0.0.1', Port_num = 5005):
        
        self._ipAddress = Ip_address
        self._portNum = Port_num
        self._bufferSize = 1024
        self._exitString = "\exit"
        self._recvString = ""
        pass

    def listen(self, ipAddress, portNum):
        self._soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._soc.bind((ipAddress,portNum))
        self._soc.listen(1)
        conn, addr = self._soc.accept()
        while(self._recvString != self._exitString):
            self._recvString = conn.recv(self._bufferSize)
            print("Received: " + self._recvString)
            conn.send(self._recvString)
            pass
        
        conn.close()
        self._soc.close()
    
    
    
        
        
        
        