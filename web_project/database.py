import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# יצירת חיבור למסד הנתונים של משתמשים
def create_users_db_connection():
    connection = mysql.connector.connect(
        host='db1',
        port='3306',
        user='root',
        password='yotam',
        database='web_users'
    )
    return connection

# יצירת חיבור למסד הנתונים של מספר הכניסות
def create_login_counts_db_connection():
    connection = mysql.connector.connect(
        host='db2',
        port='3307',
        user='root',
        password='yotam',
        database='site_entries'
    )
    return connection

# ביצוע שאילתות SELECT במסד הנתונים של משתמשים
def execute_query_users_db(query, params=None):
    connection = create_users_db_connection()
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

# ביצוע שאילתות SELECT במסד הנתונים של מספר הכניסות
def execute_query_login_counts_db(query, params=None):
    connection = create_login_counts_db_connection()
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

# בדיקה האם שם משתמש כבר קיים
def check_username_exists(username):
    query = "SELECT * FROM users WHERE username = %s"
    params = (username,)
    result = execute_query_users_db(query, params)
    return len(result) > 0

# בדיקה האם כתובת האימייל כבר קיימת
def check_email_exists(email):
    query = "SELECT * FROM users WHERE email = %s"
    params = (email,)
    result = execute_query_users_db(query, params)
    return len(result) > 0

# בדיקה האם שם המשתמש והסיסמה תואמים לנתונים במסד הנתונים
def check_credentials(username, password):
    query = "SELECT * FROM users WHERE username = %s"
    params = (username,)
    result = execute_query_users_db(query, params)
    if len(result) > 0:
        stored_password = result[0][2]
        return check_password_hash(stored_password, password)
    return False

# שמירת הנתונים של המשתמש במסד הנתונים
def insert_data_mysql(username, password, email):
    query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
    params = (username, password, email)
    execute_query_users_db(query, params)

# הבאת נתוני המשתמש ממסד הנתונים
def get_user_data(username):
    query = "SELECT * FROM users WHERE username = %s"
    params = (username,)
    result = execute_query_users_db(query, params)
    if len(result) > 0:
        user_data = {
            'id': result[0][0],
            'username': result[0][1],
            'email': result[0][3]
        }
        return user_data
    return None

# ספירת מספר הכניסות לאתר
def get_site_entries_count():
    query = "SELECT COUNT(*) FROM login_logs"
    result = execute_query_login_counts_db(query)
    return result[0][0]

# עדכון מספר הכניסות לאתר
def increment_site_entries():
    query = "INSERT INTO login_logs () VALUES ()"
    execute_query_login_counts_db(query)
