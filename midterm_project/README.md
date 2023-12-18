# Midterm Project

The course project is a part of a larger project that aims at predicting of student progress in CS and IT
disciplines based of their handwriting samples. It is expected to apply in its framework several Image
Processing methods to identify and extract graphical features that could be used in the subsequent studies.
Several Project stages are outlined below. After Stage 0, the stages can be addressed and implemented in an
arbitrary order. Depending on the progress, additional or modified stages may also be posted. You are
welcome to import and use OCR methods after proper acknowledgement and brief description.

## Stage 0: Store the images

Create a new folder /cs_handwriting in the same repository your HW01 is uploaded. Hard copies of handwriting
samples were given for scan/digitalization with an individual code on each page. The code format is
CRS.TST.ddmmyy.Cxxx (course name, test, date, lookup index – a letter H, M or L followed by 3 digits).
Create in the folder /cs_handwriting subfolder for each Cxxx and save in them the images of all pages with
such Cxxx. Name the files after the code specifying the page number as a suffix after the underscore, like
CRS.TST.ddmmyy.Cxxx_p1.png or CRS.TST.ddmmyy.Cxxx_p1.jpg. If there are several images of the same page specify 
the copy in parentheses, like CRS.TST.ddmmyy.Cxxx_p1(2).jpg.

## Stage 1: Eeliminate the printed text

Study the color distribution in each image using RGB and grayscale histograms. Suggest and test a method for 
automated removal of the printed test. If needed, suggest and test a method for automated removal of instructor’s 
marks (normally appearing in red shades). Having the handwriting extracted, suggest a test a method to crop it.
Convert the cropped image to binary format and save it under a filename CRS.TST.ddmmyy.Cxxx_p1_bin.png. 
Adjust the brightness/contrast before the conversion as needed (for example, auto-contrast, histogram match, etc.).