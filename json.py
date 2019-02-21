# Import the Twython library to work with twitter APIs

from twython import Twython
import json

# Enter your keys/secrets as strings in the following fields
credentials = {}
credentials['CONSUMER_KEY'] = '4WuVm8f55VXzkk8EaENvuALLU'
credentials['CONSUMER_SECRET'] = '2M8kWOrsn38NPo7c1Eu5zJ3iqlR38vgmbkvrbWcT5d2prAeO1O'
credentials['ACCESS_TOKEN'] = '1098540809887105024-kjzjuHhu8oZaKYnphXWKHA6rbwgYWf'
credentials['ACCESS_SECRET'] = 'X0UTVn6d8VigyDCylTXrbDqBUYKvzA1TKcKTP4lUB7oQx'

# Save the credentials object to file
with open("twitter_credentials.json", "w") as file:
    json.dump(credentials, file)
