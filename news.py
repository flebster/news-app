import feedparser
import json
from datetime import datetime

feeds = []

with open("feeds.txt", "r") as f:
    for line in f:
        name, url = line.strip().split("|")
        feeds.append((name, url))
print("LOADING FEEDS:")
for  f in feeds:
    print(f)
    print("TOTAL FEEDS:", len(feeds))
all_articles = []

for name, url in feeds:
    print(f"\nProcessing:{name}")
    print(f"URL:{url}")

    try:
        feed=feedparser.parse(url)
        
        print(f"Entries found:{len(feed.entries)}")
                                  for entry in feed.entries[:5]:
                              all_articles.append({
                                  "source":name,
                                  "title":entry.title,
                                  "link":entry.link,
                                  "published": entry.get("published", "")
                              })
                               except Exception as e:
                               print(f"FAILED FEED: {name} ERROR:{e}")
                               feed = feedparser.parse(url)

    
# sort newest first (best effort)
all_articles = all_articles[:50]

with open("news.json", "w") as f:
    json.dump({
        "updated": datetime.now().isoformat(),
        "articles": all_articles
    }, f, indent=2)
