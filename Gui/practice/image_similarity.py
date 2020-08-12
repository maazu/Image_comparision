from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
def resize_img(img_to_resize):
    img  = cv2.imread(img_to_resize)
    resized_img = cv2.resize(img , (500, 520))
    processed_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
    #processed_img = cv2.Canny(processed_img, 200,10)
    
    #processed_img = cv2.Laplacian(resized_img,cv2.CV_8U)
    
    return processed_img


def cal_img_similarity(img1,img2):
   
    background_img = cv2.imread(img1)
    background_img = cv2.resize(background_img, (500, 520)) 

    test_img = cv2.imread(img2)
    test_img = cv2.resize(test_img, (500, 520))  
    # Convert images to grayscale
    before_gray = cv2.cvtColor(background_img, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)


    # Compute SSIM between two images
    (score, diff) = ssim(before_gray, after_gray, full=True)
    print("Image similarity", score)

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0,1] 
    # so we must convert the array to 8-bit unsigned integers in the range
    # [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")


    # Threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ

    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]


    mask = np.zeros(background_img.shape, dtype='uint8')
    filled_after = test_img.copy()


    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(background_img, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.rectangle(test_img, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(mask, [c], 0, (0,255,0), -1)
            cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)

    cv2.imshow('before', background_img)
    cv2.imshow('after', test_img)

    cv2.waitKey(0)
cal_img_similarity('frame2.jpg','frame3.jpg')
