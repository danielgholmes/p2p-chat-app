__authors__ = "Daniel Holmes 551240 and Jonathan Gerrand 349361"

USER_NAME = ""
PROTOCOL = ""
CHANNELS = []

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
	command_args = command_array[1:]

	"""Abbreviated because these will be typed more often."""
	if base_command == "msg": 
		m = command_array[2:]
		message = " ".join(str(x) for x in m) 
		send_channel_message(command_array[1], message)

	elif base_command == "pvt":
		m = command_array[3:]
		message = " ".join(str(x) for x in m) 
		send_private_message(command_array[1], command_array[2], message)

	elif base_command == "file":
		send_file(command_array[1], command_array[2], command_array[3])

	elif base_command == "chat":
		display_channel_chat(command_array[1])

	elif base_command == "create":
		create_channel(command_array[1], command_array[2])

	elif base_command == "join":
		join_channel(command_array[1], command_array[2])

	elif base_command == "channels":
		get_peer_channels(command_array[1])

	elif base_command == "users":
		get_channel_peers(command_array[1])

	elif base_command == "leave":
		leave_channel(command_array[1])

	elif base_command == "requests":
		check_join_requests(command_array[1])

	elif base_command == "online":
		check_online_peers()

	elif base_command == "exit":
		exit_application()

	else:
		print_command_error()

	pass

def send_channel_message(channel, message):
	print "Sent", message, "to", channel
	pass

def send_private_message(channel, peer, message):
	print "Sent", message, "as private message to", peer, "on", channel
	pass

def send_file(channel, peer, path_to_file):
	print "Sending file at", path_to_file, "to", peer, "on channel", channel
	pass

def display_channel_chat(channel):
	print "Displaying chat messages from channel", channel
	pass

def create_channel(channel, password):
	print "Created", channel, "as a new channel with", password, "as the password"
	pass

def join_channel(channel, nick_name):
	print "Joined channel", channel, "with nickname", nick_name 
	pass

def get_peer_channels(peer):
	print "Got list of channels hosted by peer", peer 
	pass

def get_channel_peers(channel):
	print "Got list of peers on channel", channel
	pass

def leave_channel(channel):
	print "Left channel", channel
	pass

def check_join_requests(channel):
	print "Checked join requests for channel", channel
	pass

def check_online_peers():
	print "The following peers are online:"
	pass

def exit_application():
	"""Close connections, threads, etc ..."""
	exit()
	pass

def print_command_error():
	print "Error: command not recognised."

display_welcome_message()

USER_NAME = raw_input("Please enter your username: ")
PROTOCOL = raw_input("Please eneter your preferred protocol: ")

while (1):
	command = raw_input("-> ")
	process_command(command)
