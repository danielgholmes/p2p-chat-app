__authors__ = 'Daniel Holmes 551240 and Jonathan Gerrand 349361'

import socket
import pickle

class Peer(object):
    
    def __init__(self):
        #A dictionary maintained by the indexing server
        self._peer_dict = {}
        #Structure for holding commands and arguments
        self._command_list = []
        #Name of the peer for this session
        self._user_name = ""
        #The current IP address of the user
        self._user_IP_address = "127.0.0.1"
        self.BUFFER_SIZE = 1024
        
        
    
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

    def create_new_chat(self, name):
        join_message = []
        join_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #For later use
        #join_connection.connect((self._peer_dict[name], 5000))
        join_connection.connect(("127.0.0.1", 5000))
        join_message.append("JOIN")
        join_message.append(self._user_name)
        
        join_connection.send(pickle.dumps(join_message))
        join_connection.close()
        pass

    def listen_for_chats(self):
        
        pass
    
    #Name change required.
    def private_chat(self, expected_name):
        private_chat_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        private_chat_connection.bind((self._user_IP_address, 5001))
        private_chat_connection.listen(1)
    
        conn, addr = private_chat_connection.accept()        
        if (addr == self._peer_dict[expected_name]):
            
            message = ''
            message = conn.recv(self.BUFFER_SIZE)
            
            while (message != 'quit'):
            
                pass
        
            pass


#Establish new connnection fellow peer
#update_contacts("Rodger")







