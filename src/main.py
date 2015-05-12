__authors__ = "Daniel Holmes 551240 and Jonathan Gerrand 349361"

"""Imports"""
import socket
import pickle
import threading 

"""Constants"""

#The message buffer size
BUFFER_SIZE = 10240

"""Data containers"""
#The type of protocal that will be used, either TCP or UDP
protocol = ""
#Name of the peer for this session
user_name = "Test_run_user" # changed from "Jon"
#The current IP address of the user
user_IP_address = "127.0.0.1" # changed from 127.0.0.1
#A counter tracking the ports currently used
port_count = [5005]

#A dictionary maintained by the indexing server
#key: peer, ip address
peers_online = {} #changed from peer_dict

#A dictionary containing the names of all peers currently on a channel.
#This container is only shared with trusted peers
#key: channel, list: peers
channel_dict = {}

#Container of current channels hosted by user
#key: channel, list: peers and ports
hosted_channels = {} # changed from channel_names

#Container of all current channel peers
#key: channel, list: peers
channel_peers = {} # changed from channel_users as a list of lists

#Container of all current channel text, dictionary of lists
#key: channel, list: text
channel_text = {}

#Container of all outward connections for a channel
#key: channel, list: connection objects
channel_connections = {}

#Known channels hosted by other peers available for connection, dictionary of lists
#key: peer, list: channels
available_channels = {}

#Join requests for channels hosted by the user
#key: channel list: peers requesting
join_requests = {}

#All channel chat
#key: channel list: chat 
channel_chat = {}

def display_welcome_message():
	print "Welcome to the P2P Chat Application!"
	print "Created by Jonathan Gerrand and Daniel Holmes."
	print "2015"
	print ""
	pass

def process_command(command):
	command_array = command.split()

	base_command = command_array[0]

	if base_command == "msg": #Abbreviated as this command is used often
		if len(command_array) < 2: #If there are not enough arguments
			print_arguments_error()
			return
		else:
			channel = command_array[1]
			if connected_to_channel(channel):
				message = raw_input("Message: ")
				send_channel_message(channel, message)
				print "Sent", message, "to", channel
			else:
				return

	elif base_command == "pvt": #Abbreviated as this command is used often
		if len(command_array) < 3:
			print_arguments_error()
			return
		else:
			channel = command_array[1]
			peer = command_array[2]
			if connected_to_channel(channel):
				if peer_on_channel(channel, peer):
					message = raw_input("Message: ")
					send_private_message(channel, peer, message)
					print "Sent", message, "as private message to", peer, "on", channel
				else:
					return
			else:
				return

	elif base_command == "file":
		if len(command_array) !=  3:
			print_arguments_error()
			return
		else:
			channel = command_array[1]
			peer = command_array[2]
			if connected_to_channel(channel):
				if peer_on_channel(channel, peer):
					path_to_file = raw_input("File path: ")
					send_file(channel, peer, path_to_file)
					print "Sent file from", path_to_file, "to", peer, "on channel"
				else:
					return
			else:
				return

	elif base_command == "chat":
		if len(command_array) != 2:
			print_arguments_error()
			return
		else:
			channel = command_array[1]
			if connected_to_channel(channel):
				show_channel_chat(channel)
				print "Displaying chat messages from channel", channel
			else:
				return

	elif base_command == "create":
		if len(command_array) != 4:
			print_arguments_error()
			return
		else:
			channel = command_array[1]
			password = command_array[2]
			nick_name = command_array[3]
			if not hosting_channel(channel):
				create_channel(channel, password, nick_name)
				print "Created", channel, "as a new channel with", password, "as the password and nick", nick_name
			else:
				return

	elif base_command == "join":
		if len(command_array) != 4:
			print_arguments_error()
			return
		else:
			channel = command_array[1]
			peer = command_array[2]
			nick_name = command_array[3]
			if channel_available(channel, peer):
				join_channel(channel, peer, nick_name)
				print "Joined channel", channel, "with nickname", nick_name 
			else:
				return

	elif base_command == "channels":
		if len(command_array) != 2:
			print_arguments_error()
			return
		else:
			peer = command_array[1]
			if peer_online(peer):
				show_peer_channels(peer)
				print "Got list of channels hosted by peer", peer 
			else:
				return

	elif base_command == "peers":
		if len(command_array) != 2:
			print_arguments_error()
			return
		else:
			channel = command_array[1]
			if connected_to_channel(channel):
				show_channel_peers(channel)
				print "Got list of peers on channel", channel
			else:
				return

	elif base_command == "leave":
		if len(command_array) != 2:
			print_arguments_error()
			return
		else:
			channel = command_array[1]
			if connected_to_channel(channel):
				leave_channel(channel)
				print "Left channel", channel
			else:
				return

	elif base_command == "requests":
		if len(command_array) != 2:
			print_arguments_error()
			return
		else:
			channel = command_array[1]
			if hosting_channel(channel):
				if join_request_exists(channel):
					show_join_requests(channel)
					print "Displaying join requests for channel", channel
				else:
					return
			else:
				return

	elif base_command == "accept":
		if len(command_array) != 3:
			print_arguments_error()
			return
		else:
			channel = command_array[1]
			peer = command_array[2]
			if hosting_channel(channel):
				if join_request_exists(channel):
					if peer_requesting(channel, peer):
						accept_join_request(channel, peer)
						print "Accepted join request from", peer, "for channel", channel
					else:
						return
				else:
					return
			else:
				return

	elif base_command == "hosting":
		if len(command_array) != 1:
			print_arguments_error()
			return
		else:
			if hosting_channels():
				show_hosting_channels()
				print "Displaying hosted channels"
			else:
				return

	elif base_command == "online":
		if len(command_array) != 1:
			print_arguments_error()
			return
		else:
			if any_peers_online():
				show_online_peers()
				print "Displaying peers online"
			else:
				return

	elif base_command == "exit":
		if len(command_array) != 1:
			print_arguments_error()
		exit_application()

	elif base_command == "help":
		show_help()

	else:
		print_command_error()

