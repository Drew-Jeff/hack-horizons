from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Password",
        database="erp"
    )
    return conn

@app.route('/')
def home():
    return render_template('bujus clone.html')

@app.route('/assignments')
def assignments():
    return render_template('HomeWork.html')

@app.route('/lessons')
def lessons():
    return render_template('videos.html')

@app.route('/materials')
def materials():
    return render_template('study.html')

@app.route('/login')
def login():
    return "<h1>Login Page</h1>"
if __name__ == '__main__':
    app.run(debug=True)
