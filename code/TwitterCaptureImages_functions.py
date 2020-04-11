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
#######################################################################################""" 
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
#######################################################################################

# OCR image type 1 
# ocr_hqsr(path_filename_in_)
# returns: hospitalized, quarantined, supervised, recovered
exec(open('../code/TwitterCaptureImages_functions.py').read())
# import TwitterCaptureImages_functions # For some reason, this doesn't work in my Jupyter notebook...(?)
############################################################################################################

# CSV data path
path = "../data/"

# Path to the directory for captured images
imgpath = "../twitter_images/"

# Path to the directory for captured data (CSV)
twitter_data_path = "../twitter_captured_data/"

# Twitter user account
twitter_user = 'MZ_GOV_PL'

# Number of Twitter pages to read
pages_number=3


# Strings to find in tweets
start = 'Dzienny raport o'
# middle = '/'
# # mark parentheses with backslash to avoid misinterpretation!
# end = '\(wszystkie pozytywne przypadki/w tym osoby zmarłe\)' 

# Create a dictionary of tweets
tweets = []
print("Getting tweets from", twitter_user, "...")
for i in get_tweets(twitter_user, pages=pages_number):
    tweets.append(i) 
# print(repr(tweets))

# Convert tweets to pandas.DataFrame
df=pd.DataFrame.from_dict(tweets)

# display(df)

# Select rows in df which contain the string defined in the start variable
# and create df_hqsr (our twitter data frame)
df_hqsr=df[df['text'].str.contains(start, na=False)]


# Add a new column to the twitter data frame: 'tested' 
df_hqsr = df_hqsr.reindex(
    df_hqsr.columns.tolist() + ['hospitalized','quarantined','supervised','recovered'], axis=1) 

# Download images that contain data
# Find the numbers of tested in the images.
# Write these numbers in the 'tested' column.
# df_hqsr.iterrows() returns the list: index, row
# index : a row index (a number)
# row : whole row
for index, row in df_hqsr.iterrows(): 
    # Get image url
    photo_url = row['entries'].get('photos')[0]
    # Get image time stamp
    timestamp = row['time'].strftime("%Y.%m.%d")
    # Download image
    myfile = requests.get(photo_url)
    # Write image; image name will have the time stamp.
    img_file_name = imgpath+"TCImageHqsrMZ_GOV_PL."+timestamp+".jpg"
    open(img_file_name, 'wb').write(myfile.content)
    # OCR image to get the cumulative number of tested patients
    # number_list contains: hospitalized, quarantined, supervised, recovered
    numbers = ocr_hqsr(img_file_name)
    labels=['hospitalized', 'quarantined', 'supervised', 'recovered']
    
    # Create a dictionary from two lists
    labels_numbers = {labels[i]: numbers[i] for i in range(len(labels))} 
    
    for label in labels_numbers:
        # print(label, labels_numbers[label])
        number_str = labels_numbers[label]
        is_number = all(map(str.isdigit, number_str))
        if(is_number):
        # Insert the cumulative number of tested patients the 'tested' column of df_hqsr.
            df_hqsr.loc[index,label] = int(number_str)
        else:
            df_hqsr.loc[index,label] = number_str
            print("Warning! ", label, ":", number_str, " is not a number in", img_file_name )


# For some reason, the numbers entered to columns are float...    
# Convert the 'tested' column to int  
# df_hqsr = df_hqsr.astype({'hospitalized':int,'quarantined':int,'supervised':int,'recovered':int})

# Reset index (because old indexes were inherited from df) 
df_hqsr = df_hqsr.reset_index(drop=True)

# For check, write the downloaded data to a file: 
df_hqsr_to_export = df_hqsr[['time', 'hospitalized','quarantined','supervised','recovered']]
today = date.today()
today_str = today.strftime("%Y.%m.%d")

captured_data_file_name = twitter_data_path+"TChqsrMZ_GOV_PL."+today_str+".csv"
df_hqsr_to_export.to_csv (captured_data_file_name, index = False, header=True)



# Update the existing CSV data file
# 
# Automatically find the previous data file
i=0
while i<7:
    # Get a time stamp i days from now
    date_i_days_ago = datetime.now() - timedelta(days=i)
    # Format the time stamp
    day_str = date_i_days_ago.strftime("%Y.%m.%d")
    # This should be the name of the data file created i days ago (if it exists)
    filename = path + "cor." + day_str+".csv"
    # Check if the data file created i days ago exists
    file_found =  glob.glob(filename)
    if file_found:
        print("Last local data file found:" , file_found[0])
        i=7
    i=i+1


