# import the necessary packages
import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt
from rib_counting import compute_rib_gap

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
isShow = False
global annotated_original_img

#input
img_src = '../data/sample_image/sample_rib8.jpg'

image = cv2.imread(img_src)
image = cv2.resize(image, (0,0), fx=1.0, fy=1.0)
height, width = image.shape[:2]
current_x = 0
current_y = 0

#Trackbar callback function
def onTrackbarChange(trackbarValue):
    global annotated_original_img
    if(isShow):
        annotated_original_img = clone.copy()
        show_count(cv2.EVENT_LBUTTONDOWN, current_x, current_y, True, 0)
    print("Set gap distance = "+str(trackbarValue))

def show_count(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, isShow, annotated_original_img, current_x, current_y
    # annotated_original_img = clone.copy()
    count_width = 15  # The length between the vertebra line and x-position which we count rib
    spacing_height = 4  # the moving down length when annotated the original image
    gap_threshold = 10
    # gap = 17 #get from programming
    gap = cv2.getTrackbarPos('gap', 'RibCounting')
    count = 12
    tmp_height = height
    # if the left mouse button was clicked, start count the first rib from that (x, y) coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        if(isShow):
            annotated_original_img = clone.copy()
        refPt = [(x, y)]
        current_x = x
        current_y = y
        gap_list = compute_rib_gap(img_src,current_x,current_y)
        gap = cv2.getTrackbarPos('gap', 'RibCounting')
        isShow = True

        for i in range(len(gap_list)):
            if(y-i*spacing_height > 0):
                if(count % 2 == 0):
                    cv2.putText(annotated_original_img, str(count), (x, y - i*gap-spacing_height),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
                if(x<width/2):
                    cv2.line(annotated_original_img, (x - 30, y - i * gap - 2 * spacing_height),
                             (x - 10, y - i * gap - 2 * spacing_height), (0, 0, 0), 1)
                    # if(i != 11):
                    #     cv2.line(annotated_original_img, (x - 15, y - i * gap - 2 * spacing_height - int(gap/3)),
                    #              (x - 10, y - i * gap - 2 * spacing_height - int(gap/3)), (0, 0, 0), 1)
                    #     cv2.line(annotated_original_img, (x - 15, y - i * gap - 2 * spacing_height - int(2*gap/3)),
                    #              (x - 10, y - i * gap - 2 * spacing_height - int(2*gap/3)), (0, 0, 0), 1)
                else:
                    cv2.line(annotated_original_img, (x + 20, y - i * gap - 2 * spacing_height),
                             (x + 40, y - i * gap - 2 * spacing_height), (0, 0, 0), 1)
                    # if(i != 11):
                    #     cv2.line(annotated_original_img, (x + 20, y - i * gap - 2 * spacing_height - int(gap/3)),
                    #              (x +25, y - i * gap - 2 * spacing_height - int(gap/3)), (0, 0, 0), 1)
                    #     cv2.line(annotated_original_img, (x + 20, y - i * gap - 2 * spacing_height - int(2*gap/3)),
                    #              (x + 25, y - i * gap - 2 * spacing_height - int(2*gap/3)), (0, 0, 0), 1)
                print(str(count) + " height = " + str(y - i*gap-spacing_height))
                count = count - 1

    cv2.imshow('RibCounting', annotated_original_img)

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="Path to the image")
# args = vars(ap.parse_args())

# load the image, clone it, and setup the mouse callback function
# image = cv2.imread(args['RibCounting'])

#Gap value derived from cv
gap = 8

clone = image.copy()
annotated_original_img = image.copy()
cv2.namedWindow('RibCounting')
cv2.setMouseCallback('RibCounting', show_count)
cv2.createTrackbar('gap', 'RibCounting', gap, 30, onTrackbarChange)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow('RibCounting', annotated_original_img)
    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the cropping region
    if (key == ord("r")):
        annotated_original_img = clone.copy()
        isShow = False

    # if the 'c' key is pressed, break from the loop
    elif (key == ord("c")):
        break


# close all open windows
cv2.destroyAllWindows()