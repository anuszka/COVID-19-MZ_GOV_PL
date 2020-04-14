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

Improved image filtering.

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
import cv2 
import pytesseract

#######################################################################################
# Open preview window
def preview(img, window_title="Preview"):
    # Preview window
    cv2.imshow(window_title, img)
    # Wait for key press
    cv2.waitKey(0)
    return

#######################################################################################
# Get image heigth and width in pixels
# returns: height, width
def getshape(img):
    height = img.shape[0]
    width = img.shape[1]
    return height,width
#######################################################################################
# Cut image
# arguments:
#   img : image
#   keep='left' ,'right, 'top' , 'bottom' : which part of the image to keep
#   ratio : position of the cutoff pixel as the ratio of image width or height
# returns:
#   newimg : new image
def imgcut(img, ratio, keep='left'):
    # Get image heigth and width in pixels
    height, width = getshape(img)
    # Cut the image, keep the right side
    width_cutoff = int(width * ratio)
    height_cutoff = int(height * ratio)
    if keep=='right':
        # Right part: from the cutoff pixel to width
        newimg = img[:, width_cutoff:]
    elif keep=='left':
        # Left part: from 0 to the cutoff pixel
        newimg = img[:, :width_cutoff]
    elif keep=='top':
        # Top part: from 0 to the cutoff pixel
        newimg = img[ :height_cutoff , :]
    elif keep=='bottom':
        # Bottom part: from the cutoff pixel to height (i.e., bottom)
        newimg = img[height_cutoff: , :]
    return newimg

#######################################################################################
# Apply threshold to the image
# returns: new image
def threshold(img, thr): 
    img[img >= thr]= 255
    img[img < thr] = 0
    return img;

#######################################################################################
# Invert image
def invert(img):
    img[:]= -img[:]+255
    return img


#######################################################################################
# OCR image type 1 
# returns: hospitalized, quarantined, supervised, recovered
def ocr_hqsr(path_filename_in_, show_preview=False):
    # I can import packages inside a function, they are cached and are not re-imported unnecessarily.
    
    # Read image
    img = cv2.imread(path_filename_in_)
    
    ###########################
    # Preview window
    if show_preview: preview(img)
    ###########################
    
    s1 = imgcut(img, ratio=0.17, keep='right')
    
    ###########################
    # Preview window
    if show_preview: preview(s1, 's1')
    ###########################

    s2= imgcut(s1, ratio=0.2, keep='left')
    
    ###########################
    # Preview window
    if show_preview: preview(s2, 's2')
    ###########################

   
    s3= imgcut(s2, ratio=0.22, keep='bottom')

       
    ###########################
    # Preview window
    if show_preview: preview(s3, 's3')
    ###########################
   
    
    
    # Take green channel to get rid of the red lines in the background
    B, G, R = cv2.split(s3) 

    ###########################
    # Preview window
    if show_preview: preview(G)
    ###########################

    # Apply threshold to the image
    mythreshold = 200 # custom threshold, adjusted for this particular image type
    G1 = threshold(G, mythreshold)
    
    # Invert image
    G2 = invert(G1)
    
    ###########################
    # Preview window
    if show_preview: preview(G2)
    ###########################
   
    
    # Tesseract configuration
    custom_config = r'--oem 3 --psm 6 -l eng tessedit_char_whitelist=0123456789'
    # OCR the green channel image
    output_str = pytesseract.image_to_string(G2, config=custom_config)
    
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
    
    # Needed to correctly close preview windows, if used
    cv2.destroyAllWindows()
    
    # print(hospitalizowani, kwarantanna, nadzór, wyzdrow iali)
    return hospitalizowani, kwarantanna, nadzór, wyzdrowiali

#############################################################################################
#
# OCR image type 2
# returns: tested
def ocr_t(path_filename_in_, show_preview=False):
    # I can import packages inside a function, they are cached and are not re-imported unnecessarily.
    # Read image
    img = cv2.imread(path_filename_in_)
    
    
    # Get image width in pixels
    height, width = getshape(img)
   

    s1 = imgcut(img, ratio=0.55, keep='left')

    
    ###########################
    # Preview window
    if show_preview: preview(s1)
    ###########################
     

    s2 = imgcut(s1, ratio=0.30, keep='bottom')

    
    ###########################
    # Preview window
    if show_preview: preview(s2)
    ###########################

    s3 = imgcut(s2, ratio=0.35, keep='top')
    
    ###########################
    # Preview window
    if show_preview: preview(s3)
    ###########################

        
    # Take green channel to get rid of the red lines in the background
    B, G, R = cv2.split(s3) 

    ###########################
    # Preview window
    if show_preview: preview(G)
    ###########################

   
    # Apply threshold to the image
    mythreshold = 200 # custom threshold, adjusted for this particular image type
    G1 = threshold(G, mythreshold)

    
    
    # Invert image
    G2=invert(G1)
    ###########################
    # Preview window
    if show_preview: preview(G2)
    ###########################

    
    # Tesseract configuration
    custom_config = r'--oem 3 --psm 11 -l eng -c tessedit_char_whitelist=0123456789'

    # OCR the image
    output_str =pytesseract.image_to_string(G2, config=custom_config)
    
    # Split the string into a list by the dividers: '\n'
    output_list=output_str.split('\n')
    
    # Remove empty elements
    output_list = [i for i in output_list if i] 
    
    # Convert to int; Only the 0-th element in the list is an actual number
    testy = int(output_list[0])
    
    # Needed to correctly close preview windows, if used
    cv2.destroyAllWindows()
    
    return testy
#######################################################################################
