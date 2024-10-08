from flask import Flask, render_template,request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello from Flask!'

if __name__ == '__main__':
  app.run(debug=True)

@app.route('/trial', methods=['GET', 'POST'])
def trial():
    if request.method == 'POST':
        return render_template('login.html');
    return render_template('register.html')
def connect_db():
    basedir = os.path.dirname(os.path.realpath(__file__))
    # Create the absolute path to the database file
    db_path = os.path.join(basedir, 'users.db')
    return sqlite3.connect('/var/www/html/flaskapp/users/users.db')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        # Insert data into SQLite
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)",
                    (username, password, first_name, last_name, email))
        conn.commit()
        conn.close()
        return redirect(url_for('display_user', username=username))
    return render_template('register.html')
@app.route('/display/<username>')
def display_user(username):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT first_name, last_name, email FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()

    if user:
        return f"Name: {user[0]} {user[1]}, Email: {user[2]}"
    return "User not found!"
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('display_user', username=username))
    return render_template('login.html')
