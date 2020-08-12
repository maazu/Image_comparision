import numpy as np
import cv2 
from matplotlib import pyplot as plt




img1 = cv2.imread('frame1.jpg',0)          # queryImage
img2 = cv2.imread('frame4.jpg',0) # trainImage

finder = cv2.ORB_create()
lowe_ratio = 0.89
# find the keypoints and descriptors with SIFT
kp1, des1 = finder.detectAndCompute(img1,None)
kp2, des2 = finder.detectAndCompute(img2,None)




FLANN_INDEX_LSH = 6

index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6, # 12
                   key_size = 12,     # 20
                   multi_probe_level = 1) #2

search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=2)


print(len(matches))


 # Apply ratio test
good = []

for m,n in matches:
    if m.distance < lowe_ratio*n.distance:
        good.append([m])
            
print(len(good))
msg1 = ('using %s with lowe_ratio %.2f' % ('orb', lowe_ratio))
msg2 = ('there are %d good matches' % (len(good)))
print(msg1)
print(msg2)
