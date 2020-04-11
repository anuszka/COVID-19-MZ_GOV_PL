"""
Author: Anna Ochab-Marcinek 
ochab@ichf.edu.pl
http://groups.ichf.edu.pl/ochab

Tested on: 
Python 3.6.10 :: Anaconda, Inc.
jupyter-notebook 6.0.3

Functions to OCR images from the Twitter account of the Polish Health Ministry: https://twitter.com/MZ_GOV_PL

OCR image type 1 
ocr_hqsr(path_filename_in_)
returns: hospitalized, quarantined, supervised, recovered

OCR image type 2
ocr_t(path_filename_in_)
returns: tested

"""



#######################################################################################
from twitter_scraper import get_tweets
import re
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import matplotlib.dates as mdates
import glob
import requests
#######################################################################################
# OCR image type 1 
# returns: hospitalized, quarantined, supervised, recovered
def ocr_hqsr(path_filename_in_):
    # I can import packages inside a function, they are cached and are not re-imported unnecessarily.
    import cv2 
    import pytesseract
    
    # Read image
    img = cv2.imread(path_filename_in_)
    
    # Get image width in pixels
    width = img.shape[1] # img.shape[0] is image height
    
    # Cut the image, keep the right side
    ratio1 = 0.15 # custom ratio, adjusted for this particular image type
    width_cutoff = int(width * ratio1)
    
    # Left part: from 0 to the cutoff pixel
    # s1 = img[:, :width_cutoff]
    
    # Right part: from the cutoff pixel to width
    s2 = img[:, width_cutoff:]


    # Cut the new image, keep the left side
    ratio2 = 0.18 # custom ratio, adjusted for this particular image type
    width_cutoff = int(width * ratio2)
    # Left part: from 0 to the cutoff pixel
    s3 = s2[:, :width_cutoff]
#     cv2.imwrite(filename_out3, s3)

    # Take green channel to get rid of the red lines in the background
    B, G, R = cv2.split(s3) 

    # Tesseract configuration
    custom_config = r'--oem 3 --psm 6 -l eng tessedit_char_whitelist=0123456789'
    # OCR the green channel image
    output_str = pytesseract.image_to_string(G, config=custom_config)
    
    # Remove spaces
    output_str=output_str.replace(" ", "")

    # repr() : raw string
#     print(repr(output_str))
    
    # Split the string into a list by the dividers: '\n'
    output_list=output_str.split('\n')
    
    # Remove empty elements
    output_list = [i for i in output_list if i] 
    
    # Convert to int
    hospitalizowani, kwarantanna, nadzór, wyzdrowiali = output_list #[int(i) for i in output_list]  
    
    # print(hospitalizowani, kwarantanna, nadzór, wyzdrowiali)
    return hospitalizowani, kwarantanna, nadzór, wyzdrowiali

#############################################################################################
#
# OCR image type 2
# returns: tested
def ocr_t(path_filename_in_):
    # I can import packages inside a function, they are cached and are not re-imported unnecessarily.
    import cv2 
    import pytesseract
    # Read image
    img = cv2.imread(path_filename_in_)
    
    
    # Get image width in pixels
    width = img.shape[1] # img.shape[0] is image height
    
    # Cut the image, keep the left side
    ratio1 = 0.55 # custom ratio, adjusted for this particular image type
    width_cutoff = int(width * ratio1)
    # Left part: from 0 to the cutoff pixel
    s1 = img[:, :width_cutoff]

    # Tesseract configuration
    custom_config = r'--oem 3 --psm 11 -l eng -c tessedit_char_whitelist=0123456789'

    # OCR the image
    output_str =pytesseract.image_to_string(s1, config=custom_config)
    
    # Split the string into a list by the dividers: '\n'
    output_list=output_str.split('\n')
    
    # Remove empty elements
    output_list = [i for i in output_list if i] 
    
    # Convert to int; Only the 0-th element in the list is an actual number
    testy = int(output_list[0])
    return testy
#######################################################################################
