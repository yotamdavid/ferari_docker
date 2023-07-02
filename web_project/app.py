from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import re
import redis

app = Flask(__name__)
app.secret_key = 'super secret key'
r = redis.Redis(host='redis', port=6379)

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
        if r.exists(username):
            flash('שם המשתמש כבר תפוס')
            return redirect('/register')

        # בדיקה אם האימייל כבר קיים
        if r.exists(email):
            flash('כתובת האימייל כבר קיימת')
            return redirect('/register')

        # בדיקה אם האימייל חוקי
        if not is_valid_email(email):
            flash('כתובת האימייל אינה חוקית')
            return redirect('/register')

        # שמירת הנתונים של המשתמש ב־Redis
        hashed_password = generate_password_hash(password)
        r.hmset(username, {'password': hashed_password, 'email': email})
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
        user_data = r.hgetall(username)
        if user_data and check_password_hash(user_data[b'password'].decode('utf-8'), password):
            # התחברות מוצלחת - שמירת המשתמש ב-session
            session['username'] = username.decode('utf-8')
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
        user_data = r.hgetall(username)
        user_data = {key.decode('utf-8'): value.decode('utf-8') for key, value in user_data.items()}
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
    app.run(host='0.0.0.0', port=5000, debug=True)
