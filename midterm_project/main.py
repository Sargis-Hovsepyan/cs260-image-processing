from pre_processing import *

# Creating binary images of handwritings from cropped versions
input_folders = ["cs_handwriting_cropped/H101", "cs_handwriting_cropped/H102"]
output_folders = ["cs_handwriting_bin/H101", "cs_handwriting_bin/H102"]

os.makedirs(output_folders[0], exist_ok=True)
os.makedirs(output_folders[1], exist_ok=True)

tune_and_convert(input_folders[0], output_folders[0])
tune_and_convert(input_folders[1], output_folders[1])