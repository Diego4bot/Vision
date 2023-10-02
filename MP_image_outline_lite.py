#Outline CV2 and mediapipe

import cv2
import numpy as np


# Load the image
image = cv2.imread('C:/Users/user/Documents/Vision MP/girlX.jpg')

# Convert the image from BGR to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Apply a median blur to the grayscale image
gray = cv2.medianBlur(gray, 5)

# Detect edges in the grayscale image using the Canny algorithm
edges = cv2.Canny(gray, 50, 150)

# Apply a dilation operation to the edges to fill in gaps
kernel = np.ones((1, 1), np.uint8)
dilated = cv2.dilate(edges, kernel, iterations=1)

# Apply a threshold operation to the dilated edges to obtain a binary mask
ret, mask = cv2.threshold(dilated, 50, 200, cv2.THRESH_BINARY)

# Invert the binary mask to obtain the hair mask
hair_mask = cv2.bitwise_not(mask)

# Apply the hair mask to the original image
hair = cv2.bitwise_and(image, image, mask=hair_mask)

# Show the results
cv2.imshow('Original Image', image)
cv2.imshow('Hair Mask', hair_mask)
cv2.imshow('Hair', hair)
cv2.waitKey(0)
cv2.destroyAllWindows()
