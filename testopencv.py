import numpy as np
import cv2
from matplotlib import pyplot as plt
img_file = 'unc-8_3_2.tif'
#img_file = "a.jpg"
def show_img(img) :
    plt.imshow(img, cmap='gray', interpolation='bicubic')
    plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
    plt.show()

# Load an color image in grayscale
img = cv2.imread('unc-8_3_2.tif')

def is_contour_bad(c):
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) > 20:
        print len(approx)
    # the contour is 'bad' if it is not a rectangle
    return len(approx) == 6




def test():
    image = cv2.imread('unc-8_3_2.tif')
#padding since the t-shirt is touching the border, without this we cant get a continious contour around it.
    #image = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imgray = cv2.GaussianBlur(imgray, (9, 9), 0)
    ret, thresh = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if is_contour_bad(c):
            cv2.drawContours(image, [c], 0, (0, 255, 0), 3)
    plt.imshow(image)
    plt.show()


def test2():
    image = cv2.imread(img_file)
    edged = cv2.Canny(image, 1000, 200)

    # find contours in the image and initialize the mask that will be
    # used to remove the bad contours
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.ones(image.shape[:2], dtype="uint8") * 255

    # loop over the contours
    for c in cnts:
        # if the contour is bad, draw it on the mask
        if is_contour_bad(c):
            cv2.drawContours(mask, [c], -1, 0, -1)

    # remove the contours from the image and show the resulting images
    image = cv2.bitwise_and(image, image, mask=mask)
    cv2.imshow("Mask", mask)
    cv2.imshow("After", image)
    cv2.waitKey(0)


def test_canny():
    img = cv2.imread(img_file, 3)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img,1200,100)
    #kern = np.ones((5,5))
    #edges = cv2.dilate(edges, kern)
    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()

def test_() :
    CANNY_THRSH_LOW = 1000
    CANNY_THRSH_HIGH = 2000
    img = cv2.imread(img_file)
    edge = cv2.Canny(img, CANNY_THRSH_LOW, CANNY_THRSH_HIGH, apertureSize=5)
    kern = np.ones((5, 5))
    # dilatation connects most of the disparate edges
    edge = cv2.dilate(edge, kern)
    # invert edges to create one big water blob
    edge_inv = np.zeros((img.shape), np.uint8)
    edge_inv.fill(255)
    print edge_inv, edge
    edge_inv = edge_inv - edge
    contours0, hierarchy0 = cv2.findContours(edge_inv.copy(), cv2.RETR_EXTERNAL,
                                             cv2.CHAIN_APPROX_SIMPLE)


test()
#test_canny()
#test2()
    #show_img(img)
