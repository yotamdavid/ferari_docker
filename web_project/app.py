from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

# דף הראשי
@app.route('/')
def index():
 

    return render_template('index.html')


# בדיקה האם האימייל חוקי
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# דף הרשמה
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


# דף התחברות
@app.route('/login', methods=['GET', 'POST'])
def login():

    return render_template('login.html')


# דף התנתקות
@app.route('/logout')
def logout():

    return redirect('/')


# דף הלוח (רק למשתמשים מחוברים)
@app.route('/dashboard')
def dashboard():

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
