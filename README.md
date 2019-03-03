# AWS-server-
Set up an AWS server and download twitter tweets periodically

**Authors: Marco Hassan, Alexander Steeb**

## Inrtroduction

** TO BE ADDED...**

## 1. Server set-up 

**TO BE ADDED...**

## 2. Database Set Up

Once the server was properly set up we downloaded first the mySQL software on the server running the following command.

```
sudo yum install mysql-server
```

After the successfull installation on the server we specified the automatic start up of mySQL at the next reconnection with the server

```
sudo chkconfig mysqld on

sudo service mysqld start
```

Finally we specified the user admistrator for the software
```
mysqladmin -u root password <enter your password>
```

Given the successful general set up of the software we proceeded by creating a database of reference for our tweet dataset.
```
mysqladmin -u root -p create tweetsDB
```

And finally we created a data table that would met the structure of our downloaded tweets
```
CREATE TABLE tweets(

user VARCHAR(60),

date TIMESTAMP,

text  VARCHAR(300),

favorite_count INT,

 

INDEX user (user), 

INDEX date (date),

INDEX favorite_count (favorite_count)

);
```
 
Notice the use of **INDEX** in setting up the table. This  will allow a faster query of the data without slowing down the software as the tweets dataset are **static** and imported tweets will not be dynamically adjusted once the tweets are imported.
 
## 3. Python Script

In this section we are going to explain the set up of a python scrript that automatically imports  all the tweets in a given lanaguage releting to a specific topic the user can choose when running the script.

Before dwelling on the details notice that our code heavily relies on the twython package available on github and copied in the current repository. 

Moreover pieces of code are referenced from:
_________________________________________________

**Source 1:** [Accessing Twitter API with Python](https://stackabuse.com/accessing-the-twitter-api-with-python/) 


**Source 2:** **ASK ALEX**
________________________________________________



# This python script heavily relies on the twython package. The idea is
# the one of downloading Twitter tweets in a given language relating to
# a topic to be specified by the user when running the script.

# This python script leverages the twython package to interact
# with the Twitter servers through their APIs. For the successfull
# execution of this script it is therefore necessary to dispose of an
# appropriate set of API keys in order to connect with the Twitter server.
# The API keys can be obtained online following twitter instructions and
# MUST be saved in a json file called twitter_json

# Once the above step is done it is necessary to create a log file where
# - to track the script execution - and a csv file - where the downloaded
# tweets will be saved -. Moreover it will be necessary to set up a
# mysql server.

# Notice that the naming of the csv, log and database should match the one
# used in this script. An adjustment below will be necessary if different
# naming will be used. In addition if you search tweets in a different
# language than english you should specify the condition at line 178.


Local installation of mysql

pip3 install mysql-connector-python

brew install mysql

brew services start mysql

mysqladmin -u root password 1234

mysqladmin -u root -p create tweetsDB

mysql -u root -p

