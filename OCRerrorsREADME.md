# Possible errrors in image recognition
**Caution!** Image recognition is not perfect. (However, I greatly improved it in v. 1.1.0 and I fix it when image format changes.) 

+ If non-digit characters show up in the data file entries, such entries need to be corrected manually. Notifications on OCR errors are saved to `./ocr_errors/OCR_errors.log` file so that the user would know what to correct.

**Semi-manual OCR error correction**
+ `ocr_errors/OCR_error_correction.csv` contains the table of errors to be corrected or already corrected. Edit manually the last column `"should be"`: If the entry in a given row is empty (no character after `,`) then type a correct number there. Save the file after finishing edition. If the entry in a given row is non-empty then it means that the correct number has already been added to the dictionary and it will be used by the error-correcting script. 
+ After editing `./ocr_errors/OCR_error_correction.csv`, run the error-correcting script `./run_error_correction.sh`. The correct values from `./ocr_errors/OCR_error_correction.csv` will be overwritten in the newest data file in `./data/`. The old version of the data file (before corrections) will be saved as `./data/*.old`.  
+ Unfortunately, the scripts are unable to detect OCR errors which look like numbers. Some errors may still have passed undetected, e.g., on 2020.04.12, the script recognized `7` instead of `138007` as the cumulative number of `tested`. You still need to check if the new data don't look suspicious.
