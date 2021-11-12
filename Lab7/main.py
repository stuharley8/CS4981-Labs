import cv2 as cv
import sys
import numpy as np
from math import pow,sqrt

callBackImg = None

def printRGB(event, x, y, flags, params):
    (height,width,channels)=callBackImg.shape
    # EVENT_MOUSEMOVE
    if event == cv.EVENT_LBUTTONDOWN:
        if channels==3:
            print(str(x)+" "+str(y)+" "+str(callBackImg[y][x][2])+" "+str(callBackImg[y][x][1])+" "+str(callBackImg[y][x][0]))
        else:
            print(str(x) + " " + str(y) + " " + str(callBackImg[y][x][0]))


def showImage(images):
    global callBackImg
    for i in range(len(images)):
        if i == 0:
            callBackImg = images[i]
        cv.imshow("Image "+str(i),images[i])
        cv.setMouseCallback("Image "+str(i), printRGB)
    while True:
        k = cv.waitKey(0)
        if k == ord("q"):
            break
    cv.destroyAllWindows()

def getNeighbors(img,p):
    neighbors = []
    for i in range(-1, 2, 2):
        if p[0]+i < img.shape[0] and p[0]+i >= 0 and img[p[0]+i, p[1]] == 0:
            neighbors.append([p[0]+i, p[1]])
        if p[1]+i < img.shape[1] and p[1]+i >= 0 and img[p[0], p[1]+i] == 0:
            neighbors.append([p[0], p[1]+i])
    return neighbors

def dist(p1,p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

#assume start and goals are tuples of (y,x)
def astar(img, start, goal):
    visited = []
    p = dist(start, goal)
    F = [(start, p)]
    while F != []:
        testPath, testPrice = F.pop(0)
        nk = [testPath[-2], testPath[-1]]
        if nk not in visited:
            visited.append(nk)
            if goal == nk:
                finalPath = []
                for i in range(0, len(testPath), 2):
                    finalPath.append(testPath[i:i+2])
                return finalPath
            newPaths = []
            for n in getNeighbors(img, nk):
                if n not in testPath:
                    p = dist(start, nk) + dist(nk, goal)
                    newPaths.append((testPath + n, p))
            F = F + newPaths
        F.sort(key = lambda x: x[1])
    return []

def findBlob(orig):
    (height,width,channels)=orig.shape
    lower_range = (254, 254, 254)
    upper_range = (256, 256, 256)
    mask = cv.inRange(orig, lower_range, upper_range)
    mask = mask.reshape(height,width,1)
    return mask

def drawPath(img,path):
    for p in path:
        cv.circle(img, (p[1], p[0]), 5, (125), -1)

def get_center(img):
    (height, width, channels) = img.shape
    sumx = 0
    sumy = 0
    count = 0
    for i in range(height):
        for j in range(width):
            if img[i][j] > 100:
                sumx += j
                sumy += i
                count += 1
    return int(sumx / count), int(sumy / count)

def testImage1():
    orig = cv.imread(cv.samples.findFile("testImage1.png"))
    thres = findBlob(orig)
    # note for the start and goal,
    # the coordinates are backwards
    # y is [0] and x is [1]
    start = [27, 26]
    goal = [4, 3]
    path = astar(thres, start, goal)
    return [thres,path]

def testImage2():
    orig = cv.imread(cv.samples.findFile("testImage2.png"))
    thres = findBlob(orig)
    # note for the start and goal,
    # the coordinates are backwards
    # y is [0] and x is [1]
    start = [30, 25]
    goal = [2,5]
    path = astar(thres, start, goal)
    return [thres,path]

#Example with a larger image
def testImage3():
    orig = cv.imread(cv.samples.findFile("testImage3.png"))
    (height, width, channels) = orig.shape

    #We have to resize here or else the astar will take forever
    scale = 10
    resize = cv.resize(orig, (int(width / scale), int(height / scale)))
    thres = findBlob(resize)
    # note for the start and goal,
    # the coordinates are backwards
    # y is [0] and x is [1]
    start = [30,50]
    goal = [4,10]

    path = astar(thres, start, goal)
    return [thres,path]

def task2():
    global callBackImg
    orig = cv.imread(cv.samples.findFile("task2.png"))

    start = cv.inRange(orig, (195, 113, 67), (197, 115, 69))
    start = start.reshape(start.shape[0], start.shape[1], 1)
    startX, startY = get_center(start)

    end = cv.inRange(orig, (70, 172, 111), (72, 174, 113))
    end = end.reshape(end.shape[0], end.shape[1], 1)
    endX, endY = get_center(end)

    img = cv.inRange(orig, (0, 0, 254), (0, 0, 256))
    img = img.reshape(img.shape[0], img.shape[1], 1)

    path = astar(img, [startY, startX], [endY, endX])
    print(path)
    drawPath(img, path)

    cv.circle(img, (startX, startY), 5, (125), -1)
    cv.circle(img, (endX, endY), 5, (125), -1)
    cv.imshow("Display window", img)
    while True:
        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite('testSave.png', callBackImg)
        elif k == ord('q'):
            break
    return 0

def task3():
    global callBackImg
    orig = cv.imread(cv.samples.findFile("task3.png"))

    start = cv.inRange(orig, (195, 113, 67), (197, 115, 69))
    start = start.reshape(start.shape[0], start.shape[1], 1)
    startX, startY = get_center(start)

    end = cv.inRange(orig, (70, 172, 111), (72, 174, 113))
    end = end.reshape(end.shape[0], end.shape[1], 1)
    endX, endY = get_center(end)

    img = cv.inRange(orig, (48, 124, 236), (50, 126, 238))
    img = img.reshape(img.shape[0], img.shape[1], 1)
    img = cv.bitwise_not(img)

    path = astar(img, [startY, startX], [endY, endX])
    print(path)
    drawPath(img, path)
    
    cv.circle(img, (startX, startY), 5, (125), -1)
    cv.circle(img, (endX, endY), 5, (125), -1)

    cv.imshow("Display window", img)
    while True:
        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite('testSave.png', callBackImg)
        elif k == ord('q'):
            break
    return 0

def main():
    [img, path] = testImage3()
    # [img,path] = testImage2()
    # [img, path] = testImage1()


    #We are assuming we are doing astar on smaller
    #images. We then have to resize them and the
    #paths back up
    (height,width,channels) = img.shape
    scale = 10
    resize = cv.resize(img,(width*scale,height*scale))
    (height, width) = resize.shape
    resize = resize.reshape(height, width, 1)
    rPath = []
    for p in path:
        rPath.append([p[0]*scale,p[1]*scale])

    print(rPath)

    drawPath(resize,rPath)
    showImage([resize])

if __name__ == '__main__':
    # main()
    # task2()
    task3()
