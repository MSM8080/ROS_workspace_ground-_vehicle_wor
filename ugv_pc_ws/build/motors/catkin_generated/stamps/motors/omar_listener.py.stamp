#!/usr/bin/env python3
from smbus2 import SMBus,i2c_msg
import rospy
from joystick.msg import custom
def callback(msg):
	old_value=0
	value=""
	if (msg.list_axis[0]>0):
		num=int(msg.list_axis[0]*100)
		if num>=0 && num<=9:
			value="f"+"00"+str(num)
		elif num>=10 && num<=99:
			value="f"+"0"+str(num)
		elif num==100:
			value="f"+str(num)
	elif (msg.list_axis[0]<0):
		num=int(msg.list_axis[0]*-100)
		if num>=0 && num<=9:
			value="b"+"00"+str(num)		
		elif num>=10 && num<=99:
			value="b"+"0"+str(num)
		elif num==100:
			value="b"+str(num)
	elif (msg.list_axis[1]>0):
			num=int(msg.list_axis[0]*100)
		if num>=0 && num<=9:
			value="R"+"00"+str(num)
		elif num>=10 && num<=99:
			value="b"+"0"+str(num)
		elif num==100:
			value="b"+str(num)
	elif (msg.list_axis[1]<0):
			num=int(msg.list_axis[0]*-100)
		if num>=0 && num<=9:
			value="l"+"00"+str(num)
		elif num>=10 && num<=99:
			value="l"+"0"+str(num)
		elif num==100:
			value="l"+str(num)
	elif (msg.list_axis[0]==0 and msg.list_axis[1]==0 and msg.list_axis[2]==0 and msg.list_axis[3]==0):
		print("Stop")
		value="s"+str(msg.list_axis[0]*100)
	elif (msg.list_axis[2]>0):
		num=int(msg.list_axis[0]*100) 
		if num>=0 && num<=9:
			value="x"+"00"+str(num)#rotate right
		elif num>=10 && num<=99:
			value="x"+"0"+str(num)
		elif num==100:
			value="x"+str(num)
	elif (msg.list_axis[2]<0):
		num=int(msg.list_axis[0]*-100) 
		if num>=0 && num<=9:
			value="y"+"00"+str(num)#rotate left
		elif num>=10 && num<=99:
			value="y"+"0"+str(num)
		elif num==100:
			value="y"+str(num)


	elif (old_value<msg.list_axis[3]):
		num=int(msg.list_axis[3]*100)
		if num>=0 && num<=9:
			value="d"+"00"+str(num) #down
			old_value=num
		elif num>=10 && num<=99:
			value="d"+"0"+str(num)
			old_value=num
		elif num==100:
			value="d"+str(num)
			old_value=num 
	elif (old_valu>msg.list_axis[3]):
		num=int(msg.list_axis[0]*100)
		if num>=0 && num<=9:
			value="u"+"00"+str(num) #up
			old_value=num
		elif num>=10 && num<=99:
			value="u"+"0"+str(num)
			old_value=num
		elif num==100:
			value="u"+str(num) 
			old_value=num          
	write=i2c_msg.write(0x20,value)
	bus.i2c_rdwr(write)
def listener():
	rospy.init_node('listener', anonymous=True)

	rospy.Subscriber('joy', custom, callback)       
if __name__ == '__main__':
	listener()
