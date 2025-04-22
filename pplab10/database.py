import psycopg2

# Функция для подключения к базе данных PostgreSQL
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="postgres",  # Имя базы данных
        user="postgres",      # Имя пользователя
        password="2007"       # Пароль
    )

# Функция для инициализации базы данных (создание таблиц)
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Создание таблицы пользователей
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE
        );
        ''')

        # Создание таблицы для хранения очков пользователей
        cur.execute('''
        CREATE TABLE IF NOT EXISTS user_score (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            score INTEGER,
            level INTEGER
        );
        ''')

        conn.commit()  # Сохраняем изменения
        print("Tables 'users' and 'user_score' created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        cur.close()
        conn.close()

# Функция для вставки или обновления данных пользователя
def insert_or_update_user(first_name, last_name, phone):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO PhoneBook (first_name, last_name, phone)
            VALUES (%s, %s, %s)
            ON CONFLICT (phone)
            DO UPDATE SET first_name = EXCLUDED.first_name, last_name = EXCLUDED.last_name;
        """, (first_name, last_name, phone))

        conn.commit()
        print(f"Inserted or updated user: {first_name} {last_name}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

# Функция для получения пользователя по имени
def get_user(username):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()  # Получаем одного пользователя
        return user
    except Exception as e:
        print(f"Error retrieving user: {e}")
    finally:
        cur.close()
        conn.close()

# Функция для создания нового пользователя
def create_user(username):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Вставка нового пользователя в таблицу
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]  # Получаем ID нового пользователя
        conn.commit()
        return user_id  # Возвращаем ID нового пользователя
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        cur.close()
        conn.close()

# Функция для получения прогресса пользователя (счёт и уровень)
def get_user_progress(user_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT score, level FROM user_score WHERE user_id = %s", (user_id,))
        progress = cur.fetchone()  # Получаем прогресс пользователя
        return progress  # Возвращаем кортеж (score, level) или None, если прогресс не найден
    except Exception as e:
        print(f"Error retrieving user progress: {e}")
    finally:
        cur.close()
        conn.close()

# Функция для сохранения прогресса пользователя (счёт и уровень)
def save_progress(user_id, score, level):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Проверка, есть ли уже запись о пользователе
        cur.execute("SELECT * FROM user_score WHERE user_id = %s", (user_id,))
        existing_progress = cur.fetchone()

        if existing_progress:
            # Если запись существует, обновляем
            cur.execute("""
                UPDATE user_score SET score = %s, level = %s WHERE user_id = %s
            """, (score, level, user_id))
        else:
            # Если записи нет, вставляем новую
            cur.execute("""
                INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)
            """, (user_id, score, level))

        conn.commit()
        print(f"Progress saved for user {user_id}: Score = {score}, Level = {level}")
    except Exception as e:
        print(f"Error saving progress: {e}")
    finally:
        cur.close()
        conn.close()