############# Functions with threading ######################

def send_channel_message(channel, message):
    _write_text_to_channel(channel, message)
    pass
#TODO command
def send_private_message(channel, peer, message):
	pass
#TODO command
def send_file(channel, peer, path_to_file):
	pass

def create_channel(channel, password, nick_name):
    try:
         threading.Thread(target=_launch_channel_manager, args=(channel,),
                          kwargs = {'password':password, 
                          'user_nik':nick_name}).start()
    finally:
         print ("Created *"+channel+"* as a new channel with '"+password+
                "' as the password.") 
    pass

def join_channel(channel, peer, nick_name):
    _join_channel(channel, nick_name)
    pass

#TODO command
def leave_channel(channel):
	pass
#TODO command... will probably have to be internal to the thread already
def accept_join_request(channel, peer):
	pass

############################################################

################ Background functions ######################

"""Used to log the user presence with the tracking server
   as well as starting the user global listner.
   """
def _initilize_user(user_name, protocol):
    #Launch user global listner
    threading.Thread(target=_launch_user_global_listner, args=()).start()   
    #Update peer dict
    _update_contacts(user_name)
    pass

"""Creates the user listening server in a thread process"""
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
                
            #Server attempts to update peers_online
            if _recieved_command[0] == "UPDATE":
                global peers_online
                peers_online = _recieved_command[1] 
            #Fellow peer seeks channel list from user
            if _recieved_command[0] == "LISTCH":
                _returned_command = []
                _returned_command.append(hosted_channels)
                conn.send(pickle.dumps(_returned_command))
    pass

"""Inform all peers on network of having joined the channel"""
def _create_connection_to_listner(channel_name, peer_IP_address, 
                                  peer_port_num, send_command):
                                      
    peer_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        peer_con.connect((peer_IP_address, peer_port_num))
        peer_con.send(pickle.dumps(send_command))
    finally:
        print "Connection in channel - "+channel_name+" succesful!"
    pass

