# COVID-19-MZ_GOV_PL
COVID-19 statistics for Poland, captured from Polish Health Ministry's Twitter @MZ_GOV_PL

`data` directory contains CSV files.

## CSV file description:

The following is a bit inconsistent but for historical reasons: 
* Column names are in Polish; in particular, the date column name is 'Data'. 
* However, dates in the date column are in American date format: `"%m/%d/%Y"`
* File name: `"cor." + "%Y.%m.%d" + ".csv"`

### Column headers
For convenience of other users, below I explain the column headers as a dictionary: 

`original_Polish_header : English_translation # comment` 

```
"Data" : "date", 
"Dzień" : "day",  #  since the 1st case 
"Wykryci zakażeni" : "confirmed",  # cumulative
"Testy" : "tested",  # cumulative
"Hospitalizowani" : "hospitalized", 
"Zmarli" : "deaths", 
"Kwarantanna" : "quarantined", 
"Nadzór" : "supervised",  # under epidemiological supervision
"Testy, wartości przybliżone" : "tests, approximate",  # there were no data for one day, just an approximate number was given on Twitter @MZ_GOV_PL
"Kwarantanna po powrocie do kraju" : "quarantined after return to Poland", 
"Wydarzenia" : "events",  # restrictions introduced by Polish government (description in Polish)
"Wyzdrowiali" : "recovered"
```
