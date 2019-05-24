import cv2
import matplotlib.pyplot as plt

image = cv2.imread('test_image.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#cv2.imshow('orignal image ', image)
plt.imshow('gray image ', gray)

cv2.waitKey(0)
cv2.destroyAllWindows()
