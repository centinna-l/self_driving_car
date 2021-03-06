import cv2
import numpy as np
import matplotlib.pyplot as plt

# step1- convert the image to grayscale then use the gaussian blur
#


def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1, y1, x2, y2])


def canny(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    canny = cv2.Canny(blur_image, 50, 150)
    return canny


def average_slope_intercept(image, lines):
    left_lines = []
    right_lines = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_lines.append((slope, intercept))
        else:
            right_lines.append((slope, intercept))
    left_fit_average = np.average(left_lines, axis=0)
    right_fit_average = np.average(right_lines, axis=0)
    left_lines = make_coordinates(image, left_fit_average)
    right_lines = make_coordinates(image, right_fit_average)
    return np.array([left_lines, right_lines])


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image


def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

    # to insert the image we use the imread() function of the openCV
image = cv2.imread('test_image.jpg')

# now we have a copy of the image so we can convert the image to greyscale

lane_image = np.copy(image)

# canny_image = canny(lane_image)
# cropped_image = region_of_interest(canny_image)
# lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100,
#                         np.array([]), minLineLength=40, maxLineGap=5)
# average_lines = average_slope_intercept(lane_image, lines)
# lines_image = display_lines(lane_image, average_lines)
# combo_image = cv2.addWeighted(lane_image, .8, lines_image, 1, 1)
# cv2.imshow('result', combo_image)
# cv2.waitKey(0)


# we use gaussianblur to remove unwanted noise and
# blur the image inorder to get the better edge
# GaussianBlur(image, (kernerl,kernel), deviation)
# cv2.VideoCapture is used to capture the video
# we use the .read() to get the two value
# '_'represents the boolean
# frame is the individual images frames of the video

cap_video = cv2.VideoCapture("test2.mp4")
while(cap_video.isOpened):
    _, frame = cap_video.read()
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100,
                            np.array([]), minLineLength=40, maxLineGap=5)
    average_lines = average_slope_intercept(frame, lines)
    lines_image = display_lines(frame, average_lines)
    combo_image = cv2.addWeighted(frame, .8, lines_image, 1, 1)
    cv2.imshow('result', combo_image)
    if cv2.waitKey(1) == ord('q'):
        break
cap_video.release()
cap_video.destroyAllWindows()
# we have completed the lanes finding using the hough transform.
#ssh is working
