from process.feature_selection import *

# Example usage
path = "cs_handwriting_bin\H102\OOP.MT1.170215.H102_p2_bin.jpg"

props = evaluate_page_properties(path)
font_size = evaluate_font_size(path)
baseline = evaluate_baseline_orientation(path)
slant = evaluate_letter_slant(path)
space = evaluate_inter_word_spacing(path)

print("\n")
print("Page Size:               ", props["size"])
print("Page Orientation:        ", props["orientation"])
print("Baseline Orientation:    ", baseline)
print("Avarage Word Spacing:    ", space)
print("Avarage Font Size:       ", font_size)
print("Avarage Line Slant:      ", slant)