"""Create unique listening connection for a specific channel for the 
   peer. Each channel will have its own single listening connection 
   through which the user is able to recieve all channel chat text.
   """
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
                                           port_count[0],user_name])
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
                #_connection_command: password, IP addr, port, peer_nik, user_name
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
                            [_connection_command[1],_connection_command[2]], 
                            _connection_command[4])
                                                          
                        #Record the new peer on the channel
                        channel_text[channel_name].append(_connection_command[3] +
                                                          "("+_connection_command[4]+")"
                                                          " Joined the channel.")                 
    pass

"""This method launches a thread containing a server to which all initial 
   peer join requests for the channel are sent. The channel manager maintains
   the channel dictionary and is responsible for it's distribution throughout 
   all users currently on the channel"""
def _launch_channel_manager(name, password, user_nik):
    #channel variables
    _channel_command = None
    #Update the channel dict
    channel_dict[name] = []
    
    try:
        #Create channel server (TCP)
        channel_manager = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        channel_manager.bind((user_IP_address, port_count[0]))
        hosted_channels[name] = [user_IP_address, port_count[0]]
        port_count[0] += 1 #increment used ports
        
        #Launch listening connection on a thread.
        #Channel_dict is updated herein.
        threading.Thread(target=_create_listening_connection,args=(name,),
                         kwargs={'password':password, 'user_nik': user_nik}).start()
        
    finally:
        #If binding was successful       
        #Add hosting peer to the list of people on the chat
        channel_peers[name] = []
        channel_peers[name].append(user_name)
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
                conn.send(pickle.dumps(channel_peers[name]))
                pass
            
"""This is the initializing method used to call the tracking server, alerting it
   of the users presence online"""
def _update_contacts(name):
    command_list = []
    command_list.append("HELO")
    command_list.append(name)
    updating_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #This was set for the default LAN network
    updating_connection.connect(("127.0.0.1", 5001))
    updating_connection.send(pickle.dumps(command_list))
    
    global peers_online
    while len(peers_online) == 0:
        try:
            peers_online = pickle.loads(updating_connection.recv(BUFFER_SIZE))
        except EOFError:
            #Pickle receives an empty string, reload            
            pass 
    
    #Testing    
    print peers_online

    updating_connection.close()
    pass

""" Send the protocol 'LISTCH' message to the global listening port 
    of a peer and accordingly updates the channels he/she is hosting""" 
def _retrieve_peer_channels(peer_name):
    #Fill message container to request channel users
    _send_message = []
    _send_message.append("LISTCH")
    #Container for recieved hosted channels
    _peer_hosted_channels = []
    
    #Create connection for channel request
    query_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Using user global listening port
    query_connection.connect((peers_online[peer_name], 5000))
    query_connection.send(pickle.dumps(_send_message))
    
    #Wait for peer reply
    while len(_peer_hosted_channels == 0):
        try:
            _peer_hosted_channels = pickle.loads(query_connection.recv(BUFFER_SIZE))
        except EOFError:
            pass
    
    #Fill the availible channels container with the received data.
    global available_channels
    available_channels[peer_name] = _peer_hosted_channels

    pass

"""This method is used by the peer to join an existing channel hosted by another
   peer"""
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
        join_conn.connect((hosted_channels[channel_name][0], hosted_channels[channel_name][1]))
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
    _senf_command.append(user_name)
    for peer in _contact_dictionary:
        #Create connection to peer
        _create_connection_to_listner(channel_name, peer[0], 
                                      peer[1], _send_command)

    pass

"""This is a thread which is responsible for delivering the text argument
   to all peers listed within a given channel."""
def _launch_message_send(channel_name, text):
    #Fill message container to send text to a channel
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

"""Create a thread which will send a single private message to a peer who
    is on the same channel as the user"""
def _launch_private_message_send(channel_name, peer_name, text):
    #Fill message container to send text to a peer
    _send_message = []
    _send_message.append(text)
    
    #Iterate through channel to find correct user to send message to 
    for peer in channel_dict[channel_name]:
        if peer[2] == peer_name:
            message_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            message_connection.connect((peer[0],peer[1]))
            message_connection.send(pickle.dumps(_send_message))            
            #Test 
            print "All messages sent" 
            break
    pass

"""Write given text to a single peer on the network"""
def _write_text_to_peer(channel_name, peer_name, text):
    pass

