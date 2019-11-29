# filename: bwLabel Module
import cv2
import numpy as np

def labeling(bwImage):
    bw = bwImage.copy()
    (contourSeq, contourHierarchy) = cv2.findContours(bw, \
                    cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    
    grayLevel = 0
    outImage = np.zeros(bwImage.shape)
    idx = 0
    while idx >= 0:
        grayLevel = grayLevel+1
        color = (grayLevel,grayLevel,grayLevel)
        cv2.drawContours(outImage, contourSeq, idx, color, -1, 8 , contourHierarchy)
        idx = contourHierarchy[0][idx][0]

    return grayLevel, outImage
