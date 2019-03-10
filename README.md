# AWS-server

**Authors: Marco Hassan, Alexander Steeb**

This repository contains one of the three projects for the Master's class *Advanced Data Analysis and Numerical Methods* at the University of St. Gallen.

The aim was to set up a ```server```, set up a ```MySQL database```, import some data leveraging an ```API``` and finally to run a ```cron job```  periodically on the server to automate some process.

For the project we decided to use the following tools:

________________________
**Server:** AWS ec2 sever.

**Data Collection:** Collection Tweets matching user specified keywords continously and in realtime using the Twitter API and a MySQL database.

**Cron job:** Daily back up of the database.
_________________________


## Introduction

**TO BE ADDED...**

## 1. Server set-up 

**TO BE ADDED...**

## 2. Database Set Up

Once the server was properly set up we first downloaded the MySQL software on the server running the following command.

```
sudo yum install Mysql-server
```

After the successful installation on the server we specified the automatic start up of MySQL after a reboot and started the service:

```
sudo chkconfig mysqld on

sudo service mysqld start
```

Finally we specified the user administrator for the software. Of course you can change the user name and password.
```
mysqladmin -u root password <enter your password>
```

Given the successful general set up of the software we proceeded by creating a database for our tweet dataset called tweetsDB.
```
mysqladmin -u root -p create tweetsDB
```

And finally we created a data table that matches the structure of our downloaded tweets.
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
 
Notice the use of **INDEX** in the setup of the table. This allows for a faster query of the data by creating an additional index file.
 
 
## 3. Twitter API Connection, Data Collection, and Database Update

In this section we are going to explain the set up of a python script that automatically and in real time imports all tweets containing one or multiple user specified keywords.

Before dwelling on the details notice that our code uses the Twython package available on github as a wrapper for the Twitter API. 

Moreover pieces of code are referenced from:
_________________________________________________

