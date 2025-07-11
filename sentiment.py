positive_words = ["surge", "rise", "grow", "bullish", "cut", "gain", "optimism"]
negative_words = ["drop", "crash", "fall", "inflation", "bearish", "uncertainty"]

currency_pairs = {
    "EUR/USD": ["eur", "euro", "ecb"],
    "USD/JPY": ["jpy", "yen", "boj"],
    "GBP/USD": ["gbp", "pound", "boe"],
    "USD/CHF": ["chf", "franc", "swiss"],
    "AUD/USD": ["aud", "australian", "rba"],
    "USD/CAD": ["cad", "canadian", "boc"],
    "NZD/USD": ["nzd", "kiwi", "rbnz"]
}

major_pairs = {"EUR/USD", "USD/JPY", "GBP/USD", "USD/CHF", "AUD/USD", "USD/CAD", "NZD/USD"}

def analyze_sentiment(titles):
    pos, neg = 0, 0
    for title in titles:
        t = title.lower()
        if any(w in t for w in positive_words):
            pos += 1
        if any(w in t for w in negative_words):
            neg += 1
    if pos > neg:
        return "ریسک‌پذیر ✅"
    elif neg > pos:
        return "ریسک‌گریز ❌"
    return "متعادل ⚪️"

def extract_currency_impact(titles):
    impact_data = {}
    for title in titles:
        t = title.lower()
        for pair, keywords in currency_pairs.items():
            if any(k in t for k in keywords):
                if pair not in impact_data:
                    impact_data[pair] = 0
                impact_data[pair] += 1
    return impact_data

def classify_currency_type(impact_data):
    if not impact_data:
        return "نامشخص"
    total = sum(impact_data.values())
    major = sum(impact_data[p] for p in impact_data if p in major_pairs)
    major_percent = round((major / total) * 100) if total > 0 else 0
    if major_percent >= 60:
        return "جفت‌ارزهای اصلی"
    else:
        return "جفت‌ارزهای فرعی"
