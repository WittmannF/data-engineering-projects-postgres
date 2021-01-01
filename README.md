# Data Modeling with Postgres

## Summary of the Project
A startup called **Sparkify** wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## How to run the Python Scripts
1. First run:
```
$python create_tables.py
```

2. Next, run:
```
$python etl.py
```

## Database Schema
State and justify your database schema design and ETL pipeline.
Using the song and log datasets, you'll need to create a star schema optimized for queries on song play analysis. This includes the following tables.

### Fact Table

1.  **songplays** - records in log data associated with song plays i.e. records with page `NextSong`
    *   _songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent_

### Dimension Tables

1.  **users** - users in the app
    *   _user_id, first_name, last_name, gender, level_
2.  **songs** - songs in music database
    *   _song_id, title, artist_id, year, duration_
3.  **artists** - artists in music database
    *   _artist_id, name, location, latitude, longitude_
4.  **time** - timestamps of records in **songplays** broken down into specific units
    *   _start_time, hour, day, week, month, year, weekday_
