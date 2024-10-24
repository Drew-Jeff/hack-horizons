from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Establish a database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Password",
        database="erp"
    )
    return conn 
conn = get_db_connection()
cursor = conn.cursor()
query = """SELECT *from student  where student_id=1;"""
cursor.execute(query)
res = cursor.fetchall()
print(res)
student = {
    "id":res[0],
    "email":res[1],
    "fname":res[2],
    "lname":res[3],
    "dob":res[4],
    "phone":res[5],
    "mobile":res[6]
}
for i in student():
    print(i)
