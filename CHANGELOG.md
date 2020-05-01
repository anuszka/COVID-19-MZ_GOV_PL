

# Change Log

## [1.2.0] - 2020-05-01
2020.04.28: [Change of image format](https://twitter.com/MZ_GOV_PL/status/1255097510907072512) on Polish Health Ministry's Twitter @MZ_GOV_PL - number of tested persons added

### Fixed
   OCR function for capture of the numbers of tests and tested persons now uses the new format for new images and the old format for old images

## [1.1.5] - 2020-05-01
2020.04.28: [Change of image format](https://twitter.com/MZ_GOV_PL/status/1255097510907072512) on Polish Health Ministry's Twitter @MZ_GOV_PL - number of tested persons added

### Added
   OCR: Capture of the number of tested persons added

### Fixed
   Slightly corrected display

## 2020-04-28
### New data 
Additional data are now shown on [@MZ_GOV_PL](https://twitter.com/MZ_GOV_PL) Twitter: Number of persons tested.

New column added in CSV data file: 'Testowane osoby' ('Persons tested').

## [1.1.4] - 2020-04-22
### Fixed
Added whitespace removal when sanitizing the Twitter input data in TwitterCaptureMZ_GOV_PL.py

## 2020-04-20
### Data corrected
Correction to my data. There was a [supplementary Twitter message on April 7](https://twitter.com/MZ_GOV_PL/status/1247569463823732739), which I did not note. As a result, in my plots, part of the increase in the number of confirmed cases from April 7 erroneously moved to April 8. This has been corrected since [cor.2020.04.20.csv](https://github.com/anuszka/COVID-19-MZ_GOV_PL/blob/master/data/cor.2020.04.20.csv).

## [1.1.3] - 2020-04-17
### Fixed
   Bug fix
   Slightly corrected display
   
## [1.1.2] - 2020-04-17
### Changed
   Corrected image filter threshold
### Fixed
   Improved image filtering prevents OCR errors 

## [1.1.1] - 2020-04-17
   2020.04.16: [Change of image format](https://twitter.com/MZ_GOV_PL/status/1250748610276470784) on Polish Health Ministry's Twitter @MZ_GOV_PL
### Fixed
   OCR: added new image format
   
## [1.1.0] - 2020-04-15
 
### Added
   Image filters: Threshold and invert
### Changed
   Corrected image crop
### Fixed
   Improved image filtering prevents OCR errors 
 
## [1.0.2] - 2020-04-12
 
### Added
   Semi-manual error correction
### Changed
   Improved output display
<!--### Fixed-->
 
## [1.0.1] - 2020-04-11
 
### Added
   Error logs
### Changed
   Improved output display
<!--### Fixed-->

