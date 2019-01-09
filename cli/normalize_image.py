import cv2
import numpy
import os


source_path = "feima.png"
if not os.path.exists(source_path):
    raise FileNotFoundError(source_path)
source_image = cv2.imread(source_path, cv2.IMREAD_UNCHANGED)
cv2.imshow('original', source_image)
gray_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray_image, 127, 255, 0)
ret_image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(gray_image, contours, -1, (0, 255, 0), 3)
cv2.imshow('contours', gray_image)
mask = numpy.zeros_like(gray_image)
cv2.drawContours(mask, contours, -1, 255, -1)
output = numpy.zeros_like(gray_image)
output[mask == 255] = gray_image[mask == 255]
(x, y) = numpy.where(mask == 255)
(top_x, top_y) = (numpy.min(x), numpy.min(y))
(bottom_x, bottom_y) = (numpy.max(x), numpy.max(y))
output = source_image[top_x : bottom_x + 1 : , top_y : bottom_y + 1 : ]
bordersize = 10
border = cv2.copyMakeBorder(output, top = bordersize, bottom = bordersize, left = bordersize, right = bordersize, borderType = cv2.BORDER_CONSTANT, value = cv2.BORDER_DEFAULT)
cv2.imshow('ouput', output)
cv2.imshow('bordered', border)
cv2.imwrite('feima_ret.png', border)
cv2.waitKey(0)
cv2.destroyAllWindows()