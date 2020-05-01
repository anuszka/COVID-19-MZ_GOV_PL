### 2020-05-01: Additional files

Regular files `cor.*.csv` contain the last data announced on a given day (evening).

Additional files `wykryci_rano.*.csv` contain the numbers of confirmed cases announced in the earliest report on that day:

+ `"Wykryci zakażeni"` column: The last data announced on that day (evening).

+ `"Data i godzina rano"`  column: Timestamp for the first data announced on that day (morning).

+ `"Wykryci zakażeni rano"` column: The first data announced on that day (morning).

Note that on May 1-3 (holidays) the daily data are announced only once, around 13:00. I treat them as the evening data. In such a case, I treat the morning data as null.