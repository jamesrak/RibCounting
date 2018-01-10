import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('../data/sample_image/sample_rib2.jpg')
height, width = img.shape[:2]

gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
eq_img = cv2.equalizeHist(gray_img)
enhance_img = cv2.medianBlur(eq_img,3)
plt.imshow(eq_img,'gray')
plt.show()

plt.imshow(enhance_img,cmap = 'gray')
plt.show()


structuredEdgeModel = cv2.ximgproc.createStructuredEdgeDetection("../Materials/structuredEdgeModel.yml")
enhance_img2 = cv2.cvtColor(enhance_img,cv2.COLOR_GRAY2BGR)
plt.imshow(enhance_img2,cmap = 'gray')
plt.show()

enhance_img2 = np.float32(enhance_img2)
enhance_img2 = enhance_img2/255.0
plt.imshow(enhance_img2,cmap = 'gray')
plt.show()

enhance_img3 = structuredEdgeModel.detectEdges(enhance_img2)
plt.imshow(enhance_img3,cmap = 'gray')
plt.show()

enhance_img3 = enhance_img3*255
enhance_img4 = enhance_img3>2
enhance_img4
lines = cv2.HoughLinesP(enhance_img4, 1, np.pi/180, 100)
for x in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[x]:
        cv2.line(enhance_img4,(x1,y1),(x2,y2),(0,255,0),2)
plt.imshow(enhance_img4,'gray')
plt.show()

enh_low_threshold = 120
edge_img = cv2.Canny(enhance_img,enh_low_threshold, enh_low_threshold*3 )
plt.imshow(edge_img,cmap = 'gray')
plt.show()


## Thoracic vertebrae detectionh
vert_threshold_value = 100
vert_max_BINARY_value = 255
vert_threshold_type = 1

ret,vertebrae = cv2.threshold(img,vert_threshold_value, vert_max_BINARY_value, vert_threshold_type)

## Draw Lines of each rib
threshold_value = 180
max_BINARY_value = 255
threshold_type = 1
kernel = np.ones((5,5),np.uint8)

#output  = cv2.Canny(inputImage,lowThreshold,lowThreshold*4);
ret2,binary_img = cv2.threshold(img,threshold_value, max_BINARY_value,threshold_type);
output = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

# cv2.imshow("Thoracic Vertebrae",vertebrae)
# cv2.imshow("Output",output)
fig = plt.figure(figsize=(15,7))
titles = ['Original Image','BINARY','OUTPUT','VERTEBRAE']
images = [img, binary_img,output,vertebrae]
for i in range(len(titles)):
    plt.subplot(1,4,i+1),plt.imshow(images[i])
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
    plt.show()
# cv2.waitKey(0)
