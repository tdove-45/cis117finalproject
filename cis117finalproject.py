#CIS 117 Final Project
#Thaddeus Brown
#12/10/25

import tkinter as tk
from tkinter import messagebox
import sqlite3
import requests
import re
from collections import Counter


STOPWORDS = {
    "the","a","an","and","or","at","in","on","of","to","i","you","he","she",
    "it","they","them","is","was","were","am","are","be","this","that"
}

#----------------------------
# Database for top 10 words

def init_database():
    """Creates the SQLite database tables if they don't exist."""
    conn = sqlite3.connect("books.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            url TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS wordfreq (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            word TEXT,
            frequency INTEGER,
            FOREIGN KEY(book_id) REFERENCES books(id)
        )
    """)

    conn.commit()
    conn.close()


#--------------------------------
# Functions that gather the url from the Gutenberg site

def fetch_book_text(url):
    """
    Fetch raw text from a Gutenberg plain-text URL.
    Raises an exception if request fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise RuntimeError(f"Could not fetch book: {e}")


def clean_and_tokenize(text):
    """
    Remove punctuation, lowercase text, remove stopwords,
    and return a token list.
    """
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    words = text.lower().split()
    return [w for w in words if w not in STOPWORDS]


def compute_frequencies(words):
    """
    Returns the top 10 most common words as (word, frequency) list.
    """
    count = Counter(words)
    return count.most_common(10)


# ------------------------------------------
# Database Functions

def search_local_book(title):
    """
    Searches the local database for a given title.
    Returns:
        (True, [(word, freq)...]) if found
        (False, None) if not found
    """
    conn = sqlite3.connect("books.db")
    c = conn.cursor()

    c.execute("SELECT id FROM books WHERE title = ?", (title,))
    row = c.fetchone()

    if row is None:
        conn.close()
        return False, None

    book_id = row[0]
    c.execute("""
        SELECT word, frequency
        FROM wordfreq
        WHERE book_id = ?
        ORDER BY frequency DESC
        LIMIT 10
    """, (book_id,))

    results = c.fetchall()
    conn.close()
    return True, results


def save_book_to_db(title, url, wordfreq_data):
    """
    Saves a new book and its word frequency data to the database.
    wordfreq_data must be a list of (word, frequency).
    """
    conn = sqlite3.connect("books.db")
    c = conn.cursor()

    c.execute("INSERT OR IGNORE INTO books (title, url) VALUES (?, ?)",
              (title, url))

    c.execute("SELECT id FROM books WHERE title = ?", (title,))
    book_id = c.fetchone()[0]

    c.execute("DELETE FROM wordfreq WHERE book_id = ?", (book_id,))

    for word, freq in wordfreq_data:
        c.execute("""
            INSERT INTO wordfreq (book_id, word, frequency)
            VALUES (?, ?, ?)
        """, (book_id, word, freq))

    conn.commit()
    conn.close()


# ------------------------------------------
# Functions for GUI calls


def on_search_title():
    """Called when user clicks 'Search Title'."""
    title = title_entry.get().strip()
    if not title:
        messagebox.showerror("Error", "Please enter a book title.")
        return

    found, data = search_local_book(title)

    result_box.delete(0, tk.END)

    if not found:
        result_box.insert(tk.END, "Book was not found in local database.")
    else:
        for word, freq in data:
            result_box.insert(tk.END, f"{word}: {freq}")


def on_fetch_url():
    """Called when user clicks 'Fetch & Save'."""
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a Gutenberg TXT URL.")
        return

    result_box.delete(0, tk.END)

    try:
        raw_text = fetch_book_text(url)
        words = clean_and_tokenize(raw_text)
        top10 = compute_frequencies(words)

        # Extract a simple title from URL (you can improve this)
        title = url.split("/")[-1].replace(".txt", "")

        save_book_to_db(title, url, top10)

        # Display results
        for word, freq in top10:
            result_box.insert(tk.END, f"{word}: {freq}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ------------------------------
# Tkinter Application 

def create_gui():
    """Creates and runs the Tkinter GUI."""
    global title_entry, url_entry, result_box

    root = tk.Tk()
    root.title("Project Gutenberg Word Frequency Tool")

    # --- Title Search Frame ---
    tk.Label(root, text="Search by Book Title:").grid(row=0, column=0, sticky="w")
    title_entry = tk.Entry(root, width=50)
    title_entry.grid(row=1, column=0, padx=5)
    tk.Button(root, text="Search Title", command=on_search_title).grid(row=1, column=1, padx=5)

    # --- URL Fetch Frame ---
    tk.Label(root, text="Fetch From Gutenberg TXT URL:").grid(row=2, column=0, sticky="w", pady=(15,0))
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=3, column=0, padx=5)
    tk.Button(root, text="Fetch & Save", command=on_fetch_url).grid(row=3, column=1, padx=5)

    # --- Results Display ---
    tk.Label(root, text="Top 10 Words:").grid(row=4, column=0, sticky="w", pady=(15,0))
    result_box = tk.Listbox(root, width=50, height=12)
    result_box.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()


#--------------------------
# Main

if __name__ == "__main__":
    init_database()
    create_gui()