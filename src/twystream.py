#####################################################
# Server Project - Automatically downloading tweets #
#####################################################

# Code for the Server Project
# alexander.steeb@student.unisg.ch
# marco.hassan30@gmail.com
# Started 2019-02-27
#
#
# This python script relies on the twython package. The idea is
# to download Twitter tweets in a given language relating to
# a topic to be specified by the user when running the script.
#
# This python script leverages the twython package to interact
# with the Twitter servers through their APIs. For the successful
# execution of this script it is therefore necessary to dispose of an
# appropriate set of API keys in order to connect with the Twitter server.
# The API keys can be obtained online following twitter instructions and
# MUST be saved in a json file called twitter_json
#

# TODO Testen

# Once the above step is done it is necessary to create a log file where
# - to track the script execution - and a csv file - where the downloaded
# tweets will be saved -. Moreover it will be necessary to set up a
# mysql server.
#
# Notice that the naming of the csv, log and database should match the one
# used in this script. An adjustment below will be necessary if different
# naming will be used. In addition if you search tweets in a different
# language than english you should specify the condition at line 178.

#######################
# Necessary libraries #
#######################

from twython import TwythonStreamer  # to connect to twitter server via the provided API keys
import json  # to interact with the json file where the API keys are saved
import csv  # to write a csv containing the tweets
import sys  # for entering the keyword of interest for the search
import logging  # to set up a log file where the operations of the script are tracked.

# to set up a log file where the operations of the script are tracked.
import logging

# TODO pip freez on server
import pandas as pd  # To plot
import matplotlib.pyplot as plt  # to import SQL queries to panda data frame

# SQL
import mysql.connector  # to connect with the SQL server

# Time packages to get time stamps in order to save the time the tweet was connected and
# to work with those timestamps
import time
import datetime
from email.utils import parsedate_tz, mktime_tz
import pytz

##########################


##################
# General set up #
##################

# Log file creation in the local directory

log_file = input(
    "Please specify the log file name of desire w/o file format here: ")
path_log = "./" + log_file + ".log"
outfile = open(path_log, "w")
outfile.write("")
outfile.close()

# API key credentials file
credentials = input(
    "Please specify the path to the json file displaying your API credentials: ")
path_credentials = credentials

# Csv file creation in the local directory.
csv = input(
    "Please specify the document name of your csv file - w/o file format - here: ")
path_data = "./data/" + csv + ".csv"
outfile = open(csv, "w")
outfile.write("")
outfile.close()

# Setup logger

# Logging inspired by this example:
# https://docs.python.org/2.7/howto/logging.html#logging-advanced-tutorial

logger = logging.getLogger('twitter')  # specify the name of the log file.
hdlr = logging.FileHandler(path_log)  # specify the path to the log file.

formatter = logging.Formatter('%(asctime)s (%(levelname)s) - %(message)s')
# the formatter specify how the messages should be displayed in the log
# file. Here 'time (priority level) - <message>'.

hdlr.setFormatter(formatter)  # save formatter option
logger.addHandler(hdlr)  # add to the logger file the formatted options.
logger.setLevel(logging.INFO)  # Level of priority messages you want to display. Here: info level and above.

# Saves the search criteria for the tweets you specified in the shell.
keywords = sys.argv[1]

####################

########
# CODE #
########

# Import your API credentials
with open(path_credentials, "r") as file:
	creds = json.load(file)


# Create a class that inherits TwythonStreamer functionality and
# passes all the arguments of interest to the streaming functionality of
# twython.

class MyStreamer(TwythonStreamer):
    counter = 0

    # Connect to MySQL Database; ENTER YOUR SPECIFIC DATABASE AND USER
    # CHOICES HERE.
    # try to connect to the database
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='tweetsDB',
            user='root',
            password='ENTER YOUR PASSWORD')
        if conn.is_connected():
            # report successfull connection in the log file.
            logger.info('Connected to MySQL database')
            my_str = "Stream successfully established for Keywords: {}".format(
                keywords)
            # report successful connection for the specified keyword
            logger.info(my_str)

    # in case of failed connection print the error and report an error in
    # the log file.
    except mysql.connector.Error as e:
        print(e)
        logging.error('The connection with the database failed')

    # Handle API connection problem and disconnect to the database to free
    # up resources.
    def on_error(self, status_code, data):
        print(status_code, data)
        logger.error('Connection lost')
        self.disconnect()

    # Save each tweet to csv file
    def save_to_csv(self, tweet):
        with open(path_data, 'a') as file:
            # 'a' for appending and not overwriting.

            writer = csv.writer(file)
            writer.writerow(list(tweet.values()))  # write the tweet values
            # to be saved. You can specify the entries you want to save
            # at line 157. For this porgram we decided to save the date
            # user name and the text of the tweet.

    # Insert each Tweet into MySql
    def save_to_sql(self, tweet):
        try:
            self.conn.cursor().execute(
                """INSERT into tweets(date,user,text) values(%s,%s,%s)""",
                (list(tweet.values())))  # use s-strings to insert the
            # tweets into the server by entering the list elements one
            # by one.
            self.conn.commit()  # commit the execution to the database.
            print('Inserted {} tweets'.format(self.counter))

        # Inform the user of bug in saving a valid tweet to the database.
        except Exception as e:
            print(e)
            # gives the text lost in the log file
            logging.error('Insertion failed:' + str(list(tweet.values())[2]))
            self.conn.rollback()  # rollback all the changes done for the
            # the problematic tweet.

    # Decide what data to import from the tweets
    def process_tweet(self, tweet):
        d = {}

        timestamp = mktime_tz(parsedate_tz(tweet['created_at']))
        dt = datetime.datetime.fromtimestamp(
            timestamp, pytz.timezone('US/Eastern'))
        d['date'] = dt.strftime('%Y-%m-%d %H:%M:%S')

        d['user'] = tweet['user']['screen_name'].encode('utf-8')
        d['text'] = tweet['text'].encode('utf-8')

        return d

        # Notice; for above possible interesting options to be saved are:
        # d['user_loc'] = tweet['user']['location']
        # d['geo_loc'] = tweet['coordinates']
        # d['favorite_coun'] = tweet['favorite_count']
        # d['retweet_coun'] = tweet['retweet_count']
        # d['hashtags'] = [hashtag['text'].encode('utf-8')
        #                  for hashtag in tweet['entities']['hashtags']]

    # Specify the action in case no error occured.
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


# Calls the twythonstreamer filter member function that will
# call the mystreamer on_success and on_error member function of the
# Mystreamer function and execute the code.

# Moreover the function below will reactivate the tweets downloaded after
# 5 sec. after an error occurred.


def cont_streamer():
	try:
		stream.statuses.filter(track=keywords, language='en')
	except Exception as e:
		print(e)
		print('Failed; wait 5 seconds')
		time.sleep(5)
		print('Try again')
		cont_streamer()


#############
# Execution #
#############

cont_streamer()