# For some reason, I can't use the result of glob.glob(filename) above (why?)
# I use the filename instead
old_csv_file_name = filename
new_csv_file_name = path + "cor." + today_str + ".csv"
# Read the latest existing CSV data file
myfile_df = pd.read_csv(old_csv_file_name)

# Show part of the old csv file as a table (I need to improve this)
# Works in Jupyter notebook / IPython
display(myfile_df[30:45])


# The newest row (0) in the tweets data frame df_hqsr
newest_twitter_index = 0

# Newest date in df_hqsr, read as string
newest_twitter_date_str = df_hqsr.loc[newest_twitter_index,'time']

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

# df_hqsr.tail(1).index.item() : last index
last_twitter_index = df_hqsr.tail(1).index.item()

# Loop from the 0-th to last row in the Twitter data:
# print("before loop")
# print("twitter_increment_index, last_twitter_index", twitter_increment_index, last_twitter_index)
# Strange bug: This loop works only if there are more than 2 images downloaded...
# For some reason it does not update under the last index
while twitter_increment_index<=last_twitter_index:
#     print("in loop")
    # Get the dates for the new rows
    # Note the difference in time ordering of my csv file data and the Twitter data:
    # newest_myfile_index-myfile_increment_index : we move up my csv file
    # newest_twitter_index+twitter_increment_index : we move down the Twitter data
    myfile_date = \
        pd.to_datetime(myfile_df.loc[newest_myfile_index-myfile_increment_index, 'Data']).\
        strftime(myfile_date_format)
    twitter_date = df_hqsr.loc[newest_twitter_index+twitter_increment_index,'time'].\
        strftime(myfile_date_format)
    #print(myfile_date, twitter_date)
    # This will be OK at the 0-th increment 
    # because newest_myfile_index and newest_twitter_index have already been found.
    myfile_df.loc[newest_myfile_index-myfile_increment_index, 'Hospitalizowani'] =\
      df_hqsr.loc[newest_twitter_index+twitter_increment_index,'hospitalized']
    myfile_df.loc[newest_myfile_index-myfile_increment_index, 'Kwarantanna'] =\
      df_hqsr.loc[newest_twitter_index+twitter_increment_index,'quarantined']
    myfile_df.loc[newest_myfile_index-myfile_increment_index, 'Nadzór'] =\
      df_hqsr.loc[newest_twitter_index+twitter_increment_index,'supervised']
    myfile_df.loc[newest_myfile_index-myfile_increment_index, 'Wyzdrowiali'] =\
      df_hqsr.loc[newest_twitter_index+twitter_increment_index,'recovered']
# Zmienić to na pętlę po słowniku
     
    # Go to the previous day in my csv file: move by one row (each row is one day in that file)
    myfile_increment_index = myfile_increment_index + 1
    
    # Try to go to the previous day in Twitter data: move by one row
    twitter_increment_index = twitter_increment_index + 1
    


    
#     # There may be more entries for one day in Twitter data.
#     # If the  current dates in my file data and Twitter data don't match, 
#     # go one row further in Twitter data and check again.
#     while twitter_date != myfile_date:
#         twitter_increment_index = twitter_increment_index + 1
#         twitter_date = df_hqsr.loc[newest_twitter_index+twitter_increment_index,'time']\
#            .strftime(myfile_date_format)   
#     #print(myfile_date, twitter_date)
      

print("Captured images written to local directory", imgpath)
print("Captured data written to local data file:", captured_data_file_name)
# Show the captured data
# Works in Jupyter notebook / IPython
display(df_hqsr_to_export)        


# Export the updated file to CSV
myfile_df.to_csv(new_csv_file_name, index=False)
print("Update written to local data file:", new_csv_file_name)

