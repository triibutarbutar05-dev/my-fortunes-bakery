import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="db_myfortunes"
)

print("Berhasil Terhubung!")