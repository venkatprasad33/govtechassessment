# Data extraction Assessments

#### Extract restaurant data fields and store the data as .csv
```
$ python3 demo.py --type data --csv restaurants_data.csv
```

#### Extract list of restaurants that have past event within the month of April 2017 and store the data as .csv
```
$ python3 demo.py --type events --csv restaurants_events.csv
```

#### Determine the threshold for the different rating_text based on aggregate_rating
```
$ python3 analyze.py
```