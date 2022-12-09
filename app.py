# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
 
 
app = Flask(__name__)
 
 
app.secret_key = 'your secret key'
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'sapmedia'
 
 
mysql = MySQL(app)
 
 
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('user.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('username', None)
   return redirect(url_for('login'))
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'fname' in request.form and 'mname' in request.form and 'lname' in request.form and 'language' in request.form:
        username = request.form['username']
        password = request.form['password']
        fname = request.form['fname']
        mname = request.form['mname'] 
        lname = request.form['lname']
        language = request.form['language']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        user = cursor.fetchone()
        if user:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO user VALUES (% s, % s, % s, % s, % s, % s)', (username, password, fname, mname, lname, language, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
 
@app.route('/movie', methods =['GET', 'POST'])
def movie(): #This fuction will not be ready until the database is set up 
    msg = ''
    if request.method == 'POST' and 'movieTitle' in request.form and 'genre' in request.form and 'platform' in request.form and 'summary' in request.form and 'movieTime' in request.form and 'director' in request.form and 'moviePoster' in request.form:
        movieTitle = request.form['movieTitle']
        genre = request.form['genre']
        platform = request.form['platform']
        summary = request.form['summary'] 
        movieTime = request.form['movieTime']
        director = request.form['director']
        moviePoster = request.form['moviePoster'] #Not in databse yet 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO movie (movieTitle,Summary,Director,movie_time,moviePoster) VALUES (% s, % s, % s, % s, % s)', (movieTitle, summary, director, movieTime, moviePoster,  )) #Fix this line as it will not insert right now 
        mysql.connection.commit()
        msg = 'You have successfully added your movie!'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('movie.html', msg = msg)

if __name__ == "__main__":
    app.run(host ="localhost", port = int("5000"))