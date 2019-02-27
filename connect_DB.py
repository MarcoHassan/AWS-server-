# Source: https://pynative.com/python-mysql-insert-data-into-database-table/

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='tweetsDB',
                                         user='marco',
                                         password='Bianca&&007',
                                         buffered=True)
    sql_insert_query = "select * from tweets"
    cursor = connection.cursor()
    cursor.execute(sql_insert_query)
    for x in cursor:
        print(x)
    cursor.close()  # test
    cursor = connection.cursor()
    connection.commit()
    print ("Record inserted successfully into python_users table")
except mysql.connector.Error as error:
    connection.rollback()  # rollback if any exception occured
    print("Failed inserting record into python_users table {}".format(error))
finally:
    # closing database connection.
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
