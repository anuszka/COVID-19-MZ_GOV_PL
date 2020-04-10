# COVID-19-MZ_GOV_PL
COVID-19 statistics for Poland, captured from Polish Health Ministry's Twitter @MZ_GOV_PL

CSV file:

The following is a bit inconsistent but for historical reasons: 
* Column names are in Polish; in particular, the date column name is 'Data'. 
* However, dates in the date column must be in American date format:
        myfile_date_format = '%m/%d/%Y'
* File name: "cor." + "%Y.%m.%d" + ".csv"

Column headers: 

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

  "Wydarzenia" : "events",  # restrictions introduced by Polish government

  "Wyzdrowiali" : "recovered"

