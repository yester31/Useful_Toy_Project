import cv2
import numpy as np

output_image = cv2.imread('./result.png')
input_image = cv2.imread('./0030.jpg')

length = int(input_image.shape[0] / 1)

# crop piece from original image
small_image = input_image[:length:, :length]
big_image = output_image[:length * 4, :length * 4]

# Merge small image to big image
big_image[0:length, 0:length] = small_image

# draw outline
cv2.rectangle(big_image, (0, 0), (length, length), (0, 0, 255), 3)

# show
cv2.imshow('Merged_image', big_image)
cv2.waitKey(0)

# save
cv2.imwrite('./compare.png', big_image)
