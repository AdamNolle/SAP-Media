# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from base64 import b64encode
 
 
app = Flask(__name__)
 
 
app.secret_key = 'your secret key'
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'   #Change your username if applicable 
app.config['MYSQL_PASSWORD'] = 'password' #Change the password here if appliable 
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
            return render_template('home.html', msg = msg)
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
        fgenre = request.form['language']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        user = cursor.fetchone()
        if user:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO user (username,password,fName,mName,lName) VALUES (% s, % s, % s, % s, % s)', (username, password, fname, mname, lname, ))
            mysql.connection.commit()
            cursor.execute('INSERT INTO User_Genre VALUES (% s, % s)', (username, fgenre, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
 
@app.route('/addmovie', methods =['GET', 'POST'])
def addmovie(): #Need to add in genre, platform, user and platform ratings  
    msg = ''

    if request.method == 'POST' and 'movieTitle' in request.form and 'genre' in request.form and 'platform' in request.form and 'summary' in request.form and 'movieTime' in request.form and 'director' in request.form and 'userRating' in request.form and 'platformRating' in request.form and 'moviePoster' in request.form:
        movieTitle = request.form['movieTitle']
        genre = request.form['genre']
        platform = request.form['platform']
        summary = request.form['summary'] 
        movieTime = request.form['movieTime']
        director = request.form['director']
        userRating = request.form['userRating']
        platformRating = request.form['platformRating']
        moviePoster = request.form['moviePoster'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO movie (name,summary,director,duration,moviePoster) VALUES (% s, % s, % s, % s, % s)', (movieTitle, summary, director, movieTime, moviePoster,  )) 
        mysql.connection.commit()
        cursor.execute('INSERT INTO Movie_Genre (movieID,genreName) VALUE ((SELECT id FROM movie where name = %s LIMIT 1),%s)', (movieTitle,genre, ))
        mysql.connection.commit()
        cursor.execute('INSERT INTO Watch_On (movieID,platformName) VALUE ((SELECT id FROM movie where name = %s LIMIT 1),%s)', (movieTitle,platform, ))
        mysql.connection.commit()
        cursor.execute('INSERT INTO Rating (platformRating,platformName,username,movieID) VALUE (%s,%s,%s,(SELECT id FROM movie where name = %s LIMIT 1))', (platformRating,platform,session['username'], movieTitle, ))
        mysql.connection.commit()
        #cursor.execute("SELECT id FROM Rating where movieID = (SELECT id FROM movie where name = %s Limit 1)", (movieTitle,))
        #ratingID = cursor.fetchone()
        cursor.execute('INSERT INTO User_Rating (ratingID,userRating) VALUE ((SELECT id FROM Rating where movieID = (SELECT id FROM movie where name = %s LIMIT 1) Limit 1),%s)', (movieTitle,userRating, ))
        mysql.connection.commit() 
        msg = 'You have successfully added your movie!'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('addmovie.html', msg = msg)

@app.route('/profile', methods =['GET', 'POST'])
def profile():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'fname' in request.form and 'mname' in request.form and 'lname' in request.form and 'language' in request.form:
        username = request.form['username']
        password = request.form['password']
        fname = request.form['fname']
        mname = request.form['mname'] 
        lname = request.form['lname']
        fgenre = request.form['language']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        user = cursor.fetchone()
        if user:
            msg = 'Account already exists !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('UPDATE user SET  username =% s, password =% s, fname =% s, mname =% s, lname =% s WHERE username =% s', (username, password, fname, mname, lname, (session['username'], ), ))
            mysql.connection.commit()
            cursor.execute('UPDATE User_Genre set username =% s, favoriteGenre = %s WHERE username=%s' , (username,fgenre,(session['username'],),))
            session['username'] = username
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('profile.html', msg = msg)

@app.route('/editmovie', methods =['GET', 'POST'])
def editmovie(): #Need to add in genre, platform, user and platform ratings  
    msg = ''
    if request.method == 'POST' and 'movieTitle' in request.form and 'genre' in request.form and 'platform' in request.form and 'summary' in request.form and 'movieTime' in request.form and 'director' in request.form and 'userRating' in request.form and 'platformRating' in request.form and 'moviePoster' in request.form:
        movieTitle = request.form['movieTitle']
        genre = request.form['genre']
        platform = request.form['platform']
        summary = request.form['summary'] 
        movieTime = request.form['movieTime']
        director = request.form['director']
        userRating = request.form['userRating']
        platformRating = request.form['platformRating']
        moviePoster = request.form['moviePoster'] 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE movie SET  name =% s, summary =% s, director =% s, duration =% s, moviePoster =% s WHERE name = %s', (movieTitle, summary, director, movieTime, moviePoster, movieTitle, ))
        mysql.connection.commit()
        cursor.execute('SELECT id FROM movie where name = %s Limit 1', (movieTitle,))
        movieID = cursor.fetchone()
        movieID = movieID['id']
        cursor.execute('UPDATE Movie_Genre SET genreName = %s WHERE movieID = % s', (genre,movieID,))
        cursor.execute('UPDATE Watch_On SET platformName = %s WHERE movieID = % s', (platform,movieID,))
        cursor.execute('UPDATE Rating SET platformRating = %s, platformName = %s, username = %s  WHERE movieID = %s', (platformRating,platform,session['username'],movieID,))
        cursor.execute('SELECT id FROM Rating where movieID = %s Limit 1', (movieID,))
        ratingID = cursor.fetchone()
        ratingID = ratingID['id']
        cursor.execute('UPDATE User_Rating set userRating=%s where ratingID = %s', (userRating,ratingID, ))
        msg = 'You have successfully added your movie!'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('editmovie.html', msg = msg)



@app.route('/searchmovie', methods=['GET', 'POST'])
def searchmovie():
    if request.method == "POST":
        try:
            movie = request.form['movie']
            # search by author or book
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT name FROM movie where movieTitle = %s", (movie,))
            title = cursor.fetchone()
            cursor.execute("SELECT summary FROM movie where movieTitle = %s", (movie,))
            summary = cursor.fetchone()
            cursor.execute("SELECT director FROM movie where movieTitle = %s", (movie,))
            director = cursor.fetchone()
            cursor.execute("SELECT duration FROM movie where movieTitle = %s", (movie,))
            movie_time = cursor.fetchone()
            cursor.execute("SELECT moviePoster FROM movie where movieTitle = %s", (movie,))
            moviePoster = cursor.fetchone()
            cursor.execute("SELECT watched FROM movie where movieTitle = %s", (movie,))
            Watched = cursor.fetchone()
            stringList = [title,summary,director,movie_time,moviePoster,Watched]
            # all in the search box will return all the tuples
            return render_template('searchResults.html', movie = stringList )
        except:
            msg = "There is no movie by that title"
            return render_template('search.html', msg = msg) 
        
    
    return render_template('search.html')
# end point for inserting data dynamicaly in the database



if __name__ == "__main__":
    app.debug = True
    app.app_context()
    app.run(host ="localhost", port = int("5000"))