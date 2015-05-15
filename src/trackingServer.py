__authors__ = 'Daniel Holmes 551240 and Jonathan Gerrand 349361'

import socket
import pickle

userIPList = {}

tracServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Currently set for Jonathan's PC
tracServer.bind(("127.0.0.1",5001))
while(1):

    tracServer.listen(3)

    conn, addr = tracServer.accept()
    
    if conn is not None:
        recv_command_list = pickle.loads(conn.recv(10240))
        if recv_command_list[0] == "HELO":    
            #Update the IP List and send to joining user
            print recv_command_list
            if len(userIPList) != 0:
                conn.send(pickle.dumps(userIPList))
            userIPList[recv_command_list[1]] = addr[0]
            conn.close()
            
            #Send the updated list to all other peers
            _sent_command = []
            _sent_command.append("UPDATE")
            _sent_command.append(userIPList)            
            for user_name in userIPList:
                _update_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                _update_connection.connect((userIPList[user_name], 5000))
                _update_connection.send(pickle.dumps(_sent_command))
                _update_connection.close()
            pass
        
        if recv_command_list[0] == "GOODBYE":
            del userIPList[recv_command_list[1]]
            conn.close()
            pass
        




