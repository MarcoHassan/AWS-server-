# AWS-server-
Set up an AWS server and download twitter tweets periodically

**Authors: Marco Hassan, Alexander Steeb**

## Inrtroduction

** TO BE ADDED...**

## 1. Server set-up 

**TO BE ADDED...**

## 2. SQL SET UP

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

Local installation of mysql

pip3 install mysql-connector-python

brew install mysql

brew services start mysql

mysqladmin -u root password 1234

mysqladmin -u root -p create tweetsDB

mysql -u root -p

