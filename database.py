import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


def execute_query(query, params=None):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        return results

    finally:
        cursor.close()
        connection.close()