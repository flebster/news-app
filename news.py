import feedparser
import json
import os
from datetime import datetime, timedelta

FEED_FILE = "feeds.txt"
OUTPUT_FILE = "news.json"
MAX_DAYS = 3   # keep articles for 3 days

# -------------------------
# LOAD EXISTING ARTICLES
# -------------------------
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r") as f:
        existing_data = json.load(f)
        existing_articles = existing_data.get("articles", [])
else:
    existing_articles = []

# Create a lookup (avoid duplicates)
existing_links = {a["link"]: a for a in existing_articles}

# -------------------------
# LOAD FEEDS
# -------------------------
feeds = []

with open(FEED_FILE, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        parts = line.split("|")

        if len(parts) < 2:
            continue

        name, url = parts[0], parts[1]
        feeds.append((name, url))

# -------------------------
# FETCH NEW ARTICLES
# -------------------------
for name, url in feeds:
    print(f"Processing: {name}")

    try:
        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:
            link = entry.link

            # Skip if already exists
            if link in existing_links:
                continue

            article = {
                "source": name,
                "title": entry.title,
                "link": link,
                "published": entry.get("published", ""),
                "saved": False,
                "added": datetime.now().isoformat()
            }

            existing_links[link] = article

    except Exception as e:
        print(f"Error with {name}: {e}")

# -------------------------
# CLEAN OLD ARTICLES
# -------------------------
now = datetime.now()
cleaned_articles = []

for article in existing_links.values():
   if "added" in article:
    added_time = datetime.fromisoformat(article["added"])
else:
    # If old article, treat as new so it doesn't get deleted
    added_time = now

    age = now - added_time

    # Keep if:
    # - less than MAX_DAYS old
    # - OR saved
    if age < timedelta(days=MAX_DAYS) or article.get("saved"):
        cleaned_articles.append(article)

# -------------------------
# SAVE FILE
# -------------------------
with open(OUTPUT_FILE, "w") as f:
    json.dump({
        "updated": datetime.now().isoformat(),
        "articles": cleaned_articles
    }, f, indent=2)

print("DONE: retention applied")
