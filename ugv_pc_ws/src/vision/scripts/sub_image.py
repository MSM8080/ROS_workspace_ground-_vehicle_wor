#!/usr/bin/env python3
import rospy 
from sensor_msgs.msg import Image
from cv_bridge import CvBridge , CvBridgeError
import matplotlib.pyplot as plt
import cv2
# -------------------------------------------------
def callback(msg):
    print('receive frame\n')
    br = CvBridge()

    try:
        frame = br.imgmsg_to_cv2(msg,"bgr8")
    except CvBridgeError as e:
        print(e)
    cv2.imshow('frame',frame)
    if cv2.waitKey(10) & 0xff == ord('q'):
        cv2.destroyAllWindows()


# -------------------------------------------------
def subscrib_message():
    rospy.init_node('sub_image',anonymous=False)
    rospy.Subscriber("video_frames",Image,callback)
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print('not working')
    
    cv2.destroyAllWindows()
# -------------------------------------------------
if __name__ == '__main__':
    subscrib_message()