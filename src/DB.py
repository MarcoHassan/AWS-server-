import mysql.connector
import time
import datetime

# Adapted from http://www.mysqltutorial.org/python-mysql-insert/
 
def connect():
		""" Connect to MySQL database """
		try:
				conn = mysql.connector.connect(host='localhost',
																			 database='tweetsDB',
																			 user='root')
				if conn.is_connected():
						print('Connected to MySQL database')
						return conn

		except mysql.connector.Error as e:
				print(e)
 
#    finally:
#        conn.close()



ts = time.time()
my_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def insert(conn):
	try:
		conn.cursor().execute("""INSERT into tweets(date,user,text) values(%s,%s,%s)""",(my_timestamp,'test1','test2'))
		conn.commit()
		print('Inserted')
	except Exception as e: 
		print(e)
		conn.rollback()
		print('Insertion failed')


 
def main():
	conn = connect()
	insert(conn)
	conn.close()
	print('Closed connection')
 
if __name__ == '__main__':
		main()