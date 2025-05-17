import pandas as pd
from newspaper import Article
from concurrent.futures import ThreadPoolExecutor
import threading

# Shared counter and lock for atomic increment of fetch count
fetch_counter = 0
fetch_counter_lock = threading.Lock()

def fetch_article_content(url):
    global fetch_counter
    try:
        article = Article(url)
        article.download()
        article.parse()
        result = article.text
    except Exception:
        result = '[ERROR]'
    
    with fetch_counter_lock:
        fetch_counter += 1
        print(f"[{fetch_counter}] fetched: {url}")
        
    return result

def scrape(urls, max_workers=5):
    print(f"Starting scraping with {max_workers} workers...")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(fetch_article_content, urls))
    print('Scraping completed.')
    return results

# Only load the title and news_url column
partial_dataset = pd.read_csv('../data/FakeNewsNet.csv', usecols=['title', 'news_url'])
# Remove duplicated titles
partial_dataset.drop_duplicates(subset='title', inplace=True)
# Remove empty news_url rows
partial_dataset.dropna(subset='news_url', inplace=True)

# Process urls
urls = partial_dataset['news_url'].tolist()
article_contents = scrape(urls, max_workers=20)

# Add results to the full dataset
dataset_full = pd.read_csv('../data/FakeNewsNet.csv')
dataset_full.drop_duplicates(subset='title', inplace=True)
dataset_full.dropna(subset='news_url', inplace=True)

dataset_full['article_content'] = article_contents
dataset_full.to_csv('../data/FakeNewsNetWithArticleContent.csv', index=False)

print('Saved new dataset')

