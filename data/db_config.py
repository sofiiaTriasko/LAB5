import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
     host="localhost",
     database="store",
     user="root",
     password="password",
    )
    return  conn
