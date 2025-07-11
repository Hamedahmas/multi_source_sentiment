from fetch_sources import fetch_all_news, is_today
from sentiment import analyze_sentiment, extract_currency_impact, classify_currency_type
from send_telegram import send_telegram
from datetime import datetime

def format_currency_output(impact_data):
    total = sum(impact_data.values())
    if total == 0:
        return "هیچ جفت‌ارزی شناسایی نشد."

    output = ""
    for pair, count in sorted(impact_data.items(), key=lambda x: x[1], reverse=True):
        percent = round((count / total) * 100)
        type_ = classify_currency_type(impact_data)
        direction = "⏫" if any(k in pair.lower() for k in ["aud", "eur", "gbp"]) else "⏬"
        output += f"{pair} {direction} {type_} {percent}%    "
    return output.strip()

def main():
    # دریافت تمام اخبار از چندین منبع
    entries = fetch_all_news()
    if not entries:
        send_telegram("⛔️ هیچ خبری دریافت نشد.")
        return

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    mood = analyze_sentiment([entry['title'] for entry in entries])
    impact = extract_currency_impact([entry['title'] for entry in entries])
    type_ratio = classify_currency_type(impact)
    currency_output = format_currency_output(impact)

    # استخراج نمونه تیترهای خبر
    sample_titles = " ؛ ".join([entry['title'] for entry in entries[:3]])

    # گزارش کلی تحلیل
    msg = f"""📡 تحلیل بازار (چند منبع خبری)
⏰ تایم تحلیل: {now}
📰 نمونه تیتر: {sample_titles}
📄 تعداد خبرهای تحلیل‌شده: {len(entries)}
📊 احساس سرمایه‌گذاران: {mood}
📈 نوع جفت‌ارزهای تحت تأثیر: {type_ratio}
📉 جفت‌ارزهای تحت‌تأثیر:
{currency_output}
📡 تحلیل ساده با چند منبع
"""
    send_telegram(msg)

    # تحلیل اخبار امروز
    today_entries = [e for e in entries if is_today(e['published'])]
    if today_entries:
        today_msg = generate_report(today_entries, "🔵 تحلیل اخبار امروز")
        send_telegram(today_msg)
    else:
        send_telegram("❗️هیچ خبری برای امروز یافت نشد.")

def generate_report(entries, label):
    count = len(entries)
    time = datetime.utcnow().strftime("⏰ %Y-%m-%d %H:%M UTC")
    titles_sample = " ؛ ".join([entry['title'] for entry in entries[:3]])

    sentiment_result = analyze_sentiment([entry['title'] for entry in entries])
    impact_data = extract_currency_impact([entry['title'] for entry in entries])
    currency_type = classify_currency_type(impact_data)

    impact_lines = []
    total_mentions = sum(impact_data.values())
    for pair, count in impact_data.items():
        percentage = round((count / total_mentions) * 100) if total_mentions > 0 else 0
        sentiment_icon = "⏫" if percentage >= 50 else "⏬"
        trend_type = "پایدار" if sentiment_icon == "⏬" else "موقتی"
        impact_lines.append(f"{pair}{sentiment_icon}{trend_type} {percentage}%")

    impact_result = "    ".join(impact_lines) if impact_lines else "اطلاعاتی موجود نیست"

    message = f"""
📌 {label}
{time}
📰 عناوین: {titles_sample} و...
📄 تعداد خبرهای تحلیل‌شده: {count}
📊 احساس سرمایه‌گذاران: {sentiment_result}
📈 نوع جفت‌ارزهای تحت تأثیر: {currency_type}
📉 جفت‌ارزهای تحت‌تأثیر و نوع سنتیمنت و درصد تأثیر:
{impact_result}
📡 تحلیل با الگوریتم ساده سنتیمنت
"""
    return message.strip()

if __name__ == "__main__":
    main()
