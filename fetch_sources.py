# fetch_sources.py
import feedparser
from datetime import datetime

RSS_FEEDS = [
    "https://www.investing.com/rss/news_301.rss",
    "https://www.investing.com/rss/news_25.rss",
    "https://feeds.reuters.com/reuters/businessNews",
    "https://www.fxstreet.com/rss/news",
]

def fetch_all_news():
    all_entries = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                all_entries.append({
                    "title": entry.title,
                    "published": entry.get("published", "")
                })
        except Exception as e:
            print(f"خطا در خواندن {url}: {e}")
    return all_entries

def is_today(published_str):
    try:
        pub_dt = datetime(*feedparser._parse_date(published_str)[:6])
        return pub_dt.date() == datetime.utcnow().date()
    except:
        return False
