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
channel_users = {}
#Container of all current channel text
channel_text = {}
#Container of all outward connections for a channel
channel_connections = {}


"""------------------------Private functions--------------------------------"""
def _initilize_user(user_name, protocol):
    #Launch user global listner
    threading.Thread(target=_launch_user_global_listner, args=()).start   
    #Update peer dict
    _update_contacts(user_name)
    pass

def _launch_user_global_listner():
    _recieved_command = None
    _user_global_listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _user_global_listner.bind((user_IP_address,5000))
    
    while 1:
        #Accept global peer messages
        _user_global_listner.listen(3)
        conn, addr = _user_global_listner.accept()
        
        if conn != None:
            #Process incoming messages
            _recieved_command = pickle.loads(conn.recv(BUFFER_SIZE))
            #Server attempts to update peer_dict
            if _recieved_command[0] == "UPDATE":
                peer_dict = _recieved_command[1] #Hmmm?
            #Fellow peer seeks channel list from user
            if _recieved_command[0] == "LISTCH":
                _returned_command = []
                _returned_command.append(channel_names)
    pass
            
        
        

def _create_listening_connection(channel_name, password, user_nik):
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
        #channel_dict: user_nik, IP addr, port
        channel_dict[channel_name].append([user_nik, user_IP_address, 
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


def _launch_channel_manager(name, password, user_nik):
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
                         kwargs={'password':password, 'user_nik': user_nik}).start()
        
    finally:
        #If binding was successful       
        #Prepare connections container to hold new conns
        channel_connections[name] = []
        #Add hosting peer to the list of people on the chat
        channel_users[name] = []
        channel_users[name].append(user_name)
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
                conn.send(pickle.dumps(channel_users[name]))
                pass
            
def _update_contacts(name):
    command_list = []
    command_list.append("HELO")
    command_list.append(name)
    updating_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #This was set for the default LAN network
    updating_connection.connect(("127.0.0.1", 5001))
    updating_connection.send(pickle.dumps(command_list))

    while (len(peer_dict) == 0):
        peer_dict = pickle.loads(updating_connection.recv(10240))
        
    print peer_dict

    updating_connection.close()
    pass
"""------------------------end private functions----------------------------"""
        
"""-------------------------Public functions--------------------------------"""


def create_channel(channel, password, nick_name):
	#Data Validation goes here!

     try:
         threading.Thread(target=_launch_channel_manager, args=(channel,),
                          kwargs = {'password':password, 
                          'user_nik':nick_name}).start()
     finally:
         print "Created *", channel, "* as a new channel with", password, "as the password" 
     pass
     
"""-------------------------end public functions----------------------------"""
        
        
#Test Code
_initilize_user("Jon", "TCP")
create_channel("TestChan", "easy", "Working")
        
        
        
        
        
        
        
        
        