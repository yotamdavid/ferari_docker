from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from redis import Redis
import re
from database import get_data_from_redis, add_data_to_redis, execute_query_mysql, insert_data_mysql

app = Flask(__name__)
app.secret_key = 'super secret key'
redis = Redis(host='localhost', port=6379)

# דף הראשי
@app.route('/')
def index():
    return render_template('index.html')


# בדיקה האם האימייל חוקי
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # בדיקה אם שם המשתמש כבר קיים
        if redis.exists(username):
            flash('שם המשתמש כבר תפוס')
            return redirect('/register')

        # בדיקה אם האימייל כבר קיים
        if redis.exists(email):
            flash('כתובת האימייל כבר קיימת')
            return redirect('/register')

        # בדיקה אם האימייל חוקי
        if not is_valid_email(email):
            flash('כתובת האימייל אינה חוקית')
            return redirect('/register')

        # שמירת הנתונים של המשתמש ב־Redis
        hashed_password = generate_password_hash(password)
        user_data = {'password': hashed_password, 'email': email}
        add_data_to_redis(username, user_data)
        flash('נרשמת בהצלחה!')
        return redirect('/login')

    return render_template('register.html')


# התחברות למערכת
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # בדיקה אם שם המשתמש והסיסמה תואמים לנתונים ב־Redis
        user_data = get_data_from_redis(username)
        if user_data and check_password_hash(user_data['password'], password):
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
        user_data = get_data_from_redis(username)
        return render_template('dashboard.html', user=user_data)

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
   app.run(host='192.168.160.1', port=5000)
