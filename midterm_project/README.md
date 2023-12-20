# Midterm Project

The course project is a part of a larger project that aims at predicting of student progress in CS and IT
disciplines based of their handwriting samples. It is expected to apply in its framework several Image
Processing methods to identify and extract graphical features that could be used in the subsequent studies.
Several Project stages are outlined below. After Stage 0, the stages can be addressed and implemented in an
arbitrary order. Depending on the progress, additional or modified stages may also be posted. You are
welcome to import and use OCR methods after proper acknowledgement and brief description.

## Stage 0: Store the images

Created a new folder cs_handwriting. Hard copies of handwriting samples were scanned with a phone and uploaded in 
cs_handwriting with an individual code on each page. The code format is CRS.TST.ddmmyy.Cxxx (course name, test, date, 
lookup index – a letter H, M or L followed by 3 digits). Created subfolders for each Cxxx and saved in them the images 
of all pages with such Cxxx. Named the files after the code specifying the page number as a suffix after the underscore,
like CRS.TST.ddmmyy.Cxxx_p1.jpg.

## Stage 1: Eeliminate the printed text and preprocess

The cropped versions of each page is uploaded in cs_handwriting_croped folder, in appropriate subfolder. The cropped
versions contain only the code fragments, the pages that had almost no handwritting on them were ommited. The croping was 
acheved with photoshop. After cropping the pictures were fine tuned with gaussian blure and increase in contras and brightness,
additional noise was ommited. The refined versions are binarised and uploaded in cs_handwriting_bin for later processing. The 
refined versions were created by tune.py script. As long as it is run it updates the cs_handwriting_bin. Settings of tunning
can be adjusted from tune.py

The remove_printed_text is a script that does what is described above. Due to low quality pictures it was better gtgtto remove
the printed text with photoshop. The script is valid and can be applied to scanned images with very high quality.