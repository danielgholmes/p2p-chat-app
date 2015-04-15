# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 19:36:42 2015

@author: Jonathan Gerrand
"""

from tcp_server import Server

server = Server()

server.listen('127.0.0.1', 5005)