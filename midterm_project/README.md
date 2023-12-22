# Midterm Project

The course project is part of a larger project that aims to predict student progress in CS and IT
disciplines based on their handwriting samples. It is expected to apply in its framework several Image
Processing methods to identify and extract graphical features that could be used in the subsequent studies.
Several Project stages are outlined below. After Stage 0, the stages can be addressed and implemented in an
arbitrary order. Depending on the progress, additional or modified stages may also be posted. You are
welcome to import and use OCR methods after proper acknowledgment and a brief description.

## Store the images

Created a new folder, cs_handwriting. Hard copies of handwriting samples were scanned with a phone and uploaded in 
cs_handwriting with an individual code on each page. The code format is CRS.TST.ddmmyy.Cxxx (course name, test, date, 
lookup index – a letter H, M, or L followed by three digits). Created subfolders for each Cxxx and saved in them the images 
of all pages with such Cxxx. Named the files after the code specifying the page number as a suffix after the underscore,
like CRS.TST.ddmmyy.Cxxx_p1.jpg.

## Eliminate the printed text and preprocess

The cropped versions of each page are uploaded in the cs_handwriting_croped folder in the appropriate subfolder. The cropped
versions contain only the code fragments. The pages that had almost no handwriting on them were omitted. The cropping was 
achieved with Photoshop. After cropping, the pictures were fine-tuned with Gaussian blur, an increase in contrast and brightness, 
and additional noise was omitted. The refined versions are binarised and uploaded in cs_handwriting_bin for later processing.
The refined versions were created with the help of the Fine Tunnig script segment at pre_processing module. As long as it is
running, it updates the cs_handwriting_bin. Settings of tunning can be adjusted from Fine Tunning segment of the module.

The The first segment of the module is a script that does what is described above. Due to low-quality pictures, it was 
better to remove the printed text with Photoshop. The script is valid and can be applied to scanned images with very
high quality.

## Evaluate page features

The pre_processing.py contains functions designed to evaluate various aspects of handwritten text, contributing to the 
task of predicting student performance based on handwriting. 

* The `evaluate_page_properties` function analyzes the size and orientation of the page, providing insights into the structure of the
handwritten content. This information can be crucial for normalizing features in subsequent analyses. 
* The `evaluate_font_size` function assesses the average width of characters, offering a measure of the writing style and potentially
indicating variations in letter formation. 
* The `evaluate_baseline_orientation` function determines whether the baseline of the handwritten text is ascending, descending, or balanced,
which could provide valuable information about the writer's emotional state or emphasis.
* The `evaluate_letter_slant` function evaluates the overall slant of the handwritten text, providing insights into the stylistic aspects of
the writing. 
* Lastly, the `evaluate_inter_word_spacing` function calculates the average distance between words, capturing the spatial arrangement of the text.

These functions collectively contribute to the extraction of meaningful features from handwritten samples, forming a foundation for subsequent
analyses aimed at predicting student progress in computer science and information technology disciplines.

Here is an example image and example output of the functions mentioned above:

![](https://github.com/Sargis-Hovsepyan/cs260-image-processing/blob/master/midterm_project/cs_handwriting_bin/H102/OOP.MT1.170215.H102_p2_bin.jpg)

The featurs of the image:

```
Page Size:                2287034.5
Page Orientation:         90.0
Baseline Orientation:     Descending
Avarage Word Spacing:     1352.0
Avarage Font Size:        1844.0
Avarage Line Slant:       Leaning Right
```

## Evaluate page features (Hough Transform)

Applied Hough Transform to detect straight lines/segments in the cropped binary handwriting samples. In the realm of handwriting 
analysis for predicting student performance, the Hough Transform adds a layer of precision to existing evaluations. While previous 
assessments, such as baseline detection and spacing analysis, offer valuable insights, the Hough Transform systematically detects lines 
and orientations, providing a more detailed understanding of structural elements. This includes capturing subtle variations in baselines
and detecting minute slants. Integrating the Hough Transform enriches the analysis, offering a standardized representation of handwriting
features and enhancing the predictive power of models by discerning intricate patterns and nuances in students' writing.

Here is an example of Hough transform on the sample image mentioned above:

![](https://github.com/Sargis-Hovsepyan/cs260-image-processing/blob/master/midterm_project/cs_handwriting/Hough.png)

## Evaluation of Regions

The evaluate_regions function in the pre_processing module plays a crucial role in the context of student performance prediction
through handwriting analysis. By processing a binary image, it identifies distinct regions within the document, such as paragraphs
or headings. For each region, it extracts features like size, aspect ratio, and spatial coordinates. These features provide valuable
insights into the spatial organization and characteristics of a student's handwriting, reflecting aspects like text size, proportions,
and layout. The function enables a personalized analysis of different regions, contributing essential information to a holistic set of
features for machine learning models. This comprehensive approach aids in predicting student performance by capturing nuanced patterns
in the handwritten content. The significance of the function lies in its ability to derive meaningful handwriting features, facilitating
a detailed and tailored assessment for performance prediction tasks.

Here is the evaluation of the the regions of the iage displayed in this document:

```
Region 1 Details:
 - Location (x, y): (491, 1239)
 - Size: 0.0
 - Aspect Ratio: 1.0
 - Width: 1
 - Height: 1

Region 2 Details:
 - Location (x, y): (1843, 875)
 - Size: 0.0
 - Aspect Ratio: 1.0
 - Width: 1
 - Height: 1

Region 3 Details:
 - Location (x, y): (1843, 855)
 - Size: 0.0
 - Aspect Ratio: 1.0
 - Width: 1
 - Height: 1

Region 4 Details:
 - Location (x, y): (0, 0)
 - Size: 2287034.5
 - Aspect Ratio: 1.4847020933977455
 - Width: 1844
 - Height: 1242
```