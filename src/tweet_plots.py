
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector  # to connect with the SQL server

##########################
# Plot tweets per second #
##########################


def tweetPlot():

    conn = mysql.connector.connect(
        host='localhost',
        database='tweetsDB',
        user='root',
        password='ENTER YOUR PASSWORD'
    )

    cur = conn.cursor()

    cur.execute(
        """SELECT
        EXTRACT(HOUR from date) AS hour,
        EXTRACT(MINUTE from date) AS minute,
        EXTRACT(DAY from date) as day,
        count(date) as count
        FROM tweets
        GROUP BY day, hour, minute;
        """
    )

    # Put it all to a data frame

    sql_data = pd.DataFrame(cur.fetchall())
    sql_data.columns = cur.column_names

    # Close the session
    conn.close()

    return sql_data


data = tweetPlot()

data.plot(kind='line', x='day', y='count')
plt.title('Tweeets per Day')
plt.savefig('/home/ec2-user/tweets.png')
