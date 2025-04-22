import psycopg2

try:
    conn = psycopg2.connect(
        database="postgres", 
        user="postgres", 
        host="localhost", 
        password="mar.hanym2007!", 
        port=5432
    )


    # Открываем курсор для выполнения операций
    cur = conn.cursor()

    # Выполняем команду для создания таблицы
    cur.execute("""
    CREATE TABLE datacamp_courses(
        course_id SERIAL PRIMARY KEY,
        course_name VARCHAR (50) UNIQUE NOT NULL,
        course_instructor VARCHAR (100) NOT NULL,
        topic VARCHAR (20) NOT NULL
    );
    """)

    # Сохраняем изменения в базе данных
    conn.commit()

    print("Table 'datacamp_courses' created successfully!")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Закрываем курсор и соединение с базой данных
    if cur:
        cur.close()
    if conn:
        conn.close()