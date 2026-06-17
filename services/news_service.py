import feedparser
from urllib.parse import quote


def analyze_news_trend(stock_code, stock_name):
    positive_keywords = {
        "AI": 2,
        "成長": 1,
        "利多": 2,
        "營收增加": 2,
        "訂單增加": 2,
        "創高": 2,
        "獲利": 2,
        "上修": 2,
        "擴產": 1,
        "法說": 1,
        "外資": 1,
        "買超": 1
    }

    negative_keywords = {
        "虧損": -3,
        "利空": -2,
        "下修": -2,
        "衰退": -2,
        "裁員": -2,
        "跌價": -2,
        "減產": -2,
        "違約": -3,
        "賣超": -1,
        "庫存": -1
    }

    topic_keywords = {
        "AI 題材": ["AI", "伺服器", "晶片", "半導體"],
        "營收成長": ["營收", "創高", "成長", "獲利"],
        "法人籌碼": ["外資", "投信", "買超", "賣超"],
        "景氣風險": ["庫存", "下修", "衰退", "減產"]
    }

    keyword = f"{stock_name} 股票"
    url = (
        "https://news.google.com/rss/search?"
        f"q={quote(keyword)}"
        "&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    )

    try:
        feed = feedparser.parse(url)
    except Exception:
        return get_empty_news_result("新聞資料暫時無法取得，建議先以技術面判斷。")

    news_list = []

    for entry in feed.entries[:8]:
        title = getattr(entry, "title", "")
        link = getattr(entry, "link", "#")

        news_list.append({
            "title": title,
            "link": link
        })

    if len(news_list) == 0:
        return get_empty_news_result(f"{stock_name} 近期暫無明顯新聞資料")

    score = 0
    matched_positive = []
    matched_negative = []
    matched_topics = set()

    for news in news_list:
        title = news["title"]

        for keyword, weight in positive_keywords.items():
            if keyword in title:
                score += weight
                matched_positive.append(keyword)

        for keyword, weight in negative_keywords.items():
            if keyword in title:
                score += weight
                matched_negative.append(keyword)

        for topic, keywords in topic_keywords.items():
            for keyword in keywords:
                if keyword in title:
                    matched_topics.add(topic)

    news_count = len(news_list)

    if score >= 5:
        trend = "新聞明顯偏正向"
    elif score >= 2:
        trend = "新聞偏正向"
    elif score >= 0:
        trend = "新聞中性"
    elif score >= -3:
        trend = "新聞偏負向"
    else:
        trend = "新聞明顯偏負向"

    if news_count >= 6:
        heat = "高"
    elif news_count >= 3:
        heat = "中"
    else:
        heat = "低"

    if score >= 5:
        news_advice = "近期新聞動能強，若技術面也配合，短中期可列入優先觀察。"
    elif score >= 2:
        news_advice = "新聞面偏正向，但仍需搭配技術指標與成交量確認。"
    elif score >= 0:
        news_advice = "新聞面目前中性，股價表現主要仍看技術面與基本面。"
    else:
        news_advice = "新聞面出現負向訊號，建議降低追高意願並觀察後續消息。"

    return {
        "news_score": score,
        "news_trend": trend,
        "news_heat": heat,
        "news_topics": "、".join(matched_topics) if matched_topics else "暫無明顯題材",
        "positive_keywords": "、".join(set(matched_positive)) if matched_positive else "無",
        "negative_keywords": "、".join(set(matched_negative)) if matched_negative else "無",
        "news_advice": news_advice,
        "news_list": news_list
    }


def get_empty_news_result(message):
    return {
        "news_score": 0,
        "news_trend": "新聞中性",
        "news_heat": "低",
        "news_topics": "暫無明顯題材",
        "positive_keywords": "無",
        "negative_keywords": "無",
        "news_advice": message,
        "news_list": [{
            "title": message,
            "link": "#"
        }]
    }