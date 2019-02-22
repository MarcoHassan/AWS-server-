# Import the Twython library to work with twitter APIs

import twython
import json
print (json.__file__)

# Enter your keys/secrets as strings in the following fields
credentials = {}
credentials['CONSUMER_KEY'] = 'TMl0uTQk7PLcVMjjnCgEuK0Aq'
credentials['CONSUMER_SECRET'] = 'C7e9UptOOGVVAtbNpKOzEx1lfspaMm16jD4MOhmzXBVcCuFQa8'
credentials['ACCESS_TOKEN'] = '1098540809887105024-jV7APzfQHY5LoOvWl4x8irwEU2x1ql'
credentials['ACCESS_SECRET'] = '8RqDhkG4BqTaiNcETAGf2of87GNxmZ0NXeTdh6sFpknHT'

# Save the credentials object to file
with open("twitter_credentials.json", "w") as file:
    json.dump(credentials, file)
