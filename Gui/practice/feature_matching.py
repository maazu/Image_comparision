import numpy as np
import cv2
from matplotlib import pyplot as plt


def get_corrected_img(img1, img2):
    img1 = cv2.imread(img1,0)          # queryImage
    img2 = cv2.imread(img2,0) # trainImage
    cv2.imshow('oass',img1)
    MIN_MATCHES = 50

    orb = cv2.ORB_create(nfeatures=500)
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    print(len(kp1))
    print(len(kp2))
    


get_corrected_img('train10.png','detect_region10.png')
