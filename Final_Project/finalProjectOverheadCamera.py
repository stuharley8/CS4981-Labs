import cv2 as cv
import sys
import numpy as np
import math


#The way to run these functions is to follow this protocol:
#1. set up the overhead camera
#2. place one of the tires under the overhead camera to get the area of it with the areaOfTire function
#3. place the playing field under the overhead camera to get its centroid
#4. put the robot arm in the middle of the playing field
#5. scatter tires about the playing field
#6. run the findObjects function to get the locations to pick up the tires
#7. run the findAngles function to get the angles to pick up the tires

callBackImg = None
tireMaxArea = 0
tireMinArea = 0
objectLocations = []
objectAngles = []
cX = 0
cY = 0


''' May eventually be useful

'''
#Finds the approximate area of a tire with the camera configured to be used in the findObjects function
def areaOfTire():
    orig = cv.imread(cv.samples.findFile("empty playing field.jpg"))
    # Convert to graycsale

    img_gray = cv.cvtColor(orig, cv.COLOR_BGR2GRAY)

    # Blur the image for better edge detection

    # img_blur = cv.GaussianBlur(img_gray, (105,105),cv.BORDER_DEFAULT)

    (height, width) = img_gray.shape
    scale = 1
    resize = cv.resize(img_gray, (int(width / scale), int(height / scale)))
    img_blur = cv.GaussianBlur(resize, (5, 5), cv.BORDER_DEFAULT)
    edges = cv.Canny(image=img_blur, threshold1=100, threshold2=200)


    EDGES = edges

    cv.imshow("Display window", edges)


    while True:
        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite('testSave.png', callBackImg)
        elif k == ord('q'):
            break
    return edges

    '''
    orig = cv.imread(cv.samples.findFile("tire picture.jpg"))

    (height, width, channels) = orig.shape
    scale = 5
    resize = cv.resize(orig, (int(width / scale), int(height / scale)))

    gray = cv.cvtColor(resize, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]

    output = cv.connectedComponentsWithStats(thresh, 4, cv.CV_32S)
    (numLabels, labels, stats, centroids) = output
    area = 0
    x, y = 0, 0
    for i in range(0, numLabels):
        if stats[i, cv.CC_STAT_AREA] > 10 and 200000 > stats[i, cv.CC_STAT_AREA]:
            area = stats[i, cv.CC_STAT_AREA]
            tireMaxArea = area + 100
            tireMinArea = area - 100
            x, y = centroids[i]
    cv.circle(resize, (int(x), int(y)), 10, (255, 255, 0), -1)
    cv.imshow("Display window", resize)

    while True:
        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite('testSave.png', gray)
        elif k == ord('q'):
            break
    '''


#ConfigureOverheadCamera is called when the system is being set up.
#It returns the centroid of the playing field so that the camera knows where the
#base of the arm is in relation to the pixels in the picture.
def configureOverheadCamera():
    global callBackImg
    orig = cv.imread(cv.samples.findFile("empty playing field.jpg"))

    (height, width, channels) = orig.shape
    scale = 1
    resize = cv.resize(orig, (int(width / scale), int(height / scale)))

    frame_HSV = cv.cvtColor(resize, cv.COLOR_BGR2RGB)
    frame_threshold = cv.inRange(frame_HSV, (0,0,0), (40,40,40))

    # Image Opening
    kernel = np.ones((1, 1), np.uint8)
    opening = cv.morphologyEx(frame_threshold, cv.MORPH_OPEN, kernel)

    # Make a playing field that is 1 where the field is and 0 everywhere else
    playingField = np.array(opening)
    playingField[playingField == 255] = 1


    # Find the moments of the image (the intensity of each pixel)
    moments = cv.moments(opening)

    # Find the centroid of the intensity pixels
    if moments["m00"] != 0:
        x = int(moments["m10"] / moments["m00"])
        y = int(moments["m01"] / moments["m00"])
    else:
        x, y = 0, 0


    # Place a circle as the centroid
    cv.circle(resize, (x, y), 10, (255, 255, 0), -1)
    cX = x
    cY = y
    cv.imshow("Display window", resize)


    while True:
        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite('testSave.png', callBackImg)
        elif k == ord('q'):
            break

    #centroid of the playing field
    return (x,y),playingField


def findObjects(edges):
    orig = cv.imread(cv.samples.findFile("scattered objects 2.jpg"))

    (height, width, channels) = orig.shape
    scale = 1
    resize = cv.resize(orig, (int(width / scale), int(height / scale)))

    gray = cv.cvtColor(resize, cv.COLOR_BGR2GRAY)
    frame_threshold = cv.inRange(gray, (60), (180))
    #thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]

    output = cv.connectedComponentsWithStats(frame_threshold, 8, cv.CV_32S)
    (numLabels, labels, stats, centroids) = output
    area = 0
    x, y = 0, 0

    for i in range(0, numLabels):
        isIn = False
        x, y = centroids[i]
        x = int(x)
        y = int(y)
        #print(stats[i, cv.CC_STAT_AREA])
        #If it is around the area of a tire
        if stats[i, cv.CC_STAT_AREA] > 3000 and stats[i, cv.CC_STAT_AREA] < 15000:
            for i in range(-25,25):
                for n in range(-25,25):
                    if edges[y+i,x+n] == 255:
                        isIn = True
            if isIn:
                cv.circle(resize, (int(x), int(y)), 10, (255, 255, 0), -1)
                objectLocations.append((x,y))


            #    objectLocations.append((int(x), int(y)))
    #cv.circle(orig, (int(x), int(y)), 10, (255, 255, 0), -1)
    cv.imshow("Display window", resize)

    while True:
        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite('testSave.png', gray)
        elif k == ord('q'):
            break

#Finds all the angles to the objects on the playing field
def findAngles():
    for point in objectLocations:
        x,y = point
        theta = math.degrees(math.atan2(y - cY, x - cX))
        theta = abs(theta)
        objectAngles.append(theta)


if __name__ == '__main__':
    (x,y),playingField = configureOverheadCamera()
    print("Centroid: ",x,y)
    cX = x
    cY = y
    edges = areaOfTire()
    findObjects(edges)
    findAngles()
    print("Object Locations: ", objectLocations)
    print("Object Angles: ", objectAngles)

