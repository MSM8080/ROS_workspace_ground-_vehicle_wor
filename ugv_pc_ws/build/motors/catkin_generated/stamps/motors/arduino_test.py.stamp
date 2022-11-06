# license removed for brevity
#!/usr/bin/env python
# ---------------------------------------------------------
import rospy
from std_msgs.msg import String 
from motors.msg import arduino_motors           
# ---------------------------------------------------------
def servo_node():
    rospy.init_node('servo_node', anonymous=False)
    pub = rospy.Publisher('servo',arduino_motors, queue_size=10)
    rate = rospy.Rate(1)  # 10hz
    msg = arduino_motors()
    
    while not rospy.is_shutdown():
        st1 = input("Enter direction: ") # Right (r) | left (l)
        st2 = input("Enter speed: ") # spedd (0,1,2,3,4)
        msg.direction = str(st1)
        msg.speed = int(st2)
        print(msg)
        pub.publish(msg)
        rate.sleep()
# ---------------------------------------------------------
if __name__ == '__main__':
    try:
        servo_node()
    except rospy.ROSInterruptException:
        pass

