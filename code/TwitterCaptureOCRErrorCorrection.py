""" 
Author: Anna Ochab-Marcinek 
ochab@ichf.edu.pl
http://groups.ichf.edu.pl/ochab

Tested on: 
Python 3.6.10 :: Anaconda, Inc.
jupyter-notebook 6.0.3

This script 

Saves manual corrections of OCR errors to the CSV data file.


"""

#######################################################################################
import re
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
import matplotlib.dates as mdates
import glob
import requests
import sys
import os
import shutil
#######################################################################################
exec(open('../code/TwitterCaptureOther_functions.py').read())
# import TwitterCaptureImages_functions # For some reason, this doesn't work in my Jupyter notebook...(?)
############################################################################################################
# CSV data path
path = "../data/"
# Error log path
err_log_path = "../ocr_errors/"
# OCR correction file
corr_filename = err_log_path + 'OCR_error_correction.csv'
# Temporarily: Data range to display when running the script
data_range=slice(40,45,None)
# Temporarily: Max column width to display when running the script
max_column_width=20


# Automatically find the newest data file
data_filename = find_last_local_data_file()
# Copy as old version
shutil.copy(data_filename, data_filename+'.old')

# Load data file as data frame 
data_file_df = pd.read_csv(data_filename)
# Show part of the data csv file as a table (I need to improve this)
# Works in Jupyter notebook / IPython
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_colwidth', max_column_width)
display(data_file_df[data_range])
# Load OCR correction file as data frame
corr_file_df = pd.read_csv(corr_filename)
# Create dictionary from the data frame
corr_file_dict = dict(zip(corr_file_df['is'], corr_file_df['should be']))
# Replace wrong strings with correct values from dictionary
data_file_df.replace(corr_file_dict, inplace=True)

# Export the updated file to CSV
data_file_df.to_csv(data_filename, index=False)

# Show part of the new csv file as a table (I need to improve this)
# Works in Jupyter notebook / IPython
display(data_file_df[data_range])