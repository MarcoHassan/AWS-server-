# Import the Twython class
from twython import Twython
import pandas as pd
import json

# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

# Instantiate an object
twitter = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

# Create our query
query = {'q': 'tradewar',
         'result_type': 'recent',  # both popular and most recent results
         'count': 100,
         'lang': 'en',  # restrict results to english language tweets
         }

# Search tweets
dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}

for status in twitter.search(**query)['statuses']:
    dict_['user'].append(status['user']['screen_name'])
    dict_['date'].append(status['created_at'])
    dict_['text'].append(status['text'])
    dict_['favorite_count'].append(status['favorite_count'])

# Structure data in a pandas DataFrame for easier manipulation
df = pd.DataFrame(dict_)
#df.sort_values(by='favorite_count', inplace=True, ascending=False)

file_name = 'temp_csv.csv'
df.to_csv(file_name, encoding='utf-8', index=False)
