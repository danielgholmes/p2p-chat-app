from future.backports.socket import socket

__authors__ = 'Daniel Holmes 551240 and Jonathan Gerrand 349361'

import socket
import pickle

userIPList = {}

tracServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tracServer.bind(("127.0.0.1",5005))
while(1):

    tracServer.listen(1)

    conn, addr = tracServer.accept()
    
    if conn is not None :
        recv_command_list = pickle.loads(conn.recv(10240))
        if recv_command_list[0] == "HELO":    
            print recv_command_list
            if len(userIPList) != 0:
                conn.send(pickle.dumps(userIPList))
            userIPList[recv_command_list[1]] = addr[0]
            conn.close()
            pass
        
        if recv_command_list[0] == "GOODBYE":
            del userIPList[recv_command_list[1]]
            conn.close()
            pass
        




