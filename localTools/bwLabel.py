# filename: bwLabel Module
import cv2
import numpy as np

def labeling(bwImage):
    bw = bwImage.copy()
    (contourSeq, [contourHierarchy]) = cv2.findContours(bw, \
                    cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    grayLevel = 0
    outImage = np.zeros(bwImage.shape)
    for i in range(len(contourSeq)):
        # tests if it is not an internal contour and its area is grater than a minArea value
        if contourHierarchy[i][3] < 0 :
            grayLevel = grayLevel+1;
            color = (grayLevel,grayLevel,grayLevel)
            cv2.drawContours(outImage, contourSeq, i, color, -1)
    return grayLevel, outImage