# Show part of the new csv file as a table (I need to improve this)
# Works in Jupyter notebook / IPython
display(myfile_df[30:45])""" 
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
#######################################################################################
# OCR image type 2
# ocr_t(path_filename_in_)
# returns: tested
exec(open('../code/TwitterCaptureImages_functions.py').read())
# import TwitterCaptureImages_functions # For some reason, this doesn't work in my Jupyter notebook...(?)
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
pages_number=3


# Strings to find in tweets
start = 'W ciągu doby wykonano'
# middle = '/'
# # mark parentheses with backslash to avoid misinterpretation!
# end = '\(wszystkie pozytywne przypadki/w tym osoby zmarłe\)' 

# Create a dictionary of tweets
tweets = []
print("Getting tweets from", twitter_user, "...")
for i in get_tweets(twitter_user, pages=pages_number):
    tweets.append(i) 
# print(repr(tweets))

# Convert tweets to pandas.DataFrame
df=pd.DataFrame.from_dict(tweets)

# display(df)

# Select rows in df which contain the string defined in the start variable
# and create df_tested (our twitter data frame)
df_tested=df[df['text'].str.contains(start, na=False)]


# Add a new column to the twitter data frame: 'tested' 
df_tested = df_tested.reindex(
    df_tested.columns.tolist() + ['tested'], axis=1) 

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
    tested = ocr_t(img_file_name)
    # Insert the cumulative number of tested patients the 'tested' column of df_tested.
    df_tested.loc[index,'tested'] = tested


# For some reason, the numbers entered to columns are float...    
# Convert the 'tested' column to int  
df_tested = df_tested.astype({'tested': int})

# Reset index (because old indexes were inherited from df) 
df_tested = df_tested.reset_index(drop=True)

# For check, write the downloaded data to a file: 
# data_file_name = path+"TCImageTestedMZ_GOV_PL."+today_str+".csv"
df_tested_to_export = df_tested[['time', 'tested']]
today = date.today()
today_str = today.strftime("%Y.%m.%d")

captured_data_file_name = twitter_data_path+"TCTestedMZ_GOV_PL."+today_str+".csv"
df_tested_to_export.to_csv (captured_data_file_name, index = False, header=True)



# Update the existing CSV data file
# 
# Automatically find the previous data file
i=0
while i<7:
    # Get a time stamp i days from now
    date_i_days_ago = datetime.now() - timedelta(days=i)
    # Format the time stamp
    day_str = date_i_days_ago.strftime("%Y.%m.%d")
    # This should be the name of the data file created i days ago (if it exists)
    filename = path + "cor." + day_str+".csv"
    # Check if the data file created i days ago exists
    file_found =  glob.glob(filename)
    if file_found:
        print("Last local data file found:" , file_found[0])
        i=7
    i=i+1


# For some reason, I can't use the result of glob.glob(filename) above (why?)
# I use the filename instead
old_csv_file_name = filename
new_csv_file_name = path + "cor." + today_str + ".csv"
# Read the latest existing CSV data file
myfile_df = pd.read_csv(old_csv_file_name)

# Show part of the old csv file as a table (I need to improve this)
# Works in Jupyter notebook / IPython
display(myfile_df[30:45])


# The newest row (0) in the tweets data frame df_tested
newest_twitter_index = 0

# Newest date in df_tested, read as string
newest_twitter_date_str = df_tested.loc[newest_twitter_index,'time']

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
while twitter_increment_index<last_twitter_index:
#     print("in loop")
    # This will be OK at the 0-th increment 
    # because newest_myfile_index and newest_twitter_index have already been found.
    myfile_df.loc[newest_myfile_index-myfile_increment_index, 'Testy'] =\
      df_tested.loc[newest_twitter_index+twitter_increment_index,'tested']
      
    # Go to the previous day in my csv file: move by one row (each row is one day in that file)
    myfile_increment_index = myfile_increment_index + 1
    
    # Try to go to the previous day in Twitter data: move by one row
    twitter_increment_index = twitter_increment_index + 1
    
    # Get the dates for the new rows
    # Note the difference in time ordering of my csv file data and the Twitter data:
    # newest_myfile_index-myfile_increment_index : we move up my csv file
    # newest_twitter_index+twitter_increment_index : we move down the Twitter data
    myfile_date = \
        pd.to_datetime(myfile_df.loc[newest_myfile_index-myfile_increment_index, 'Data']).\
        strftime(myfile_date_format)
    twitter_date = df_tested.loc[newest_twitter_index+twitter_increment_index,'time'].\
        strftime(myfile_date_format)
#     print(myfile_date, twitter_date)
    
#     # There may be more entries for one day in Twitter data.
#     # If the  current dates in my file data and Twitter data don't match, 
#     # go one row further in Twitter data and check again.
#     while twitter_date != myfile_date:
#         twitter_increment_index = twitter_increment_index + 1
#         twitter_date = df_tested.loc[newest_twitter_index+twitter_increment_index,'time']\
#            .strftime(myfile_date_format)   
#     #print(myfile_date, twitter_date)
      
print("Captured images written to local directory", imgpath)    
print("Captured data written to local data file:", captured_data_file_name)
# Show the captured data
# Works in Jupyter notebook / IPython        
display(df_tested_to_export)


# Export the updated file to CSV
myfile_df.to_csv(new_csv_file_name, index=False)
print("Update written to local data file:", new_csv_file_name)

# Show part of the new csv file as a table (I need to improve this)
# Works in Jupyter notebook / IPython
display(myfile_df[30:45])""" 
Author: Anna Ochab-Marcinek 
ochab@ichf.edu.pl
http://groups.ichf.edu.pl/ochab

