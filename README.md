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

#### General Information

The python script we are going to present relies on the existence of two files and one database to run smoothly.

In this sense before running the script it is necessary to make sure ot have:

(i) A csv file where the imported tweeets will be saved under the correct path location ../data/tweets.csv
 
(ii) A log file where the user can find documentation on the smoothly operation of the script; this should be saved under ../log/twitter.log

(iii) A fully specified mySQL database specified as in 2. above.

**Notice moreover that the naming conventions of the files should meet the one in the script. Should that not be the case it will be necessary to manually adjust the script.**

**The default language of the tweets is english and can be altered at line 178; moreover we invite you to control and update the mySQL connectivity entries at line 103.**


#### Libraries

The script relies on the following packages that should be downloaded -either on the virtual environment as in our case, or in the appropriate directory using the pip/pip3 package manager.

Would you wish to follow our approach we invite you to follow the following steps:

1. Actiavte and switch to your local environment
```
source /home/shared/venv/python36/bin/activate 
```

2. Dowload the needed packages
```
pip install json
pip install twython
pip mysql.connector
```

#### Code

Please find the python code for the project in the above src directory in the twystream.py file. We tried to describe the code in the most exhaustive possible way.


#### Instruction for the script execution

Once you imported the python script, created the supporting files and database and updated the connectivity and naming appropriately you will be able to run the script through the following command:

```
python/python3 <path>/twystream.py
```

The script will start running at this point. Notice that the script will run infinitely as when errors occurs the program will simply reactivate after 5 sec. 

You can therefore interrupt the execution of the program with the Keyboard interrupt command. It is moreover advisable to run the program in the background by running the following code
```
ASK ALEX
```
Moreover due to the set up of a log file of reference in the python script you will be able to follow and check the operations of the program by inspecting the **twitter.log** file generated at the begging.

**Congrats!** You have at this stage a fully functional program automatically downloading and importing the tweets of your specific interest. You can find them both in your database as well as in the csv file.

## 4. Crontab Set Up
