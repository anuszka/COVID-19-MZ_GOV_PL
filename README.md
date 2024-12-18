# COVID-19-MZ_GOV_PL (This project is no loner maintained)
COVID-19 statistics for Poland, captured from Polish Health Ministry's Twitter [@MZ_GOV_PL](https://twitter.com/MZ_GOV_PL)

My plots of these data are here: [archived](https://web.archive.org/web/20231207090158/http://soft.ichf.edu.pl/ochab/coronavirus_poland/)

For example, [my comments on the statistics for 2020.04.20 (in Polish)](https://web.archive.org/web/20200803055411/http://soft.ichf.edu.pl/ochab/coronavirus_poland/2020.04.20.a/koronawirus_statystyki.2020.04.20.a.html).

## Why from Twitter

Polish Ministry of Health does not publish data in human-readable format.

On the Ministry of Health website, the <a href="https://www.gov.pl/web/koronawirus/wykaz-zarazen-koronawirusem-sars-cov-2">the incidence table</a> shows only the current day status and only in two categories: Number of confirmed cases (cumulative) and number of deaths (cumulative).

On <a href="https://twitter.com/MZ_GOV_PL">their Twitter account</a>, the Ministry of Health shows data in 7 categories in 3 ways:

* The number of confirmed cases (cumulative) and the number of deaths (cumulative) - in text form, as numbers in tweets.
* The number of tests performed (cumulative) - as a bitmap image(!)
* Hospitalized (for the current day), quarantined (for the current day), under surveillance (for the current day), recovered (cumulative) - as another bitmap image(!) which changes its format(!)


I automated downloading these data from Twitter using scripts in Python.

To read the numbers from bitmaps, I used Python packages for image recognition (to filter colors in the background and then to OCR the text).

Data in other columns were entered manually.

**Caution!** Image recognition is not perfect. (However, I greatly improved it in v. 1.1.0 and I fix it when image format changes.) Go to  [OCRerrorsREADME.md](https://github.com/anuszka/COVID-19-MZ_GOV_PL/blob/master/OCRerrorsREADME.md) to see what errors may occur and how to correct them.
  

## Data
### Where are the data
`data` directory contains CSV files with the data on COVID-19 statistics for Poland, captured from Polish Health Ministry's Twitter @MZ_GOV_PL.
### CSV file description
#### Format
The following is a bit inconsistent but for historical reasons: 
* Column names are in Polish; in particular, the date column name is 'Data'. 
* However, dates in the date column are in American date format: `"%m/%d/%Y"`
* File name: `"cor." + "%Y.%m.%d" + ".csv"`

#### Column headers
For convenience of users, below I explain the column headers:
| Polish | English | Comment |
|--------|---------|---------|
| "Data" |  "date" |         | 
| "Dzień" |  "day"|   since the 1st case | 
| "Wykryci zakażeni"| "confirmed"|  cumulative| 
| "Testy" |  "tested"|  cumulative| 
| "Hospitalizowani" |  "hospitalized"| for a given day, not cumulative| 
| "Zmarli" |  "deaths"|  cumulative| 
| "Kwarantanna" |  "quarantined"| for a given day, not cumulative| 
| "Nadzór" |  "surveillance"|   under epidemiological surveillance; for a given day, not cumulative| 
| "Testy, wartości przybliżone" |  "tests, approximate"|  there were no data for one day, just an approximate number was given on Twitter @MZ_GOV_PL; cumulative| 
| "Kwarantanna po powrocie do kraju" | "quarantined after return to Poland"| for a given day, not cumulative| 
| "Wydarzenia" | "events"| restrictions introduced by Polish government (described in Polish)| 
| "Wyzdrowiali" |  "recovered"|  cumulative| 
| "Testowane osoby" | "persons tested" | cumulative |

Here, column headers as a dictionary (perhaps this will be useful for copy-pasting into Python code): 

`original_Polish_header : English_translation # comment` 

```
"Data" : "date", 
"Dzień" : "day",  #  since the 1st case 
"Wykryci zakażeni" : "confirmed",  # cumulative
"Testy" : "tested",  # cumulative
"Hospitalizowani" : "hospitalized", # for a given day, not cumulative
"Zmarli" : "deaths", # cumulative
"Kwarantanna" : "quarantined", # for a given day, not cumulative
"Nadzór" : "surveillance",  # under epidemiological surveillance; for a given day, not cumulative
"Testy, wartości przybliżone" : "tests, approximate",  # there were no data for one day, 
                                                       # just an approximate number was given 
                                                       # on Twitter @MZ_GOV_PL; cumulative
"Kwarantanna po powrocie do kraju" : "quarantined after return to Poland", # for a given day,
                                                                           # not cumulative
"Wydarzenia" : "events",  # restrictions introduced by Polish government (described in Polish)
"Wyzdrowiali" : "recovered" # cumulative
"Testowane osoby" : "persons tested"  # cumulative
```
#### Restrictions introduced by Polish government
For convenience of users, below I explain the cells content in `"Wydarzenia"` ("events") column: 

| Polish | English | 
|--------|---------|
|"Zamknięcie szkół i instytucji kulturalnych"| "Closing schools and cultural institutions|
|"Ogłoszenie stanu epidemii"|"State of epidemic announced"|
|"Dalsze restrykcje (zgromadzenia max 2 os.)" | "Further restrictions (public meetings  not allowed for more than 2 people)"|
|"Kolejne restrykcje (zakaz wychodzenia młodzieży, 2 m odstępu, zamknięcie salonów fryzjerskich etc.)" | "Next restrictions (going out not allowed for youth < 18 years old, maintain a distance of at least  2 m in public, closing of hairdressing salons, etc.)"|
|"Dalsze restrykcje (zasłanianie twarzy)"| "Further restrictions (face covering)"|
|"Zniesienie części restrykcji (otwarcie parków i lasów, przemieszczanie rekreacyjne, sklepy i kościoły – więcej osób, swobodne przemieszczanie powyżej 13 roku życia)"|"Restrictions partially lifted (opening parks and forests, recreational movement allowed, more people allowed in shops and churches, free movement allowed > 13 y.o.)"|
|"Zniesienie części restrykcji (otwarte hotele, galerie handlowe, biblioteki)"|"Restrictions partially lifted (open hotels, malls, libraries)"|
|"Zniesienie części restrykcji (brak masek w przestrzeniach otwartych)"|"Restrictions partially lifted (no masks in the open air)"|

Here, cells content in `"Wydarzenia"` ("events") column is shown as a dictionary (perhaps this will be useful for copy-pasting into Python code): 
`original_Polish_header : English_translation # comment` 

```
"Zamknięcie szkół i instytucji kulturalnych" : "Closing schools and cultural institutions",
"Ogłoszenie stanu epidemii" : "State of epidemic announced",
"Dalsze restrykcje (zgromadzenia max 2 os.)" : "Further restrictions (public meetings \
  not allowed for more than 2 people)",
"Kolejne restrykcje (zakaz wychodzenia młodzieży, 2 m odstępu, zamknięcie salonów fryzjerskich etc.)" : \
  "Next restrictions (going out not allowed for youth < 18 years old, maintain a distance of at least \
  2 m in public, closing of hairdressing salons, etc.)",
"Dalsze restrykcje (zasłanianie twarzy)" : "Further restrictions (face covering)" ,
"Zniesienie części restrykcji (otwarcie parków i lasów, przemieszczanie rekreacyjne, sklepy i kościoły \
– więcej osób, swobodne przemieszczanie powyżej 13 roku życia)":\
"Restrictions partially lifted (opening parks and forests, recreational movement allowed, more people \
allowed in shops and churches, free movement allowed > 13 y.o.)",
"Zniesienie części restrykcji (otwarte hotele, galerie handlowe, biblioteki)":"Restrictions partially \
lifted (open hotels, malls, libraries)",
"Zniesienie części restrykcji (brak masek w przestrzeniach otwartych)":"Restrictions partially lifted \
(no masks in the open air)"

```
### 2020-04-28: New data 
Additional data are now shown on [@MZ_GOV_PL](https://twitter.com/MZ_GOV_PL) Twitter: Number of persons tested.

New column added in CSV data file: 'Testowane osoby' ('Persons tested').

### 2020-04-20: Data corrected!

Correction to my data. There was a [supplementary Twitter message on April 7](https://twitter.com/MZ_GOV_PL/status/1247569463823732739), which I did not note. As a result, in my data files, part of the increase in the number of confirmed cases from April 7 erroneously moved to April 8. This has been corrected since [cor.2020.04.20.csv](https://github.com/anuszka/COVID-19-MZ_GOV_PL/blob/master/data/cor.2020.04.20.csv).

### 2020-05-30: Data corrected!
Correction to my data for 26-30.05.2020 in 'recovered'.

