# Project 1: Query Project

- In the Query Project, you will get practice with SQL while learning about
  Google Cloud Platform (GCP) and BiqQuery. You'll answer business-driven
  questions using public datasets housed in GCP. To give you experience with
  different ways to use those datasets, you will use the web UI (BiqQuery) and
  the command-line tools, and work with them in jupyter notebooks.

- We will be using the Bay Area Bike Share Trips Data
  (https://cloud.google.com/bigquery/public-data/bay-bike-share). 

#### Problem Statement

- You're a data scientist at Ford GoBike (https://www.fordgobike.com/), the
  company running Bay Area Bikeshare. You are trying to increase ridership, and
  you want to offer deals through the mobile app to do so. What deals do you
  offer though? Currently, your company has three options: a flat price for a
  single one-way trip, a day pass that allows unlimited 30-minute rides for 24
  hours and an annual membership. 

- Through this project, you will answer these questions: 
  * What are the 5 most popular trips that you would call "commuter trips"?
  * What are your recommendations for offers (justify based on your findings)?

Changed this

---

## Part 1 - Querying Data with BigQuery

### What is Google Cloud?
- Read: https://cloud.google.com/docs/overview/

### Get Going

- Go to https://cloud.google.com/bigquery/
- Click on "Try it Free"
- It asks for credit card, but you get $300 free and it does not autorenew after the $300 credit is used, so go ahead (OR CHANGE THIS IF SOME SORT OF OTHER ACCESS INFO)
- Now you will see the console screen. This is where you can manage everything for GCP
- Go to the menus on the left and scroll down to BigQuery
- Now go to https://cloud.google.com/bigquery/public-data/bay-bike-share 
- Scroll down to "Go to Bay Area Bike Share Trips Dataset" (This will open a BQ working page.)


### Some initial queries
Paste your SQL query and answer the question in a sentence.

- What's the size of this dataset? (i.e., how many trips)

```text
SELECT COUNT(*)
FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
```

THe size of the dataset is 983, 648 entries.

- What is the earliest start time and latest end time for a trip?

```text

SELECT MIN(TIME(start_date))
FROM `bigquery-public-data.san_francisco.bikeshare_trip`

SELECT MAX(TIME(end_date))
FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
```


The earlist start date is 00:00:00, and the latest end time is 23:59:00.

- How many bikes are there?

```text
SELECT COUNT(DISTINCT bike_number)
FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
```

There are 700 bikes.


### Questions of your own
- Make up 3 questions and answer them using the Bay Area Bike Share Trips Data.
- Use the SQL tutorial (https://www.w3schools.com/sql/default.asp) to help you with mechanics.

- Question 1: What is the average bike trip length?
  * Answer: 16.98 minutes
  * SQL query: 
  
```text
SELECT AVG(DATETIME_DIFF(DATETIME(end_date), DATETIME(start_date), MINUTE)) as trip_average
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
```

- Question 2: What is the % utilization of bike stations between 8am and 10 am?
  * Answer:  0.457
  * SQL query: 
```text
SELECT AVG(bikes_available/NULLIF(bikes_available+docks_available, 0))
FROM `bigquery-public-data.san_francisco.bikeshare_status` 
WHERE Time(time) BETWEEN "08:00:00" AND "10:00:00"
```

- Question 3: How many bike stations are there that are in SF, have a dock count over 30, and were built before 2017?
  * Answer: 2
  * SQL query: 
```text 
SELECT *
FROM `bigquery-public-data.san_francisco.bikeshare_stations` 
WHERE landmark="San Francisco" AND dockcount > 30 AND DATETIME(installation_date) < '2017-01-01 00:00:00'
```
---

## Part 2 - Querying data from the BigQuery CLI - set up 

### What is Google Cloud SDK?
- Read: https://cloud.google.com/sdk/docs/overview

- If you want to go further, https://cloud.google.com/sdk/docs/concepts has
  lots of good stuff.

### Get Going

- Install Google Cloud SDK: https://cloud.google.com/sdk/docs/

- Try BQ from the command line:

  * General query structure

    ```
    bq query --use_legacy_sql=false '
        SELECT count(*)
        FROM
           `bigquery-public-data.san_francisco.bikeshare_trips`'
    ```

### Queries

1. Rerun last week's queries using bq command line tool (Paste your bq
   queries):

- What's the size of this dataset? (i.e., how many trips)

```
bq query --use_legacy_sql=false ' SELECT COUNT(*)
> FROM `bigquery-public-data.san_francisco.bikeshare_trips`'
```

- What is the earliest start time and latest end time for a trip?

```
bq query --use_legacy_sql=false 'SELECT MIN(TIME(start_date))
FROM `bigquery-public-data.san_francisco.bikeshare_trip'

bq query --use_legacy_sql=false 'SELECT MAX(TIME(end_date))
FROM `bigquery-public-data.san_francisco.bikeshare_trip'
```

- How many bikes are there?
```
bq query --use_legacy_sql=false 'SELECT COUNT(DISTINCT bike_number)
FROM `bigquery-public-data.san_francisco.bikeshare_trips`'
```

2. New Query (Paste your SQL query and answer the question in a sentence):

- How many trips are in the morning vs in the afternoon?
```
bq query --use_legacy_sql=false 'SELECT COUNT(*)
FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
WHERE Time(end_date) BETWEEN "00:00:00" AND "11:59:59"'
```

**There are 400,144 rides that start in the afternoon**

```
bq query --use_legacy_sql=false 'SELECT COUNT(*)
FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
WHERE Time(end_date) BETWEEN "12:00:00" AND "23:59:59"'
```

**There are 583,504 rides that start in the afternoon**

### Project Questions
Identify the main questions you'll need to answer to make recommendations (list
below, add as many questions as you need).

