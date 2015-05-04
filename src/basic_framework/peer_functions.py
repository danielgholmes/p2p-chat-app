# -*- coding: utf-8 -*-
"""
Created on Mon May 04 20:03:21 2015

@author: Jonathan Gerrand
"""

import socket
import pickle
import threading 

"""Data containers"""
#A dictionary maintained by the indexing server
peer_dict = {}
#Structure for holding commands and arguments
command_list = []
#Name of the peer for this session
user_name = "Jon"
#The current IP address of the user
user_IP_address = "127.0.0.1"
#The message buffer size
BUFFER_SIZE = 10240
#A counter tracking the ports currently used
port_count = [5006]
#A dictionary containing the names of all peers currently on a channel.
#This container is only shared with trusted peers
channel_dict = {}
#Container of current channels hosted by peer
channel_names = {}
#Container of all current channel users
channel_users = []
#Container of all current channel text
channel_text = {}
#Container of all outward connections for a channel
channel_connections = {}


"""------------------------Private functions--------------------------------"""

def _create_listening_connection(channel_name, password, peer_nik):
    #connection variables
    _connection_command = None
    _trusted_address = None
    channel_connections[channel_name] = []
    try:
        listen_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_connection.bind((user_IP_address, port_count[0]))
    finally:
        #Update the channel dict
        channel_dict[channel_name] = []
        #channel_dict: peer_nik, IP addr, port
        channel_dict[channel_name].append([peer_nik, user_IP_address, 
                                           port_count[0]])
        port_count[0] += 1
        
        while 1:
            listen_connection.listen(3)
            #Check incoming message
            conn, addr = listen_connection.accept()
            
            if conn != None:
                _connection_command = pickle.loads(conn.recv(BUFFER_SIZE))
                
                #The trusted peer sends a message
                if _trusted_address == addr:
                    channel_text[channel_name].append(_connection_command[0])
                
                #The correct peer has responded
                #_connection_command: password, IP addr, port, peer_nik
                if _connection_command[0] == password:
                    _trusted_address = addr
                    #Create an outward connection to peer
                    try:
                        out_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        out_conn.connect((_connection_command[1], _connection_command[2]))
                    finally:
                        #Update the channel dict
                        channel_dict[channel_name].append([_connection_command[3],
                                                          _connection_command[1],
                                                          _connection_command[2]])
                        #Store this connection in channel_connections dict.
                        channel_connections[channel_name].append(out_conn)
                        channel_text[channel_name].append(_connection_command[3] + 
                                                          "Joined the channel.")
    pass


def _launch_channel_manager(name, password, peer_nik):
    #channel variables
    _channel_name = name
    _channel_command = None
    
    try:
        #Create channel server (TCP)
        channel_manager = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        channel_manager.bind((user_IP_address, port_count[0]))
        channel_names[name] = [user_IP_address, port_count[0]]
        port_count[0] += 1 #increment used ports
        
        #Launch listening connection on a thread.
        #Channel_dict is updated herein.
        threading.Thread(target=_create_listening_connection,args=(name,),
                         kwargs={'password':password, 'peer_nik': peer_nik}).start()
        
    finally:
        #If binding was successful       
        #Prepare connections container to hold new conns
        channel_connections[name] = []
        #Add hosting peer to the list of people on the chat
        channel_users.append(user_name)
        #Create an entry for this channels text and add initial line        
        channel_text[name] = []
        channel_text[name].append("== " + user_name + " Created: '"+ 
                                  name +"' ===" )
    
    #Wait for peers to chat
    while 1:
        channel_manager.listen(1)
        #Check connection        
        conn, addr = channel_manager.accept()
        
        if conn != None:
            #De-serialize incomming message
            _channel_command = pickle.loads(conn.recv(BUFFER_SIZE))
            
            #--Evaluate command--
            #Command structure - command, channel_name, peer's name
            if (_channel_command[0] == "JOIN") and (_channel_command[1] == _channel_name):
               #Successful -> Must make decision to let peer join!!
               _reply_command = []
               _reply_command.append("PASS")
               _reply_command.append(password)
               _reply_command.append(channel_dict)
               conn.send(pickle.dumps(_reply_command))
               pass
                
                
            if _channel_command[0] == "LISTUSERS":
                #Send channel user container
                conn.send(pickle.dumps(channel_users))
                pass
        
        
     
        
        
        
        
        
        
        
        
        
        
        
        
        
        