import os
import cv2

def fine_tune(input_path, output_path):
    image = cv2.imread(input_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply auto-contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_img = clahe.apply(gray)

    # Apply Gaussian blur for smoothing
    blurred_img = cv2.GaussianBlur(enhanced_img, (5, 5), 0)

    # Increase contrast and brightness
    alpha = 1.2  # Contrast control (1.0 means no change)
    beta = 10    # Brightness control (0 means no change)
    contrast_bright_img = cv2.convertScaleAbs(blurred_img, alpha=alpha, beta=beta)

    # Convert to binary image
    _, binary_img = cv2.threshold(contrast_bright_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Save the fine-tuned image
    cv2.imwrite(output_path, binary_img)

def tune_and_convert(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace("_cropped.jpg", "_bin.jpg"))
            fine_tune(input_path, output_path)


input_folders = ["cs_handwriting_cropped/H101", "cs_handwriting_cropped/H102"]
output_folders = ["cs_handwriting_bin/H101", "cs_handwriting_bin/H102"]

os.makedirs(output_folders[0], exist_ok=True)
os.makedirs(output_folders[1], exist_ok=True)

tune_and_convert(input_folders[0], output_folders[0])
tune_and_convert(input_folders[1], output_folders[1])