from future.backports.socket import socket
from sqlalchemy.sql.functions import user

__authors__ = 'Daniel Holmes 551240 and Jonathan Gerrand 349361'

import socket
import pickle

userIPList = {}

tracServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tracServer.bind(("127.0.0.1",5005))
i = 1
while(1):

    tracServer.listen(1)

    conn, addr = tracServer.accept()
    if conn is not None:
        i += 1
        print conn.recv(1024)
        userIPList[i] = addr
        conn.send(pickle.dumps(userIPList))
        conn.close()
        pass





