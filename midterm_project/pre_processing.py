import cv2, os, math
import numpy as np

"""
Description: This function takes an input image, processes it to remove
printed fragments and instructor marks, applies Gaussian blur, and then
saves the resulting binary image.

Parameters:
- input_path: String, the file path of the input image.
- output_path: String, the file path to save the resulting binary image.
"""

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

"""
Description: This function processes a folder of input images, applies the 
extract_handwriting function to each image, and saves the resulting binary
images in an output folder.

Parameters:
- input_folder: String, the path of the folder containing input images.
- output_folder: String, the path to save the resulting binary images.
"""

def extract_handwriting__and_convert(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace(".jpg", "_bin.jpg"))
            extract_handwriting(input_path, output_path)

################################# FINE TUNNING ###################################################
            
"""
Description: This function performs fine-tuning on an input image to enhance its quality.
It includes operations such as converting to grayscale, applying auto-contrast and Gaussian
blur, increasing contrast and brightness, converting to a binary image, and sharpening.

Parameters:
- input_path: String, the file path of the input image.
- output_path: String, the file path to save the fine-tuned image.
"""

def fine_tune(input_path, output_path):
    image = cv2.imread(input_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply auto-contrast & Gaussian Blure 
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_img = clahe.apply(gray)
    blurred_img = cv2.GaussianBlur(enhanced_img, (5, 5), 0)

    # Increase contrast and brightness
    alpha = 1.2  # Contrast control (1.0 means no change)
    beta = 10    # Brightness control (0 means no change)
    contrast_bright_img = cv2.convertScaleAbs(blurred_img, alpha=alpha, beta=beta)

    # Convert to binary image
    _, binary_img = cv2.threshold(contrast_bright_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Sharpening
    kernel_sharpening = np.array([[-1, -1, -1],
                                  [-1, 9, -1],
                                  [-1, -1, -1]])
    sharpened_image = cv2.filter2D(binary_img, -1, kernel_sharpening)

    # Save the fine-tuned image
    cv2.imwrite(output_path, sharpened_image)

"""
Description: This function processes a folder of input images, applies the fine_tune
function to each image, and saves the resulting fine-tuned images in an output folder.

Parameters:
- input_folder: String, the path of the folder containing input images.
- output_folder: String, the path to save the resulting fine-tuned images.
"""

def tune_and_convert(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace("_cropped.jpg", "_bin.jpg"))
            fine_tune(input_path, output_path)


################################# FEATURE SELECTION #############################################

"""
Description: This function takes the path of a binary image, reads it, and evaluates
the size and orientation of the page. It calculates the area and orientation of the
largest contour in the image, assuming it corresponds to the page.

Parameters:
- path (String): The path of the binary image.

Returns:
- size: The area of the largest contour (page size).
- orientation: The orientation angle of the page.
- If no contours are found, it returns None.
"""

def evaluate_page_properties(path):
    # Read the image
    binary_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # Evaluate size and orientation of the page
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        # Assuming the largest contour corresponds to the page
        largest_contour = max(contours, key=cv2.contourArea)
        page_size = cv2.contourArea(largest_contour)
        page_orientation = cv2.minAreaRect(largest_contour)[-1]

        # Convert orientation angle to the range [0, 180) degrees
        if page_orientation < -45:
            page_orientation += 90

        # Return the results in a dictionary
        return { "size": page_size, "orientation": page_orientation }
    else:
        print("No contours found. Unable to evaluate page properties.")
        return None

"""
Description: This function takes the path of a binary image, reads it, 
and evaluates the font size. It finds contours in the image, calculates the
bounding box for each contour, and extracts the width of each bounding box.
It filters out small widths as noise and returns the mean width as the font
size.

Parameters:
- path (String): The path of the binary image.

Returns:
- font_size: The mean width of the contours.
- If no contours are found, it returns None.
"""

def evaluate_font_size(path):
    # Read the image
    binary_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        print("No contours found. Unable to evaluate font size.")
        return None

    # Calculate the bounding box for each contour
    bounding_boxes = [cv2.boundingRect(contour) for contour in contours]

    # Extract the width of each bounding box
    widths = [box[2] for box in bounding_boxes]

    # Filter out extremely small widths as noise
    widths = [width for width in widths if width > 5]
    if len(widths) == 0:
        print("No valid widths found. Unable to evaluate font size.")
        return None

    return np.mean(widths)

"""
Description: This function takes the path of a binary image, reads it,
and evaluates the baseline orientation. It finds contours in the image,
sorts them by their y-coordinate, and calculates the differences between
consecutive y-coordinates. It then determines if the baseline is ascending,
descending, or balanced based on a threshold.

Parameters:
- path (String): The path of the binary image.

Returns:
- baseline_orientation: "Ascending," "Descending," or "Balanced."
- If no contours are found, it returns None.
"""

def evaluate_baseline_orientation(path):
    # Read the image
    binary_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        print("No contours found. Unable to evaluate baseline orientation.")
        return None

    # Sort contours by their y-coordinate to get the order of text lines
    sorted_contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[1])

    # Extract the y-coordinates of the bounding boxes' top edges
    top_edges_y = [cv2.boundingRect(contour)[1] for contour in sorted_contours]

    # Check if there is only one contour
    if len(top_edges_y) <= 1:
        print("Only one contour found. Unable to evaluate baseline orientation.")
        return None

    # Calculate the differences between consecutive y-coordinates
    differences = np.diff(top_edges_y)

    # Threshold to determine if the baseline is ascending, descending, or balanced
    threshold = 5  # Adjust as needed
    max_difference = max(differences)

    if max_difference > threshold:
        if differences[0] > threshold:
            return "Descending"
        elif differences[-1] > threshold:
            return "Ascending"
    else:
        return "Balanced"

    return None

"""
Description: This function takes the path of a binary image, reads it,
and evaluates the letter slant. It finds contours in the image, sorts
them by their y-coordinate, calculates the angle of each bounding box, 
and determines if the letters are leaning left, right, or balanced based
on a threshold.

Parameters:
- path (String): The path of the binary image.

Returns:
- letter_slant: "Leaning Left," "Leaning Right," or "Balanced."
- If no contours are found, it returns None.
"""

def evaluate_letter_slant(path):
    # Read the image
    binary_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        print("No contours found. Unable to evaluate letter slant.")
        return None

    # Sort contours by their y-coordinate to get the order of text lines
    sorted_contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[1])

    # Extract the bounding boxes of the contours
    bounding_boxes = [cv2.boundingRect(contour) for contour in sorted_contours]

    # Calculate the angle of each bounding box
    angles = [box[-1] for box in bounding_boxes]

    # Filter out small angles as noise
    angles = [angle for angle in angles if abs(angle) > 2]
    if len(angles) == 0:
        print("No valid angles found. Unable to evaluate letter slant.")
        return None

    # Calculate the average angle
    average_angle = np.mean(angles)

    # Threshold to determine if letters are leaning left, right, or balanced
    threshold = 2  # Adjust as needed

    if average_angle > threshold:
        return "Leaning Right"
    elif average_angle < -threshold:
        return "Leaning Left"
    else:
        return "Balanced"

