from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

db_config = {
    'host': 'db1',
    'user': 'root',
    'password': 'yotam',
    'database': 'users'
}

def execute_query(query, values=None, fetch=False):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = None
        
        cursor.close()
        connection.close()
        
        return result
        
    except mysql.connector.Error as err:
        print('Error:', err)
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        query = 'INSERT INTO users (username, password) VALUES (%s, %s)'
        values = (username, password)
        
        execute_query(query, values)
        
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        query = 'SELECT * FROM users WHERE username = %s AND password = %s'
        values = (username, password)
        
        result = execute_query(query, values, fetch=True)
        
        if result:
            session['username'] = username  # שמירת שם המשתמש ב-session
            return redirect('/')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # הסרת שם המשתמש מה-session
    return redirect('/')


# דפים נוספים
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/ferari_f8')
def ferari_f8():
    return render_template('ferari_f8.html')


@app.route('/ferari_roma')
def ferari_roma():
    return render_template('ferari_roma.html')


@app.route('/ferari_296')
def ferari_296():
    return render_template('ferari_296.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0', port=5000)
