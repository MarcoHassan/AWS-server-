# -*- coding: utf-8 -*-
#   TODO INSERT DESCRIPTION HERE
#
#


from twython import TwythonStreamer
import json
import csv
import sys  # For command line arguments
import logging

# SQL
import mysql.connector

# Time packages
import time
import datetime
from email.utils import parsedate_tz, mktime_tz
import pytz  # $ pip install pytz

######################################


# File paths
path_credentials = "../twitter_credentials.json"
path_data = "../data/" + sys.argv[1] + ".csv"
path_log = "../log/" + sys.argv[2] + ".log"

# Setup logger
logger = logging.getLogger('twitter')
hdlr = logging.FileHandler(path_log)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

# Keywords to track
keywords = sys.argv[1]

######################################
# TWITTER
######################################


# Import your credentials
with open(path_credentials, "r") as file:
    creds = json.load(file)


# Create a class that inherits TwythonStreamer
class MyStreamer(TwythonStreamer):

    # Create counter variable & date variable
    counter = 0

    # Connect to MySQL Database
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='tweetsDB',
            user='root')
        if conn.is_connected():
            print('Connected to MySQL database')
            my_str = "Stream successfully established for Keywords: {}".format(keywords)
            logger.info(my_str)
    except mysql.connector.Error as e:
        print(e)

    # Problem with the API
    def on_error(self, status_code, data):
        print(status_code, data)
        logger.error('Connection lost')
        self.disconnect()

    # Save each tweet to csv file
    def save_to_csv(self, tweet):
        with open(path_data, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(list(tweet.values()))

    # Insert each Tweet into MySql
    def save_to_sql(self, tweet):
        try:
            self.conn.cursor().execute("""INSERT into tweets(date,user,text) values(%s,%s,%s)""", (list(tweet.values())))
            self.conn.commit()
            print('Inserted {} tweets'.format(self.counter))
        except Exception as e:
            print(e)
            self.conn.rollback()
            print('Insertion failed')

    # Filter out unwanted data
    def process_tweet(self,tweet):
        d = {}

        timestamp = mktime_tz(parsedate_tz(tweet['created_at']))
        dt = datetime.datetime.fromtimestamp(timestamp, pytz.timezone('US/Eastern'))
        d['date'] = dt.strftime('%Y-%m-%d %H:%M:%S')

        d['user'] = tweet['user']['screen_name'].encode('utf-8')
        d['text'] = tweet['text'].encode('utf-8')
        #   d['user_loc'] = tweet['user']['location']
        #	d['geo_loc'] = tweet['coordinates']
        #	d['favorite_coun'] = tweet['favorite_count']
        #	d['retweet_coun'] = tweet['retweet_count']
        #    d['hashtags'] = [hashtag['text'].encode('utf-8')
        #                   for hashtag in tweet['entities']['hashtags']]
        return d

    # Received data
    def on_success(self, data):
        # Process the tweets
        tweet_data = self.process_tweet(data)

        # Save them
        self.save_to_csv(tweet_data)
        self.save_to_sql(tweet_data)

        # Log it
        my_str = "{} Tweets saved since start".format(self.counter)
        logger.info(my_str)
        self.counter += 1

# Instantiate streaming class
stream = MyStreamer(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
                    creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])


# Wrapper function for MyStremer which restarts if error occurs
def cont_streamer():
    try:
        stream.statuses.filter(track=keywords, language='en')
    except Exception as e:
        print(e)
        print('Failed; wait 30 seconds')
        time.sleep(30)
        print('Try again')
        cont_streamer()


######################################
####	MAIN						 
######################################

def main():
    cont_streamer()


if __name__ == '__main__':
    main()
