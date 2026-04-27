import cv2
import numpy as np
from rembg import remove

img_path = "./SAMPLE EXPLANATION IMAGES/1-input.jpg"
img = cv2.imread(img_path)
img = cv2.resize(img, (960, 540)) 
# Selecting a range of image
r = cv2.selectROI("select the area", img)
# r = [X, Y, width, height]
# print(r)

start_row = r[1]
end_row = r[1]+r[3]
start_col = r[0]
end_col = r[0]+r[2]
# Crop image (with numpy arrays) - source_image[ start_row : end_row, start_col : end_col]
cropped_image = img[start_row:end_row, start_col:end_col]

# to remove the background of the image
rmbg_img = remove(cropped_image)

# converting to gray scale, so it would be easy to find the contours in the image
gray = cv2.cvtColor(rmbg_img, cv2.COLOR_BGR2GRAY)
# for better accuracy
edges = cv2.Canny(gray, 30, 200)

# finding the contours, edges. The second parameter is the cv2.RETR_EXTERNAL, which finds the external contours of the image. The cv2.CHAIN_APPROX_NONE simply stores all possible points of the contours. To get all (internal and external) the contours present in an image the second parameter should be, cv2.RETR_LIST.
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# -1 to say we want all the contours to be displayed in the image, can be 1 to show only 1 contour present, 2 for 2 contours and so on.. next parameter to represent the color of the contour and last parameter to denote the thickness of the contour line.
cv2.drawContours(rmbg_img, contours, -1, (0,255,0), 2)

# Display contoured image
cv2.imshow("Cropped image", rmbg_img)
# cv2.waitKey(0)

# print(img.shape, rmbg_img.shape)
# ones = np.ones((img.shape[0], img.shape[1]))*255
# img = np.dstack([img, ones])

print(img.shape, rmbg_img.shape)
img[start_row:end_row, start_col:end_col, 0] = rmbg_img[:, :, 0]
print(img.shape, rmbg_img.shape)

# alpha_image_3 = rmbg_img[:, :, 3] / 255.0
# alpha_image = 1 - alpha_image_3
# for c in range(0, 3):
#     img[start_row:end_row, start_col:end_col, c] = ((alpha_image*rmbg_img[:, :, c]) + (alpha_image_3*img[start_row:end_row, start_col:end_col, c]))

cv2.imshow("final", img)
cv2.waitKey(0)
