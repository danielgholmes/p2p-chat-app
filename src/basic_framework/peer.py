__authors__ = 'Daniel Holmes 551240 and Jonathan Gerrand 349361'

import socket
import pickle
import threading 

def launch_channel_manager()


class Peer(object):
    
    def __init__(self, user_name = "User", IP_address = "127.0.0.1"):
        #A dictionary maintained by the indexing server
        self._peer_dict = {}
        #Structure for holding commands and arguments
        self._command_list = []
        #Name of the peer for this session
        self._user_name = user_name
        #The current IP address of the user
        self._user_IP_address = IP_address
        #The message buffer size
        self.BUFFER_SIZE = 1024
        #A counter tracking the ports currently used
        self._port_count = 5006
        #Container of current channels hosted by peer
        self._channel_names = []
        #Container of all current channel users
        self._channel_users = []
        #Container of all current channel text
        self._channel_text = []
        
        
    
    def update_contacts(self, name):
        self._command_list = []
        self._command_list.append("HELO")
        self._command_list.append(name)
        peer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #This was set for the default LAN network
        peer.connect(("127.0.0.1", 5005))
        peer.send(pickle.dumps(self._command_list))

        while (len(self._peer_dict) == 0):
            self._peer_dict = pickle.loads(peer.recv(10240))
        
        print self._peer_dict

        peer.close()
        pass

    def init_global_listner(self):
        self._global_listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._global_listner.bind(("127.0.0.1", 5000))
        self._global_listner.listen(1)
        pass

    def create_channel(self, channel, password):
        #Attempt to establish a channel on a port
        try:
            pass
    










