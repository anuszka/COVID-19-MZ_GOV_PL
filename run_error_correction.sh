#!/bin/bash

# Tested on: 
# Python 3.6.10 :: Anaconda, Inc.
# jupyter-notebook 6.0.3
# ipython 7.13.0

# My anaconda environment for Python 3.6:
myenv_name=python3.6

echo "Make sure you have entered correct values in the file: ./ocr_errors/OCR_error_correction.csv"
read -n 1 -p "Continue (y/n)?" CONT
if [ "$CONT" = "y" ]; then
  cd ./code 
  conda run -n $myenv_name ipython ./TwitterCaptureOCRErrorCorrection.py
  echo "Corrections done. Please note that some errors may still have passed undetected, e.g., 7 instead of 138007. Check if the new data don't look suspicious."
  cd ..
  echo
else
  echo
fi
echo

