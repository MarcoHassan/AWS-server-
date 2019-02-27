# -*- coding: utf-8 -*-
#
#
#



from twython import TwythonStreamer 
import pandas as pd
import json
import csv
import sys 			# For command line arguments
import logging

import mysql.connector
import time
import datetime

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
####	MYSQL						 
######################################

def sql_connect():
	""" Connect to MySQL database """
	try:
		conn = mysql.connector.connect(
			host='localhost',
			database='tweetsDB',
			user='root')
		if conn.is_connected():
			print('Connected to MySQL database')
			return conn

	except mysql.connector.Error as e:
				print(e)
 
#    finally:
#    conn.close()

def sql_insert(conn,data):
	try:
		conn.cursor().execute("""INSERT into tweets(date,user,text) values(%s,%s,%s)""",data)
		conn.commit()
		print('Inserted')
	except Exception as e: 
		print(e)
		conn.rollback()
		print('Insertion failed')


# Do we have to close the connection again?
#conn.close()
#print('Closed connection')

ts = time.time()
my_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


######################################
####	TWITTER						 
######################################


# Import your credentials
with open(path_credentials, "r") as file:
	creds = json.load(file)

# Create a class that inherits TwythonStreamer
class MyStreamer(TwythonStreamer):

	# Creat counter variable & date variable
	counter = 0
	start_date = datetime.datetime.now()
	
	# Logging
	def logging(self):
		if self.counter == 0:
			str = "Stream successfully established for Keywords: {}".format(keywords)
			logger.info(str)
		else: 
			str = "{} Tweets saved since start".format(self.counter)        
			logger.info(str)
		self.counter += 1
			
	# Received data
	def on_success(self, data):
		tweet_data = process_tweet(data)
		self.save_to_csv(tweet_data)
		self.save_to_sql(tweet_data)
		self.logging()

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
		sql_insert(conn,tweet)




# Filter out unwanted data
def process_tweet(tweet):

	d = {}
	d['date'] = tweet['created_at']
	d['user'] = tweet['user']['screen_name'].encode('utf-8')
#   d['user_loc'] = tweet['user']['location']
#	d['geo_loc'] = tweet['coordinates']
#	d['favorite_coun'] = tweet['favorite_count']
#	d['retweet_coun'] = tweet['retweet_count']
#    d['hashtags'] = [hashtag['text'].encode('utf-8')
#                   for hashtag in tweet['entities']['hashtags']]
	d['text'] = tweet['text'].encode('utf-8')
	return d




# Instantiate from our streaming class
stream = MyStreamer(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
					creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

# Wrapper function for MyStremer which restarts if error occurs 
def continous_streamer():
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
	conn = sql_connect()
	continous_streamer()
	 
if __name__ == '__main__':
		main()
