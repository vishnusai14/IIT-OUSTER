import cv2
import numpy as np
from skimage.io import imread
from skimage.morphology import remove_small_objects

rgb = imread('./plot.png')
# convert to HSV for thresholding
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)

# threshold hue channel for purple tubes, value channel for blue tubes
thresh_hue = cv2.threshold(hsv[..., 0], 127, 255, cv2.THRESH_BINARY)[1]
thresh_val = cv2.threshold(hsv[..., 2], 200, 255, cv2.THRESH_BINARY)[1]

# combine purple tubes with blue tubes
thresh = thresh_hue | thresh_val

cv2.imwrite('threshold_result.png', thresh)

# morphologically close the gaps between purple and blue tubes
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

cv2.imwrite('closing_result.png', thresh)

# morphological opening with horizontal and vertical kernels
h_kernel = np.zeros((11, 11), dtype=np.uint8)
h_kernel[5, :] = 1

v_kernel = np.zeros((11, 11), dtype=np.uint8)
v_kernel[:, 5] = 1

h_tubes = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, h_kernel, iterations=6)
v_tubes = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, v_kernel, iterations=7)

cv2.imwrite('horizontal_tubes.png', h_tubes)
cv2.imwrite('vertical_tubes.png', v_tubes)

# find contours and draw rectangles with constant widths through centers
h_contours = cv2.findContours(h_tubes, cv2.RETR_LIST,
                              cv2.CHAIN_APPROX_SIMPLE)[0]
h_lines = np.zeros(thresh.shape, np.uint8)

for cnt in h_contours:
    x, y, w, h = cv2.boundingRect(cnt)
    y += int(np.floor(h / 2) - 4)
    cv2.rectangle(h_lines, (x, y), (x + w, y + 8), 255, -1)

v_contours = cv2.findContours(v_tubes, cv2.RETR_LIST,
                              cv2.CHAIN_APPROX_SIMPLE)[0]
v_lines = np.zeros(thresh.shape, np.uint8)

for cnt in v_contours:
    x, y, w, h = cv2.boundingRect(cnt)
    x += int(np.floor(w / 2) - 4)
    cv2.rectangle(v_lines, (x, y), (x + 8, y + h), 255, -1)

# combine horizontal and vertical lines
all_lines = h_lines | v_lines

cv2.imwrite('all_lines.png', all_lines)

# remove small objects around the intersections
xor = np.bool8(h_lines ^ v_lines)
removed = xor ^ remove_small_objects(xor, 350)

result = all_lines & ~removed * 255

cv2.imwrite('result.png', result)