"""Write given text to a specific channel"""
def _write_text_to_channel(channel_name, text):
    #Launch a thread to perform writing opperation to all peers in channel
    threading.Thread(target=_launch_message_send, args=(channel_name,),
                     kwargs={'text':text}).start() 
    pass

############################################################

# perhaps add a command so show all channels that the user is hosting

def show_channel_chat(channel):
	chat = channel_chat[channel]
	print "Chat for channel", channel
	for c in chat:
		print c
	pass

def show_peer_channels(peer):
	channels = available_channels[peer]
	print "Channels hosted by", peer
	for c in channels:
		print c
	pass

def show_channel_peers(channel):
	peers = channel_peers[channel]
	print "Peers on channel", channel, ":"
	for p in peers:
		print p	
	pass

def show_join_requests(channel):
	requesting_peers =  join_requests[channel]
	print "Join requests for channel", channel, ":"
	for r in requesting_peers:
		print r
	pass

def show_online_peers():
	peers = peers_online.keys()
	print "Peers online:"
	for p in peers:
		print p
	pass

def show_hosting_channels():
	channels = hosted_channels.keys()
	print "Hosting channels:"
	for c in channels:
		print c
	pass

def exit_application():
	"""Close connections, threads, etc ..."""
	exit()
	pass

def show_help():
	print "P2P Chat Application command help."
	print ""
	print "help:\t\t\t\tthis help"
	print "show which peers are online:\tonline"
	print "send message on channel:\tmsg [channel]"
	print "send private message:\t\tpvt [channel] [peer]"
	print "send a file:\t\t\tfile [channel] [peer]"
	print "display channel chat:\t\tchat [channel]"
	print "create a new channel:\t\tcreate [channel name] [password] [nickname]"
	print "join a channel:\t\t\tjoin [channel] [peer host] [nickname]"
	print "show channels hosted by peer:\tchannels [peer]"
	print "show channels you are hosting:\thosting"
	print "show peers on a channel:\t\tpeers [channel]"
	print "show channel join requests:\trequests [channel]"
	print "accept channel join request:\taccept [channel] [peer]"
	print "leave a channel:\t\tleave [channel]"
	print "close the application:\t\texit"
	print "" 

################# Validation and Error checking ####################

def connected_to_channel(channel):
	if channel in channel_connections.keys():
		return True
	else:
		print "Error: not connected to channel", channel 
		return False

def channel_available(channel, peer):
	if peer in available_channels.keys():
		channels = available_channels[peer]
		if channel in channels:
			return True
		else:
			print "Error:", peer, "is not hosting channel", channel
			return False
	else:
		print "Error:", peer, "is not hosing any channels"
		return False

def hosting_channel(channel):
	if channel in hosted_channels.keys():
		return True
	else:
		print "Not currently hosting channel", channel
		return False

def hosting_channels():
	if hosted_channels:
		return True
	else:
		print "Not hosting any channels."
		return False

def join_request_exists(channel):
	requests = join_requests[channel]
	if len(requests) != 0:
		return True
	else:
		print "No requests for channel", channel
		return False

def peer_requesting(channel, peer):
	requests = join_requests[channel]
	if peer in requests:
		return True
	else:
		print peer, "has not requested to join channel", channel
		return False

def peer_on_channel(channel, peer):
	if peer in channel_peers[channel]:
		return True
	else:
		print "Error:", peer, "is not on channel", channel
		return False


def any_peers_online():
	if peers_online:
		return True
	else:
		print "No peers online"
		return False	

def peer_online(peer):
	if peer in peers_online.keys():
		return True
	else:
		print "Error:", peer, "is not online"

def print_arguments_error():
	print "Error: invalid command arguments"
	print 'For list of commands and arguments, type "help"'

def print_command_error():
	print "Error: command not recognised."
	print 'For list of commands and arguments, type "help"'
		
####################################################################

display_welcome_message()

user_name = raw_input("Please enter your username: ")
protocol = raw_input("Please eneter your preferred protocol: ")
_initilize_user(user_name,protocol)
print 'Type "help" for more information'
print ""

while (1):
	command = raw_input(user_name + "@chat-cmd-> ")
	process_command(command)
