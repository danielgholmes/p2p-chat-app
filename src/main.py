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
peers_online = {} #changed from peer_dict

#A dictionary containing the names of all peers currently on a channel.
#This container is only shared with trusted peers
#key: channel, list: peers
channel_dict = {}

#Container of current channels hosted by user
#key: channel, list: peers and ports
hosted_channel_names = {} # changed from channel_names

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
available_channels = {}

#Join requests for channels hosted by the user
#key: channel list: peers requesting
join_requests = {}

def display_welcome_message():
	print "=============================================="
	print "Welcome to the P2P Chat Application!"
	print "Created by Jonathan Gerrand and Daniel Holmes."
	print "2015"
	print "=============================================="
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
			if connected_to_channel(channel):
				peer = command_array[2]
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
			if connected_to_channel(channel):
				peer = command_array[2]
				if peer_on_channel(channel, peer):
					path_to_file = raw_input("File path: ")
					send_file(channel, peer, path_to_file)
					print "Sent file from", path, "to", peer, "on channel"
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
			create_channel(channel, password, nick_name)
			print "Created", channel, "as a new channel with", password, "as the password"


	elif base_command == "join":
		if len(command_array) != 4:
			print_usage()
			return
		else:
			channel = command_array[1]
			if channel_available(channel, peer):
				nick_name = command_array[2]
				join_channel(channel, nick_name)
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
				get_peer_channels(peer)
				print "Got list of channels hosted by peer", peer 
			else:
				return

	elif base_command == "peers":
		if len(command_array) != 2:
			print_usage()
			return
		else:
			channels = command_array[1]
			if connected_to_channel(channel):
				get_channel_peers(channel)
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
			if hosting_channel(channel):
				if join_requests(channel):
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
			if hosting_channel(channel):
				if join_requests(channel):
					peer = command_array[2]
					if peer_requesting(peer):
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

	else:
		print_command_error()

def send_channel_message(channel, message):
	pass

def send_private_message(channel, peer, message):
	pass
	
def send_file(channel, peer, path_to_file):
	pass

def display_channel_chat(channel):
	pass

def create_channel(channel, password, nick_name):
	pass

def join_channel(channel, peer, nick_name):
	pass

def get_peer_channels(peer):
	pass

def get_channel_peers(channel):
	pass

def leave_channel(channel):
	pass

def show_join_requests(channel):
	pass

def accept_join_request(channel, peer):
	pass

def show_online_peers():
	print "The following peers are online:"
	pass

def exit_application():
	"""Close connections, threads, etc ..."""
	exit()
	pass

def print_usage():
	print "help..."

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
			return False
	else:
		return False

def hosting_channel(channel):
	if channel in join_requests.keys():
		return True
	else:
		print "Not hosting channel", channel
		return False

def join_requests(channel):
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
	if peer in peer_online.keys():
		return True
	else:
		print "Error:", peer, "is not online"

def print_command_error():
	print "Error: command not recognised."
		
####################################################################

display_welcome_message()

user_name = raw_input("Please enter your username: ")
protocol = raw_input("Please eneter your preferred protocol: ")

while (1):
	command = raw_input("-> ")
	process_command(command)
