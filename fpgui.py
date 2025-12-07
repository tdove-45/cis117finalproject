#Thaddeus Brown
#December 5, 2025
# A Tkinter appilcation that manages and diplays the top 10 frequences from the Project Gutenberg books
import tkinter as tk
from tkinter import messagebox, scrolledtext
import main as core # pyright: ignore[reportMissingImports]

class GutenbergApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gutenberg Book Analyzer")
        self.root.geometry("600x500")
        
        core.db.create_table() # Ensure the DB table exists when the app starts

        self.create_widgets()

    def create_widgets(self):
        # --- Section 1: Search Local Database ---
        frame_search_db = tk.Frame(self.root, padx=10, pady=10)
        frame_search_db.pack(fill='x')
        tk.Label(frame_search_db, text="Search Local DB by Title:").pack(side=tk.LEFT)
        
        self.entry_title_query = tk.Entry(frame_search_db, width=40)
        self.entry_title_query.pack(side=tk.LEFT, expand=True, fill='x', padx=10)
        
        self.btn_search_db = tk.Button(frame_search_db, text="Search DB", command=self.on_search_db)
        self.btn_search_db.pack(side=tk.RIGHT)

        # --- Section 2: Scrape URL and Update DB ---
        frame_scrape_url = tk.Frame(self.root, padx=10, pady=10)
        frame_scrape_url.pack(fill='x')
        tk.Label(frame_scrape_url, text="Scrape URL & Update DB:").pack(side=tk.LEFT)
        
        self.entry_book_url = tk.Entry(frame_scrape_url, width=40)
        self.entry_book_url.insert(0, "www.gutenberg.org")
        self.entry_book_url.pack(side=tk.LEFT, expand=True, fill='x', padx=10)
        
        self.btn_scrape_url = tk.Button(frame_scrape_url, text="Scrape URL", command=self.on_scrape_url)
        self.btn_scrape_url.pack(side=tk.RIGHT)

        # --- Section 3: Results Display ---
        frame_results = tk.Frame(self.root, padx=10, pady=10)
        frame_results.pack(fill='both', expand=True)

        tk.Label(frame_results, text="Results (Top 10 Freq Words):", font=("Helvetica", 12, "bold")).pack(anchor='w')

        self.results_display = scrolledtext.ScrolledText(frame_results, wrap=tk.WORD, padx=5, pady=5, state=tk.DISABLED)
        self.results_display.pack(fill='both', expand=True, pady=10)

    def display_results(self, title, frequencies):
        self.results_display.config(state=tk.NORMAL)
        self.results_display.delete('1.0', tk.END)
        if frequencies:
            display_text = f"--- Book Title: {title} ---\n\n"
            display_text += "{:<20} {:<10}\n".format("Word", "Frequency")
            display_text += "-"*30 + "\n"
            for word, freq in frequencies.items():
                display_text += "{:<20} {:<10}\n".format(word, freq)
            self.results_display.insert(tk.END, display_text)
        else:
            self.results_display.insert(tk.END, "Book was not found or no significant words found.")
        self.results_display.config(state=tk.DISABLED)

    def on_search_db(self):
        title_query = self.entry_title_query.get().strip()
        if not title_query:
            messagebox.showwarning("Input Error", "Please enter a book title to search.")
            return

        results_dict = core.search_and_display_book(title_query)
        
        if results_dict:
            # When retrieved from DB, we don't know the exact title used for storage without extra logic, 
            # so we use the query as a placeholder for display
            self.display_results(f"'{title_query}' (from DB)", results_dict)
        else:
            self.display_results(title_query, None)
            messagebox.showinfo("Search Results", "Book not found in local database.")

    def on_scrape_url(self):
        url = self.entry_book_url.get().strip()
        if not url:
            messagebox.showwarning("Input Error", "Please enter a Project Gutenberg URL.")
            return

        title, frequencies = core.process_url_and_store(url)
        
        if title and frequencies:
            self.display_results(title, frequencies)
            messagebox.showinfo("Scrape Success", f"Successfully scraped and stored '{title}'.")
        else:
            self.display_results("URL Processing Failed", None)
            messagebox.showerror("Scrape Error", "Failed to retrieve or process data from the provided URL. Check the URL format (must be .txt link).")

# Main execution block
if __name__ == "__main__":
    root = tk.Tk()
    app = GutenbergApp(root)
    root.mainloop()