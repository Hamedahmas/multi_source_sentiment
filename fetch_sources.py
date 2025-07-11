# fetch_sources.py
import feedparser
from datetime import datetime
from dateutil import parser as date_parser

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
                published_raw = entry.get("published", "")
                all_entries.append({
                    "title": entry.title,
                    "published": published_raw
                })
        except Exception as e:
            print(f"❌ خطا در خواندن {url}: {e}")
    return all_entries

def is_today(published_str):
    try:
        pub_dt = date_parser.parse(published_str)
        return pub_dt.date() == datetime.utcnow().date()
    except Exception as e:
        print(f"[!] فرمت تاریخ نامشخص: {published_str} → {e}")
        return False
