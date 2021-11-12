import cv2 as cv
import sys
import numpy as np

callBackImg = None
cX = 0
cY = 0


def printRGB(event, x, y, flags, params):
    # EVENT_MOUSEMOVE
    if event == cv.EVENT_LBUTTONDOWN:
        print(str(x) + " " + str(y) + " " + str(callBackImg[y][x][2]) + " " + str(callBackImg[y][x][1]) + " " + str(
            callBackImg[y][x][0]))


def mouseCallback(event, x, y, flags, param):
    # EVENT_MOUSEMOVE
    global cX, cY
    if event == cv.EVENT_MOUSEMOVE:
        cX = x
        cY = y
    elif event == cv.EVENT_LBUTTONDOWN:
        print(str(x) + " " + str(y) + " (" + str(callBackImg[y][x]) + ", " + str(callBackImg[y][x]) + ", " + str(
            callBackImg[y][x]) + ")")


def myGray(orig):
    (height, width, channels) = orig.shape
    ret = np.zeros((height, width, 1), dtype=np.int8)
    for i in range(height):
        for j in range(width):
            g = int((int(orig[i][j][0]) + int(orig[i][j][1]) + int(orig[i][j][2])) / 3.0) - 128
            ret[i][j] = g
    return ret


def readVid():
    global callBackImg
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, callBackImg = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        cv.circle(callBackImg, (cX, cY), 10, (255, 0, 0), 1)
        cv.imshow("Display window", callBackImg)
        cv.setMouseCallback("Display window", mouseCallback)

        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite('savedFrame.png', callBackImg)
        elif k == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


def readIMG():
    global callBackImg
    orig = cv.imread(cv.samples.findFile("testImage1.png"))
    print(orig.shape)
    gray = myGray(orig)
    callBackImg = gray
    cv.imshow("Display window", gray)
    cv.setMouseCallback("Display window", mouseCallback)

    while True:
        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite('testSave.png', callBackImg)
        elif k == ord('q'):
            break


def segment(orig, lower, upper):
    (height, width, channels) = orig.shape
    ret = np.zeros((height, width, 1), dtype=np.int8)
    for i in range(height):
        for j in range(width):
            if lower[0] <= orig[i][j][0] <= upper[0] >= orig[i][j][1] >= lower[1] and upper[2] >= orig[i][j][2] >= \
                    lower[2]:
                ret[i][j] = 127
            else:
                ret[i][j] = -128
    return ret


def get_center(blue):
    (height, width, channels) = blue.shape
    sumx = 0
    sumy = 0
    count = 0
    for i in range(height):
        for j in range(width):
            if blue[i][j] > 100:
                sumx += j
                sumy += i
                count += 1
    return int(sumx / count), int(sumy / count)


def dilate(orig):
    (height, width, channels) = orig.shape
    ret = np.zeros((height - 2, width - 2, 1), dtype=np.int8)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            found = False
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if orig[i + x][j + y] == 255:
                        found = True
            if found:
                ret[i - 1][j - 1] = 127
            else:
                ret[i - 1][j - 1] = -128

    return ret


def erode(orig):
    (height, width, channels) = orig.shape
    ret = np.zeros((height - 2, width - 2, 1), dtype=np.int8)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            found = False
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if orig[i + x][j + y] == 0:
                        found = True
            if found:
                ret[i - 1][j - 1] = -128
            else:
                ret[i - 1][j - 1] = 127

    return ret


def laplacian(orig):
    (height, width, channels) = orig.shape
    ret = np.zeros((height - 2, width - 2, 1), dtype=np.int8)
    kernel = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            value = -128
            for x in range(-1, 2):
                for y in range(-1, 2):
                    value = value + orig[i + x][j + y] * kernel[x + 1][y + 1]
            ret[i - 1][j - 1] = value

    return ret


def hor_sobel(orig):
    (height, width, channels) = orig.shape
    ret = np.zeros((height - 2, width - 2, 1), dtype=np.int8)
    kernel = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            value = -128
            for x in range(-1, 2):
                for y in range(-1, 2):
                    value = value + orig[i + x][j + y] * kernel[x + 1][y + 1]
            ret[i - 1][j - 1] = value

    return ret


def vert_sobel(orig):
    (height, width, channels) = orig.shape
    ret = np.zeros((height - 2, width - 2, 1), dtype=np.int8)
    kernel = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            value = -128
            for x in range(-1, 2):
                for y in range(-1, 2):
                    value = value + orig[i + x][j + y] * kernel[x + 1][y + 1]
            ret[i - 1][j - 1] = value

    return ret


