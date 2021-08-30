import sqlite3
import logging

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort



# Function to get a database connection.
# This function connects to database with the name `database.db`

conn_counter = 0

def get_db_connection():
    global conn_counter
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    conn_counter += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',   
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

 #Define the /metrics endpoint 
# Return a 200 HTTP JSON response
# Return the updated amount of posts (“post_count”) and number of connections made with the database (“db_connection_count”)
# len() returns the lenght of a string 

@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    response = app.response_class(
        response=json.dumps({"status": "success", "code": 0, "data": {"db_connection_count": conn_counter, "post_count": len(posts)}}),
        status=200,
        mimetype='application/json'
    )
    return response
    

# Return a 200 HTTP JSON response with a message “OK - healthy”
@app.route('/healthz')
def healthz(): 
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    response = app.response_class(
        response=json.dumps({'success': True, "data":"OK - healthy"}),
        status=200, 
        mimetype='application/json'
    )
    return response


# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)


# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info('Article does not exist')
      return render_template('404.html'), 404
    else:
      app.logger.info('Article request successfull')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    ## log line
    app.logger.info('About Us request successfull')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))
            
    app.logger.info('Article created successfull')
    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":

    ## stream logs to app.log file
    logging.basicConfig(filename='app.log',level=logging.DEBUG)

    app.run(host='0.0.0.0', port='3111')
