import redis

# יצירת חיבור למסד הנתונים של Redis
r = redis.Redis(host='localhost', port=6379)

# פונקציה לקריאת נתונים ממפת גביעים ב-Redis
def get_data_from_redis(key):
    data = r.hgetall(key)
    return data

# פונקציה להוספת נתונים למפת גביעים ב-Redis
def add_data_to_redis(key, value):
    r.hmset(key, value)

# פונקציה לביצוע שאילתות פשוטות והחזרת התוצאות ממסד הנתונים ב-MySQL
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

# פונקציה להכנסת נתונים למסד הנתונים ב-MySQL
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
