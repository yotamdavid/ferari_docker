import mysql.connector

# יצירת חיבור למסד הנתונים
def create_db_connection():
    connection = mysql.connector.connect(
        host='db',
        user='root',
        password='yotam',
        database='web_users'
    )
    return connection

# ביצוע שאילתות SELECT
def execute_query_mysql(query, params=None):
    connection = create_db_connection()
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
    result = execute_query_mysql(query, params)
    return len(result) > 0

# בדיקה האם כתובת האימייל כבר קיימת
def check_email_exists(email):
    query = "SELECT * FROM users WHERE email = %s"
    params = (email,)
    result = execute_query_mysql(query, params)
    return len(result) > 0

# בדיקה האם שם המשתמש והסיסמה תואמים לנתונים במסד הנתונים
def check_credentials(username, password):
    query = "SELECT * FROM users WHERE username = %s"
    params = (username,)
    result = execute_query_mysql(query, params)
    if len(result) > 0:
        stored_password = result[0][2]
        return check_password_hash(stored_password, password)
    return False

# שמירת הנתונים של המשתמש במסד הנתונים
def insert_data_mysql(username, password, email):
    query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
    params = (username, password, email)
    execute_query_mysql(query, params)

# הבאת נתוני המשתמש ממסד הנתונים
def get_user_data(username):
    query = "SELECT * FROM users WHERE username = %s"
    params = (username,)
    result = execute_query_mysql(query, params)
    if len(result) > 0:
        user_data = {
            'id': result[0][0],
            'username': result[0][1],
            'email': result[0][3]
        }
        return user_data
    return None
