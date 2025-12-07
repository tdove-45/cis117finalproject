#Thaddeus Brown
#December 5, 2025
# Main script 
import fpdatabase as db # type: ignore
import fptextscrap as ta # type: ignore

def search_and_display_book(title_query):
    print(f"Searching for '{title_query}' in local database...")
    results = db.get_book_data(title_query)

    if results:
        print(f"Found '{title_query}' in local DB:")
        return results
    else:
        print(f"Book '{title_query}' not found in local DB.")
        return None

def process_url_and_store(url):
    """Fetches book from URL to analyze, store it, and return results"""
    print(f"Processing URL: {url}")
    raw_text = ta.get_text_from_url(url)
    if raw_text:
        title = ta.extract_title_from_text(raw_text)
        frequencies = ta.clean_and_count_words(raw_text)

        if title and frequencies:
            db.insert_book_data(title, frequencies)
            print(f"Successfully scraped, analyzed, and stored '{title}'.")
            return title, frequencies
        else:
            print("Could not analyze text or extract title.")
            return None, None

    else:
        return None, None