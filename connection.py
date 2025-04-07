import mysql.connector as myconn

mydb=myconn.connect(host="localhost",user="root",password="root")

db_cursor = mydb.cursor()

db_cursor.execute("create database learncoding")
print("database created")