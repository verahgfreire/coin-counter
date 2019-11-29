# -*- coding: latin-1 -*-
"""
@authors: Vera Freire, n. 40526 e Beatriz Dimas, n.40668
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


def abrirImg(path):
    img = cv2.imread(path)
    return img,img[:,:,2],img[:,:,1],img[:,:,0]

def conversaoCinzento(img):
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return imgray

def threshold(img):
    ret,thresh = cv2.threshold(img,127,255,0) #limiar 127, nao usamos metodo
    return ret, thresh

def mostrarImg(name, img):
    cv2.imshow(name,img)
    cv2.waitKey(0)

def compararPlanos(img):
    plt.figure(1)

    # Red
    plt.subplot(231)
    plt.imshow(img[:,:,2],'gray')
    plt.title('R')

    # Green
    plt.subplot(232)
    plt.imshow(img[:,:,1],'gray')
    plt.title('G')

    # Blue
    plt.subplot(233)
    plt.imshow(img[:,:,0],'gray')
    plt.title('B')

    # Hist Red
    plt.subplot(234)
    hist = cv2.calcHist([img],[2],None,[256],[0,256])
    plt.plot(hist)
    plt.title('R Hist')

    # Hist Green
    plt.subplot(235)
    hist = cv2.calcHist([img],[1],None,[256],[0,256])
    plt.plot(hist)
    plt.title('G Hist')

    # Hist Blue
    plt.subplot(236)
    hist = cv2.calcHist([img],[0],None,[256],[0,256])
    plt.plot(hist)
    plt.title('B Hist')

    plt.tight_layout()
    plt.show()

def melhoramento(img):
    eKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,8))
    eKernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(48,48))

    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, eKernel)
    erode = cv2.erode(closing, eKernel2)
    return erode

def circularidade(area, perimetro):
    return (perimetro)**2/area

def filtrarContornos(contours, hierarchy):
    contornos = []
    hierarquia = []

    h = hierarchy[0].tolist()
    j=0
    while j < len(contours):
        area = cv2.contourArea(contours[j])
        perimeter = cv2.arcLength(contours[j],True)
        circularity = circularidade(area,perimeter)
        if (h[j][2] == -1) and (h[j][3] == -1) and circularity > 13.8 and circularity < 15.6:
            contornos.append(contours[j])
            hierarquia.append(h[j])
        j+=1

    return contornos, hierarquia

def contadorMoedas(imagesPath):
    for i in range(len(imagesPath)):
        img,imgRed,imgGreen,imgBlue = abrirImg(imagesPath[i])
        #mostrarImg("img",img)

        ### Histogramas
        #compararPlanos(img)

        ### Transformacao para niveis cinzentos
        #imgray = conversaoCinzento(img)

        ### Binarizacao da imagem
        ret,thresh = threshold(imgRed)
        #mostrarImg("thresh",thresh)

        ### Melhoramento da imagem
        imgM = melhoramento(thresh)

        ### Extracao de componentes
        contours, hierarchy = cv2.findContours(imgM,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        ### Extracao de propriedades

        contornos, hierarquia = filtrarContornos(contours, hierarchy)
        total = 0. ## quantia total
        cv2.drawContours(img, contornos, -1, (0,255,0), 3)

        for k in range(len(contornos)):
            c = contornos[k]
            area = cv2.contourArea(c)
            perimeter = cv2.arcLength(c,True)
            moment = cv2.moments(c)
            circularity = circularidade(area,perimeter)

            #centroide
            cx = int(moment['m10']/moment['m00'])
            cy = int(moment['m01']/moment['m00'])


        ### Classificacao dos objetos e total da quantia em cada imagem

            if area >= 10176.5 and area < 10928: #moeda 1 Euro
                cv2.putText(img,("1 Euro"), (cx,cy), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0),1)
                total += 1.
            if area >= 11597 and area < 12137: #moeda 50 cent
                cv2.putText(img,("50 Cent"), (cx,cy), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0),1)
                total += 0.50
            if area >= 8518 and area < 9838: #moeda 20 cent
                cv2.putText(img,("20 Cent"), (cx,cy), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0),1)
                total += 0.20
            if area >= 6095 and area < 6864.5: #moeda 10 cent
                cv2.putText(img,("10 Cent"), (cx,cy), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0),1)
                total += 0.10
            if area >= 7598.5 and area < 8204.5: #moeda 5 cent
                cv2.putText(img,("5 Cent"), (cx,cy), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0),1)
                total += 0.05
            if area >= 5467.5 and area < 5893.5: #moeda 2 cent
                cv2.putText(img,("2 Cent"), (cx,cy), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0),1)
                total += 0.02
            if area >= 3304.5 and area < 3499.5: #moeda 1 cent
                cv2.putText(img,("1 Cent"), (cx-10,cy), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0),1)
                total += 0.01

        cv2.putText(img,("Quantia na imagem: "+ str(total) + " euros"), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),2)
        mostrarImg("Contour",img)
        print "O total da quantia na imagem " + `imagesPath[i]` + " = " + str(total) + " €"
        print " "


if __name__ == '__main__':

    imagesPath = ['PIV_16_17_TL1pack/P1000697s.jpg',\
    'PIV_16_17_TL1pack/P1000698s.jpg','PIV_16_17_TL1pack/P1000699s.jpg',\
    'PIV_16_17_TL1pack/P1000703s.jpg','PIV_16_17_TL1pack/P1000705s.jpg',\
    'PIV_16_17_TL1pack/P1000706s.jpg','PIV_16_17_TL1pack/P1000709s.jpg',\
    'PIV_16_17_TL1pack/P1000710s.jpg','PIV_16_17_TL1pack/P1000713s.jpg']

    contadorMoedas(imagesPath)
