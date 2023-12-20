import os
import cv2
import numpy as np

def extract_handwriting(input_path, output_path):
    # Read the input image
    image = cv2.imread(input_path)

    # Remove printed fragments
    mask = cv2.inRange(image, (0, 0, 0), (120, 100, 80))
    inv_mask = cv2.bitwise_not(mask)
    kernel = np.ones((5, 5), np.uint8)
    inv_mask = cv2.erode(inv_mask, kernel, iterations=1)
    inv_mask = cv2.merge((inv_mask,)*3)
    image_filter = np.where(inv_mask == 0, (255, 255, 255), image)
    image_filter = np.where(image_filter > (240, 240, 240), (255, 255, 255), image)

    # Remove instructor marks
    (R, G, B) = cv2.split(image_filter)
    img_ = np.uint8(B)
    mask_b = np.where(img_ > 180, 255, 0)
    mask_b = cv2.merge((mask_b,)*3)
    final_img = np.where(mask_b == 0, image, 255)

    final_img = cv2.GaussianBlur(final_img, (5, 5), 0)

    # Save the binary image
    cv2.imwrite(output_path, final_img)

def extract_and_convert(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace(".jpg", "_bin.jpg"))
            extract_handwriting(input_path, output_path)

input_folders = ["cs_handwriting/H101", "cs_handwriting/H102"]
output_folders = ["cs_handwriting_bin/H101", "cs_handwriting_bin/H102"]

os.makedirs(output_folders[0], exist_ok=True)
os.makedirs(output_folders[1], exist_ok=True)

extract_and_convert(input_folders[0], output_folders[0])
extract_and_convert(input_folders[1], output_folders[1])