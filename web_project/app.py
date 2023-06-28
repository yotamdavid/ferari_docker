from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
# חיבור לבסיס הנתונים
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='yotam',
    database='web_users'
)

# יצירת טבלת משתמשים אם היא עדיין לא קיימת
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    )
''')
db.commit()

# דף הראשי
@app.route('/')
def index():
    return render_template('index.html')


# רישום משתמש חדש
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # בדיקה אם שם המשתמש כבר קיים בבסיס הנתונים
        cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
        user = cursor.fetchone()
        if user:
            flash('שם המשתמש כבר תפוס')
            return redirect('/register')

        # בדיקה אם האימייל כבר קיים בבסיס הנתונים
        cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
        user = cursor.fetchone()
        if user:
            flash('כתובת האימייל כבר קיימת')
            return redirect('/register')

        # שמירת הנתונים של המשתמש בבסיס הנתונים
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)', (username, hashed_password, email))
        db.commit()

        flash('נרשמת בהצלחה!')
        return redirect('/login')

    return render_template('register.html')


# התחברות למערכת
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # בדיקה אם שם המשתמש והסיסמה תואמים לנתונים בבסיס הנתונים
        cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user[2], password):
            # התחברות מוצלחת - שמירת המשתמש ב-session
            session['username'] = username
            flash('התחברת בהצלחה!')
            return redirect('/dashboard')

        flash('שם המשתמש או הסיסמה שגויים')
        return redirect('/login')

    return render_template('login.html')


# דף הלוח (רק למשתמשים מחוברים)
@app.route('/dashboard')
def dashboard():
    # בדיקה אם המשתמש מחובר
    if 'username' in session:
        # משתמש מחובר - הצגת הנתונים שלו בדף הלוח
        username = session['username']
        cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
        user = cursor.fetchone()
        return render_template('dashboard.html', user=user)

    # אם המשתמש לא מחובר, הוא מועבר לדף הראשי
    return redirect('/')


# התנתקות מהמערכת
@app.route('/logout')
def logout():
    # בדיקה אם המשתמש מחובר
    if 'username' in session:
        # מחיקת המשתמש מ-session
        session.pop('username', None)
        flash('התנתקת בהצלחה!')
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
    app.run()
