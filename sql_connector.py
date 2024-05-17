from decouple import config
from utility import send_email_notification
import mysql.connector
from mysql.connector import Error

def create_connection():
    host_name=config('HOST_NAME')
    user_name=config('USER_NAME')
    user_password=config('USER_PASSWORD')
    db_name=config('DB_NAME')

    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        send_email_notification(f"Unable to connect DB --> {e}")
        print(f"The error '{e}' occurred")
    return connection

def execute_query(query):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()

