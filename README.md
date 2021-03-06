# AWS-server
 
**March 2019**
 
**Marco Hassan**

**Alexander Steeb - alexander.steeb@gmx.de**

________________________

**Short description:**

This repository contains one of the three projects for the Master's class *Advanced Data Analysis and Numerical Methods* at the University of St. Gallen.

The aim was to set up a ```server```, set up a ```MySQL database```, import some data leveraging an ```API``` and finally to run a ```cron job```  periodically on the server to automate some process.

This file is intended as the documentation to the following **[Github: AWS-Server](https://github.com/MarcoHassan/AWS-server-)**

________________________
**For the project we decided to use the following tools:**

**Server:** AWS EC2 sever.

**Data Collection:** Collecting tweets matching user specified keywords continuously and in realtime using 
the Twitter API and a MySQL database.

**Cron job:** Daily back up of the database.
_________________________


## Introduction

Data is the most valuable resource of the 21st century. 
With a relatively small investment and some programming skills one can gain insights 
that would otherwise not be freely accessible. 
A lot of data - while in principle free - is often only available for a short period and mostly not in a convenient format. 

A server that runs 24/7 with a program that collects such data in a user specified format 
and at a regular interval can mitigate these problems.

Such a setup can be useful in a variety of different scenarios. For example, it can be used to generate data for research or business purposes or simply to build fun projects.

This project is intended to demonstrate how relatively easy it is to collect data otherwise not freely available in the same way

The structure of this documentation is as follows: 

1. Server setup
2. Database setup
3. Twitter API Connection, Data Collection, and Database Update
4. Plotting the acquired data

## 1. Server setup 
 
**First, we considered multiple different offerings for a server to host our project.**

The requirements were rather simple. 
+ At least on decent CPU core 
+ At least 1GB of ram/storage 
+ A good internet connection 
+ High availability

Especially the last point was important for this project since we will collect the twitter data 
not periodically but constantly 24/7.

Based on those requirements we chose a free tier AWS EC2 instance for the following reasons:
+ We already had an account and their free tier fulfills our basic requirements and promises extremely high reliability.
+ A basic understanding of the AWS ecosystem could be a valuable skill considering the importance AWS has today in all kinds of disciplines.
+ AWS offers free (limited) access to many of its features including a full year of free access to a basic EC2 instance.
+ AWS comes with many added features which are on the one hand intimidating and difficult to master but on the other hand can also be highly useful. 
  For example, we used the extensive monitoring capabilities of AWS to check the CPU usage of our system and similar stats from the browser without the need to connect to the instance.


**Next, we set up our instance in the following way:**

We will only briefly explain the EC2 setup since there are many great tutorial already online like for example 
[here](https://aws.amazon.com/getting-started/tutorials/launch-a-virtual-machine/?trk=gs_card).

1. **Create an AWS account** (credit card required but nothing will be charged since we only use the free tier EC2 instance)

2. **Launch an instance** with the following operating system: *Amazon Linux AMI 2018.03.0 (HVM), SSD Volume Type*. 
   This image already includes a variety of useful programs.

3. **Next select the instance type**. In this case we choose *t2.micro* which is the typ included in the free tier.
   If your program has higher hardware requirements you could simply select a stronger instance that fits your projects needs.

4. **Generate / select key pair** to access the instance and properly store it on your local machine. 
   This can include the need to change the privileges of the private key.
   ```
   chmod 0400 <path to .pem file>
   ``` 

5. **Connect to your server** using ssh. You will need the full path to the unique .pem file, the user name, and the server ip. 
   The last two can be found on the AWS-EC2 management console. 
   ```
   ssh -i <path to .pem file> <user>@<server-ip>
   ```

6. **Update everything** simply using the following command. This is always highly important and therefore best done first.
    ```
    sudo yum update
    ```
7. **Install python 3.6** if not already installed.
    ```
    sudo yum install python36 -y
    ```
    And verify where it is located.
    ```
    which python
    ```
 
8. **Create virtual environment** for easy package handling. 
   The tool **virtualenv** is highly useful when working on different python projects.
   It allows one to create an isolated python environments for each projects which solves many of the issues related to package management.
   Documentation for virtualenv can be found [here](https://virtualenv.pypa.io/en/stable/)
    
   First we install virtualenv.
   ```
   pip install virtualenv
   ``` 
   
   Next we create a new virtualenv as follows.
   ```
   cd ~ 
   mkdir venv
   cd venv
   virtualenv -p /usr/bin/python3.6 python36   
   ```
   The *-p flag* in the last line lets you specify which python version you want to use. We use Python 3.6.
   
   Now we can use the virtualenv. This command activates the virtualenv.
   ```
   source <path to virtualenv>/venv/python36/bin/activate
   ```
   Use `which python` to verify that it has worked. Once activated the `python` and `pip` commands reference to the earlier specified python version.
   The virtualenv can be exited with the command `deactivate`.
     
#### Additional tools we used
       
**Cyberduck**

For convenience reasons we used the free SFTP client **[Cyberduck](https://cyberduck.io)**
to quickly transfer files between our local machines and our server.

**Git/Github**

To further facilitate collaboration we used Git and Github. 
As mentioned above the whole project can also be found **[here](https://github.com/MarcoHassan/AWS-server-)**.


## 2. Database setup

Once the server was properly set up we first downloaded the MySQL software on the server running the following command.

```
sudo yum install mysql-server
```

After the successful installation on the server we specified the automatic start up of MySQL after a reboot and started the service:

```
sudo chkconfig mysqld on

sudo service mysqld start
```

Finally we specified the user administrator for the software. Of course, you can change the user name and password.
```
mysqladmin -u root
```

Given the successful general set up of the software we proceeded by creating a database for our tweets dataset called tweetsDB.
```
mysqladmin -u root -p create tweetsDB
```

And finally, we created a data table that matches the structure of our downloaded tweets.


```
CREATE TABLE tweets(

    user VARCHAR(60) NOT NULL,

    date TIMESTAMP NOT NULL,

    text  VARCHAR(300) NOT NULL,

    latitude FLOAT,
    longitude FLOAT,

    hashtags VARCHAR(300),

    INDEX user (user),

    INDEX date (date)
);
```
 
Notice the use of **INDEX** in the setup of the table. This allows for a faster query of the data by creating an additional index file.
 
 
## 3. Twitter API Connection, Data Collection, and Database Update

In this section we are going to explain the set up of a python script that automatically and in real time imports all tweets containing one or multiple user specified keywords.

Before delving on the details notice that our code heavily relies on the twython package available on github. 

_________________________________________________

Moreover pieces of code are referenced from:

**Source 1:** [Accessing Twitter API with Python](https://stackabuse.com/accessing-the-twitter-api-with-python/) 


**Source 2:** [MySQL - Connector/Python Coding Examples](https://dev.mysql.com/doc/connector-python/en/connector-python-examples.html)
________________________________________________

#### Twitter API Keys

In order to avoid of the misuse of tweets information, Twitter will require people willing to extract their tweets data through their APIs to do that through the use of ```API keys```. This will allow Twitter to keep track of a sepecific user queries and to get back to the user in case of misconduct.

In order to obtain such a pair of keys it will be necessary to register on [Twitter Apps](https://twitter.com/login?redirect_after_login=https%3A%2F%2Fdeveloper.twitter.com%2Fapps) and generate a new couple of keys.

With such a set of unique API keys it will be possible to leverage on the Twitter API. For portability we decided in our programs to save the API keys in a  ```json``` file and to import the keys in our python script by reading such file. This is the common used practice in order to deal with sensible information and to mask such private information when operating in shared projects.

An example of the `json` file layout is included.

#### General Information

The python script will interact with two different files and one database.

In this sense when running the script you will be asked to specify the path to a .json file where your twitter API credentials are properly stored.

Moreover you will be asked to specify the naming of two files that exist in your shell working directory or that will be created:

1. A **csv file** where the imported tweets will be saved in addition to the MySQL file. 
(Just to be save, since storage was not a limitation for our application)
 
2. A **log file** where the user can find documentation on the smooth operation of the script and for example the number of downloaded tweets.

Both will be saved under the working directory of your shell at the moment of running the python script.

Moreover, you will be asked to provide your login credentials for your MySQL database system  at line 103.

As a final note, please notice that the default language of the tweets to be downloaded is english and can be altered at line 178.

#### Libraries

The required packages for the script are documented in the **requirements.txt** file.

If you are using virtual environments you can simply create a new environment and run the following commands to install exactly the packages we use:

1. Create a new virtual environment
   ```
   virtualenv -p /usr/bin/python3.6 python36
   ```
   It could be that your python version is installed in a different location. In this case you would have to adjust the python path.

2. Activate the local environment
   ```
   source ./venv/python36/bin/activate
   ```

3. Install exactly the packages specified in the requirements.txt file 
   ```
   pip install -r requirements.txt
   ```
   The requirements file was created with the following command which saves the exact setup of an active virtualenv into a text file.
   ```
   pip freeze > requirements.txt
   ```
   
Alternatively you can, of course, also install the required packages specified in requirements.txt without virtualenv by simply using pip/pip3.  


#### Code

Please find the python code for the project in the twystream.py file in the src directory. 
We tried to describe the code in the most exhaustive way possible.

Do not hesitate to contact us in case of doubts.


#### Instruction for the script execution

Once you have imported the python script, created the supporting files and database, and updated the SQL and Twitter API credentials you will be able to run the script with the following command:

```
mkdir output
python src/twystream.py -d output/data_test -l output/log_test -c twitter_credentials -k 'Trump Kim' 
```

The script will start running at this point. Notice that the script will run infinitely as when errors occurs the program will simply reactivate after 5 sec. 

This ensures that after a disconnect for whatever reason the program automatically tries to reconnect immediately.

You can interrupt the execution of the program with the keyboard interrupt command. 

It is moreover advisable to run the program in the background by running the following code. This will also detach the command 
from the active shall so that it does not stop if the shell connection is lost.

```
nohup python -u  src/twystream.py -d output/data_test -l output/log_test -c twitter_credentials -k 'Trump Kim' &
```

Moreover due to the set up of a log file of reference in the python script you will be able to follow and check the operations of the program by inspecting the **.log** file generated at the beginning.

**Congrats!** You have at this stage a fully functional program automatically downloading and importing the tweets of your specific interest. You can find them both in your database as well as in the csv file.

## 4. Connect to the Database and Plot

Having the server fully running in the back it is possible now to set up python scripts connecting to the server, extracting data and performing the analysis of interest.

As an example we decided to set up briefly a python script connecting to the tweetsDB database, extracting the number of collected tweets by time frame. 

You can find the script in the repository above in the tweet_plot.py file available under the src repository.

If you use virtual environments to keep your working environment clean, recall to active the virtual environment first.

The collected tweets can then be quickly inspected selecting the time frame of interest as done in our script, where we decided to plot the number of collected tweets per day, plot them, and save the corresponding graph in the home directory of ec2-user of the server.

The result will be as in the image below and can be potentially used to visually inspect for the occurence of major events related to the keyword of interest.

![immagine](https://user-images.githubusercontent.com/42472072/54092644-e0f3c580-438e-11e9-9a7d-d623ae570f4d.png)


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

Given the structure of the mysqldump command that will save all of the syntax of the database it will be sufficient to run the following command 
```
mysql -u <user> -p < <path>/backup.sql
```

Should you be interested in compressing the backup or saving|restoring multiple databases at once, we refer you to this  [mysqldump Tutorial](http://webcheatsheet.com/sql/mysql_backup_restore.php).



