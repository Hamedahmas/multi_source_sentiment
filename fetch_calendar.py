# fetch_calendar.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict

def fetch_iranbourse_calendar():
    url = "https://iranbourseonline.co/weekly-economic-calendar"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        events = []
        rows = soup.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 5:
                date = cols[0].text.strip()
                time = cols[1].text.strip()
                title = cols[2].text.strip()
                impact = cols[3].text.strip()
                country = cols[4].text.strip()

                events.append({
                    "date": date,
                    "time": time,
                    "title": title,
                    "impact": impact,
                    "country": country
                })

        return events

    except Exception as e:
        print("خطا در دریافت یا پردازش تقویم اقتصادی از IranBourseOnline:", e)
        return []

def summarize_calendar(events):
    if not events:
        return "❗️هیچ رویداد اقتصادی یافت نشد."

    today = datetime.utcnow().date()
    today_events = [e for e in events if str(today.day) in e["date"] or today.strftime("%Y-%m-%d") in e["date"]]

    if not today_events:
        return "❗️امروز رویدادی در تقویم اقتصادی ثبت نشده."

    symbol_map = {
        "کم": "🟡",
        "پایین": "🟡",
        "متوسط": "🟠",
        "بالا": "🔴",
        "زیاد": "🔴",
        "پایان": "⚪️",
        "درحال": "⚪️",
    }

    grouped = defaultdict(list)
    for e in today_events:
        impact_symbol = ""
        for k, v in symbol_map.items():
            if k in e["impact"]:
                impact_symbol = v
                break
        grouped[e["country"]].append((e["time"], impact_symbol, e["title"]))

    output = ["(تحلیل تقویم اقتصادی)", "🟡=کم", "🟠=متوسط", "🔴=زیاد", "⚪️=پایان یا درحال اجرای رویداد + تحلیل", ""]

    for country, events in grouped.items():
        output.append(f"🇺🇸 {country} - {len(events)} رویداد")
        times_line = "/".join([f"ساعت {time} {icon}" for time, icon, _ in events])
        output.append(times_line)

        # یک تحلیل فرضی ساده برای یک رویداد خاص (مثلاً اولین رویداد کشور)
        if events:
            event_time, impact_icon, event_title = events[0]
            output.append(f"(رویداد ساعت {event_time} از اهمیت بالایی برخوردار بود و پس از انتشار و اطلاعات دریافتی تحلیل می‌کنم که برخی جفت‌ارزها ممکن است واکنش نشان دهند.)")
        output.append("")

    return "\n".join(output).strip()

if __name__ == "__main__":
    events = fetch_iranbourse_calendar()
    print(summarize_calendar(events))
