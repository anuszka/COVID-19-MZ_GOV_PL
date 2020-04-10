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
"Hospitalizowani" : "hospitalized", # at the current day, not cumulative
"Zmarli" : "deaths", # cumulative
"Kwarantanna" : "quarantined", # at the current day, not cumulative
"Nadzór" : "supervised",  # under epidemiological supervision; at the current day, not cumulative
"Testy, wartości przybliżone" : "tests, approximate",  # there were no data for one day, 
                                                       # just an approximate number was given 
                                                       # on Twitter @MZ_GOV_PL; cumulative
"Kwarantanna po powrocie do kraju" : "quarantined after return to Poland", # at the current day,
                                                                           # not cumulative
"Wydarzenia" : "events",  # restrictions introduced by Polish government (description in Polish)
"Wyzdrowiali" : "recovered" # cumulative
```
#### Restrictions introduced by Polish government
For convenience of other users, below I explain as a dictionary the cells content in the `"Wydarzenia"` ("events") column: 

`original_Polish_header : English_translation # comment` 

```
"Zamknięcie szkół i instytucji kulturalnych" : "Closing schools and cultural institutions
"Ogłoszenie stanu epidemii" : "State of epidemic announced"
"Dalsze restrykcje (zgromadzenia max 2 os.)" : "Further restrictions (public meetings \
  not allowed for more than 2 people)"
"Kolejne restrykcje (zakaz wychodzenia młodzieży, 2 m odstępu, zamknięcie salonów fryzjerskich etc.)" : \
  "Next restrictions (going out not allowed for youth < 18 years old, maintain a distance of at least \
  2 m in public, closing of hairdressing salons, etc.")
```
