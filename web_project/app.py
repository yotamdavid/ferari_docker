from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'db1',
    'port': '3306',
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
        
        # בדיקה שהסיסמה עומדת בדרישות
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            session['password_requirements'] = 'הסיסמה חייבת להיות מורכבת מלפחות 8 תווים, כולל אותיות ומספרים.'
            return redirect('/register')
        
        query = 'INSERT INTO users (username, password_hash) VALUES (%s, %s)'
        password_hash = generate_password_hash(password)
        values = (username, password_hash)
        execute_query(query, values)
        
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = 'SELECT * FROM users WHERE username = %s'
        values = (username,)
        result = execute_query(query, values, fetch=True)
        if result:
            if check_password_hash(result[0][2], password):
                session['username'] = username
                return redirect('/')
            else:
                flash('סיסמה שגויה. אנא נסה שוב.', 'error')
        else:
            flash('שם משתמש לא קיים. אנא נסה שוב.', 'error')
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

# שאר הדפים
# ...

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0', port=5000)
