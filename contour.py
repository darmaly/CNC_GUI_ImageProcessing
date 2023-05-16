import cv2
import numpy as np

from PIL import Image

# Load the input image
img = cv2.imread("ants.ppm")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Find the contours in the grayscale image
contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Create a black image
output = np.zeros_like(img)

# Draw the contours on the black image
cv2.drawContours(output, contours, -1, (0, 255, 0), 2)

# Save the output image
cv2.imwrite("output_image.ppm", output)