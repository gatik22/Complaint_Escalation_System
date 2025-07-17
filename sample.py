import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_mysql_password",
    database="yash_infocity"
)
print(conn.is_connected())
