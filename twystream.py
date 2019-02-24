from twython import TwythonStreamer 
import pandas as pd
import json
import csv
import datetime


# Import your credentials
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

# Filter out unwanted data
def process_tweet(tweet):

    d = {}
    d['date'] = tweet['created_at']
    d['user'] = tweet['user']['screen_name']
    d['user_loc'] = tweet['user']['location']
    d['geo_loc'] = tweet['coordinates']
    d['favorite_coun'] = tweet['favorite_count']
    d['retweet_coun'] = tweet['retweet_count']
    d['hashtags'] = [hashtag['text']
                    for hashtag in tweet['entities']['hashtags']]
    d['text'] = tweet['text']
    return d


# Create a class that inherits TwythonStreamer
class MyStreamer(TwythonStreamer):

    # Creat counter variable & date variable
    counter = 0
    start_date = datetime.datetime.now()
    
    print("{}: Stream successfully established".format(datetime.datetime.now().strftime("%c")))
    
    # Received data
    def on_success(self, data):

        # Only collect tweets in English
        if data['lang'] == 'en':
            tweet_data = process_tweet(data)
            self.save_to_csv(tweet_data)
            self.counter += 1
            str = "{}: {} Tweets saved since start".format(datetime.datetime.now().strftime("%c"),self.counter)        
            print(str)

    # Problem with the API
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

    # Save each tweet to csv file
    def save_to_csv(self, tweet):
        with open(r'data/saved_tweets.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(list(tweet.values()))

# Instantiate from our streaming class
stream = MyStreamer(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
                    creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

# Start the stream
stream.statuses.filter(track='Tradewar,Trade US China')




