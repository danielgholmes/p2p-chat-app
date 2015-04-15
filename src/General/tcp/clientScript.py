# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 19:29:24 2015

@author: Jonathan Gerrand
"""
from tcp_client import Client

client = Client()
messageInput = ""

while(messageInput != "\exit"):
    messageInput = raw_input("Please enter a message: ")
    client.sendMessage(messageInput)
    client.receiveMessage()
    pass

client.closeConnection()
