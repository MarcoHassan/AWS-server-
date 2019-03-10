###################################
# Plot number of tweets over time #
###################################

# Code for the Server Project
#
# alexander.steeb@student.unisg.ch &
# marco.hassan30@gmail.com
# Started 2019-02-27


import pandas as pd
import mysql.connector  # to connect with the SQL server
import matplotlib.pyplot as plt


##########################
# Get Data from Database #
##########################

def tweetPlot():

	conn = mysql.connector.connect(
		host='localhost',
		database='tweetsDB',
		user='root',
		password = '1234'
	)

	cur = conn.cursor()

	cur.execute(
		"""
		SELECT date as date
		FROM tweets;
		"""
	)

	# Put it all to a data frame
	sql_data = pd.DataFrame(cur.fetchall())
	sql_data.columns = cur.column_names

	# Close the session
	conn.close()

	return sql_data


data = tweetPlot()

##########################
# Clean Data abd plot it #
##########################

data['count'] = 1
data.set_index('date', inplace=True)

# Resample to 5 minute intervals
data = data.resample('5T').sum()

# Plot the data
fig, ax = plt.subplots(figsize=(15, 7))
data.plot(ax=ax, kind='line')

plt.title('Tweets per 5 minutes containing both Trump and Kim')
plt.savefig('/home/ec2-user/tweets.png')