def task1():
    global callBackImg
    orig = cv.imread(cv.samples.findFile("testImage1.png"))

    # blue = segment(orig, (203, 71, 62),(205, 73, 64))
    blue = cv.inRange(orig, (203, 71, 62), (205, 73, 64))
    blue = blue.reshape(blue.shape[0], blue.shape[1], 1)

    centerX, centerY = get_center(blue)
    callBackImg = blue
    cv.circle(callBackImg, (centerX, centerY), 5, 125, -1)

    cv.imshow("Display window", blue)
    cv.setMouseCallback("Display window", mouseCallback)
    while True:
        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite('testSave.png', callBackImg)
        elif k == ord('q'):
            break


def task2():
    global callBackImg
    orig = cv.imread(cv.samples.findFile("testImage1.png"))

    blue = cv.inRange(orig, (203, 71, 62), (205, 73, 64))
    blue = blue.reshape(blue.shape[0], blue.shape[1], 1)
    # blue = erode(blue)
    # blue = dilate(blue)

    kernel = np.ones((3, 3), np.uint8)
    # blue = cv.dilate(blue, kernel, iterations=1)
    blue = cv.erode(blue, kernel, iterations=1)
    blue = blue.reshape(blue.shape[0], blue.shape[1], 1)

    centerX, centerY = get_center(blue)
    callBackImg = blue
    cv.circle(callBackImg, (centerX, centerY), 5, 125, -1)

    cv.imshow("Display window", blue)
    cv.setMouseCallback("Display window", mouseCallback)
    while True:
        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite('testSave.png', callBackImg)
        elif k == ord('q'):
            break


def task3():
    global callBackImg
    orig = cv.imread(cv.samples.findFile("testImage1.png"))

    blue = cv.inRange(orig, (203, 71, 62), (205, 73, 64))
    blue = blue.reshape(blue.shape[0], blue.shape[1], 1)

    kernel = np.ones((3, 3), np.uint8)
    blue = cv.erode(blue, kernel, iterations=1)
    blue = blue.reshape(blue.shape[0], blue.shape[1], 1)

    # blue = laplacian(blue)
    # blue = hor_sobel(blue)
    # blue = vert_sobel(blue)

    blue = cv.Laplacian(src=blue, dst=blue, ddepth=-1)
    blue = blue.reshape(blue.shape[0], blue.shape[1], 1)
    # blue = cv.Sobel(src=blue, dst=blue, ddepth=-1, dx=0, dy=1, ksize=3)  # Horizontal
    # blue = cv.Sobel(src=blue, dst=blue, ddepth=-1, dx=1, dy=0, ksize=3)  # Vertical

    centerX, centerY = get_center(blue)
    callBackImg = blue
    cv.circle(callBackImg, (centerX, centerY), 5, 125, -1)

    cv.imshow("Display window", blue)
    cv.setMouseCallback("Display window", mouseCallback)
    while True:
        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite('testSave.png', callBackImg)
        elif k == ord('q'):
            break

def task4() :
    global callBackImg
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, callBackImg = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        segmented = cv.inRange(callBackImg, (20, 30, 140), (80, 100, 255))
        segmented = segmented.reshape(segmented.shape[0], segmented.shape[1], 1)


        kernel = np.ones((3, 3), np.uint8)
        segmented = cv.erode(segmented, kernel, iterations=1)
        segmented = segmented.reshape(segmented.shape[0], segmented.shape[1], 1)

        centerX, centerY = get_center(segmented)
        callBackImg = segmented
        cv.circle(callBackImg, (centerX, centerY), 5, 125, -1)
        cv.imshow("Display window", callBackImg)
        cv.setMouseCallback("Display window", mouseCallback)

        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite('savedFrame.png', callBackImg)
        elif k == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


def task5() :
    global callBackImg
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, callBackImg = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        segmented = cv.inRange(callBackImg, (20, 30, 180), (255, 255, 255))
        segmented = segmented.reshape(segmented.shape[0], segmented.shape[1], 1)

        num_labels, labels, stats, centroids = cv.connectedComponentsWithStats(segmented, 4)

        max = -1
        max_index = 0
        for i in range(num_labels) :
            if stats[i, cv.CC_STAT_AREA] > max :
                max = stats[i, cv.CC_STAT_AREA]
                max_index = i

        cX, cY = centroids[max_index]
        cX = int(cX)
        cY = int(cY)
        print(cX, cY)

        callBackImg = segmented
        cv.circle(callBackImg, (cX, cY), 5, 125, -1)
        cv.imshow("Display window", callBackImg)
        cv.setMouseCallback("Display window", mouseCallback)

        k = cv.waitKey(1)
        if k == ord('s'):
            cv.imwrite('savedFrame.png', callBackImg)
        elif k == ord('q'):
            break


if __name__ == '__main__':
    task5()
    #readVid()
