#!/bin/bash

# Tested on: 
# Python 3.6.10 :: Anaconda, Inc.
# jupyter-notebook 6.0.3
# ipython 7.13.0

# My anaconda environment for Python 3.6:
myenv_name=python3.6


conda run -n $myenv_name ipython ./code/TwitterCaptureMZ_GOV_PL.py

conda run -n $myenv_name ipython ./code/TwitterCaptureImagesTestedMZ_GOV_PL.py

conda run -n $myenv_name ipython ./code/TwitterCaptureImagesHQSR-MZ_GOV_PL.py
