#!/usr/bin/env python3
import rospy 
from sensor_msgs.msg import Image
from cv_bridge import CvBridge , CvBridgeError
import cv2
import pytesseract
import numpy as np
import time
# -------------------------------------------------
# function of stack images together (external function from internet) 
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
# -------------------------------------------------
def callback(msg):
    print('receive frame\n')
    br = CvBridge()

    try:
        frame = br.imgmsg_to_cv2(msg,"bgr8")
    except CvBridgeError as e:
        print(e)


    # blur the frame to reduce high frequency noise 
    blur_frame = cv2.GaussianBlur(frame, (11, 11), 0)

    # make it gray
    gray = cv2.cvtColor(blur_frame,cv2.COLOR_BGR2GRAY)

    # make it black and white by THRESH_BINARY
    ret,thresh = cv2.threshold(gray,220,255,cv2.THRESH_BINARY)
    
    # to remove any small blobs that may be left on the mask
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # use pytesseract to exctrct the strings inside frames    
    config = r'--oem 3 --psm 6 outputbase digits'
    boxes = pytesseract.image_to_data(thresh,lang='eng',config=config)

    for x,b in enumerate(boxes.splitlines()):
            if x != 0:
                b = b.split()
                if len(b) == 12:
                    if int(b[10]) > 90:
                        x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
                        cv2.putText(frame,b[11],(x,y),fontFace=cv2.FONT_HERSHEY_DUPLEX,thickness=3,color=(0,255,0),lineType=cv2.FILLED,fontScale=3)
                        print('\n')
                        print('accuracy: {}'.format(int(b[10])))
                        print('numbers: {}'.format(int(b[11])))

    # stacj the image together
    imgStack = stackImages(0.4,([frame,thresh]))


    # display original & mask & res of frame
    cv2.imshow("Image",imgStack)


    # exit button
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


# -------------------------------------------------
def subscrib_message():
    rospy.init_node('detect_numbers',anonymous=False)
    rospy.Subscriber("video_frames",Image,callback)
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print('not working')
    
    cv2.destroyAllWindows()
# -------------------------------------------------
if __name__ == '__main__':
    subscrib_message()