- Question 1: **What is the average subscriber ride time vs customer ride time?**
- Question 2: **When is rush hour? What is the ditribution of ride times?**
- Question 3: **What are the most popular routes in general?**
- Question 4: **Which stations have the least bikes origniating from them, and which ones have the least ending at them?**
- Question 5: **When is bike utilization the lowest?**


### Answers

Answer at least 4 of the questions you identified above You can use either
BigQuery or the bq command line tool.  Paste your questions, queries and
answers below.

- Question 1: What is the average subscriber ride time? 
  * Answer: 9.71 minutes
  * SQL query:
```
SELECT AVG(DATETIME_DIFF(DATETIME(end_date), DATETIME(start_date), MINUTE)) as trip_average 
FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
WHERE subscriber_type	= "Subscriber"
```

- Question 2: What are all the distinct routes that are taken?
  * Answer: Table of 2139 values
  * SQL query: 
```  
SELECT * 
FROM (SELECT DISTINCT CONCAT( start_station_name, end_station_name)
      FROM  `bigquery-public-data.san_francisco.bikeshare_trips`) as dt
```

- Question 3: Bucket rides into times
  * Answer: Table with results (can be seen in Jupyter notebook)
  * SQL query:

```text
SELECT 
  case when TIME(start_date) BETWEEN "00:00:00" AND "00:59:59" then '00-01'
       when TIME(start_date) BETWEEN "01:00:00" AND "01:59:59" then '01-02'
       when TIME(start_date) BETWEEN "02:00:00" AND "02:59:59" then '02-03'
       when TIME(start_date) BETWEEN "03:00:00" AND "03:59:59" then '03-04'
       when TIME(start_date) BETWEEN "04:00:00" AND "04:59:59" then '04-05'
       when TIME(start_date) BETWEEN "05:00:00" AND "05:59:59" then '05-06'
       when TIME(start_date) BETWEEN "06:00:00" AND "06:59:59" then '06-07'
       when TIME(start_date) BETWEEN "07:00:00" AND "07:59:59" then '07-08'
       when TIME(start_date) BETWEEN "08:00:00" AND "08:59:59" then '08-09'
       when TIME(start_date) BETWEEN "09:00:00" AND "09:59:59" then '09-10'
       when TIME(start_date) BETWEEN "10:00:00" AND "10:59:59" then '10-11'
       when TIME(start_date) BETWEEN "11:00:00" AND "11:59:59" then '11-12'
       when TIME(start_date) BETWEEN "12:00:00" AND "12:59:59" then '12-13'
       when TIME(start_date) BETWEEN "13:00:00" AND "13:59:59" then '13-14'
       when TIME(start_date) BETWEEN "14:00:00" AND "14:59:59" then '14-15'
       when TIME(start_date) BETWEEN "15:00:00" AND "15:59:59" then '15-16'
       when TIME(start_date) BETWEEN "16:00:00" AND "16:59:59" then '16-17'
       when TIME(start_date) BETWEEN "17:00:00" AND "17:59:59" then '17-18'
       when TIME(start_date) BETWEEN "18:00:00" AND "18:59:59" then '18-19'
       when TIME(start_date) BETWEEN "19:00:00" AND "19:59:59" then '19-20'
       when TIME(start_date) BETWEEN "20:00:00" AND "20:59:59" then '20-21'
       when TIME(start_date) BETWEEN "21:00:00" AND "21:59:59" then '21-22'
       when TIME(start_date) BETWEEN "22:00:00" AND "22:59:59" then '22-23'
       when TIME(start_date) BETWEEN "23:00:00" AND "23:59:59" then '23-24'
  end PriceRange,
  count(*) as TotalWithinRange
FROM `bigquery-public-data.san_francisco.bikeshare_trips`
WHERE subscriber_type = "Subscriber"
GROUP BY 1
ORDER BY PriceRange
```


- Question 4: What are the 5 stations (get all of them) that have the least amount of trips finishing at them.
  * Answer: 5th St at E. San Salvador St (1), Sequoia Hospital (14), San Jose Government Center (23), 5th S at E. San Salvador St (24), Cyril Magnin St at Ellis St (68)
  
  * SQL query:
```  
SELECT DISTINCT(end_station_name) as end_station, COUNT(*) as counts 
FROM `bigquery-public-data.san_francisco.bikeshare_trips` 
GROUP BY end_station 
ORDER BY counts ASC
```


---

## Part 3 - Employ notebooks to synthesize query project results

### Get Going

Use JupyterHub on your midsw205 cloud instance to create a new python3 notebook. 


#### Run queries in the notebook 

```
! bq query --use_legacy_sql=FALSE '<your-query-here>'
```

- NOTE: 
- Queries that return over 16K rows will not run this way, 
- Run groupbys etc in the bq web interface and save that as a table in BQ. 
- Query those tables the same way as in `example.ipynb`


#### Report
- Short description of findings and recommendations 
- Add data visualizations to support recommendations 

### Resource: see example .ipynb file 

[Example Notebook](example.ipynb)
