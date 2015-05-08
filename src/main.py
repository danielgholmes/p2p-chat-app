__authors__ = "Daniel Holmes 551240 and Jonathan Gerrand 349361"

"""Constants"""

#The message buffer size
BUFFER_SIZE = 10240

"""Data containers"""
#The type of protocal that will be used, either TCP or UDP
protocol = ""
#Name of the peer for this session
user_name = "" # changed from "Jon"
#The current IP address of the user
user_IP_address = "" # changed from 127.0.0.1
#A counter tracking the ports currently used
port_count = [5006]

#A dictionary maintained by the indexing server
#key: peer, ip address
peers_online = {'Bob': '0.0.0.0'} #changed from peer_dict

#A dictionary containing the names of all peers currently on a channel.
#This container is only shared with trusted peers
#key: channel, list: peers
channel_dict = {}

#Container of current channels hosted by user
#key: channel, list: peers and ports
hosted_channels = {'ble': ["Bob", "Ralph"]} # changed from channel_names

#Container of all current channel peers
#key: channel, list: peers
channel_peers = {'bla': ["Bob", "Ralph"]} # changed from channel_users as a list of lists

#Container of all current channel text, dictionary of lists
#key: channel, list: text
channel_text = {}

#Container of all outward connections for a channel
#key: channel, list: connection objects
channel_connections = {'bla': []}

#Known channels hosted by other peers available for connection, dictionary of lists
#key: peer, list: channels
available_channels = {'Bob': ['channel1', 'channel2']}

#Join requests for channels hosted by the user
#key: channel list: peers requesting
join_requests = {'ble': ['Bob', 'Ralph']}

#All channel chat
#key: channel list: chat 
channel_chat = {'bla': ["Bob: Hello Ralph!", "Ralph: Hello Bob!"]}

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
			print_usage()
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
			print_usage()
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
			print_usage()
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
			print_usage()
			return
		else:
			channel = command_array[1]
			if connected_to_channel(channel):
				display_channel_chat(channel)
				print "Displaying chat messages from channel", channel
			else:
				return

	elif base_command == "create":
		if len(command_array) != 4:
			print_usage()
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
			print_usage()
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
			print_usage()
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
			print_usage()
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
			print_usage()
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
			print_usage()
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
			print_usage()
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

	elif base_command == "online":
		show_online_peers()

	elif base_command == "exit":
		exit_application()

	elif base_command == "help":
		print_usage()

	else:
		print_command_error()
		print_usage()

############# Functions with threading ######################

def send_channel_message(channel, message):
	pass

def send_private_message(channel, peer, message):
	pass
	
def send_file(channel, peer, path_to_file):
	pass

def create_channel(channel, password, nick_name):
	pass

def join_channel(channel, peer, nick_name):
	pass

def leave_channel(channel):
	pass

def accept_join_request(channel, peer):
	pass

############################################################

def display_channel_chat(channel):
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

def exit_application():
	"""Close connections, threads, etc ..."""
	exit()
	pass

def print_usage():
	print "P2P Chat Application command usage."
	print ""
	print "help:\t\t\t\tthis help"
	print "see which peers are online:\tonline"
	print "send message on channel:\tmsg [channel]"
	print "send private message:\t\tpvt [channel] [peer]"
	print "send a file:\t\t\tfile [channel] [peer]"
	print "display channel chat:\t\tchat [channel]"
	print "create a new channel:\t\tcreate [channel name] [password] [nickname]"
	print "join a channel:\t\t\tjoin [channel] [peer host] [nickname]"
	print "see channels hosted by peer:\tchannels [peer]"
	print "see peers on a channel:\t\tpeers [channel]"
	print "see channel join requests:\trequests [channel]"
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

def peer_online(peer):
	if peer in peers_online.keys():
		return True
	else:
		print "Error:", peer, "is not online"

def print_command_error():
	print "Error: command not recognised."
		
####################################################################

display_welcome_message()

user_name = raw_input("Please enter your username: ")
protocol = raw_input("Please eneter your preferred protocol: ")
print ""

while (1):
	command = raw_input(user_name + "@chat-cmd-> ")
	process_command(command)
