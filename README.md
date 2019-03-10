# AWS-server

**Authors: Marco Hassan, Alexander Steeb**

This repository contains one of the three projects for the Master's class *Advanced Data Analysis and Numerical Methods* at the University of St. Gallen.

The aim was to set up a ```server```, set up a ```MySQL database```, import some data leveraging an ```API``` and finally to run a ```cron job```  periodically on the server to automate some process.

This file is intended as the documentation to the following Github:

TODO 
[Github - AWS-Server](GITHUB LINK)


For the project we decided to use the following tools:

________________________
**Server:** AWS ec2 sever.

**Data Collection:** Collection Tweets matching user specified keywords continously and in realtime using the Twitter API and a MySQL database.

**Cron job:** Daily back up of the database.
_________________________


## Introduction

Data is the most valuable resource of the 21st century. With a relatively small investment and some programming skills one can gain insights that would otherwise not be freely accessible. A lot of data - while in principle free - is only available for a short amount of time. 

A server that runs 24/7 with a program that collects such data in a user specified format and at a regular interval can mitigate these problems.

This can be useful in a variety of different scenarios. For example, it can be useful to generate data for research or business purposes or simply to build fun projects.

This project is intended to demonstrate how relatively easy it is to collect data otherwise not freely available in the same way

Structure: 

## 1. Set-up 
 
First, we considered multiple different offerings for a server to host our project.

The requirements were rather simple. It had to have at least on decent CPU core, at least 1gb of ram/storage and a good internet connection. Especially important for this project was the uptime of the server since we will acquire our twitter data not periodically but constantly 24/7.

Based on those requirements we chose a free tier AWS EC2 instance for the following reasons
o	We already had an account and their free tier fulfills our basic requirements and promises extremely high reliability
o	A basic understanding of the AWS Ecosystem could be a valuable skill considering the importance AWS today has in all kinds of disciplines.
o	AWS comes with many added features which are on the one hand intimidating and difficult to master but on the other hand also can be highly useful. For example, we used the extensive monitoring capabilities of AWS to check the CPU usage of our system and similar stats from the browser without the need to connect to the instance.

The steps that were necessary for the setup of our EC2 instance were the following:

Creating an account (credit card required but all we use is free tier)
Launch of the free tier ec2 instance with the following operating system:
o	LINUX […]

Connect to the server
 
Launch Linux instance 
Create pem key file
Change ownership of pem key file
chmod 0400 Server1.pem
 
Connect through ssh
 
Using the instance`s root name and public dns
 
Replace user/ server
ssh -i Server1.pem <user>@<server dns>
 
Update everything
```Sudo yum update all```
 
 
install python 3.6 
sudo yum install python36




### Launch instance and connect to instance

The first step is to set-up a server. We decided to use the free-tier AWS server. 

### Install / Update

### Create virtualenv

### Github setup

install python 3.6 
sudo yum install python36

Create virtual environment for easy package handling and because of:
"Also realize that some functions of the Amazon Linux AMI might rely on python pointing to version 2.7.x, so you’d probably be better off exploring virtualenv instead, but I digress."
(http://outofmyhead.olssonandjones.com/2018/02/24/how-to-install-python-3-x-on-amazon-ec2-instance/)


cd ~ 
mkdir venv
cd venv
virtualenv -p /usr/bin/python3.6 python36
source /home/ec2-user/venv/python36/bin/activate
source /home/shared/venv/python36/bin/activate
deactivate

Source: https://aws.amazon.com/premiumsupport/knowledge-center/python-boto3-virtualenv/


	- Due to the virtual environment both the commands python and pip link to the respective versions we use. So if you don't use a virtualenvironment you may need to use python3 and pip3 instead.
	- A simple pip install 
### Github setup (Link to tutorial)



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

**#favorites???**

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

Before delving on the details notice that our code heavily relies on the twython package available on github and copied in the current repository. 

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

#### Twitter API Keys

In order to avoid of the misuse of tweets information, Twitter will require people willing to extract their tweets data through their APIs to do that through the use of ```API keys```. This will allow Twitter to keep track of a sepecific user queries and to get back to the user in case of misconduct.

In order to obtain such pair of keys it will be necessary to register on [Twitter Apps](https://twitter.com/login?redirect_after_login=https%3A%2F%2Fdeveloper.twitter.com%2Fapps) and generate a new couple of keys.

With such set of unique API keys it will be possible to leverage on the Twitter API. For portability we decided in our programs to save the API keys in a  ```json``` file and to import the keys in our python script by reading such file. This is the common used practice in order to deal with sensible information and to mask such private information when operating in shared projects.

#### Libraries

The required packages for the script are documented in the **requirements.txt** file.

If you are using virtual environments you can simply create a new environment and run the following commands to install exactly the packages we use:

1. Create a new virtual environment
```
mkdir venv-server
cd venv-server
virtualenv -p /usr/bin/python3.6 python36
```
It could be that your python version is installed in a different location. In this case you would have to adjust the python path.


2. Activate the local environment
```
source ./venv/python36/bin/activate
```

3. Install exactly the packages specified in the requirements.txt file 
```
pip install json
pip install twython
pip install mysql.connector
pip install matplotlib.pyplot 
pip install pandas
```

Alternatively you can, of course, also install the required packages specified in requirements.txt without virtualenv by simply using pip/pip3.  


#### Code

Please find the python code for the project in the twystream.py file in the src directory. 
We tried to describe the code in the most exhaustive way possible.

Do not hesitate to contact us in case of doubts.


#### Instruction for the script execution

Once you have imported the python script, created the supporting files and database, and updated the SQL and Twitter API credentials you will be able to run the script with the following command:

```
python <path>/twystream.py
```

The script will start running at this point. Notice that the script will run infinitely as when errors occurs the program will simply reactivate after 5 sec. 

This ensures that after a disconnect for whatever reason the program automatically tries to reconnect immediately.

You can interrupt the execution of the program with the keyboard interrupt command. It is moreover advisable to run the program in the background by running the following code

```
 nohup ....
