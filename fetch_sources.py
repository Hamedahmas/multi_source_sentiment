import feedparser
import requests
from bs4 import BeautifulSoup

# تابع برای دریافت اخبار از فید RSS
def fetch_rss_entries(url):
    """
    این تابع اخبار را از یک URL فید RSS می‌گیرد
    """
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries:
        entries.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published
        })
    return entries

# تابع برای استخراج اخبار از سایت Investing.com (اسکرپینگ)
def fetch_investing_news():
    """
    این تابع اخبار را از سایت Investing.com می‌گیرد
    """
    url = "https://www.investing.com/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    headlines = soup.find_all('a', class_='title')  # جستجو برای عناوین اخبار
    news = []
    
    for headline in headlines:
        title = headline.text.strip()
        link = headline['href']
        news.append({
            'title': title,
            'link': f"https://www.investing.com{link}",
            'published': 'N/A'  # برای سایت‌هایی که تاریخ انتشار ندارند
        })
    
    return news

# تابع برای دریافت اخبار از چند منبع مختلف
def fetch_all_news():
    """
    این تابع تمام اخبار را از منابع مختلف جمع‌آوری می‌کند
    """
    rss_urls = [
        "https://rsshub.app/telegram/channel/fxfactoryfarsi",
        "https://rsshub.app/telegram/channel/UtoFx",
        "https://rsshub.app/telegram/channel/xnewsforex",
        "https://rsshub.app/telegram/channel/ForexCalendar",
        # اضافه کردن بقیه فیدها در اینجا
    ]
    
    all_entries = []
    
    # جمع‌آوری اخبار از فیدهای RSS
    for url in rss_urls:
        all_entries.extend(fetch_rss_entries(url))

    # جمع‌آوری اخبار از سایت investing.com
    investing_news = fetch_investing_news()
    all_entries.extend(investing_news)

    return all_entries

# تابع برای دریافت فقط اخبار امروز
def is_today(date_str):
    """
    این تابع بررسی می‌کند که آیا تاریخ وارد شده مربوط به امروز است یا نه
    """
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    date_obj = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    return date_obj.strftime('%Y-%m-%d') == today
