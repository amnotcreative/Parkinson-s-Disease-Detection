import cv2
import numpy as np

# Read the input image from the user
img = cv2.imread("test samples/6.jpg")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding to create a binary image
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Find the contours in the binary image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Find the contour with the largest area
max_area = 0
largest_contour = None
for contour in contours:
    area = cv2.contourArea(contour)
    if area > max_area:
        max_area = area
        largest_contour = contour

# Find the minimum area rectangle that bounds the largest contour
rect = cv2.minAreaRect(largest_contour)

# Determine the angle of rotation of the rectangle with respect to the y-axis
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
theta = rect[2]
if theta < -45:
    theta += 90

# Calculate the angle with respect to the y-axis
angle = theta if rect[1][1] > rect[1][0] else theta + 90

# Print the angle of skew
skew_angle = 90 - angle
print("Angle of skew: ", skew_angle)


if(skew_angle > -10 and skew_angle <=10): 
    print("Sample is probably of a healthy person")
else:
    print("Sample is probably of a Parkinson's patient")