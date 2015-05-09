# -*- coding: utf-8 -*-
"""
Created on Mon May 04 20:03:21 2015

@author: Jonathan Gerrand
"""

import socket
import pickle
import threading 
import time

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
"""Data containers end"""


"""------------------------Private functions--------------------------------"""
def _initilize_user(user_name, protocol):
    #Launch user global listner
    threading.Thread(target=_launch_user_global_listner, args=()).start()   
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
            try:
                _recieved_command = pickle.loads(conn.recv(BUFFER_SIZE))
            except EOFError:
                print "Global listner received a blank command."
                
            #Server attempts to update peer_dict
            if _recieved_command[0] == "UPDATE":
                global peer_dict
                peer_dict = _recieved_command[1] 
            #Fellow peer seeks channel list from user
            if _recieved_command[0] == "LISTCH":
                _returned_command = []
                _returned_command.append(channel_names)
                conn.send(pickle.dumps(_returned_command))
    pass

def _create_connection_to_listner(channel_name, peer_IP_address, 
                                  peer_port_num, send_command):
                                      
    peer_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        peer_con.connect((peer_IP_address, peer_port_num))
        peer_con.send(pickle.dumps(send_command))
    finally:
        global channel_connections
        channel_connections[channel_name].append(peer_con)
        print "Connection in channel - "+channel_name+" succesful!"
    pass
            
def _create_listening_connection(channel_name, password, user_nik):
    #connection variables
    _connection_command = None
    _trusted_address = {}

    try:
        listen_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_connection.bind((user_IP_address, port_count[0]))
    finally:
        #channel_dict: IP addr, port
        channel_dict[channel_name].append([user_IP_address, 
                                           port_count[0]])
        port_count[0] += 1
        
        while 1:
            listen_connection.listen(1)
            #Check incoming message
            conn, addr = listen_connection.accept()
            
            if conn != None:
                _connection_command = pickle.loads(conn.recv(BUFFER_SIZE))
                
                #A trusted peer sends a message -> Short validation and save text
                if addr[0] in _trusted_address.keys():
                    global channel_text
                    channel_text[channel_name].append(
                    _trusted_address[addr[0]] + ": " + _connection_command[0])
                    #Test - got into if statement
                    print "recorded text"
                
                #The correct peer has responded
                #_connection_command: password, IP addr, port, peer_nik
                if _connection_command[0] == password:
                    _trusted_address[addr[0]] = _connection_command[3]
                    
                    #Create an outward connection to peer
                    try:
                        out_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        out_conn.connect((_connection_command[1], _connection_command[2]))
                    finally:
                        #Update the channel dict if user is not already recorded
                        found = False
                        for item in channel_dict[channel_name]:
                            if addr[0] in item:
                                found = True
                        #IP address not in the record
                        if found != True:
                            channel_dict[channel_name].append(
                            [_connection_command[1],_connection_command[2]])
                                                          
                        #Store this connection in channel_connections dict.
                        channel_connections[channel_name].append(out_conn)
                        channel_text[channel_name].append(_connection_command[3] + 
                                                          " Joined the channel.")
                        
                        
    pass


def _launch_channel_manager(name, password, user_nik):
    #channel variables
    _channel_command = None
    #Update the channel dict
    channel_dict[name] = []
    
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
            if (_channel_command[0] == "JOIN") and (_channel_command[1] == name):
               #Successful -> Must make decision to let peer join!!
               #TODO Include functionality for a rejection command
               _reply_command = []
               _reply_command.append("PASS")
               _reply_command.append(password)
               _reply_command.append(channel_dict[name])
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
    
    global peer_dict
    while len(peer_dict) == 0:
        try:
            peer_dict = pickle.loads(updating_connection.recv(BUFFER_SIZE))
        except EOFError:
            #Pickle receives an empty string, reload            
            pass 
        
    print peer_dict

    updating_connection.close()
    pass

def _join_channel(channel_name, user_nickname):
    #Channel variables
    _received_channel_password = ""
    _received_command = []
    _send_command = []
    _contact_dictionary = None
    
    #Fill send command structure to send
    _send_command.append("JOIN")
    _send_command.append(channel_name)
    
    #Send request to channel host
    join_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        join_conn.connect((channel_names[channel_name][0], channel_names[channel_name][1]))
    finally:
        join_conn.send(pickle.dumps(_send_command))
        
        #Wait for reply from channel host
        while len(_received_command) == 0:
            try:
                _received_command = pickle.loads(join_conn.recv(BUFFER_SIZE))
            except EOFError:
                #Pickle receives an empty string, reload 
                pass
            
            #Unpack received response
            if _received_command[0] == "PASS":
                _received_channel_password = _received_command[1]
                _contact_dictionary = _received_command[2]
            else: 
                print "Your request to join: " + channel_name + ", has been rejected" 
    
    #Add current connection to the channel connections container
    channel_connections[channel_name].append(join_conn)
                
    #Launch personal listening server thread for the channel
    threading.Thread(target=_create_listening_connection, args=(channel_name,),
                     kwargs={'password':_received_channel_password, 
                     'user_nik':user_nickname}).start()
    
    #Establish connections to all peers in channel
    _send_command = []
    _send_command.append(_received_channel_password)
    _send_command.append(user_IP_address)
    _send_command.append(port_count[0]-1)#Check
    _send_command.append(user_nickname)
    for peer in _contact_dictionary:
        #Create connection to peer
        _create_connection_to_listner(channel_name, peer[0], 
                                      peer[1], _send_command)

    pass

def _launch_message_send(channel_name, text):
    _send_message = []
    _send_message.append(text)
    
    #Send message to all connections
    for peer in channel_dict[channel_name]:
        message_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        message_connection.connect((peer[0],peer[1]))
        message_connection.send(pickle.dumps(_send_message))
    #Test 
    print "All messages sent" 
    pass

def _write_text_to_channel(channel_name, text):
    #Launch a thread to perform writing opperation to all peers in channel
    threading.Thread(target=_launch_message_send, args=(channel_name,),
                     kwargs={'text':text}).start() 
    pass

#TODO functions
def _list_peer_channels(peer_name):
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
         print ("Created *"+channel+"* as a new channel with '"+password+
                "' as the password.") 
     pass
     
"""-------------------------end public functions----------------------------"""
        
        
#Test Code
_initilize_user("Jon", "TCP")
create_channel("TestChan", "easy", "Gerrand")
create_channel("Bobby_channel", "peasy", "David")
_join_channel("TestChan", "squiddle")
_write_text_to_channel("TestChan", "This is a big, fluffy dog :)")
time.sleep(1)
_write_text_to_channel("TestChan", "It is a cute dog.") 
time.sleep(1)      

        
        
        
        
        