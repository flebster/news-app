import feedparser
import json
from datetime import datetime

feeds = []

# --- LOAD FEEDS SAFELY ---
with open("feeds.txt", "r") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue  # skip empty lines

        parts = line.split("|")

        if len(parts) != 3:
            print(f"Skipping bad line: {line}")
            continue

        name, category, url = parts
        feeds.append((name, category, url))

# --- DEBUG: SHOW LOADED FEEDS ---
print("\nLOADING FEEDS:")
for f in feeds:
    print(f)

print(f"\nTOTAL FEEDS: {len(feeds)}\n")

# --- COLLECT ARTICLES ---
all_articles = []

for name, category, url in feeds:
    print(f"\nProcessing: {name}")
    print(f"URL: {url}")

    try:
        feed = feedparser.parse(url)

        print(f"Entries found: {len(feed.entries)}")

        for entry in feed.entries[:5]:
            all_articles.append({
                "source": name,
                "category": category,
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", "")
            })

    except Exception as e:
        print(f"FAILED FEED: {name} ERROR: {e}")

# --- LIMIT TOTAL ARTICLES ---
all_articles = all_articles[:100]

# --- SAVE OUTPUT ---
with open("news.json", "w") as f:
    json.dump({
        "updated": datetime.now().isoformat(),
        "articles": all_articles
    }, f, indent=2)

print("\nDONE: news.json updated\n")
