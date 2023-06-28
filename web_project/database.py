from mysql.connector import MySQLConnection, Error

# פונקציה ליצירת חיבור לבסיס הנתונים
def create_db_connection(host, port, user, password, database):
    try:
        connection = MySQLConnection(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# פונקציה לשליפת נתונים מבסיס הנתונים
def fetch_data(query, params=None):
    connection = create_db_connection('db', 3306, 'root', 'yotam', 'web_users')
    if connection:
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return result
        except Error as e:
            print(f"Error while fetching data from database: {e}")
    return None

# פונקציה להכנסת נתונים לבסיס הנתונים
def insert_data(query, params=None):
    connection = create_db_connection('db', 3306, 'root', 'yotam', 'web_users')
    if connection:
        try:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error while inserting data into database: {e}")
    return False