```

Moreover due to the set up of a log file of reference in the python script you will be able to follow and check the operations of the program by inspecting the **twitter.log** file generated at the beginning.

**Congrats!** You have at this stage a fully functional program automatically downloading and importing the tweets of your specific interest. You can find them both in your database as well as in the csv file.

## 4. Connect to the Database and Plot

Having the server fully running in the back it is possible now to set up python scripts connecting to the server, extracting data and performing the analysis of interest.

As an example we decided to set up briefly a python script connecting to the tweetsDB database, extracting the number of collected tweets by time frame. 

You can find the script in the repository above in the tweet_plot.py file available under the src repository.

If you use virtual environments to keep your working environment clean, recall to active the virtual environment first.

The collected tweets can then be quickly inspected selecting the time frame of interest as done in our script, where we decided to plot the number of collected tweets per day, plot them, and save the corresponding graph in the home directory of ec2-user of the server.

The result will be as in the image below and can be potentially used to visually inspect for the occurence of major events related to the keyword of interest.

![immagine](https://user-images.githubusercontent.com/42472072/53753139-d29a3b00-3eb0-11e9-9410-6bb412c74c60.png)


## 5. Crontab Set Up

In this last part we are going to descrbe the cron job set up in order to run a backup of the database periodically and to automatically generated an updated plot as the one shown above.

As a first step it is important to operate through the root user to set up the cron job or to give sudo permission to the user of choice.

Given the well being of the permissions, it is necessary to specify the cron job in the correct repository.

For the project we decided to implement the job in the generally valid */var/spool/cron* repository. An alternative approach would consists in saving the different cron jobs under the minute/hourly/etc. repositories.

```
# go to the directory where you aim to specify the cron job
cd /var/spool/cron

# to create a crontab in the repository where to specify the cron job to be executed
crontab -e 
```

After the following step it will be possible to specify the desired time and job to be executed with your favourite editor.

In our case, we decided to run an automatic backup of the mySQL database every 24h at 01:01 a.m., and to save an updated png plot of the downloaded tweets each day at 23:59 running the following command

```
########
# Cron #
########

MAILTO= <mail> # Enter a mail on, which to be informed about the cron executions.

01 0 1 * * echo "Cron in running at: $(date)" >> /home/ec2-user/cron.log && /usr/bin/mysqldump -u root -p'ENTER YOUR PASSWORD' tweetsDB > /home/ec2-user/backup.sql && echo "Cron is running smoothly and saved a backup of the tweewtsDB database at: $(date)" >> /home/ec2-user/cron.log || echo "At $(date) back-up did not complete asan error occured." >> /home/ec2-user/cron.log

59 23 * * * echo "Cron running at: $(date) and generating the updated tweets.png plot" >> /home/ec2-user/prova.log && source /home/ec2-user/venv/python36/bin/activate >> /home/ec2-user/prova.log 2>&1 && python /home/ec2-user/tweets_plot2.py && echo "Cron job terminated and successfully generated the plot" >> /home/ec2-user/prova.log || "Cron terminating without plotting. An error occured." >> /home/ec2-user/prova.log
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
# 01  01  *  *  *  ## Part 1
# 59  23  *  *  *  ## Part 2
```

(ii) Inform the user that the cron job start running and specify the hour.
```
echo "Cron in running at: $(date)" >> /home/ec2-user/cron.log ## Part 1

echo "Cron running at: $(date) and generating the updated tweets.png plot" >> /home/ec2-user/prova.log  ## Part 2
```

(iii)(a) Run the backup in Part 1
```
&& /usr/bin/mysqldump -u root -p'ENTER YOUR PASSWORD' tweetsDB > /home/ec2-user/backup.sql
```
(iii)(b) Run the python script for updating the recent tweets trends plot in Part 2
```
## Activate virtual environment
&& source /home/ec2-user/venv/python36/bin/activate >> /home/ec2-user/prova.log 2>&1 

## Generate the plot
&& python /home/ec2-user/tweets_plot2.py 
```

(iv) If successful (*the &&*) inform the user in the log file that the backup of the server was performed and the plot was generated correctly and saved into a ```png```file.
```
&& echo "Cron is running smoothly and saved a backup of the tweewtsDB database at: $(date)" >> /home/ec2-user/cron.log

&& echo "Cron job terminated and successfully generated the plot" >> /home/ec2-user/prova.log
```

(v) Else, when unsuccessful (*the ||*) infrom the  user in the log file that the backup and/or the plotting failed.
```
|| echo "At $(date) back-up did not complete asan error occured." >> /home/ec2-user/cron.log

|| "Cron terminating without plotting. An error occured." >> /home/ec2-user/prova.log
```

#### Restore the database through the backup file

#TODO 
Given the structure of the mysqldump command that will save all of the syntax of the database it will be sufficient to run the following command 
```
mysql -u <user> -p < <path>/backup.sql
```

Should you be interested in compressing the backup or saving|restoring multiple databases at once, we refer you to this  [mysqldump Tutorial](http://webcheatsheet.com/sql/mysql_backup_restore.php).



