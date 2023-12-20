import cv2
import numpy as np

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