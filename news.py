import feedparser
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

sources = []

with open("feeds.txt", "r") as f:
    for line in f:
        parts = line.strip().split("|")

        if len(parts) != 4:
            continue

        type_, name, source, keywords = parts
        sources.append((type_, name, source, keywords))

all_articles = []

def matches_keywords(text, keywords):
    text = text.lower()
    for kw in keywords:
        if kw.strip().lower() not in text:
            return False
    return True

for type_, name, source, keywords in sources:
    keyword_list = keywords.split(",")

    print(f"Processing {name} ({type_})")

    # -----------------------
    # RSS MODE
    # -----------------------
    if type_ == "RSS":
        feed = feedparser.parse(source)

        for entry in feed.entries:
            text = entry.title + " " + entry.get("summary", "")

            if matches_keywords(text, keyword_list):
                all_articles.append({
                    "source": name,
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "")
                })

    # -----------------------
    # SEARCH/SCRAPE MODE (simple version)
    # -----------------------
    if type_ == "SEARCH":
        try:
            r = requests.get(source, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            text = soup.get_text()

            if matches_keywords(text, keyword_list):
                all_articles.append({
                    "source": name,
                    "title": f"Match found for {name}",
                    "link": source,
                    "published": ""
                })

        except Exception as e:
            print(f"Error scraping {name}: {e}")

# SAVE
with open("news.json", "w") as f:
    json.dump({
        "updated": datetime.now().isoformat(),
        "articles": all_articles
    }, f, indent=2)
