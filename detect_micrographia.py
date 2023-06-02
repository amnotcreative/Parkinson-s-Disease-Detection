import cv2
import numpy as np

# Read the image
img = cv2.imread('test samples/writing_2.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply image filters to enhance the contrast and remove noise
blur = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Compute the horizontal projection profile
h_proj = np.sum(thresh, axis=1)

# Threshold the horizontal projection profile to detect the lines
line_thresh = 37.5  # 1/8th of an inch at 300 DPI
lines = []
line_start = None
for i in range(len(h_proj)):
    if h_proj[i] > line_thresh and line_start is None:
        line_start = i
    elif h_proj[i] < line_thresh and line_start is not None:
        lines.append((line_start, i))
        line_start = None

# Compute the average height of the lines
line_heights = [line[1] - line[0] for line in lines]
avg_line_height = sum(line_heights) / len(line_heights) if len(line_heights) > 0 else 0

# Skip the rest of the code if the average line height is 0
if avg_line_height == 0:
    print("No lines detected.")
else:
    # Extract the regions corresponding to each line
    line_regions = [thresh[line[0]:line[1], :] for line in lines]

    # Compute the average of each line
    line_averages = []
    for region in line_regions:
        line_avg = np.mean(region)
        line_averages.append(line_avg)
    # Determine if the handwriting sample exhibits micrographia
    micrographia_threshold = 12 
    if np.mean(line_averages) >= micrographia_threshold:
        print("Micrographia detected.")
    else:
        print("No micrographia detected.")