Tested on: 
Python 3.6.10 :: Anaconda, Inc.
jupyter-notebook 6.0.3


This script 

1. Gets data on 
confirmed COVID-19 cases (cumulative numbers) 
and 
COVID-19 deaths (cumulative numbers)
in Poland
from the Twitter account of the Polish Health Ministry: https://twitter.com/MZ_GOV_PL

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
#######################################################################################


# CSV data path
path = "../data/"

# Path to the directory for captured data (CSV)
twitter_data_path = "../twitter_captured_data/"

# Twitter user account
twitter_user = 'MZ_GOV_PL'

# Number of Twitter pages to read
pages_number=3


# Strings to find in tweets
start = 'iczba zakażonych koronawirusem'
middle = '/'
# mark parentheses with backslash to avoid misinterpretation!
end = '\(wszystkie pozytywne przypadki/w tym osoby zmarłe\)' 

# Create a dictionary of tweets
tweets = []
print("Getting tweets from", twitter_user, "...")
for i in get_tweets(twitter_user, pages=pages_number):
    tweets.append(i) 

# Convert tweets to pandas.DataFrame
df=pd.DataFrame.from_dict(tweets)


# Select rows in df which contain the string defined in the start variable
# and create df_confirmed_deaths (our twitter data frame)
df_confirmed_deaths=df[df['text'].str.contains(start, na=False)]

# Add new columns to the twitter data frame: 'confirmed' and 'deaths' 
df_confirmed_deaths = df_confirmed_deaths.reindex(
    df_confirmed_deaths.columns.tolist() + ['confirmed','deaths'], axis=1) 

# Find the numbers of confirmed cases and deaths in df_confirmed_deaths['text'].
# Write these numbers in the 'confirmed' and 'deaths' columns.
# df_confirmed_deaths.iterrows() returns the list: index, row
# index : a row index (a number)
# row : whole row
for index, row in df_confirmed_deaths.iterrows():

    # Select the 'text' column from the row, i.e., get the 'text' cell content for the current row
    tweet_text = row['text']

    # String concatenation:
    # '%s something %s' % ('aaa','zzz') 
    # returns 'aaa something zzz'
    #
    # Regex search: 
    # %s : some string
    # (.*) : the string we look for
    # 
    # Search for 2 strings between start, middle, end
    result = re.search('%s(.*)%s(.*)%s' % (start, middle, end), tweet_text)
    # result.group(N) : 
    # N=0 : whole string
    # N=1 : result 1
    # N=2 : result 2
    confirmed_str, deaths_str = result.group(1), result.group(2)

    # Sanitize the result strings: filter only numbers 
    confirmed_sanitized = re.search("([0-9]+)",confirmed_str).group(1)
    deaths_sanitized = re.search("([0-9]+)",deaths_str).group(1)

    # Convert strings to integer numbers
    confirmed = int(confirmed_sanitized)
    deaths = int(deaths_sanitized)

    # I must check how to deal with data frame copies. Sometimes a warning shows up...?
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    # For now:
    df_confirmed_deaths.loc[index,'confirmed'] = confirmed
    df_confirmed_deaths.loc[index,'deaths'] = deaths

# For some reason, the numbers entered to columns are float...    
# Convert the 'confirmed' and 'deaths' columns to int  
df_confirmed_deaths = df_confirmed_deaths.astype({'confirmed': int, 'deaths': int})

# Reset index (because old indexes were inherited from df) 
df_confirmed_deaths = df_confirmed_deaths.reset_index(drop=True)

