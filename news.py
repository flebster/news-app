import feedparser
import json
from datetime import datetime

feeds = []

with open("feeds.txt", "r") as f:
    for line in f:
        name, url = line.strip().split("|")
        feeds.append((name, url))

all_articles = []

for name, url in feeds:
    feed = feedparser.parse(url)

    for entry in feed.entries[:5]:
        all_articles.append({
            "source": name,
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", "")
        })

# sort newest first (best effort)
all_articles = all_articles[:50]

with open("news.json", "w") as f:
    json.dump({
        "updated": datetime.now().isoformat(),
        "articles": all_articles
    }, f, indent=2)
