# phonebook.py
import csv
from database import *  # Импортируем все функции из database.py

# Вставка данных с консоли
def insert_from_console():
    name = input("Enter name: ")
    last_name = input("Enter last name: ")
    phone = input("Enter phone: ")
    insert_or_update_user(name, last_name, phone)

# Вставка данных из CSV
def insert_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 3:  # Проверка, что в строке 3 столбца
                insert_or_update_user(row[0], row[1], row[2])  # Вставка данных
            else:
                print(f"Skipping row (incorrect number of columns): {row}")

# Обновление данных
def update_data(identifier, new_value, field):
    conn = get_connection()
    cur = conn.cursor()
    if field == "first_name":
        cur.execute("UPDATE PhoneBook SET first_name = %s WHERE phone = %s", (new_value, identifier))
    elif field == "phone":
        cur.execute("UPDATE PhoneBook SET phone = %s WHERE first_name = %s", (new_value, identifier))
    conn.commit()
    print("Updated.")
    cur.close()
    conn.close()

# Удаление данных
def delete_data(identifier, by_field="first_name"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM PhoneBook WHERE {by_field} = %s", (identifier,))
    conn.commit()
    print("Deleted.")
    cur.close()
    conn.close()

# Поиск данных
def query_data(filter_by=None, value=None):
    conn = get_connection()
    cur = conn.cursor()
    if filter_by and value:
        cur.execute(f"SELECT * FROM PhoneBook WHERE {filter_by} = %s", (value,))
    else:
        cur.execute("SELECT * FROM PhoneBook")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

if __name__ == '__main__':
    init_db()  # Инициализация базы данных (создание таблиц)
    insert_from_csv('a.csv')  # Вставка данных из файла CSV
