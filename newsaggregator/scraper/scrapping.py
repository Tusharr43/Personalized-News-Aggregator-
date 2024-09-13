import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Function to scrape articles from CNN
def scrape_cnn():
    my_url = 'https://www.cnn.com/'
    response = requests.get(my_url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code != 200:
        print(f"Failed to retrieve the page from CNN. Status code: {response.status_code}")
        return []

    page_soup = BeautifulSoup(response.text, "html.parser")
    containers = page_soup.find_all("span", {"class": "container__headline-text"})
    
    articles = []
    for container in containers:
        try:
            title = container.get_text(strip=True)
            summary = "No summary available"  # CNN headlines don't have summaries in this container
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current date and time
            source = "CNN"
            url = my_url  # URL is the base URL

            articles.append([title, summary, date, source, url])
        except Exception as e:
            print(f"Error (CNN): {e}")
    
    print(f"CNN Articles: {len(articles)}")
    return articles

# Function to scrape articles from BBC
def scrape_bbc_category(category_url):
    url = f"https://www.bbc.com{category_url}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for article in soup.find_all("article"):
        try:
            title_tag = article.find("h3")
            title = title_tag.get_text() if title_tag else "No title"

            summary_tag = article.find("p")
            summary = summary_tag.get_text() if summary_tag else "No summary"

            url_tag = article.find("a")
            article_url = "https://www.bbc.com" + url_tag["href"] if url_tag else "No URL"

            publication_date_tag = article.find("time")
            publication_date = publication_date_tag["datetime"] if publication_date_tag else "No date"

            source = "BBC"
            articles.append([title, summary, publication_date, source, article_url])
        except Exception as e:
            print(f"Error (BBC): {e}")
    
    print(f"BBC Articles: {len(articles)}")
    return articles

def scrape_bbc():
    categories = [
        "/news/world",
        "/news/technology",
        "/news/business",
        "/news/science",
        "/news/politics",
        "/news/sports",
        "/news/entertainment"
    ]

    all_articles = []
    for category in categories:
        print(f"Scraping BBC category: {category}")
        articles = scrape_bbc_category(category)
        all_articles.extend(articles)

    return all_articles

# Function to scrape articles from The Onion
def scrape_the_onion_category(category_url):
    url = f"https://www.theonion.com{category_url}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for article in soup.find_all("article"):
        try:
            title_tag = article.find("h1") or article.find("h2") or article.find("h3")
            title = title_tag.get_text(strip=True) if title_tag else "No title"

            summary_tag = article.find("div", class_="excerpt") or article.find("p") or article.find("div", class_="content") or article.find("div", class_="entry-content")
            summary = summary_tag.get_text(strip=True) if summary_tag else "No summary"

            url_tag = article.find("a", href=True)
            article_url = "https://www.theonion.com" + url_tag["href"] if url_tag else "No URL"

            publication_date = "No date"  # The Onion doesn't have a specific publication date

            source = "The Onion"
            articles.append([title, summary, publication_date, source, article_url])
        except Exception as e:
            print(f"Error (The Onion): {e}")
    
    print(f"The Onion Articles: {len(articles)}")
    return articles

def scrape_the_onion():
    categories = [
        "",
        "/news",
        "/satire",
        "/video",
        "/sports",
        "/entertainment"
    ]

    all_articles = []
    for category in categories:
        print(f"Scraping The Onion category: {category}")
        articles = scrape_the_onion_category(category)
        all_articles.extend(articles)

    return all_articles

# Saving to CSV
def save_to_csv(articles, filename='news_articles.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Summary", "Publication Date", "Source", "URL"])
        writer.writerows(articles)

# Main function to scrape from multiple sources
def scrape_all_sources():
    cnn_articles = scrape_cnn()
    bbc_articles = scrape_bbc()
    the_onion_articles = scrape_the_onion()

    # Combine articles from all sources
    all_articles = cnn_articles + bbc_articles + the_onion_articles

    # Print the total number of articles scraped
    print(f"Total Articles: {len(all_articles)}")

    # Save to CSV
    save_to_csv(all_articles)

# Run the scraper
scrape_all_sources()
