import psycopg2
import csv

# Function to connect to the database
def connect():
    return psycopg2.connect(
        host="localhost",
        database="postgres",  # Change to your database name
        user="postgres",      # Change to your database username
        password="2007"       # Change to your database password
    )

# Function to search by a pattern (e.g., part of the name, surname, or phone number)
def search_by_pattern(pattern):
    conn = connect()
    cur = conn.cursor()
    query = f"SELECT * FROM PhoneBook WHERE first_name ILIKE %s OR last_name ILIKE %s OR phone ILIKE %s"
    cur.execute(query, (f"%{pattern}%", f"%{pattern}%", f"%{pattern}%"))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

# Function to insert or update a user based on the phone number
def insert_or_update_user(first_name, last_name, phone):
    conn = connect()
    cur = conn.cursor()
    query = """
    INSERT INTO PhoneBook (first_name, last_name, phone)
    VALUES (%s, %s, %s)
    ON CONFLICT (phone) 
    DO UPDATE SET first_name = EXCLUDED.first_name, last_name = EXCLUDED.last_name;
    """
    cur.execute(query, (first_name, last_name, phone))
    conn.commit()
    print(f"Inserted or updated user: {first_name} {last_name}")
    cur.close()
    conn.close()

# Function to insert multiple users (with phone validation)
def insert_multiple_users(users_data):
    conn = connect()
    cur = conn.cursor()
    for user_record in users_data:
        user_name, user_phone = user_record
        if len(user_phone) == 10 and user_phone.isdigit():  # Validating phone number
            query = "INSERT INTO PhoneBook (first_name, phone) VALUES (%s, %s)"
            cur.execute(query, (user_name, user_phone))
        else:
            print(f"Invalid phone number {user_phone}, skipping.")
    conn.commit()
    print("Users inserted.")
    cur.close()
    conn.close()

# Function to query data with pagination (limit and offset)
def query_with_pagination(limit, offset):
    conn = connect()
    cur = conn.cursor()
    query = f"SELECT * FROM PhoneBook LIMIT {limit} OFFSET {offset}"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

# Function to delete a user by username or phone
def delete_user_by_identifier(identifier, by_field="first_name"):
    conn = connect()
    cur = conn.cursor()
    if by_field == "first_name":
        cur.execute("DELETE FROM PhoneBook WHERE first_name = %s", (identifier,))
    elif by_field == "phone":
        cur.execute("DELETE FROM PhoneBook WHERE phone = %s", (identifier,))
    conn.commit()
    print(f"Deleted user with {by_field}: {identifier}")
    cur.close()
    conn.close()

# Function to query data based on a filter (e.g., by first_name, last_name, or phone)
def query_data(filter_by=None, value=None):
    conn = connect()
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

# Main function to interact with user input and run actions
def main():
    # 1. Inserting or updating a user
    insert_or_update_user('John', 'Doe', '+1234567890')

    # 2. Inserting multiple users from a list
    users = [
        ('Alice', '+9876543210'),
        ('Bob', '+1234432111'),
        ('Charlie', '+5647382910')
    ]
    insert_multiple_users(users)

    # 3. Searching users by pattern
    search_by_pattern('John')

    # 4. Querying data with pagination
    query_with_pagination(2, 0)  # Display first 2 records

    # 5. Deleting a user by first name
    delete_user_by_identifier('Alice', 'first_name')

    # 6. Deleting a user by phone
    delete_user_by_identifier('+1234432111', 'phone')

    # 7. Query data with a specific filter
    query_data(filter_by="phone", value="+1234432111")

if __name__ == "__main__":
    main()
