from fetch_sources import get_all_titles
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
        type_ = classify_currency_type(pair)
        direction = "⏫" if any(k in pair.lower() for k in ["aud", "eur", "gbp"]) else "⏬"
        output += f"{pair} {direction} {type_} {percent}%    "
    return output.strip()

def main():
    titles = get_all_titles()
    if not titles:
        send_telegram("⛔️ هیچ خبری دریافت نشد.")
        return

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    mood = analyze_sentiment(titles)
    impact = extract_currency_impact(titles)
    type_ratio = classify_currency_type(impact)
    currency_output = format_currency_output(impact)

    sample_titles = " ؛ ".join(titles[:3])
    msg = f"""📡 تحلیل بازار (چند منبع خبری)
⏰ تایم تحلیل: {now}
📰 نمونه تیتر: {sample_titles}
📄 تعداد خبرهای تحلیل‌شده: {len(titles)}
📊 احساس سرمایه‌گذاران: {mood}
📈 نوع جفت‌ارزهای تحت تأثیر: {type_ratio}
📉 جفت‌ارزهای تحت‌تأثیر:
{currency_output}
📡 تحلیل ساده با چند منبع
"""
    send_telegram(msg)

if __name__ == "__main__":
    main()
