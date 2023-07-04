from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import re
from database import execute_query_mysql, insert_data_mysql, check_username_exists, check_email_exists, check_credentials, get_user_data

app = Flask(__name__)

# דף הראשי
@app.route('/')
def index():
    # קבלת מספר הכניסות לאתר
    site_entries = get_site_entries_count()

    return render_template('index.html', site_entries=site_entries)


# בדיקה האם האימייל חוקי
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# דף הרשמה
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # בדיקה אם שם המשתמש כבר קיים
        if check_username_exists(username):
            flash('שם המשתמש כבר תפוס')
            return redirect('/register')

        # בדיקה אם האימייל כבר קיים
        if check_email_exists(email):
            flash('כתובת האימייל כבר קיימת')
            return redirect('/register')

        # בדיקה אם האימייל חוקי
        if not is_valid_email(email):
            flash('כתובת האימייל אינה חוקית')
            return redirect('/register')

        # שמירת הנתונים של המשתמש במסד הנתונים
        hashed_password = generate_password_hash(password)
        insert_data_mysql(username, hashed_password, email)
        flash('נרשמת בהצלחה!')
        return redirect('/login')

    return render_template('register.html')


# דף התחברות
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # בדיקה אם שם המשתמש והסיסמה תואמים לנתונים במסד הנתונים
        if check_credentials(username, password):
            # התחברות מוצלחת - שמירת המשתמש ב-session
            session['username'] = username
            flash('התחברת בהצלחה!')
            return redirect('/')

        flash('שם המשתמש או הסיסמה שגויים')
        return redirect('/login')

    return render_template('login.html')


# דף התנתקות
@app.route('/logout')
def logout():
    # בדיקה אם המשתמש מחובר
    if 'username' in session:
        # מחיקת המשתמש מ-session
        session.pop('username', None)
        flash('התנתקת בהצלחה!')
    return redirect('/')


# דף הלוח (רק למשתמשים מחוברים)
@app.route('/dashboard')
def dashboard():
    # בדיקה אם המשתמש מחובר
    if 'username' in session:
        # משתמש מחובר - הצגת הנתונים שלו בדף הלוח
        username = session['username']
        user_data = get_user_data(username)
        return render_template('dashboard.html', user=user_data)

    # אם המשתמש לא מחובר, הוא מועבר לדף הראשי
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
