__authors__ = 'Daniel Holmes 551240 and Jonathan Gerrand 349361'

import socket
import pickle

peer_dict = {}
command_list = []

def update_contacts(name):
    command_list.append("HELO")
    command_list.append(name)
    peer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    peer.connect(("127.0.0.1", 5005))
    peer.send(pickle.dumps(command_list))

    while (len(peer_dict) == 0):
        peer_dict = pickle.loads(peer.recv(10240))
        
    print peer_dict

    peer.close()
    pass

#Establish new connnection fellow peer

update_contacts("Bob")







