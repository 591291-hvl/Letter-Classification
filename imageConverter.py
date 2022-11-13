import base64
from PIL import Image, ImageOps
import numpy as np
from scipy.ndimage import gaussian_filter
import cv2

# Converts base64 png to .png
def convertBase64ToPng(b64):
    with open("img.png", "wb") as fn:
        return fn.write(base64.b64decode(b64))

# Please ignore this, just trust that it converts 128x128 to 28x28
# Image converting
def imageConvert(): #Igonore bad code

    #The steps being done is described in https://arxiv.org/pdf/1702.05373v1.pdf
    #Read page 4 if you want to understand

    image = Image.open("img.png")
    #Step 1
    image = ImageOps.grayscale(image)
    image = ImageOps.invert(image)
    array = np.asarray(image)
    #Step 2
    arrayGau = gaussian_filter(array,sigma = 1)

    #Step 3
    topMost = -1
    bottomMost = -1
    rightMost = -1
    leftMost = -1

    #left to right
    for x in range(128):
        for y in range(128):

            #save first non zero value (top)
            if not arrayGau[x][y] == 0 and topMost == -1:
                topMost = (x,y)

            #save last non zero value (bottom)
            if not arrayGau[x][y] == 0:
                bottomMost = (x,y)

    #top to bottom
    for x in range(128):
        for y in range(128):

            #save first non zero value (left)
            if not arrayGau[y][x] == 0 and leftMost == -1:
                leftMost = (x,y)

            #save last non zero value (right)
            if not arrayGau[y][x] == 0:
                rightMost = (x,y)
    heigth = abs(topMost[0] - bottomMost[0])
    width = abs(leftMost[0] - rightMost[0])
    #print(heigth)
    #print(width)

    #Step 4?

    #heigth is more, change width both sides
    if heigth > width:
        padding = (heigth - abs(rightMost[0]-leftMost[0]))//2
        #add padding to width
        newArray = np.zeros(shape=(heigth,heigth))
        for x in range(width+1):
            for y in range(heigth):
                # newArray[topMost[0] + x][padding +y] = 1
                newArray[y][padding + x] = arrayGau[y+ topMost[0]][x + leftMost[0]]

    elif heigth < width:
        padding = (width - abs(bottomMost[0]-topMost[0]+1))//2
        #add padding to height?
        newArray = np.zeros(shape=(width,width))
        for x in range(width):
            for y in range(heigth+1):
                # newArray[padding + y][x] = 1
                newArray[padding + y][x] = arrayGau[y+ topMost[0]][x+leftMost[0]]

    reducedArray = newArray
    #Step 5
    img_resized = cv2.resize(reducedArray, dsize=[28,28] ,fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    # flatImg = img_resized.reshape(1,-1)

    return img_resized