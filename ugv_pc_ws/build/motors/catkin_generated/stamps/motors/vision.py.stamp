import rospy
import cv2
import sys
from sensor_msgs.msg import Image
from cv_bridge import CvBridge ,CvBridgeError
# --------------------------------------------------------------------
bridge = CvBridge()
# --------------------------------------------------------------------
def image_callback(ros_image):
    global bridge
    try:
        cv_image = bridge.imgmsg_to_cv2(ros_image,'bgr8')
    except CvBridgeError as e:
        print(e)
    
    cv2.imshow('image',cv_image)
    cv2.waitKey(3)
# ---------------------------------------------------------------------
def main(*args):
    rospy.init_node('vision',anonymous=False)
    sub =rospy.Subscriber('usb_cam/image_raw',Image,image_callback)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()
# --------------------------------------------------------------------
if __name__ == '__main__': #start nod
    main(sys.argv)  


