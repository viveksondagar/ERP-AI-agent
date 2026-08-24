from database import get_connection

try:
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT DATABASE()")
    result = cursor.fetchone()

    print("Connected successfully!")
    print("Database:", result[0])

    cursor.close()
    connection.close()

except Exception as e:
    print("Connection failed:")
    print(e)