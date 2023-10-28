Sanskrit OCR is a tool to convert images of Sanskrit text to english sentences! The main purpose of this project was to help prevent sanskrit texts from dissapearing by having a way to convert it and store in an online database.

Steps to run:
1. Have python installed! Made using Python 3.10.7
2. run pip install requirements.txt
3. Store your jpg files in images. Run main.py
4. Results will be generated in the results folder. Be sure to have unique names of the image files else they'll be overwritten in the results.

Note: 
1. Only images with jpg, png extensions will work. Will add support for more image types in the future!
2. Having CUDA installed in your system with a CUDA supported gpu will really help as the recognition model uses cuda features.