import sqlite3
from utils import load_sql_statement


class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file

    def __enter__(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            return self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


def check_translation_exists(cursor, text, translations):
    try:
        query = load_sql_statement("sql/check_translation.sql")
        parameters = [text] + list(translations.values())
        cursor.execute(query, parameters)
        result = cursor.fetchone()
        return result is not None
    except sqlite3.Error as e:
        print(f"Database query error: {e}")


def add_translation_to_db(cursor, text, translations):
    try:
        query = load_sql_statement("sql/add_translation.sql")
        parameters = [text] + list(translations.values())
        cursor.execute(query, parameters)
    except sqlite3.Error as e:
        print(f"Database query error: {e}")
