#!/usr/bin/env python3
import rospy 
from sensor_msgs.msg import Image
from cv_bridge import CvBridge , CvBridgeError
import cv2
import numpy as np

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

# action of trackbar function
def nothing(x):
    pass
# -------------------------------------------------
# create tracks windows
cv2.namedWindow('tracks_HSV')
cv2.namedWindow('tracks_blobs')

# creat tracks of blob params Circularity,Convexity,Area,Inertia Ratio 
cv2.createTrackbar('LCI','tracks_blobs',0,100,nothing) # lower Circularity
cv2.createTrackbar('UCI','tracks_blobs',0,100,nothing) # upper Circularity
cv2.createTrackbar('LA','tracks_blobs',1,800000,nothing) # lower Area
cv2.createTrackbar('UA','tracks_blobs',1,800000,nothing) # upper Area
cv2.createTrackbar('LIR','tracks_blobs',0,100,nothing) # lower Inertia Ratio
cv2.createTrackbar('UIR','tracks_blobs',0,100,nothing) # upper Inertia Ratio


# creat tracks of hue,saturation,value
cv2.createTrackbar('LH','tracks_HSV',0,255,nothing) # lower hue
cv2.createTrackbar('UH','tracks_HSV',0,255,nothing) # upper hue
cv2.createTrackbar('LS','tracks_HSV',0,255,nothing) # lower saturation
cv2.createTrackbar('US','tracks_HSV',0,255,nothing) # upper saturation
cv2.createTrackbar('LV','tracks_HSV',0,255,nothing) # lower value
cv2.createTrackbar('UV','tracks_HSV',0,255,nothing) # upper value
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

    # change system of coloring to HSV (hue,saturatiom,value)
    hsv_frame = cv2.cvtColor(blur_frame,cv2.COLOR_BGR2HSV)

    # get values for Circularity,Convexity,Area,Inertia Ratio
    lci = cv2.getTrackbarPos('LCI','tracks_blobs') # lower Circularity 
    uci = cv2.getTrackbarPos('UCI','tracks_blobs') # upper Circularity
    la = cv2.getTrackbarPos('LA','tracks_blobs') # lower Area
    ua = cv2.getTrackbarPos('UA','tracks_blobs') # upper Area
    lir = cv2.getTrackbarPos('LIR','tracks_blobs') # lower Inertia Ratio
    uir = cv2.getTrackbarPos('UIR','tracks_blobs') # upper Inertia Ratio

    # get values for hue,saturation,value
    lh = cv2.getTrackbarPos('LH','tracks_HSV') # lower hue
    uh = cv2.getTrackbarPos('UH','tracks_HSV') # upper hue
    ls = cv2.getTrackbarPos('LS','tracks_HSV') # lower saturation
    us = cv2.getTrackbarPos('US','tracks_HSV') # upper saturation
    lv = cv2.getTrackbarPos('LV','tracks_HSV') # lower value
    uv = cv2.getTrackbarPos('UV','tracks_HSV') # upper value

    # define ranges of color 
    lower_color = np.array([lh,ls,lv])
    upper_color = np.array([uh,us,uv])

    # make mask for particular colored objects 
    mask = cv2.inRange(hsv_frame,lower_color,upper_color)

    # to remove any small blobs that may be left on the mask
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # inverting mask by THRESH_BINARY_INV
    ret,thresh = cv2.threshold(mask,127,255,cv2.THRESH_BINARY_INV)

    # mix the mask frame with original frame
    res_frame  = cv2.bitwise_and(frame,frame,mask=mask)

    # creat blob params
    params = cv2.SimpleBlobDetector_Params()
        # Filter by Color (off)
    params.filterByColor = False;
    params.filterByArea = True 
    params.minArea = la
    params.maxArea = ua     
        # Filter by Circularity (on)
    params.filterByCircularity = True 
    params.minCircularity = lci/100
    params.maxCircularity = uci/100
        # Filter by Convexity (on)
    params.filterByConvexity = False  
        # Filter by Inertia Ratio (on) 
    params.filterByInertia =True 
    params.minInertiaRatio = lir/100
    params.maxInertiaRatio = uir/100

    # creat blob detector 
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(thresh)

    # draw circles around blobs
    key_frame_origin = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  
    key_frame_thresh = cv2.drawKeypoints(thresh, keypoints, np.array([]), (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    key_frame_res = cv2.drawKeypoints(res_frame, keypoints, np.array([]), (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    key_frame_mask = cv2.drawKeypoints(mask, keypoints, np.array([]), (0, 0, 255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    try:
        x = keypoints[0].pt[0]
        y = keypoints[0].pt[1]
        print('coordinates: ({},{})'.format(x,y))
    except:
        pass
    # stacj the image together
    imgStack = stackImages(0.5,([key_frame_origin,key_frame_res],[key_frame_mask,key_frame_thresh]))

    # display original & mask & res of frame
    cv2.imshow("ImageStack",imgStack)

    # exit button
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()


# -------------------------------------------------
def subscrib_message():
    rospy.init_node('detect_objects',anonymous=False)
    rospy.Subscriber("video_frames",Image,callback)
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print('not working')
    
    cv2.destroyAllWindows()
# -------------------------------------------------
if __name__ == '__main__':
    subscrib_message()
