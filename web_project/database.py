import mysql.connector

# פונקציה ליצירת חיבור למסד הנתונים של MySQL
def create_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        port='3306',
        password='yotam',
        database='db'
    )
    return connection

# פונקציה לביצוע שאילתות פשוטות והחזרת התוצאות ממסד הנתונים של MySQL
def execute_query_mysql(query, params=None):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    else:
        return None

# פונקציה להכנסת נתונים למסד הנתונים של MySQL
def insert_data_mysql(query, params=None):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    else:
        return False
