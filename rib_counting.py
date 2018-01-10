import cv2
import numpy as np
from matplotlib import pyplot as plt

def convert_func(x):
    if(x==True):
        x = 255
    else:
        x = 0
    return(x)


def compute_rib_gap(img_src, y, count_width=15, spacing_height=4, gap_threshold=10):
    # output
    gap_list = []

    img = cv2.imread(img_src)
    # img = cv2.resize(img, (0, 0), fx=2.0, fy=2.0)
    height, width = img.shape[:2]
    gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur_img = cv2.GaussianBlur(gray_img,(5,5),0)

    ### Edge detection ###

    # otsu's threshold
    ret,binary_img = cv2.threshold(blur_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    thinning_img = cv2.ximgproc.thinning(binary_img)

    vetebra_img = cv2.cvtColor(blur_img,cv2.COLOR_GRAY2BGR)
    vetebra_img = np.float32(vetebra_img)
    vetebra_img = vetebra_img/255.0
    structuredEdgeModel = cv2.ximgproc.createStructuredEdgeDetection("../Materials/structuredEdgeModel.yml")
    vetebra_img = structuredEdgeModel.detectEdges(vetebra_img)

    binary_vertebra = vetebra_img*255
    binary_vertebra = binary_vertebra>25
    conv_func = np.vectorize(convert_func)
    binary_vertebra = conv_func(binary_vertebra)
    binary_vertebra = np.array(binary_vertebra, dtype = np.uint8)

    thinning_img_bgr = cv2.cvtColor(thinning_img,cv2.COLOR_GRAY2BGR)
    annotated_img = np.zeros((height,width,3), dtype=np.uint8)
    annotated_original_img = np.zeros((height,width,3), dtype=np.uint8)
    np.copyto(annotated_img,thinning_img_bgr)
    np.copyto(annotated_original_img,img)
    lines = cv2.HoughLinesP(binary_vertebra, 1, np.pi/180, 100)

    #Find Left and right vertebra line
    x_center = (np.amin(lines, axis=0)[0][0] + np.amax(lines, axis=0)[0][0])/2
    right_lines = lines[lines[:,:,0]-x_center>=0]
    right_line = right_lines[np.argmin(right_lines[:,0])]
    left_lines = lines[lines[:,:,0]-x_center<0]
    left_line = left_lines[np.argmax(left_lines[:,0])]

    #Annotated
    # cv2.line(annotated_img,(left_line[0],left_line[1]),(left_line[2],left_line[3]),(0,255,0),2)
    # cv2.line(annotated_img,(right_line[0],right_line[1]),(right_line[2],right_line[3]),(0,255,0),2)

    # cv2.line(annotated_original_img,(left_line[0],left_line[1]),(left_line[2],left_line[3]),(0,255,0),2)
    # cv2.line(annotated_original_img,(right_line[0],right_line[1]),(right_line[2],right_line[3]),(0,255,0),2)

    # count_width = 15   #The length between the vertebra line and x-position which we count rib
    # spacing_height = 4 #the moving down length when annotated the original image
    # gap_threshold = 10

    count = 12
    tmp_height = height
    for i in range(height-1,0,-1):
        gap = abs(i - tmp_height)
        if((annotated_img[i][left_line[0]-count_width][0] != 0) and (gap >= gap_threshold) ):
            gap_list.append(gap)
            # cv2.circle(annotated_img,(left_line[0]-count_width,i), 2, (0,0,255), -1)
            # cv2.putText(annotated_original_img,str(count),(left_line[0]-count_width+2,i-spacing_height),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,255),1)
            print(str(count)+" height = " + str(i) + " gap = "+str(gap))
            tmp_height = i
            count = count - 1
    # fig = plt.figure(figsize=(15, 10))
    # plt.subplot(1, 2, 1), plt.imshow(annotated_img, 'gray')
    # plt.subplot(1, 2, 2), plt.imshow(annotated_original_img)
    # plt.show()
    return gap_list


# imgurl = '../data/sample_image/sample_rib8.jpg'
# print(compute_rib_gap(imgurl,245))
