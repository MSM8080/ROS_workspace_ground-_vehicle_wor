#! /usr/bin/env python3 
import rospy                    # for python
import pickle                   # for convert to binary
import socket             # for send data on server
from sensor_msgs.msg import Joy # message type : joystic data
# -------------------------------------------------------------------------------------
ip = '192.168.1.11'                      # ip of raspberry pi
port = 5050                               # port of send code programme
s_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #UDP
# -------------------------------------------------------------------------------------
def callback(msg):
    global ip
    global port
    try:
        print(msg)
        msg = pickle.dumps(msg)
        s_socket.sendto(msg,(ip,port))
        
    except:    
        print('error') 
# -------------------------------------------------------------------------------------
# subscriber function
def listener(): 
    rospy.init_node('turtle_joy',anonymous=False) # intilize the supscriber nose
    rospy.Subscriber("joy",Joy,callback)          # subscripe to joy topic
    rospy.spin()                                  # work until node is shutdown
# -------------------------------------------------------------------------------------
if __name__ == '__main__': #start nod
    listener()             # do listener function

