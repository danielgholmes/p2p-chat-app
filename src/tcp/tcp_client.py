# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 18:44:48 2015

@author: Jonathan Gerrand
"""

class Client(object):
    
    
    def __init__(self, Ip_address = '127.0.0.1', Port_num = 5005):
        import socket
        self._ipAddress = Ip_address
        self._portNum = Port_num
        self._bufferSize = 1024
        self._soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._soc.connect((self._ipAddress,self._portNum))
        pass
    
    def sendMessage(self,message):
        self._soc.send(message)
        pass
    
    def receiveMessage(self):
        print("Received message: " + self._soc.recv(self._bufferSize)) 
        pass
    
    def closeConnection(self):
        print("Closing the client connection")
        self._soc.close()
        pass
    
    
        