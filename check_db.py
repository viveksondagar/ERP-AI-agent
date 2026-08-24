from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("SHOW TABLES")

tables = cursor.fetchall()

print("\nERP DATABASE TABLES:")
print("-" * 40)

for table in tables:
    print(table[0])

cursor.close()
connection.close()