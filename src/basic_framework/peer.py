__authors__ = 'Daniel Holmes 551240 and Jonathan Gerrand 349361'

import socket
import pickle

peerDict = {}

peer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

peer.connect(("127.0.0.1", 5005))

peer.send("HELO")

while (len(peerDict) == 0):

    peerDict = pickle.loads(peer.recv(10240))

print peerDict


