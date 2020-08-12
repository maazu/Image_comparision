from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np
import glob
import os
import uuid
import argparse
from skimage.io import imread
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import jaccard_similarity_score





def resize_img(img_to_resize):
    img  = cv2.imread(img_to_resize)
    resized_img = cv2.resize(img , (524 , 480)) # w x h
    #grayscaled = cv2.cvtColor(resized_img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(resized_img,100,200)
    #final_img = remove_noise(edges)
    return edges 




def middle_half(img):
    img = get_region(img)
    first_region = img[0:238, 0:524] # Crop from {x, y, w, h } => {0, 0, 300, 400}
    return first_region


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

    


def detect_features(img):
    img  = resize_img(img)
    orb = cv2.ORB_create(edgeThreshold = 4, scoreType=cv2.ORB_FAST_SCORE)
    #orb = cv2.ORB_create(100, 1.2, nlevels=9, edgeThreshold = 4, scoreType=cv2.ORB_FAST_SCORE)
    kp1, des1 = orb.detectAndCompute(img, None)
    keypoints_without_size = np.copy(img)
    new_img = cv2.drawKeypoints(img, kp1, keypoints_without_size, color = (0, 255, 0))
    return len(kp1)





def compare_features(img1,img2):

    #orb = cv2.ORB_create(nfeatures=10000, scoreType=cv2.ORB_FAST_SCORE)
    img1 = cv2.imread(img1)
    img2 = cv2.imread(img2)
    orb = cv2.ORB_create(edgeThreshold = 4, scoreType=cv2.ORB_FAST_SCORE)
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    keypoints_without_size = np.copy(img1)
    keypoints_with_size = np.copy(img2)

    #cv2.drawKeypoints(img1, kp1, keypoints_without_size, color = (0, 255, 0))

    #cv2.drawKeypoints(img2, kp1, keypoints_with_size, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
  

    print("Number of Keypoints Detected In The Training Image: ", len(kp1))
    print("Number of Keypoints Detected In The Query Image: ", len(kp2))
    
    # Create a Brute Force Matcher object.
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
    matches = bf.match(des1, des2)
   
    matches = sorted(matches, key = lambda x : x.distance)
    good_matches = matches[:512] # Good matches

    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches     ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()
    result = cv2.drawMatches(img1, kp1, img2, kp2, matches, img2, flags = 2)
    print("Perfect matches Total matches",len(matchesMask))
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
    
    cv2.imshow("GOOD FeatureS Matching", img3)
   
    print("Good Matches", len(good_matches))
    return len(good_matches)





#compare_features('detect_region101.png','detect_region11.png')  #testting image 

def look_for_features(image,frame_number):
    path = 'detected_regions\\'
     
    
    score_dic =  {}
   
   
    first = first_region(image)
    score_dic['first'] = detect_features(image)
  
    second = sec_region(image)
    score_dic['second'] = detect_features(image)

    third = third_region(image)
    score_dic['third'] = detect_features(image)
    
    fourth = fourth_region(image)
    score_dic['fourth'] = detect_features(image)

    maximum = max(score_dic, key=score_dic.get)
    print(score_dic)
    highest = (maximum, score_dic[maximum])
    #print(highest[1])
   
    if(highest[1] > 0.40):  
        if( highest[0] == 'first'):
            #display_histogram(first)
          
            cv2.imwrite(os.path.join(path , 'detect_region'+str(frame_number)+'.png'), first)
            print('first imgae writed')
        elif( highest[0] == 'second'):
            #display_histogram(first)
            cv2.imwrite(os.path.join(path , 'detect_region'+str(frame_number)+'.png'), second)
            print(' second imgae writed')
        elif( highest[0] == 'third'):
            #display_histogram(third)
            cv2.imwrite(os.path.join(path , 'detect_region'+str(frame_number)+'.png'), third)
            print('third imgae writed')
        elif( highest[0] == 'fourth'):
            cv2.imwrite(os.path.join(path , 'detect_region'+str(frame_number)+'.png'), fourth)
            print('fourth imgae writed')
        elif( highest[0] == 'Lower part'): 
            #cv2.imwrite(os.path.join(path , 'detect_region'+str(frame_number)+'.jpg'), Lower part)
            print('Lower part imgae writed')
        elif( highest[0] == 'upper part'):
            #cv2.imwrite(os.path.join(path , 'detect_region'+str(frame_number)+'.jpg'), upper part)
            print('upper part imgae writed')
        else:
            print('sad')
    else:
        print('irrelevant img')

    
    return highest



#look_for_features('train10.jpg',1) Testing method



def structual_similarity(img1,img2):
    img1 =imread(img1)
    img2 =imread(img2)
    (score, diff) = ssim(img1, img2, full=True,gaussian_weights=False,multichannel=True)
    return score