**Source 1:** [Accessing Twitter API with Python](https://stackabuse.com/accessing-the-twitter-api-with-python/) 


**Source 2:** [MySQL - Connector/Python Coding Examples](https://dev.mysql.com/doc/connector-python/en/connector-python-examples.html)
________________________________________________

#### General Information

The python script we are going to present relies on the existence of two files and one database to run smoothly.

In this sense before running the script it is necessary to make sure to have:

**Stimmt das???**

(i) A csv file where the imported tweets will be saved under the correct path location ../data/tweets.csv
 
(ii) A log file where the user can find documentation on the smoothly operation of the script; this should be saved under ../log/twitter.log

(iii) A MySQL database as specified above.

*Note 1:* the naming conventions of the files should meet the one in the script. Should that not be the case it will be necessary to manually adjust the script.

*Note 2:* the default language of the tweets is english and can be altered at line 178; moreover we invite you to control and update the MySQL connectivity entries at line 103.


#### Libraries

The required packages for the script are documented in the **requirements.txt** file.

If you are using virtual environments you can simply create a new environment and run the following commands to install exactly the packages we use:

1. Create a new virtual environment
```
mkdir venv
cd venv
virtualenv -p /usr/bin/python3.6 python36
```
It could be that your python version is installed in a different location. In this case you would have to adjust the python path.


2. Activate and switch to your local environment
```
source ./venv/python36/bin/activate
```

3. Install exactly the packages specified in the requirements.txt file 
```
pip install -r requirements.txt
```

Alternatively you can, of course, also install the required packages without virtualenv by simply using pip/pip3.  


#### Code

Please find the python code for the project in the above src directory in the twystream.py file. 
We tried to describe the code in the most exhaustive way possible.

Do not hesitate to contact us in case of doubts.


#### Instruction for the script execution

Once you imported the python script, created the supporting files and database, and updated the connectivity and naming appropriately you will be able to run the script through the following command:

```
python <path>/twystream.py
```

The script will start running at this point. Notice that the script will run infinitely as when errors occurs the program will simply reactivate after 5 sec. 

You can therefore interrupt the execution of the program with the Keyboard interrupt command. It is moreover advisable to run the program in the background by running the following code
```
ASK ALEX
```
Moreover due to the set up of a log file of reference in the python script you will be able to follow and check the operations of the program by inspecting the **twitter.log** file generated at the begging.

**Congrats!** You have at this stage a fully functional program automatically downloading and importing the tweets of your specific interest. You can find them both in your database as well as in the csv file.

## 4. Crontab Set Up

In this last part we are going to descrbe the cron job set up in order to run a backup of the precious database periodically.

As a first step it is important to operate through the root user to set up the cron job or to give sudo permission to the user of choice.

Given the well being of the permissions, it is necessary to specify the cron job in the correct repository.

For the project we decided to implement the job in the generally valid */var/spool/cron* repository. An alternative approach would consists in saving the different cron jobs under the minute/hourly/etc. repositories.

```
# go to the directory where you aim to specify the cron job
cd /var/spool/cron

# to create a crontab in the repository where to specify the cron job to be executed
crontab -e cron linux repository
```

After the following step it will be possible to specify the desired time and job to be executed with your favourite editor.

In our case, we decided to run an automatic backup of the mySQL database every 24h at 01:01 a.m., running the following command

```
########
# Cron #
########

MAILTO= <mail> # Enter a mail on, which to be informed about the cron executions.

01 0 1 * * echo "Cron in running at: $(date)" >> /home/ec2-user/cron.log && /usr/bin/mysqldump -u root -p'ENTER YOUR PASSWORD' tweetsDB > /home/ec2-user/backup.sql && echo "Cron is running smoothly and saved a backup of the tweewtsDB database at: $(date)" >> /home/ec2-user/cron.log || echo "At $(date) back-up did not complete asan error occured." >> /home/ec2-user/cron.log
```

#### Breaking the code up

(i) Time selection
```
# Example of job definition:
#  .---------------- minute (0 - 59)
#  |   .------------- hour (0 - 23)
#  |   |  .---------- day of month (1 - 31)
#  |   |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
#  |   |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
#  |   |  |  |  |
# 01  01  *  *  * 
```

(ii) Inform the user that the cron job start running and specify the hour.
```
echo "Cron in running at: $(date)" >> /home/ec2-user/cron.log
```

(iii) Run the backup 
```
&& /usr/bin/mysqldump -u root -p'ENTER YOUR PASSWORD' tweetsDB > /home/ec2-user/backup.sql
```

(iv) If successful (*the &&*) inform the user in the log file that the backup of the server was performed
```
&& echo "Cron is running smoothly and saved a backup of the tweewtsDB database at: $(date)" >> /home/ec2-user/cron.log
```

(v) Else, when unsuccessful (*the ||*) infrom the  user in the log file that the backup failed.
```
|| echo "At $(date) back-up did not complete asan error occured." >> /home/ec2-user/cron.log
```

#### Restore the database through the backup file

Given the structure of the mysqldump command that will save all of the syntax of the database it will be sufficient to run the following command 
```
mysql -u <user> -p < <path>/backup.sql
```

Should you be interested in compressing the backup or saving|restoring multiple databases at once, we refer you to this  [mysqldump Tutorial](http://webcheatsheet.com/sql/mysql_backup_restore.php).

## 5. Connect to the Database and Plot

Having the server fully running in the back it is possible now to set up python scripts connecting to the server, extracting data and performing the analysis of interest.

As an example we decided to set up briefly a python script connecting to the tweetsDB database, extracting the number of collected tweets by time frame. 

You can find the script in the repository above in the tweet_plot.py file available under the src repository.

If you use virtual environments to keep your working environment clean, recall to active the virtual environment first.

The collected tweets can then be quickly inspected selecting the time frame of interest as done in our script, where we decided to plot the number of collected tweets per day, plot them, and save the corresponding graph in the home directory of ec2-user of the server.

The result will be as in the image below and can be potentially used to visually inspect for the occurence of major events related to the keyword of interest.

![immagine](https://user-images.githubusercontent.com/42472072/53753139-d29a3b00-3eb0-11e9-9410-6bb412c74c60.png)



