#Thaddeus Brown
#December 5, 2025
# A script that gathers the data of the top 10 words and their freqencies
import sqlite3

database_name = 'gutenberg_books.db'

def connect_db():
    return sqlite3.connect(database_name)

def create_table():
    """"Creates the table """
    conn = connect_db()
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title,
        word,
        freqency
    );
    """
    conn.commit()
    conn.close()

def insert_book_data(title, word_frequencies):
    """Inserts/updates book data into the database"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE title = ?", (title,))

    for word, freq in word_frequencies.items():
        cursor.execute("""
            INSERT INTO books (title, word, frequency) VALUES (?, ?, ?)
        """, (title, word, freq))
    conn.commit()
    conn.close()

def get_book_data(title):
    """Gets the top 10 word and frequencies for a title"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT word, frequency FROM books WHERE title LIKE ? ORDER BY frequency DESC LIMIT 10
    ''', ('%' + title + '%'))
    results = cursor.fetchall()
    conn.close()
    return dict(results)