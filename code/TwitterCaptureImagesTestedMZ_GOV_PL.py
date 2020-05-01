"""
Author: Anna Ochab-Marcinek 
ochab@ichf.edu.pl
http://groups.ichf.edu.pl/ochab

Tested on: 
Python 3.6.10 :: Anaconda, Inc.
jupyter-notebook 6.0.3

This script 

1. Gets data on COVID-19:
tested (cumulative numbers) 
in Poland
from the Twitter account of the Polish Health Ministry: https://twitter.com/MZ_GOV_PL
    a) Get the images from Twitter
    b) OCR the images to get numbers
    
2. Updates an existing local CSV data file.
Prerequisites: 
    a) The old data file must exist.
    b) The old data file name format must be the following: old_csv_file_name = path + "cor." + day_str + ".csv" 
    where day_str = date_i_days_ago.strftime("%Y.%m.%d")
    For example, the old data file is: ../cor.2020.04.07.csv
    c) The old data file should have the following column headers:
    Data,Dzień,Wykryci zakażeni,Testy,Hospitalizowani,Zmarli,Kwarantanna,Nadzór,"Testy, wartości przybliżone",Kwarantanna po powrocie do kraju,Wydarzenia,Wyzdrowiali
    d) The following is a bit inconsistent but, for historical reasons: 
        - Column names are in Polish; in particular, the date column name is 'Data'. 
        - However, dates in the date column must be in American date format:
        myfile_date_format = '%m/%d/%Y'
Output is written to: new_csv_file_name = path + "cor." + today_str + ".csv"


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
import sys 
#######################################################################################
# OCR image type 2
# ocr_t(path_filename_in_)
# returns: tested
exec(open('../code/TwitterCaptureImages_functions.py').read())
# import TwitterCaptureImages_functions # For some reason, this doesn't work in my Jupyter notebook...(?)
#######################################################################################
exec(open('../code/TwitterCaptureOther_functions.py').read())
#######################################################################################

# CSV data path
path = "../data/"

# Path to the directory for captured images
imgpath = "../twitter_images/"

# Path to the directory for captured data (CSV)
twitter_data_path = "../twitter_captured_data/"

# Twitter user account
twitter_user = 'MZ_GOV_PL'

# Number of Twitter pages to read
pages_number=2

# Temporarily: Data range to display when running the script
data_range=slice(55,65,None)
# Temporarily: Max column width to display when running the script
max_column_width=20

# Strings to find in tweets
start = 'W ciągu doby wykonano'
# middle = '/'
# # mark parentheses with backslash to avoid misinterpretation!
# end = '\(wszystkie pozytywne przypadki/w tym osoby zmarłe\)' 

# Create a dictionary of tweets
tweets = []
print_spacer()
print("Getting tweets from", twitter_user, "...")
for i in get_tweets(twitter_user, pages=pages_number):
    tweets.append(i) 
# print(repr(tweets))

# Convert tweets to pandas.DataFrame
df=pd.DataFrame.from_dict(tweets)


# Select rows in df which contain the string defined in the start variable
# and create df_tested (our twitter data frame)
df_tested=df[df['text'].str.contains(start, na=False)]


# Add a new column to the twitter data frame: 'tested' 
df_tested = df_tested.reindex(
    df_tested.columns.tolist() + ['tested'], axis=1) 
df_tested = df_tested.reindex(
    df_tested.columns.tolist() + ['persons tested'], axis=1)

# Download images that contain data
# Find the numbers of tested in the images.
# Write these numbers in the 'tested' column.
# df_tested.iterrows() returns the list: index, row
# index : a row index (a number)
# row : whole row
for index, row in df_tested.iterrows(): 
    # Get image url
    photo_url = row['entries'].get('photos')[0]
    # Get image time stamp
    timestamp = row['time'].strftime("%Y.%m.%d")
    # Download image
    myfile = requests.get(photo_url)
    # Write image; image name will have the time stamp.
    img_file_name = imgpath+"TCImageTestedMZ_GOV_PL."+timestamp+".jpg"
    open(img_file_name, 'wb').write(myfile.content)
    # OCR image to get the cumulative number of tested patients
    
    d1=pd.to_datetime(row['time'])
    d2=datetime(2020,4,28,0,0,0) # change of image format on this date
    if(d1>=d2): 
        tested, persons_tested = ocr_t(img_file_name)
    else:
        tested, persons_tested = ocr_t_old(img_file_name), np.NaN # for old image format
    
    # Insert the cumulative number of tested patients the 'tested' column of df_tested.
    df_tested.loc[index,'tested'] = tested
    df_tested.loc[index,'persons tested'] = persons_tested

# Convert the 'tested' column to int
df_tested = df_tested.astype({'tested': 'Int64', 'persons tested': 'Int64'})


# Reset index (because old indexes were inherited from df) 
df_tested = df_tested.reset_index(drop=True)

# For check, write the downloaded data to a file: 
# data_file_name = path+"TCImageTestedMZ_GOV_PL."+today_str+".csv"
df_tested_to_export = df_tested[['time', 'tested', 'persons tested']]
today = date.today()
today_str = today.strftime("%Y.%m.%d")

captured_data_file_name = twitter_data_path+"TCTestedMZ_GOV_PL."+today_str+".csv"

df_tested_to_export.to_csv (captured_data_file_name, index = False, header=True)
# For some reason, the numbers entered to columns are float... This is probably to keep NaNs...


# Update the existing CSV data file
# 
# Automatically find the previous data file
i=0
filename = find_last_local_data_file()


# For some reason, I can't use the result of glob.glob(filename) above (why?)
# I use the filename instead
old_csv_file_name = filename
new_csv_file_name = path + "cor." + today_str + ".csv"
# Read the latest existing CSV data file
myfile_df = pd.read_csv(old_csv_file_name)

# Show part of the old csv file as a table (I need to improve this)
# Works in Jupyter notebook / IPython
# Display more columns in Ipython
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_colwidth', max_column_width)
display(myfile_df[data_range])


# The newest row index is 0 in the tweets data frame df_confirmed_deaths
# Newest date in df_tested, read as string
newest_twitter_date_str = df_tested.loc[0,'time']

# Note that my csv file uses the American date format!
myfile_date_format = '%m/%d/%Y'

# Convert newest_twitter_date to myfile_date_format.
# newest_twitter_date is the date corresponding to the last record of my Twitter data.
newest_twitter_date = newest_twitter_date_str.strftime(myfile_date_format)

# This will be the row index of my csv file corresponding to the last record of my Twitter data.
# In other words, the row with newest_myfile_index will have the same date as newest_twitter_date.
# For now, we set it to 0.
newest_myfile_index = 0

# To get newest_myfile_index:
# Search for newest_twitter_date in all rows of myfile_df, in the 'Data' column
for myfile_index, row in myfile_df.iterrows():
    # For some reason, I need to re-format the 'Data' column content (...?)
    reformatted_date = pd.to_datetime(row['Data']).strftime(myfile_date_format)
    # If newest_twitter_date is found in myfile_df:
    if reformatted_date == newest_twitter_date:
        # Remember newest_myfile_index
        newest_myfile_index  = myfile_index
#         print("reformatted_date, newest_twitter_date", reformatted_date, newest_twitter_date)


# Update my file        
# We will loop through the rows of my file data and Twitter data 
# and overwrite the data in my file with the Twitter data
myfile_increment_index=0
twitter_increment_index=0

# df_tested.tail(1).index.item() : last index
last_twitter_index = df_tested.tail(1).index.item()

# Loop from the 0-th to last row in the Twitter data:
# print("before loop")
# print("twitter_increment_index, last_twitter_index", twitter_increment_index, last_twitter_index)
# Strange bug: This loop works only if there are more than 2 images downloaded...
while twitter_increment_index<=last_twitter_index:
    myfile_df.loc[newest_myfile_index-myfile_increment_index, 'Testy'] =\
    df_tested.loc[twitter_increment_index,'tested']
    myfile_df.loc[newest_myfile_index-myfile_increment_index, 'Testowane osoby'] =\
    df_tested.loc[twitter_increment_index,'persons tested']
    # Go to the previous day in my csv file: move by one row (each row is one day in that file)
    myfile_increment_index = myfile_increment_index + 1
    # Go to the previous day in my csv file: move by one row (each row is one day in that file)
    twitter_increment_index = twitter_increment_index + 1
    


   
print_message("Captured images written to local directory:", imgpath)
print_message("Captured data written to local data file:", captured_data_file_name)

# Show the captured data
# Works in Jupyter notebook / IPython        
display(df_tested_to_export)
print_spacer()

# Export the updated file to CSV
myfile_df.to_csv(new_csv_file_name, index=False)
print("Update written to local data file:", new_csv_file_name)

# Show part of the new csv file as a table (I need to improve this)
# Works in Jupyter notebook / IPython
display(myfile_df[data_range])
