import mysql.connector

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='db',
            port="3306",
            user='root',
            password='yotam',
            database='web_users'
        )
        return connection
    except mysql.connector.Error as error:
        print(f"Failed to connect to the database: {error}")
        return None


def fetch_data(query, params=None):
    try:
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
    except mysql.connector.Error as error:
        print(f"Failed to fetch data from the database: {error}")
        return None


def insert_data(query, params=None):
    try:
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
    except mysql.connector.Error as error:
        print(f"Failed to insert data into the database: {error}")
        return False
