import feedparser
import requests
from bs4 import BeautifulSoup

def get_rss_titles(url):
    try:
        d = feedparser.parse(url)
        return [entry.title for entry in d.entries]
    except:
        return []

def get_reuters_titles():
    try:
        res = requests.get("https://www.reuters.com/markets/commodities/", timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        return [a.text.strip() for a in soup.select("a[data-testid='Heading']")][:10]
    except:
        return []

def get_fxstreet_titles():
    try:
        res = requests.get("https://www.fxstreet.com/news", timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        return [h.text.strip() for h in soup.select("h3 a")][:10]
    except:
        return []

def get_all_titles():
    titles = []
    titles += get_rss_titles("https://www.investing.com/rss/news_301.rss")
    titles += get_reuters_titles()
    titles += get_fxstreet_titles()
    return titles
