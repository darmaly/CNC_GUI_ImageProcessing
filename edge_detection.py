import cv2
import os

# Load image
image = cv2.imread('ants.ppm')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blur = cv2.GaussianBlur(gray, (3, 3), 0)

# Perform Canny edge detection
edges = cv2.Canny(blur, 100, 200)

# Save resulting image to current working directory
filename = 'edges.ppm'
cv2.imwrite(os.path.join(os.getcwd(), filename), edges, [cv2.IMWRITE_PXM_BINARY, 1])

# Display resulting image
cv2.imshow('Edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()