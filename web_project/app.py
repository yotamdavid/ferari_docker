from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # מפתח סודי לשימור הסשן

# רשימת משתמשים רשומים
users = []


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

        # בדיקה אם שם המשתמש כבר קיים
        if any(user['username'] == username for user in users):
            flash('שם המשתמש כבר תפוס')
            return redirect('/register')

        # שמירת הנתונים של המשתמש
        hashed_password = generate_password_hash(password)
        users.append({'username': username, 'password': hashed_password})

        flash('נרשמת בהצלחה!')
        return redirect('/login')

    return render_template('register.html')


# התחברות למערכת
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # בדיקה אם שם המשתמש והסיסמה תואמים לנתונים במערכת
        user = next((user for user in users if user['username'] == username), None)
        if user and check_password_hash(user['password'], password):
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
        user = next((user for user in users if user['username'] == username), None)
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