"""
Description: This function takes the path of a binary image, reads it,
and evaluates the inter-word spacing. It finds contours in the image,
sorts them by their x-coordinate, calculates the distances between
consecutive bounding boxes, and returns the average inter-word spacing.

Parameters:
- path (String): The path of the binary image.

Returns:
- inter_word_spacing: The average distance between words.
- If no contours are found, it returns None.
"""

def evaluate_inter_word_spacing(path):
    # Read the image
    binary_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        print("No contours found. Unable to evaluate inter-word spacing.")
        return None

    # Sort contours by their x-coordinate to get the order of words
    sorted_contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])

    # Extract the bounding boxes of the contours
    bounding_boxes = [cv2.boundingRect(contour) for contour in sorted_contours]

    # Calculate the distances between consecutive bounding boxes
    distances = np.diff([box[0] + box[2] for box in bounding_boxes])

    # Filter out small distances as noise
    distances = [distance for distance in distances if distance > 5]  # Adjust as needed
    if len(distances) == 0:
        print("No valid distances found. Unable to evaluate inter-word spacing.")
        return None

    # Calculate the average inter-word spacing
    return np.mean(distances)


################################# HOUGH TRANSFORM ###############################################

"""
Description: This function takes the path of a grayscale image, reads it,
and applies the Hough Transform to detect straight lines or line segments
in the image. It uses the Canny edge detector to highlight edges and then
applies Probabilistic Line Transform to identify and draw lines on the image.

Parameters:
- image_path (String): The path of the grayscale image.

Returns:
- The function displays the original image along with the detected lines in red using the Probabilistic Line Transform.

"""

def hough_transform(image_path):
    # Read the image
    src = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        return -1

    # Resize the source image to your desired window size
    target_window_size = (800, 600)
    src_resized = cv2.resize(src, target_window_size)

    dst = cv2.Canny(src_resized, 50, 200, None, 3)

    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)

    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)

    cv2.imshow("Source", src)
    cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


################################# REGION PROCESSING #############################################

def extract_regions(path, kernel_size=5, threshold_area=100):
    # Read the binary image
    binary_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    # Apply morphological operations
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilation = cv2.dilate(binary_image, kernel, iterations=2)
    erosion = cv2.erode(dilation, kernel, iterations=1)

    # Find contours in the binary image
    contours, _ = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    binary_regions = []

    # Iterate through contours
    for contour in contours:
        # Calculate area and filter small regions
        area = cv2.contourArea(contour)
        if area > threshold_area:
            # Draw rectangle around the region
            x, y, w, h = cv2.boundingRect(contour)
            binary_regions.append(binary_image[y:y+h, x:x+w])

    return binary_regions