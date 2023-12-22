from pre_processing import *

## Creating binary images of handwritings from cropped versions ##

# Step 1: Crop images, fine tune and make them binary

input_folders = ["cs_handwriting_cropped/H101", "cs_handwriting_cropped/H102"]
output_folders = ["cs_handwriting_bin/H101", "cs_handwriting_bin/H102"]

os.makedirs(output_folders[0], exist_ok=True)
os.makedirs(output_folders[1], exist_ok=True)

tune_and_convert(input_folders[0], output_folders[0])
tune_and_convert(input_folders[1], output_folders[1])


## Doing Pre-processing on an image as an example ##

path = "cs_handwriting_bin\H102\OOP.MT1.170215.H102_p2_bin.jpg"

# Step 2: Evaluate page properties
page_properties = evaluate_page_properties(path)
print("\nPage Properties:", page_properties)

# Step 3: Evaluate baseline orientation
baseline_orientation = evaluate_baseline_orientation(path)
print("Baseline Orientation:", baseline_orientation)

# Step 4: Evaluate letter slant
letter_slant = evaluate_letter_slant(path)
print("Letter Slant:", letter_slant)

# Step 5: Evaluate inter-word spacing
inter_word_spacing = evaluate_inter_word_spacing(path)
print("Inter-Word Spacing:", inter_word_spacing)

# Step 6: Evaluate font size
font_size = evaluate_font_size(path)
print("Font Size:", font_size)

# Step 7: Even could apply hough_transform to see the lines
# hough_transform(path)

# Step 8: Evaluations of regions and region info
regions, region_features = evaluate_regions(path)

for i, feature in enumerate(region_features):
    print(f"\nRegion {i + 1} Details:")
    print(f" - Location (x, y): ({feature['x']}, {feature['y']})")
    print(f" - Size: {feature['size']}")
    print(f" - Aspect Ratio: {feature['aspect_ratio']}")
    print(f" - Width: {feature['width']}")
    print(f" - Height: {feature['height']}")
    print("\n")