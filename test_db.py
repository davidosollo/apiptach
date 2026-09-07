from database.db import get_connection


try:
    conn = get_connection()

    with conn.cursor() as cursor:
        cursor.execute("SELECT DATABASE() AS database_name")
        result = cursor.fetchone()

    print("Conexión OK")
    print(result)

    conn.close()

except Exception as e:
    print("Error de conexión:")
    print(e)