import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tmppassword11!",
    database="health"
)

cursor = conn.cursor()