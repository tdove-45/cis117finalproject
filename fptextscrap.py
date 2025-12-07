#Thaddeus Brown
#December 5, 2025
#Text/URL scraping to get the content
import requests
import re
from collections import Counter
from bs4 import BeautifulSoup
import string

stop_words = set({
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself',
    'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll",
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
    'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
    'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
    's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're',
    've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',
    "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',
    "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren',
    "weren't", 'won', "won't", 'wouldn', "wouldn't"
    })

def get_text_from_url(url):
    """Gets the text content from the Project Gutenberg URL"""
    try:
        repsonse = requests.get(url)
        repsonse.raise_for_status()
        return repsonse.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def clean_and_count_words(text):
    """Filters stop words and counts the top 10 words and thier frequneces"""
    if not text:
        return {}

    text = text.lower()
    words = re.findall(r'\b[a-z]+\b', text)

    filtered_words = [word for word in words if word not in stop_words and len(word) > 1]

    word_count = Counter(filtered_words)

    return dict(word_count.most_common(10))

def extract_title_from_text(text):
    """Extracts the book title from the Gutenberg text"""
    match = re.search(r'Title: (.*?)\n', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "Unknown Title"