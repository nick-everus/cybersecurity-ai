import psycopg2
import re

# Database connection information
db_config = {
    'dbname': 'your_database',
    'user': 'your_user',
    'password': 'your_password',
    'host': 'localhost',
    'port': 5432
}


# Connect to the PostgreSQL database
def connect_to_db():
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        print("Database connection successful!")
        return connection, cursor
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None, None


# Check for weak passwords (basic length and complexity check)
def check_weak_passwords():
    password = db_config['password']
    if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[0-9]", password):
        print("Warning: Weak password detected.")
    else:
        print("Password complexity check passed.")


# SQL Injection vulnerability test
def test_sql_injection(cursor):
    test_queries = ["' OR '1'='1", "'; DROP TABLE users; --", "' OR 1=1; --"]
    for query in test_queries:
        try:
            cursor.execute(f"SELECT * FROM users WHERE username = '{query}'")
            results = cursor.fetchall()
            if results:
                print(f"Potential SQL Injection vulnerability with query: {query}")
            else:
                print(f"Query: {query} seems safe.")
        except Exception as e:
            print(f"Query execution failed for {query}, which is good: {e}")


# Check for outdated database version
def check_db_version(cursor):
    try:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Database version: {version[0]}")
        # Check for known vulnerable versions (example for PostgreSQL)
        vulnerable_versions = ['9.5', '9.6']  # Add versions as needed
        for v in vulnerable_versions:
            if v in version[0]:
                print(f"Warning: Vulnerable database version detected: {v}")
    except Exception as e:
        print(f"Failed to retrieve database version: {e}")


# Check for misconfigured permissions (example for PostgreSQL)
def check_permissions(cursor):
    try:
        cursor.execute("SELECT usename, usecreatedb, usesuper FROM pg_user;")
        users = cursor.fetchall()
        for user in users:
            username, can_create_db, is_superuser = user
            if can_create_db or is_superuser:
                print(
                    f"Warning: User {username} has high privileges (createdb: {can_create_db}, superuser: {is_superuser}).")
            else:
                print(f"User {username} has safe permissions.")
    except Exception as e:
        print(f"Failed to check user permissions: {e}")


# Main function
def main():
    connection, cursor = connect_to_db()
    if connection and cursor:
        check_weak_passwords()
        test_sql_injection(cursor)
        check_db_version(cursor)
        check_permissions(cursor)

        # Close the connection
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()