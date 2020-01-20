from flask import Flask, render_template, g
import sqlite3

# Constants.
PATH = 'db/jobs.sqlite'

# Application.
app = Flask(__name__)

# Open connection.
def open_connection():
  connection = getattr(g, '_connection', None)

  if(connection == None):
    connection = g._connection = sqlite3.connect(PATH)
  
  connection.row_factory = sqlite3.Row
  return connection

# Close connection.
@app.teardown_appcontext
def close_connection(exception):
  connection = getattr(g, '_connection', None)
  if(connection != None): connection.close()

# Execute sql.
def execute_sql(sql, values = (), commit = False, single = False):
  connection = open_connection()

  cursor = connection.execute(sql, values)

  if(commit == True):
    results = connection.commit()
  else: 
    results = cursor.fetchone() if single else cursor.fetchall()

  cursor.close()

  return results

# Routes.
@app.route('/')
@app.route('/jobs')
def jobs():
  return render_template("index.html")
