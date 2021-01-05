import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Extract song table from a JSON file, transform it by selecting specific 
    columns and load it to the database.

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        A database cursor
    filepath : string
        Filepath to a valid JSON file
    """
    
    # open song file
    df = pd.read_json(filepath, lines=True) 

    # insert song record
    cols=['song_id', 'title', 'artist_id', 'year', 'duration']
    song_data = list(df[cols].values[0])
    
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    cols=['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 
          'artist_longitude']
    artist_data = list(df[cols].values[0]) 
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Extract data from a logfile JSON file, transform it and load into the following 
    tables: user, time and songplay. 

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        A database cursor
    filepath : string
        Filepath to a valid JSON file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.query('page=="NextSong"')

    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts, unit='ms')
    
    # insert time data records
    time_data = [df.ts.values,
             t.dt.hour.values,
             t.dt.day.values,
             t.dt.weekofyear.values,
             t.dt.month,
             t.dt.year,
             t.dt.weekday, 
            ]
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    cols=['userId', 'firstName', 'lastName', 'gender', 'level']
    user_df = df[cols]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [row.ts, 
                         row.userId, 
                         row.level, 
                         songid, 
                         artistid, 
                         row.sessionId, 
                         row.location, 
                         row.userAgent] 
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Read all JSON files from `filepath`, iterate over files and preprocess
    using function defined in `func`.

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        A database cursor
    conn : psycopg2.extensions.connection
        A connection object
    filepath : string
        Filepath to a directory containing JSON files
    func : function
        Function to preprocess each JSON file
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Main function. Connect to the database, and preprocess the song_data and the log_data
    directories.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()