from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import jaccard_similarity_score
import matplotlib.pyplot as plt
import cv2
import numpy as np
import glob
import os
from PIL import Image




def resize_img(img_to_resize):
    img  = cv2.imread(img_to_resize)
    resized_img = cv2.resize(img , (524 , 480)) # w x h
    #processed_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(resized_img, 100,130)
    #processed_img = cv2.Laplacian(resized_img,cv2.CV_8U) 
    return processed_img

#To draw a rectangle, you need top-left corner and bottom-right corner of rectangle. This time we will draw a green rectangle at the top-right corner of image.


def get_region(img):
    img = resize_img(img)
    img1 = cv2.line(img,(254,0),(254,480),(255,0,0),2)
    img2 = cv2.line(img1,(0,240),(524,240),(255,0,0),2)
    return img2

def upper_half(img):
    img = get_region(img)
    first_region = img[0:238, 0:524] # Crop from {x, y, w, h } => {0, 0, 300, 400}
    return first_region

def lower_half(img):
    img = get_region(img)
    first_region = img[240:524, 0:524] # Crop from {x, y, w, h } => {0, 0, 300, 400}
    return first_region
    
def first_region(img):
    img = get_region(img)
    first_region = img[0:238, 0:249] # Crop from {x, y, w, h } => {0, 0, 300, 400}
    return first_region

def sec_region(img):
    img = get_region(img)
    sec_region = img[240:480, 0:249] 
    return sec_region

def third_region(img):
    img = get_region(img)
    third_region = img[0:240, 254:524] 
    return third_region
 

def fourth_region(img):
    img = get_region(img)
    fourth_region = img[240:524, 254:524] 
    return fourth_region




image1 = 'frame635.jpg'
image2 = 'frame742.jpg'
#image1 = 'frame5.jpg'
#image2 = 'frame6.jpg'


img1 = get_region(image1)
img2 = get_region(image2)


uimg1 = upper_half(image1)
uimg2 = upper_half(image2)


limg1 = lower_half(image1)
limg2 = lower_half(image2)


first = first_region(image1)
first2 = first_region(image2)

second = sec_region(image1)
second2 = sec_region(image2)

third = third_region(image1)
third2 = third_region(image2)

fourth = fourth_region(image1)
fourth2 = fourth_region(image2)

roi = 0.01
reg_score = []
score_dic =  {}




def detect_features(img1,img2):

    #orb = cv2.ORB_create(nfeatures=10000, scoreType=cv2.ORB_FAST_SCORE)
    orb = cv2.ORB_create(1000, 1.2, nlevels=9, edgeThreshold = 4)
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    keypoints_without_size = np.copy(img1)
    keypoints_with_size = np.copy(img2)

    cv2.drawKeypoints(img1, kp1, keypoints_without_size, color = (0, 255, 0))

    cv2.drawKeypoints(img2, kp1, keypoints_with_size, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
  

    print("Number of Keypoints Detected In The Training Image: ", len(kp1))
    print("Number of Keypoints Detected In The Query Image: ", len(kp2))
    
    # Create a Brute Force Matcher object.
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
    matches = bf.match(des1, des2)
    #matches = bf.knnMatch(des1,des2, k=2)
    # The matches with shorter distance are the ones we want.
    matches = sorted(matches, key = lambda x : x.distance)
    good_matches = matches[:512] # Good matches

    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches     ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()
    result = cv2.drawMatches(img1, kp1, img2, kp2, matches, img2, flags = 2)

    h,w = img1.shape[:2]
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)

    dst = cv2.perspectiveTransform(pts,M)
    dst += (w, 0)  # adding offset

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

    img3 = cv2.drawMatches(img1,kp1,img2,kp2,good_matches, None,**draw_params)

    # Draw bounding box in Red
    img3 = cv2.polylines(img3, [np.int32(dst)], True, (0,0,255),3, cv2.LINE_AA)
    
    cv2.imshow("result", img3)
   
    print("\nNumber of Matching Keypoints Between The Training and Query Images: ", len(matches))
    






(score, diff) = ssim(img1, img2, full=True)
print("without Image similarity", score)
score_dic['without'] = score

(score, diff) = ssim(uimg1, uimg2, full=True)
print("upper half Image similarity", score)
reg_score.append(score)
score_dic['uper part'] = score



(score, diff) = ssim(limg1, limg2, full=True)
print("lower half Image similarity", score)
score_dic['Lower part'] = score



(score, diff) = ssim(first, first2, full=True)
print("first region similarity", score)
score_dic['first'] = score


(score, diff) = ssim(second, second2, full=True)
print("second region similarity", score)
score_dic['second'] = score


(score, diff) = ssim(third, third2, full=True)
print("third region similarity", score)
score_dic['third'] = score


(score, diff) = ssim(fourth, fourth2, full=True)
print("fourth region similarity", score)
score_dic['fourth'] = score





maximum = max(score_dic, key=score_dic.get)  # Just use 'min' instead of 'max' for minimum.
highest = (maximum, score_dic[maximum])
print('Highest Matched Region',highest)

detect_features(first,first2)


if( highest[0] == 'first'):
    cv2.imwrite('third.png', first)
    print('imgae writed')


elif( highest[0] == 'second'):
    cv2.imwrite('second.png', second)
    print('imgae writed')
elif( highest[0] == 'third'):
    cv2.imwrite('third.png', third)
    print('imgae writed')
elif( highest[0] == 'fourth'):
   cv2.imwrite('fourth.png', fourth)
   print('imgae writed')
else:
    print('sad')
cv2.imshow("img",third)





'''

template = cv2.imread('mario_coin.png',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('res.png',img_rgb)



'''


'''

cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)


x1,y1 ------
|          |
|          |
|          |
--------x2,y2


def match_bf(img1, img2, num_keypoints=1000):
    img1 = resize_img(img1)
    img2 = resize_img(img2)
   
    
    orb = cv2.ORB_create(nfeatures=100, scoreType=cv2.ORB_FAST_SCORE)    
    #orb = cv2.ORB_create(edgeThreshold=15, patchSize=31, nlevels=8, fastThreshold=30, scaleFactor=1.2, WTA_K=2,scoreType=cv2.ORB_FAST_SCORE, firstLevel=0, nfeatures=10000)
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp, des2 = orb.detectAndCompute(img2, None)  
    img3 = cv2.drawKeypoints(img1, kp, None, color=(0,255,0), flags=0)
    cv2.imshow("st2.png", img3)



image1 = '3.jpg'
image2 = '4.jpg'


#match_bf(image1,image2)



ratio = 0.65





        


image1 = '2.jpg'
image2 = '3.jpg'


#match_bf(image1,image2)


###caaaall 
match_flann(image1,image2)





def register(frame1, frame2):
    frame1 = cv2.imread(frame1)
    frame2 = cv2.imread(frame2)
    orb = cv2.ORB_create(nfeatures=1000, scoreType=cv2.ORB_FAST_SCORE)

    keypoints1, descriptors1 = orb.detectAndCompute(frame1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(frame2, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * 1000)
    matches = matches[:numGoodMatches]

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    print(points1)
    print(points2)
    print(register(image1,image1))
'''

