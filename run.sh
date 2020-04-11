#!/bin/bash

# Tested on: 
# Python 3.6.10 :: Anaconda, Inc.
# jupyter-notebook 6.0.3
# ipython 7.13.0

# My anaconda environment for Python 3.6:
myenv_name=python3.6

cd ./code 

conda run -n $myenv_name ipython ./TwitterCaptureMZ_GOV_PL.py

conda run -n $myenv_name ipython ./TwitterCaptureImagesTestedMZ_GOV_PL.py

conda run -n $myenv_name ipython ./TwitterCaptureImagesHQSR-MZ_GOV_PL.py

cd ..
