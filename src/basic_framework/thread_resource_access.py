# -*- coding: utf-8 -*-
"""
Created on Mon May 04 17:39:42 2015

@author: Jonathan Gerrand
"""
import threading
import time

my_list = []
thread_list = []
class_list = []
num = 0


# Basic method for thread access to a list
def access_first(num_to_add):
    for i in range(2,20):
        my_list.append(num_to_add)
        time.sleep(0.5)
        print num_to_add
    pass

# See how threads use objects
class dummyClass(object):

    def __init__(self, name):
        self.name = name
        pass
    
    def respond(self):
        return self.name
        pass
    
# Method to create dummy class objects
def create_class(name):
    dum = dummyClass(name)
    class_list.append(dum)
    pass

def inc_int(number_to_inc_by):    
    num = number_to_inc_by

#thread_num1 = threading.Thread(target=inc_int, args=(5,))
#thread_num2 = threading.Thread(target=inc_int, args=(1,))
#
#thread_num1.start()
#thread_num2.start()

#print num

#thread1 = threading.Thread(target=access_first, args=(2,))
#thread2 = threading.Thread(target=access_first, args=(1,))

#class_thread1 = threading.Thread(target=create_class, args=("Billy",))
#class_thread2 = threading.Thread(target=create_class, args=("Bob",))
        
#thread_list.append(thread1)
#thread_list.append(thread2)        
#thread_list.append(class_thread1)
#thread_list.append(class_thread2)
        
#thread1.start()
#thread2.start()
#
#class_thread1.start()
#class_thread2.start()
#
#print my_list
#print threading.active_count
#
#for cls in class_list:
#    print cls.respond()