# For check, write the downloaded data to a file: 
# data_file_name = path+"TwitterCaptureMZ_GOV_PL."+today_str+".csv"
df_confirmed_deaths_to_export = df_confirmed_deaths[['time', 'confirmed', 'deaths']]
today = date.today()
today_str = today.strftime("%Y.%m.%d")

captured_data_file_name = twitter_data_path+"TCcdMZ_GOV_PL."+today_str+".csv"
df_confirmed_deaths_to_export.to_csv (captured_data_file_name, index = False, header=True)



# Update the existing CSV data file
# 
# Automatically find the previous data file
i=0
while i<7:
    # Get a time stamp i days from now
    date_i_days_ago = datetime.now() - timedelta(days=i)
    # Format the time stamp
    day_str = date_i_days_ago.strftime("%Y.%m.%d")
    # This should be the name of the data file created i days ago (if it exists)
    filename = path + "cor." + day_str+".csv"
    # Check if the data file created i days ago exists
    file_found =  glob.glob(filename)
    if file_found:
        print("Last local data file found:" , file_found[0])
        i=7
    i=i+1


# For some reason, I can't use the result of glob.glob(filename) above (why?)
# I use the filename instead
old_csv_file_name = filename
new_csv_file_name = path + "cor." + today_str + ".csv"
# Read the latest existing CSV data file
myfile_df = pd.read_csv(old_csv_file_name)

# Show part of the old csv file as a table (I need to improve this)
# Works in Jupyter notebook / IPython
display(myfile_df[30:45])


# The newest row (0) in the tweets data frame df_confirmed_deaths
newest_twitter_index = 0

# Newest date in df_confirmed_deaths, read as string
newest_twitter_date_str = df_confirmed_deaths.loc[newest_twitter_index,'time']

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

# Update my file        
# We will loop through the rows of my file data and Twitter data 
# and overwrite the data in my file with the Twitter data
myfile_increment_index=0
twitter_increment_index=0

# df_confirmed_deaths.tail(1).index.item() : last index
last_twitter_index = df_confirmed_deaths.tail(1).index.item()

# Loop from the 0-th to last row in the Twitter data:
while twitter_increment_index<last_twitter_index-1:
    # Get the dates for the new rows
    # Note the difference in time ordering of my csv file data and the Twitter data:
    # newest_myfile_index-myfile_increment_index : we move up my csv file
    # newest_twitter_index+twitter_increment_index : we move down the Twitter data
    myfile_date = \
        pd.to_datetime(myfile_df.loc[newest_myfile_index-myfile_increment_index, 'Data']).\
        strftime(myfile_date_format)
    twitter_date = df_confirmed_deaths.loc[newest_twitter_index+twitter_increment_index,'time'].\
        strftime(myfile_date_format)

    # There may be more entries for one day in Twitter data.
    # If the  current dates in my file data and Twitter data don't match, 
    # go one row further in Twitter data and check again.
    while twitter_date != myfile_date:
        twitter_increment_index = twitter_increment_index + 1
        twitter_date = df_confirmed_deaths.loc[newest_twitter_index+twitter_increment_index,'time']\
           .strftime(myfile_date_format)   
    #print(myfile_date, twitter_date)
    # This will be OK at the 0-th increment 
    # because newest_myfile_index and newest_twitter_index have already been found.
    myfile_df.loc[newest_myfile_index-myfile_increment_index, 'Wykryci zakażeni'] =\
      df_confirmed_deaths.loc[newest_twitter_index+twitter_increment_index,'confirmed']
    myfile_df.loc[newest_myfile_index-myfile_increment_index, 'Zmarli'] =\
      df_confirmed_deaths.loc[newest_twitter_index+twitter_increment_index,'deaths']

    # Go to the previous day in my csv file: move by one row (each row is one day in that file)
    myfile_increment_index = myfile_increment_index + 1

    # Try to go to the previous day in Twitter data: move by one row
    twitter_increment_index = twitter_increment_index + 1


print("Captured data written to local data file:", captured_data_file_name)
# Show the captured data
# Works in Jupyter notebook / IPython
display(df_confirmed_deaths_to_export)


# Export the updated file to CSV
myfile_df.to_csv(new_csv_file_name, index=False)
print("Update written to local data file:", new_csv_file_name)

# Show part of the new csv file as a table (I need to improve this)
# Works in Jupyter notebook / IPython
display(myfile_df[30:45])
